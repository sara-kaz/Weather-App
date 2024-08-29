from flask import Flask, render_template, request
from datetime import datetime
import requests

app = Flask(__name__)

api_key = "a324848564b117b70fadd84deae50d18"  # OpenWeatherMap API Key
units = "metric"  # Use "imperial" for Fahrenheit
base_url = "http://api.openweathermap.org/data/2.5/"

def make_request(url):
    response = requests.get(url)
    return response.json()

def format_date(date_str):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    
    # Format the date as "Tuesday, 24th July"
    formatted_date = date_obj.strftime('%A, %-d')
    
    # Get the day number
    day = int(date_obj.strftime('%d'))
    
    # Determine the appropriate suffix
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd", "th"][min(day % 10, 3)]
    
    # Add the suffix and month
    formatted_date += suffix + date_obj.strftime(' %B')
    
    return formatted_date

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city_name = request.form.get('city')
    url = f"{base_url}weather?q={city_name}&units={units}&appid={api_key}"
    json_data = make_request(url)
    
    if json_data.get("cod") != 200:
        error_message = json_data.get("message", "Failed to fetch weather data")
        return render_template('index.html', error=error_message)
    
    weather_details = {
        "description": json_data["weather"][0]["description"],
        "temperature": json_data["main"]["temp"],
        "feels_like": json_data["main"]["feels_like"],
        "humidity": json_data["main"]["humidity"],
        "wind_speed": json_data["wind"]["speed"],
        "icon": json_data["weather"][0]["icon"]  # Get weather icon code
    }

    return render_template('index.html', weather=weather_details, city=city_name)

@app.route('/forecast', methods=['POST'])
def forecast():
    city_name = request.form.get('city')
    url = f"{base_url}forecast?q={city_name}&units={units}&appid={api_key}"
    json_data = make_request(url)
    
    if json_data.get("cod") != "200":
        error_message = json_data.get("message", "Failed to fetch forecast data")
        return render_template('index.html', error=error_message)
    
    forecast_list = []
    for i in range(0, len(json_data["list"]), 8):  # 8 intervals per day
        forecast_details = {
            "date": format_date(json_data["list"][i]["dt_txt"]),  # Format the date
            "temperature": json_data["list"][i]["main"]["temp"],
            "description": json_data["list"][i]["weather"][0]["description"],
            "icon": json_data["list"][i]["weather"][0]["icon"]  # Get weather icon code
        }
        forecast_list.append(forecast_details)
    
    return render_template('index.html', forecast=forecast_list, city=city_name)

@app.route('/weather-by-location-form', methods=['POST'])
def weather_by_location_form():
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    url = f"{base_url}weather?lat={lat}&lon={lon}&units={units}&appid={api_key}"
    json_data = make_request(url)
    
    if json_data.get("cod") != 200:
        error_message = json_data.get("message", "Failed to fetch weather data")
        return render_template('index.html', error=error_message)
    
    weather_details = {
        "description": json_data["weather"][0]["description"],
        "temperature": json_data["main"]["temp"],
        "feels_like": json_data["main"]["feels_like"],
        "humidity": json_data["main"]["humidity"],
        "wind_speed": json_data["wind"]["speed"],
        "icon": json_data["weather"][0]["icon"]  # Get weather icon code
    }

    return render_template('index.html', weather=weather_details, city=f"({lat}, {lon})")

@app.route('/info')
def info():
    return render_template('index.html', info=True)

if __name__ == '__main__':
    app.run(debug=True)