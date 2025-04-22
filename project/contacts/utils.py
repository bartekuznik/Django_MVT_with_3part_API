import requests
from django.core.cache import cache

def get_contact_data(cache_key, lat, lon):
    """
    Handles fetching data from 'open-meteo' API, and return selected
    weather data.

    Args:
        cache_key: Unique id for each contact
        lat: city latitude
        lon: city longitude

    """

    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,is_day,rain,cloud_cover')
    response.raise_for_status()
    data = response.json()
    weather = {
            'temperature': data['current']['temperature_2m'],
            'humidity': data['current']['relative_humidity_2m'],
            'windspeed': data['current']['wind_speed_10m'],
            'is_day': data['current']['is_day'],
            'rain': data['current']['rain'],
            'cloud_cover': data['current']['cloud_cover'],
        }
    cache.set(cache_key, weather, timeout=600)

    return weather