from flask import Flask, render_template, request
from datetime import datetime
import requests

app = Flask(__name__)

api_key = "a324848564b117b70fadd84deae50d18"  # Your OpenWeatherMap API Key
units = "metric"  # Use "imperial" for Fahrenheit
base_url = "http://api.openweathermap.org/data/2.5/"

def make_request(url):
    response = requests.get(url)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

def get_weather_by_address(address):
    # First, get the coordinates from the address
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={address}&limit=1&appid={api_key}"
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()
    
    if not geocoding_data:
        return None, "Address not found"
    
    lat = geocoding_data[0]['lat']
    lon = geocoding_data[0]['lon']
    
    # Now use these coordinates to get the weather
    weather_url = f"{base_url}weather?lat={lat}&lon={lon}&units={units}&appid={api_key}"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    if weather_data.get("cod") != 200:
        error_message = weather_data.get("message", "Failed to fetch weather data")
        return None, error_message
    
    weather_details = {
        "description": weather_data["weather"][0]["description"],
        "temperature": weather_data["main"]["temp"],
        "feels_like": weather_data["main"]["feels_like"],
        "humidity": weather_data["main"]["humidity"],
        "wind_speed": weather_data["wind"]["speed"],
        "icon": weather_data["weather"][0]["icon"]
    }

    return weather_details, None

@app.route('/weather', methods=['POST'])
def weather():
    address = request.form.get('address')
    weather_details, error = get_weather_by_address(address)
    
    if error:
        return render_template('index.html', error=error)
    
    return render_template('index.html', weather=weather_details, city=address)

@app.route('/forecast', methods=['POST'])
def forecast():
    address = request.form.get('address')
    
    # Get coordinates from address
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={address}&limit=1&appid={api_key}"
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()
    
    if not geocoding_data:
        return render_template('index.html', error="Address not found")
    
    lat = geocoding_data[0]['lat']
    lon = geocoding_data[0]['lon']
    
    url = f"{base_url}forecast?lat={lat}&lon={lon}&units={units}&appid={api_key}"
    json_data = make_request(url)
    
    if json_data.get("cod") != "200":
        error_message = json_data.get("message", "Failed to fetch forecast data")
        return render_template('index.html', error=error_message)
    
    forecast_list = []
    for i in range(0, len(json_data["list"]), 8):  # 8 intervals per day
        forecast_details = {
            "date": json_data["list"][i]["dt_txt"],
            "temperature": json_data["list"][i]["main"]["temp"],
            "description": json_data["list"][i]["weather"][0]["description"],
            "icon": json_data["list"][i]["weather"][0]["icon"]
        }
        forecast_list.append(forecast_details)
    
    return render_template('index.html', forecast=forecast_list, city=address)

@app.route('/info')
def info():
    return render_template('index.html', info=True)

if __name__ == '__main__':
    app.run(debug=True)