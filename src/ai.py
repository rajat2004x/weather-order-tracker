import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types


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

    Retries temporary Gemini failures and uses a fallback message
    if the AI service is unavailable.
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
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=100,
                    http_options=types.HttpOptions(
                        timeout=10000
                    )
                )
            )

            if response.text:
                return " ".join(response.text.strip().split())

        except errors.ServerError as error:

            print(
                f"  → Gemini server error "
                f"(attempt {attempt}/3)"
            )

            if attempt < 3:
                time.sleep(2)

        except Exception as error:

            print(
                f"  → Gemini request failed: {error}"
            )

            break

    # Safe fallback
    return (
        f"Hi {customer}, your order to {city} is delayed due to "
        f"{weather_description}, and we appreciate your patience."
    )