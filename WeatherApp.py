import requests
import json

api_key = "a324848564b117b70fadd84deae50d18" # OpenWeatherMap API key
units = "metric"  # or "imperial" for Fahrenheit
base_url = "http://api.openweathermap.org/data/2.5/"

def make_request(url):
    response = requests.get(url)
    return response.json()

def print_weather_details(json_data):
    print("Weather:", json_data["weather"][0]["description"])
    print("Temperature:", json_data["main"]["temp"], "°C")
    print("Feels Like:", json_data["main"]["feels_like"], "°C")
    print("Humidity:", json_data["main"]["humidity"], "%")
    print("Wind Speed:", json_data["wind"]["speed"], "m/s")

def get_weather_by_city(city_name):
    url = f"{base_url}weather?q={city_name}&units={units}&appid={api_key}"
    json_data = make_request(url)
    if json_data:
        print_weather_details(json_data)
    else:
        print("Failed to fetch weather data")

def get_weather_by_location(latitude, longitude):
    url = f"{base_url}weather?lat={latitude}&lon={longitude}&units={units}&appid={api_key}"
    json_data = make_request(url)
    if json_data:
        print_weather_details(json_data)
    else:
        print("Failed to fetch weather data")

def get_5_day_forecast(city_name):
    url = f"{base_url}forecast?q={city_name}&units={units}&appid={api_key}"
    json_data = make_request(url)
    if json_data:
        for i in range(0, len(json_data["list"]), 8):  # 8 intervals per day
            print("Date:", json_data["list"][i]["dt_txt"])
            print("Temperature:", json_data["list"][i]["main"]["temp"], "°C")
            print("Weather:", json_data["list"][i]["weather"][0]["description"])
            print("-----------------------------------")
    else:
        print("Failed to fetch forecast data")

def main():
    print("Weather App")
    print("1. Get current weather by city")
    print("2. Get current weather by location")
    print("3. Get 5-day forecast by city")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        city_name = input("Enter city name: ")
        get_weather_by_city(city_name)
    elif choice == 2:
        latitude = float(input("Enter latitude: "))
        longitude = float(input("Enter longitude: "))
        get_weather_by_location(latitude, longitude)
    elif choice == 3:
        city_name = input("Enter city name: ")
        get_5_day_forecast(city_name)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
