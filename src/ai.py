import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_weather_apology(
    customer,
    city,
    weather_main,
    weather_description
):
    """
    Generate a personalized weather-aware delivery delay message.

    Retries temporary Gemini server failures before using a safe
    fallback message.
    """

    prompt = f"""
Create a short, professional and empathetic delivery-delay message.

Customer: {customer}
Destination: {city}
Weather condition: {weather_main}
Weather description: {weather_description}

Requirements:
- Address the customer by name.
- Mention the destination city.
- Explain that the order is delayed because of the weather.
- Be polite and reassuring.
- Keep it to one sentence.
- Do not invent additional information.
"""

    for attempt in range(1, 4):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            if response.text:
                return " ".join(response.text.strip().split())

        except errors.ServerError:

            if attempt < 3:
                time.sleep(2)
            else:
                break

        except Exception:
            break

    # Safe fallback if the AI service is temporarily unavailable
    return (
        f"Hi {customer}, your order to {city} is delayed due to "
        f"{weather_description}, and we appreciate your patience."
    )