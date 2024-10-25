import requests
import time
import pandas as pd
from datetime import datetime
from database import Database
from alerts import AlertSystem

API_KEY = 'YOUR_API_KEY'  # Replace with your OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
INTERVAL = 300  # 5 minutes

class WeatherMonitor:
    def __init__(self):
        self.db = Database()
        self.alert_system = AlertSystem()
        self.weather_data = []

    def fetch_weather(self, city):
        response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY})
        if response.status_code == 200:
            data = response.json()
            self.process_data(data)
        else:
            print(f"Failed to retrieve data for {city}")

    def process_data(self, data):
        main = data['main']
        weather = data['weather'][0]
        temp_celsius = main['temp'] - 273.15  # Convert Kelvin to Celsius
        feels_like_celsius = main['feels_like'] - 273.15

        weather_info = {
            'city': data['name'],
            'temp': temp_celsius,
            'feels_like': feels_like_celsius,
            'condition': weather['main'],
            'timestamp': datetime.fromtimestamp(data['dt'])
        }
        self.weather_data.append(weather_info)
        self.db.store_weather_data(weather_info)
        self.alert_system.check_alerts(weather_info)

    def run(self):
        while True:
            for city in CITIES:
                self.fetch_weather(city)
            time.sleep(INTERVAL)

if __name__ == "__main__":
    monitor = WeatherMonitor()
    monitor.run()