from microdot import Microdot, Response
import requests
import os

app = Microdot()
Response.default_content_type = 'text/html'

API_KEY = '6dab7aebdc26ed61cdd4765e502e7ed9' # Replace with your OpenWeatherMap API Key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_weather(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if response.status_code != 200:
        print(f"Error fetching weather data: {data.get('message')}")
        return None

    return data


def htmldoc(weather_data):
    return f'''
        <html>
            <head>
                <title>Weather Station</title>
            </head>
            <body>
                <h1>Weather in {weather_data["name"]}, {weather_data["sys"]["country"]}</h1>
                <p>Coordinates: Lon {weather_data["coord"]["lon"]}, Lat {weather_data["coord"]["lat"]}</p>
                <p>Weather ID: {weather_data["weather"][0]["id"]}</p>
                <p>Weather Main: {weather_data["weather"][0]["main"]}</p>
                <p>Weather Description: {weather_data["weather"][0]["description"]}</p>
                <p>Temperature: {weather_data["main"]["temp"]}K</p>
                <p>Feels like: {weather_data["main"]["feels_like"]}K</p>
                <p>Minimum Temperature: {weather_data["main"]["temp_min"]}K</p>
                <p>Maximum Temperature: {weather_data["main"]["temp_max"]}K</p>
                <p>Pressure: {weather_data["main"]["pressure"]}hPa</p>
                <p>Humidity: {weather_data["main"]["humidity"]}%</p>
                <p>Visibility: {weather_data["visibility"]}m</p>
                <p>Wind Speed: {weather_data["wind"]["speed"]}m/s</p>
                <p>Wind Degree: {weather_data["wind"]["deg"]}</p>
                <p>Clouds: {weather_data["clouds"]["all"]}%</p>
                <p>Sunrise: {weather_data["sys"]["sunrise"]}</p>
                <p>Sunset: {weather_data["sys"]["sunset"]}</p>
                <p>Timezone: {weather_data["timezone"]}</p>
            </body>
        </html>
    '''



@app.route('/')
def home(request):
    city_name = 'Boca Raton' # Default city name
    weather_data = fetch_weather(city_name)

    if weather_data is None:
        return "<h1>Error fetching weather data. Please try again later.</h1>"
    
    return htmldoc(weather_data)
    
    

app.run(debug=True, port=8008)





