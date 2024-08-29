from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your actual API keys
weather_api_key = "a324848564b117b70fadd84deae50d18"  # OpenWeatherMap API Key
geocode_api_key = "BD0DEB1A43A63549A797B52B5FC92990"  # OpenCage API Key

units = "metric"  # Use "imperial" for Fahrenheit
weather_base_url = "http://api.openweathermap.org/data/2.5/"
geocode_base_url = "https://api.opencagedata.com/geocode/v1/json"

def make_request(url):
    response = requests.get(url)
    return response.json()

def geocode_address(address):
    url = f"{geocode_base_url}?q={address}&key={geocode_api_key}"
    json_data = make_request(url)
    
    if json_data['results']:
        return json_data['results'][0]['geometry']['lat'], json_data['results'][0]['geometry']['lng']
    else:
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city_name = request.form.get('city')
    url = f"{weather_base_url}weather?q={city_name}&units={units}&appid={weather_api_key}"
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
    url = f"{weather_base_url}forecast?q={city_name}&units={units}&appid={weather_api_key}"
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
            "icon": json_data["list"][i]["weather"][0]["icon"]  # Get weather icon code
        }
        forecast_list.append(forecast_details)
    
    return render_template('index.html', forecast=forecast_list, city=city_name)

@app.route('/weather-by-address', methods=['POST'])
def weather_by_address():
    address = request.form.get('address')
    lat, lon = geocode_address(address)
    
    if lat is None or lon is None:
        error_message = "Unable to geocode the address. Please try again."
        return render_template('index.html', error=error_message)
    
    url = f"{weather_base_url}weather?lat={lat}&lon={lon}&units={units}&appid={weather_api_key}"
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

    return render_template('index.html', weather=weather_details, city=address)

@app.route('/info')
def info():
    return render_template('index.html', info=True)

if __name__ == '__main__':
    app.run(debug=True)