import requests

class ThirdPartyService:
    def __init__(self):
        self.weather_api_url = "https://api.openweathermap.org/data/2.5/weather?lat=33.7182&lon=73.0714&appid=8ca0e3398bfda8b1eda90a7a45d89d51"

    def get_weather(self):
        response = requests.get(self.weather_api_url)
        print(response.status_code)
        print(response)
        if response.status_code == 200:
            data = response.json()
            return data
        return "Unable to fetch weather data at the moment."
