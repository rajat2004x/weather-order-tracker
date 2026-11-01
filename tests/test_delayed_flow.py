from src.ai import generate_weather_apology


def test_delayed_weather_ai_message():

    customer = "Alice Smith"
    city = "New York"
    weather_main = "Rain"
    weather_description = "heavy rain"

    delay_weather = {"Rain", "Snow", "Extreme"}

    status = (
        "Delayed"
        if weather_main in delay_weather
        else "Pending"
    )

    print("\n" + "=" * 60)
    print("              GOLDEN FLOW TEST")
    print("=" * 60)

    print(f"Weather condition : {weather_main}")
    print(f"Weather detail    : {weather_description}")

    assert status == "Delayed"

    print(f"Delay condition   : YES")
    print(f"Order status      : {status}")

    # Call the Weather-Aware Apology function
    message = generate_weather_apology(
        customer=customer,
        city=city,
        weather_main=weather_main,
        weather_description=weather_description
    )

    assert message
    assert customer in message
    assert city in message

    print("AI function       : generate_weather_apology()")
    print("AI message        :")
    print(f"  {message}")

    print("=" * 60)
    print("✓ GOLDEN FLOW TEST PASSED")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    test_delayed_weather_ai_message()