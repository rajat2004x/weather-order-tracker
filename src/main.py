import asyncio
import json
import aiohttp

from weather import fetch_weather
from ai import generate_weather_apology
from utils import setup_logger


ORDERS_FILE = "data/orders.json"
OUTPUT_FILE = "data/updated_orders.json"

DELAY_WEATHER = {"Rain", "Snow", "Extreme"}


def print_header():
    print("\n" + "=" * 60)
    print("             WEATHER ORDER TRACKER")
    print("=" * 60)
    print("Weather-aware delivery monitoring system")
    print("=" * 60 + "\n")


async def main():

    logger = setup_logger()

    print_header()

    # Load orders
    with open(ORDERS_FILE, "r", encoding="utf-8") as file:
        orders = json.load(file)

    logger.info(
        f"Starting weather processing | Orders: {len(orders)}"
    )

    print(f"📦 Orders to process : {len(orders)}")
    print("⚡ Fetching weather concurrently...\n")

    async with aiohttp.ClientSession() as session:

        # Create one task for every order
        tasks = [
            fetch_weather(session, order["city"])
            for order in orders
        ]

        # Execute all weather requests concurrently
        weather_results = await asyncio.gather(*tasks)

    print("-" * 60)
    print("WEATHER RESULTS")
    print("-" * 60)

    for order, result in zip(orders, weather_results):

        if result["success"]:

            weather_main = result["main"]
            description = result["description"]

            logger.info(
                f"Weather fetched successfully | "
                f"City: {order['city']} | "
                f"Condition: {weather_main}"
            )

            # Display weather result
            print(
                f"✓ {order['customer']:<18} "
                f"| {order['city']:<16} "
                f"| {weather_main:<10} "
                f"| {description}"
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

                print("  → ⚠ DELIVERY DELAY DETECTED")
                print("  → Order status: Delayed")

                # Generate personalized AI apology
                apology = generate_weather_apology(
                    customer=order["customer"],
                    city=order["city"],
                    weather_main=weather_main,
                    weather_description=description
                )

                order["delay_message"] = apology

                logger.info(
                    f"AI delay message generated | "
                    f"Order: {order['order_id']}"
                )

                print("  → 🤖 AI message generated")
                print(f"  → {apology}")

            else:

                order["status"] = "Pending"

        else:

            # Invalid city/API errors do not stop processing
            print(
                f"✗ {order['customer']:<18} "
                f"| {order['city']:<16} "
                f"| ERROR"
            )

            print(f"  → ⚠ {result['error']}")

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

    print("\n" + "=" * 60)
    print("PROCESSING COMPLETED")
    print("=" * 60)
    print(f"✓ Orders processed : {len(orders)}")
    print(f"✓ Output file      : {OUTPUT_FILE}")
    print(f"✓ Error handling   : Enabled")
    print(f"✓ Concurrent fetch : Enabled")
    print(f"✓ AI integration   : Enabled")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())