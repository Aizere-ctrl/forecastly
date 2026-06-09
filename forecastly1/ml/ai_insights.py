def generate_scenario_insights(scenarios):
    insights = []

    realistic = scenarios.get("realistic", 0)
    optimistic = scenarios.get("optimistic", 0)
    pessimistic = scenarios.get("pessimistic", 0)

    if optimistic > realistic:
        insights.append("Optimistic scenario shows higher sales potential. Consider preparing additional stock.")

    if pessimistic < realistic:
        insights.append("Pessimistic scenario shows possible demand decrease. Monitor sales activity carefully.")

    if optimistic - pessimistic > realistic * 0.3:
        insights.append("Scenario gap is high, which means demand may be unstable.")

    return insights


def generate_analytics_insights(analytics):
    insights = []

    if analytics["growth_rate"] > 10:
        insights.append("Sales are growing positively compared to the first recorded period.")
    elif analytics["growth_rate"] < -10:
        insights.append("Sales are decreasing. Consider checking pricing, stock availability, or promotion strategy.")
    else:
        insights.append("Sales are relatively stable with no major growth or decline.")

    if analytics["average_forecast"] > analytics["average_sales"]:
        insights.append("Forecasted sales are higher than historical average sales.")
    else:
        insights.append("Forecasted sales are lower than or close to historical average sales.")

    return insights


def generate_anomaly_insights(anomalies):
    insights = []

    if len(anomalies) == 0:
        insights.append("No significant anomalies were detected in the sales data.")
    else:
        insights.append(f"{len(anomalies)} unusual sales pattern(s) detected.")
        insights.append("Review anomaly dates to identify possible stock-outs, promotions, or data errors.")

    return insights