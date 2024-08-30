
from flask import Flask, render_template, request
import requests
from dataclasses import dataclass
from typing import List, Optional

app = Flask(__name__)

API_KEY = "a324848564b117b70fadd84deae50d18"
UNITS = "metric"
BASE_URL = "http://api.openweathermap.org/data/2.5/"
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"

@dataclass
class WeatherDetails:
    description: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    icon: str

@dataclass
class ForecastDetails:
    date: str
    temperature: float
    description: str
    icon: str

def make_request(url: str, params: dict) -> dict:
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_coordinates(address: str) -> tuple:
    params = {
        "q": address,
        "limit": 1,
        "appid": API_KEY
    }
    data = make_request(GEOCODING_URL, params=params)
    if not data:
        raise ValueError(f"Unable to find coordinates for address: {address}")
    return data[0]["lat"], data[0]["lon"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    address = request.form.get('address')
    try:
        lat, lon = get_coordinates(address)
        params = {
            "lat": lat,
            "lon": lon,
            "units": UNITS,
            "appid": API_KEY
        }
        json_data = make_request(f"{BASE_URL}weather", params=params)
        
        weather_details = WeatherDetails(
            description=json_data["weather"][0]["description"],
            temperature=json_data["main"]["temp"],
            feels_like=json_data["main"]["feels_like"],
            humidity=json_data["main"]["humidity"],
            wind_speed=json_data["wind"]["speed"],
            icon=json_data["weather"][0]["icon"]
        )
        return render_template('index.html', weather=weather_details, city=address)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/forecast', methods=['POST'])
def forecast():
    address = request.form.get('address')
    try:
        lat, lon = get_coordinates(address)
        params = {
            "lat": lat,
            "lon": lon,
            "units": UNITS,
            "appid": API_KEY
        }
        json_data = make_request(f"{BASE_URL}forecast", params=params)
        
        forecast_list = [
            ForecastDetails(
                date=item["dt_txt"],
                temperature=item["main"]["temp"],
                description=item["weather"][0]["description"],
                icon=item["weather"][0]["icon"]
            )
            for item in json_data["list"][::8]  # 8 intervals per day
        ]
        return render_template('index.html', forecast=forecast_list, city=address)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/info')
def info():
    return render_template('index.html', info=True)

if __name__ == '__main__':
    app.run(debug=True)