from src.ai import generate_weather_apology


def test_delayed_weather_ai_message():

    customer = "Alice Smith"
    city = "New York"
    weather_main = "Rain"
    weather_description = "heavy rain"

    status = "Delayed" if weather_main in {
        "Rain",
        "Snow",
        "Extreme"
    } else "Pending"

    message = generate_weather_apology(
        customer=customer,
        city=city,
        weather_main=weather_main,
        weather_description=weather_description
    )

    assert status == "Delayed"
    assert message
    assert customer in message
    assert city in message

    print("\nDelayed-flow test passed")
    print(f"Status: {status}")
    print(f"AI Message: {message}")


if __name__ == "__main__":
    test_delayed_weather_ai_message()