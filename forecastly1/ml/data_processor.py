import pandas as pd


def load_and_prepare_data(file_path):
    """
    Prepares Forecastly dataset for revenue forecasting.

    Required columns:
    date, sku_id, sku_name, sales_units, price, revenue
    """

    if file_path.lower().endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip().str.lower()

    required_columns = [
        "date",
        "sku_id",
        "sku_name",
        "sales_units",
        "price",
        "revenue"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["sales_units"] = pd.to_numeric(df["sales_units"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

    df = df.dropna(subset=["date", "revenue"])

    if df.empty:
        raise ValueError("Dataset has no valid date/revenue rows.")

    daily_df = df.groupby("date", as_index=False).agg({
        "sales_units": "sum",
        "revenue": "sum"
    })

    daily_df = daily_df.sort_values("date")

    daily_df["sales"] = daily_df["revenue"]
    daily_df["day_number"] = range(1, len(daily_df) + 1)

    return daily_df