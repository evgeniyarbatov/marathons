import requests
import json

from urllib.parse import quote

def cache(file_name):
    def decorator(original_func):
        try:
            cache = json.load(open(file_name, 'r'))
        except (IOError, ValueError):
            cache = {}

        def new_func(param):
            if param not in cache:
                cache[param] = original_func(param)
                json.dump(cache, open(file_name, 'w'))
            return cache[param]

        return new_func

    return decorator

@cache('cache/api.geonames.org.json')
def call_geonames_api(city_name):
    city_name = quote(city_name)
    response = requests.get(
        f'http://api.geonames.org/searchJSON?q={city_name}&maxRows=1&username=arbatov'
    )
    return response.json()

def get_country_code(city_name):
    data = call_geonames_api(city_name)
    country_code = data['geonames'][0]['countryCode']
    return country_code