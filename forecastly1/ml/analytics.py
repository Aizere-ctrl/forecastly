import numpy as np
import pandas as pd


def calculate_analytics(df, forecast_data):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    if "revenue" not in df.columns:
        if "sales_units" in df.columns and "price" in df.columns:
            df["revenue"] = df["sales_units"] * df["price"]
        elif "sales_units" in df.columns:
            df["revenue"] = df["sales_units"]
        else:
            return default_analytics()

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df = df.dropna(subset=["revenue"])

    if df.empty:
        return default_analytics()

    total_revenue = round(df["revenue"].sum(), 2)
    average_revenue = round(df["revenue"].mean(), 2)

    first_value = df["revenue"].iloc[0]
    last_value = df["revenue"].iloc[-1]

    if first_value != 0:
        growth_rate = round(((last_value - first_value) / first_value) * 100, 2)
    else:
        growth_rate = 0

    actual_values = df["revenue"].tail(len(forecast_data)).values

    predicted_values = []

    for item in forecast_data:
        if isinstance(item, dict):
            predicted_values.append(
                item.get("predicted_revenue")
                or item.get("forecast")
                or item.get("revenue")
                or 0
            )

    predicted_values = np.array(predicted_values[:len(actual_values)], dtype=float)

    if len(actual_values) == len(predicted_values) and len(actual_values) > 0:
        mae = round(np.mean(np.abs(actual_values - predicted_values)), 2)
        rmse = round(np.sqrt(np.mean((actual_values - predicted_values) ** 2)), 2)

        non_zero_actual = np.where(actual_values == 0, 1, actual_values)
        mape = round(np.mean(np.abs((actual_values - predicted_values) / non_zero_actual)) * 100, 2)

        accuracy = round(max(0, 100 - mape), 2)
    else:
        mae = 0
        rmse = 0
        mape = 0
        accuracy = 0

    return {
        "total_sales": total_revenue,
        "average_sales": average_revenue,
        "growth_rate": growth_rate,
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "accuracy": accuracy,
        "model_type": "Linear Regression with Feature Engineering",
        "target_variable": "Revenue",
        "features_used": "Date features, lag values, rolling average, trend"
    }


def default_analytics():
    return {
        "total_sales": 0,
        "average_sales": 0,
        "growth_rate": 0,
        "mae": 0,
        "rmse": 0,
        "mape": 0,
        "accuracy": 0,
        "model_type": "Linear Regression with Feature Engineering",
        "target_variable": "Revenue",
        "features_used": "Date features, lag values, rolling average, trend"
    }