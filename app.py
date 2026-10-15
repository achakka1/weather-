from flask import Flask, render_template
import requests

app = Flask(__name__)

WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Freezing fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy drizzle",
    56: "Light freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with light hail",
    99: "Thunderstorm with heavy hail",
}


@app.route("/")
def index():
    temperature = None
    description = None
    error = None
    status = 200

    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 37.3382,
                "longitude": -121.8863,
                "current": "temperature_2m,weather_code",
                "temperature_unit": "fahrenheit",
                "timezone": "America/Los_Angeles",
            },
            timeout=10,
        )

        response.raise_for_status()
        current = response.json()["current"]

        temperature = float(current["temperature_2m"])
        description = WEATHER_DESCRIPTIONS.get(
            current["weather_code"],
            "Unknown conditions",
        )

    except (requests.RequestException, KeyError, ValueError, TypeError):
        error = "Weather is unavailable right now. Please refresh to try again."
        status = 503

    return render_template(
        "index.html",
        temperature=temperature,
        description=description,
        error=error,
    ), status, {"Cache-Control": "no-store"}


if __name__ == "__main__":
    app.run(port=5000)