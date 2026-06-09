def generate_scenarios(forecast_data):
    forecast_values = []

    for item in forecast_data:
        if isinstance(item, dict):
            value = (
                item.get("predicted_revenue")
                or item.get("forecast")
                or item.get("revenue")
                or 0
            )
            forecast_values.append(float(value))

    if not forecast_values:
        return {
            "optimistic": 0,
            "realistic": 0,
            "pessimistic": 0,
            "total_forecast": 0,
            "average_forecast": 0,
            "description": "Not enough forecast data to generate scenarios."
        }

    total_forecast = round(sum(forecast_values), 2)
    average_forecast = round(total_forecast / len(forecast_values), 2)

    return {
        "optimistic": round(total_forecast * 1.15, 2),
        "realistic": total_forecast,
        "pessimistic": round(total_forecast * 0.85, 2),
        "total_forecast": total_forecast,
        "average_forecast": average_forecast,
        "description": "Scenario analysis is based on the total predicted revenue."
    }