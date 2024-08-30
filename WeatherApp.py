from flask import Flask, render_template, request
import requests
from typing import Dict, Any, List, Optional

app = Flask(__name__)

# Configuration constants
API_KEY = "a324848564b117b70fadd84deae50d18"  # OpenWeatherMap API Key
UNITS = "metric"  # Use "imperial" for Fahrenheit
BASE_URL = "http://api.openweathermap.org/data/2.5/"

def make_api_request(url: str) -> Dict[str, Any]:
    """
    Make a GET request to the specified URL and return the JSON response.

    Args:
        url (str): The URL to make the request to.

    Returns:
        Dict[str, Any]: The JSON response from the API.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad responses
    return response.json()

def get_weather_details(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract relevant weather details from the API response.

    Args:
        data (Dict[str, Any]): The JSON data from the API response.

    Returns:
        Dict[str, Any]: A dictionary containing extracted weather details.
    """
    weather = data.get("weather", [{}])[0]
    main = data.get("main", {})
    wind = data.get("wind", {})

    return {
        "description": weather.get("description", "N/A"),
        "temperature": main.get("temp", "N/A"),
        "feels_like": main.get("feels_like", "N/A"),
        "humidity": main.get("humidity", "N/A"),
        "wind_speed": wind.get("speed", "N/A"),
        "icon": weather.get("icon", "N/A")
    }

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    """Handle the weather request for a city."""
    city_name = request.form.get('city')
    url = f"{BASE_URL}weather?q={city_name}&units={UNITS}&appid={API_KEY}"
    
    try:
        json_data = make_api_request(url)
        weather_details = get_weather_details(json_data)
        return render_template('index.html', weather=weather_details, city=city_name)
    except requests.RequestException as e:
        return render_template('index.html', error=f"Failed to fetch weather data: {str(e)}")

@app.route('/forecast', methods=['POST'])
def forecast():
    """Handle the 5-day forecast request for a city."""
    city_name = request.form.get('city')
    url = f"{BASE_URL}forecast?q={city_name}&units={UNITS}&appid={API_KEY}"
    
    try:
        json_data = make_api_request(url)
        forecast_list = get_forecast_list(json_data)
        return render_template('index.html', forecast=forecast_list, city=city_name)
    except requests.RequestException as e:
        return render_template('index.html', error=f"Failed to fetch forecast data: {str(e)}")

def get_forecast_list(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract the 5-day forecast from the API response.

    Args:
        data (Dict[str, Any]): The JSON data from the API response.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing forecast details for each day.
    """
    return [
        {
            "date": item.get("dt_txt", "N/A"),
            "temperature": item.get("main", {}).get("temp", "N/A"),
            "description": item.get("weather", [{}])[0].get("description", "N/A"),
            "icon": item.get("weather", [{}])[0].get("icon", "N/A")
        }
        for item in data.get("list", [])[::8]  # 8 intervals per day
    ]

@app.route('/weather-by-location-form', methods=['POST'])
def weather_by_location_form():
    """Handle the weather request for a specific latitude and longitude."""
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    url = f"{BASE_URL}weather?lat={lat}&lon={lon}&units={UNITS}&appid={API_KEY}"
    
    try:
        json_data = make_api_request(url)
        weather_details = get_weather_details(json_data)
        return render_template('index.html', weather=weather_details, city=f"({lat}, {lon})")
    except requests.RequestException as e:
        return render_template('index.html', error=f"Failed to fetch weather data: {str(e)}")

@app.route('/info')
def info():
    """Render the info page."""
    return render_template('index.html', info=True)

if __name__ == '__main__':
    app.run(debug=True)