import json
from collections.abc import Callable
from typing import Any, TypeVar

import pycountry
from geopy.exc import GeocoderServiceError, GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim

T = TypeVar("T")


def cache(file_name: str) -> Callable[[Callable[[str], T]], Callable[[str], T]]:
    def decorator(original_func: Callable[[str], T]) -> Callable[[str], T]:
        try:
            with open(file_name) as f:
                cached: dict[str, T] = json.load(f)
        except (OSError, ValueError):
            cached = {}

        def new_func(param: str) -> T:
            if param not in cached:
                cached[param] = original_func(param)
                with open(file_name, "w") as f:
                    json.dump(cached, f)
            return cached[param]

        return new_func

    return decorator


@cache("cache/nomimatim-api.json")
def call_nominatim_api(city_name: str) -> dict[str, Any] | None:
    geolocator = Nominatim(user_agent="get-country-codes")
    try:
        location = geolocator.geocode(
            city_name, exactly_one=True, language="en", addressdetails=True
        )
    except (GeocoderServiceError, GeocoderTimedOut, GeocoderUnavailable):
        return None
    result: dict[str, Any] | None = location.raw if location else None
    return result


def get_country_code(city_name: str) -> str | None:
    location = call_nominatim_api(city_name)
    if not location:
        return None

    address = location["address"]
    country_code = address.get("country_code", None)

    return country_code.lower() if country_code else None


def get_athlete_country(alpha3: str | None) -> str | None:
    if alpha3 is None:
        return None
    if len(alpha3) == 2:
        return alpha3.lower()
    try:
        country = pycountry.countries.get(alpha_3=alpha3)
        return country.alpha_2.lower() if country else None
    except AttributeError:
        return None
