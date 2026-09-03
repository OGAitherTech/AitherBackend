from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/weather", tags=["weather"])
OPEN_METEO = "https://api.open-meteo.com/v1/forecast"
GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"


def _get_json(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "AitherBackend/2.0"})
    try:
        with urlopen(request, timeout=12) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Weather provider unavailable") from exc


@router.get("")
def weather(latitude: float = Query(..., ge=-90, le=90), longitude: float = Query(..., ge=-180, le=180)):
    params = urlencode({
        "latitude": latitude, "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m,wind_gusts_10m",
        "hourly": "temperature_2m,precipitation_probability,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset,uv_index_max",
        "forecast_days": 7, "timezone": "auto", "temperature_unit": "fahrenheit", "wind_speed_unit": "mph",
    })
    data = _get_json(f"{OPEN_METEO}?{params}")
    data["source"] = "AitherBackend"
    return data


@router.get("/search")
def search(q: str = Query(..., min_length=1, max_length=100)):
    params = urlencode({"name": q, "count": 5, "language": "en", "format": "json", "countryCode": "US"})
    data = _get_json(f"{GEOCODING}?{params}")
    results = [{
        "name": ", ".join(filter(None, [item.get("name"), item.get("admin1")])),
        "lat": item.get("latitude"), "lon": item.get("longitude"), "country": item.get("country_code")
    } for item in data.get("results", [])]
    return {"results": results, "source": "AitherBackend"}
