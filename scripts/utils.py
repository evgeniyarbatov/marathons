import json

import pycountry

from geopy.geocoders import Nominatim

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

@cache('cache/nomimatim-api.json')
def call_nominatim_api(city_name):
    geolocator = Nominatim(user_agent="get-country-codes")
    location = geolocator.geocode(city_name, exactly_one=True, language="en", addressdetails=True)
    return location.raw if location else None

def get_country_code(city_name):
    location = call_nominatim_api(city_name)
    if not location:
        return None
    
    address = location['address']
    country_code = address.get('country_code', None)
    
    return country_code.lower()

def get_athlete_country(alpha3):
    if alpha3 == None:
        return None
    if len(alpha3) == 2: 
        return alpha3.lower()
    try:
        country = pycountry.countries.get(alpha_3=alpha3)
        return country.alpha_2.lower() if country else None
    except AttributeError:
        return None