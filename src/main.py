import asyncio
import json
import aiohttp

from weather import fetch_weather
from ai import generate_weather_apology
from utils import setup_logger


ORDERS_FILE = "data/orders.json"
OUTPUT_FILE = "data/updated_orders.json"

DELAY_WEATHER = {"Rain", "Snow", "Extreme"}


async def main():

    logger = setup_logger()

    # Load orders
    with open(ORDERS_FILE, "r", encoding="utf-8") as file:
        orders = json.load(file)

    logger.info(
        f"Starting weather processing | Orders: {len(orders)}"
    )

    print(f"Processing {len(orders)} orders...\n")

    async with aiohttp.ClientSession() as session:

        # Create a task for every order
        tasks = [
            fetch_weather(session, order["city"])
            for order in orders
        ]

        # Execute weather requests concurrently
        weather_results = await asyncio.gather(*tasks)

    print("Weather Results:\n")

    for order, result in zip(orders, weather_results):

        if result["success"]:

            weather_main = result["main"]

            logger.info(
                f"Weather fetched successfully | "
                f"City: {order['city']} | "
                f"Condition: {weather_main}"
            )

            print(
                f"✓ {order['city']}: "
                f"{weather_main} - "
                f"{result['description']}"
            )

            # Golden Flow
            if weather_main in DELAY_WEATHER:

                order["status"] = "Delayed"

                logger.warning(
                    f"Order delayed | "
                    f"Order: {order['order_id']} | "
                    f"City: {order['city']} | "
                    f"Weather: {weather_main}"
                )

                print("  → Order marked as Delayed")

                # Generate personalized AI apology
                apology = generate_weather_apology(
                    customer=order["customer"],
                    city=order["city"],
                    weather_main=weather_main,
                    weather_description=result["description"]
                )

                order["delay_message"] = apology

                logger.info(
                    f"AI delay message generated | "
                    f"Order: {order['order_id']}"
                )

                print(f"  → AI message: {apology}")

            else:

                order["status"] = "Pending"

        else:

            # Invalid city/API errors do not stop other orders
            print(
                f"✗ {order['city']}: "
                f"{result['error']}"
            )

            logger.error(
                f"Weather fetch failed | "
                f"City: {order['city']} | "
                f"Error: {result['error']}"
            )

    # Save updated orders
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=2)

    logger.info(
        f"Processing completed | Output: {OUTPUT_FILE}"
    )

    print("\nUpdated orders saved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.run(main())