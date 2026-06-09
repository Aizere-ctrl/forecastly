import pandas as pd
import numpy as np


def detect_anomalies(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    if "revenue" not in df.columns:
        if "sales_units" in df.columns and "price" in df.columns:
            df["revenue"] = df["sales_units"] * df["price"]
        elif "sales_units" in df.columns:
            df["revenue"] = df["sales_units"]
        else:
            return []

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
    else:
        df["date"] = pd.date_range(start="2026-01-01", periods=len(df))

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df = df.dropna(subset=["revenue"])

    daily_data = (
        df.groupby("date", as_index=False)
        .agg({"revenue": "sum"})
        .sort_values("date")
    )

    if len(daily_data) < 5:
        return []

    mean_revenue = daily_data["revenue"].mean()
    std_revenue = daily_data["revenue"].std()

    if std_revenue == 0 or np.isnan(std_revenue):
        return []

    daily_data["z_score"] = (
        daily_data["revenue"] - mean_revenue
    ) / std_revenue

    daily_data["rolling_mean"] = daily_data["revenue"].rolling(
        window=3,
        min_periods=1
    ).mean()

    anomalies = []

    for _, row in daily_data.iterrows():
        z_score = row["z_score"]

        if abs(z_score) >= 2:
            if z_score > 0:
                anomaly_type = "Revenue Spike"
                severity = "High"
                message = "Revenue was unusually high compared to the normal sales pattern."
            else:
                anomaly_type = "Revenue Drop"
                severity = "High"
                message = "Revenue was unusually low compared to the normal sales pattern."

            anomalies.append({
                "date": row["date"].strftime("%Y-%m-%d"),
                "type": anomaly_type,
                "severity": severity,
                "value": round(float(row["revenue"]), 2),
                "z_score": round(float(z_score), 2),
                "description": message
            })

    return anomalies