import os
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_weather(session, city):
    """
    Fetch current weather for a city from OpenWeatherMap.
    Errors are returned as data so one failed city does not stop
    processing of other orders.
    """

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        async with session.get(
            BASE_URL,
            params=params,
            timeout=aiohttp.ClientTimeout(total=10)
        ) as response:

            data = await response.json()

            if response.status != 200:
                return {
                    "city": city,
                    "success": False,
                    "error": data.get(
                        "message",
                        "Weather API request failed"
                    )
                }

            weather = data["weather"][0]

            return {
                "city": city,
                "success": True,
                "main": weather["main"],
                "description": weather["description"],
                "temperature": data["main"]["temp"]
            }

    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        return {
            "city": city,
            "success": False,
            "error": str(error)
        }