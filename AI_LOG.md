# AI Log

## 1. Parallel Weather Fetching

### Prompt
> Build a Python solution that fetches weather information for multiple orders concurrently instead of processing each city sequentially. Use asyncio and aiohttp, and ensure all weather requests can execute concurrently.

### Result
The implementation uses `asyncio.gather()` to execute one asynchronous weather request per order.

```python
tasks = [
    fetch_weather(session, order["city"])
    for order in orders
]

weather_results = await asyncio.gather(*tasks)
```

This allows the weather requests for New York, Mumbai, London, and InvalidCity123 to be initiated concurrently.

---

## 2. Error Handling and Resilience

### Prompt
> Design error handling for a weather API workflow where an invalid city should produce an error message but must not terminate processing for the remaining valid cities.

### Result
The weather function returns a structured error result instead of raising the API error to the main workflow.

```python
{
    "city": city,
    "success": False,
    "error": "city not found"
}
```

The main workflow logs the error and continues processing the remaining orders.

---

## 3. Weather-Aware AI Message

### Prompt
> Create a short, professional and empathetic delivery-delay message using the customer's name, destination city, weather condition, and weather description. Address the customer by name, explain that the order is delayed because of the weather, remain polite and reassuring, and keep the message concise.

### Result
Gemini generates a personalized message for delayed orders.

Example:

> Dear Alice Smith, we apologize for the delay in your delivery to New York due to heavy rain and appreciate your patience as we work to deliver your order safely.

---

## 4. AI Reliability

A retry mechanism was added for temporary Gemini server failures. If the AI service remains unavailable after retries, the system uses a safe fallback message so that order processing does not terminate unexpectedly.