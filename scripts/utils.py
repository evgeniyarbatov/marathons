import json
from collections.abc import Callable
from typing import Any, TypeVar

import pycountry
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

T = TypeVar("T")


def cache(file_name: str) -> Callable[[Callable[[str], T]], Callable[[str], T]]:
    def decorator(original_func: Callable[[str], T]) -> Callable[[str], T]:
        try:
            with open(file_name, encoding="utf-8") as f:
                cached: dict[str, T] = json.load(f)
        except (OSError, ValueError):
            cached = {}

        def new_func(param: str) -> T:
            if param not in cached:
                cached[param] = original_func(param)
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(cached, f, indent=2, ensure_ascii=False)
                    f.write("\n")
            return cached[param]

        return new_func

    return decorator


# Nominatim's usage policy caps clients at 1 request/second; errors must raise so they aren't cached.
geocode = RateLimiter(
    Nominatim(user_agent="marathons (github.com/evgeniyarbatov/marathons)").geocode,
    min_delay_seconds=1,
    swallow_exceptions=False,
)


@cache("cache/nomimatim-api.json")
def call_nominatim_api(city_name: str) -> dict[str, Any] | None:
    location = geocode(city_name, exactly_one=True, language="en", addressdetails=True)
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
