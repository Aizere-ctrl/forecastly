import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

def generate_forecast(df, forecast_days=7):
    df = clean_input_data(df)

    daily_data = (
        df.groupby("date", as_index=False)
        .agg({"revenue": "sum"})
        .sort_values("date")
    )

    if daily_data.empty:
        raise ValueError("Not enough data to generate forecast.")

    if len(daily_data) < 10:
        return simple_fallback_forecast(daily_data, forecast_days)

    daily_data = create_features(daily_data)

    feature_columns = [
        "day_index",
        "day_of_week",
        "month",
        "lag_1",
        "lag_2",
        "lag_3",
        "rolling_mean_3",
        "rolling_mean_7"
    ]

    X = daily_data[feature_columns]
    y = daily_data["revenue"]

    models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),

    "Decision Tree": DecisionTreeRegressor(
        random_state=42,
        max_depth=5
    ),

    "Random Forest": RandomForestRegressor(
        n_estimators=120,
        random_state=42,
        max_depth=7
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=120,
        learning_rate=0.08,
        max_depth=3,
        random_state=42
    ),

    "XGBoost": XGBRegressor(
        n_estimators=150,
        learning_rate=0.05,
        max_depth=4,
        objective="reg:squarederror",
        random_state=42
    )
}

    best_model_name, best_model, metrics = choose_best_model(models, X, y)

    best_model.fit(X, y)

    forecast = []
    history = daily_data.copy()
    last_date = daily_data["date"].max()

    for i in range(1, forecast_days + 1):
        future_date = last_date + pd.Timedelta(days=i)

        future_row = create_future_row(history, future_date)

        prediction = best_model.predict(future_row)[0]
        prediction = max(float(prediction), 0)

        forecast.append({
            "period": i,
            "date": future_date.strftime("%Y-%m-%d"),
            "forecast": round(prediction, 2),
            "predicted_revenue": round(prediction, 2),
            "model_used": best_model_name,
            "mae": metrics.get("mae"),
            "rmse": metrics.get("rmse"),
            "mape": metrics.get("mape")
        })

        new_row = {
            "date": future_date,
            "revenue": prediction,
            "day_index": len(history),
            "day_of_week": future_date.dayofweek,
            "month": future_date.month,
            "lag_1": future_row["lag_1"].iloc[0],
            "lag_2": future_row["lag_2"].iloc[0],
            "lag_3": future_row["lag_3"].iloc[0],
            "rolling_mean_3": future_row["rolling_mean_3"].iloc[0],
            "rolling_mean_7": future_row["rolling_mean_7"].iloc[0]
        }

        history = pd.concat(
            [history, pd.DataFrame([new_row])],
            ignore_index=True
        )

    return forecast


def clean_input_data(df):
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    if "date" not in df.columns:
        raise ValueError("Dataset must contain a date column.")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    if "revenue" not in df.columns:
        if "sales_units" in df.columns and "price" in df.columns:
            df["revenue"] = df["sales_units"] * df["price"]
        elif "sales_units" in df.columns:
            df["revenue"] = df["sales_units"]
        else:
            raise ValueError("Dataset must contain revenue or sales_units column.")

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df = df.dropna(subset=["revenue"])

    return df


def create_features(daily_data):
    daily_data = daily_data.copy()

    daily_data["day_index"] = range(len(daily_data))
    daily_data["day_of_week"] = daily_data["date"].dt.dayofweek
    daily_data["month"] = daily_data["date"].dt.month

    daily_data["lag_1"] = daily_data["revenue"].shift(1)
    daily_data["lag_2"] = daily_data["revenue"].shift(2)
    daily_data["lag_3"] = daily_data["revenue"].shift(3)

    daily_data["rolling_mean_3"] = (
        daily_data["revenue"]
        .rolling(window=3, min_periods=1)
        .mean()
    )

    daily_data["rolling_mean_7"] = (
        daily_data["revenue"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    revenue_mean = daily_data["revenue"].mean()

    for col in [
        "lag_1",
        "lag_2",
        "lag_3",
        "rolling_mean_3",
        "rolling_mean_7"
    ]:
        daily_data[col] = daily_data[col].fillna(revenue_mean)

    return daily_data


def choose_best_model(models, X, y):
    if len(X) < 15:
        model = LinearRegression()
        return "Linear Regression", model, {
            "mae": 0,
            "rmse": 0,
            "mape": 0
        }

    split_index = int(len(X) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    best_model_name = None
    best_model = None
    best_metrics = None
    best_error = float("inf")

    for model_name, model in models.items():
        try:
            model.fit(X_train, y_train)

            predictions = model.predict(X_test)
            predictions = np.maximum(predictions, 0)

            mae = mean_absolute_error(y_test, predictions)
            rmse = np.sqrt(mean_squared_error(y_test, predictions))

            y_test_safe = np.where(y_test == 0, 1, y_test)
            mape = np.mean(np.abs((y_test - predictions) / y_test_safe)) * 100

            if mae < best_error:
                best_error = mae
                best_model_name = model_name
                best_model = model
                best_metrics = {
                    "mae": round(float(mae), 2),
                    "rmse": round(float(rmse), 2),
                    "mape": round(float(mape), 2)
                }

        except Exception as e:
            print(f"Model error in {model_name}: {e}")

    if best_model is None:
        return "Linear Regression", LinearRegression(), {
            "mae": 0,
            "rmse": 0,
            "mape": 0
        }

    return best_model_name, best_model, best_metrics


def create_future_row(history, future_date):
    lag_1 = history["revenue"].iloc[-1]
    lag_2 = history["revenue"].iloc[-2] if len(history) >= 2 else lag_1
    lag_3 = history["revenue"].iloc[-3] if len(history) >= 3 else lag_2

    rolling_mean_3 = history["revenue"].tail(3).mean()
    rolling_mean_7 = history["revenue"].tail(7).mean()

    return pd.DataFrame([{
        "day_index": len(history),
        "day_of_week": future_date.dayofweek,
        "month": future_date.month,
        "lag_1": lag_1,
        "lag_2": lag_2,
        "lag_3": lag_3,
        "rolling_mean_3": rolling_mean_3,
        "rolling_mean_7": rolling_mean_7
    }])


def simple_fallback_forecast(daily_data, forecast_days):
    daily_data = daily_data.copy()
    last_date = daily_data["date"].max()

    if len(daily_data) >= 3:
        base_value = daily_data["revenue"].tail(3).mean()
    else:
        base_value = daily_data["revenue"].mean()

    forecast = []

    for i in range(1, forecast_days + 1):
        forecast.append({
            "period": i,
            "date": (last_date + pd.Timedelta(days=i)).strftime("%Y-%m-%d"),
            "forecast": round(float(base_value), 2),
            "predicted_revenue": round(float(base_value), 2),
            "model_used": "Fallback Average Forecast",
            "mae": 0,
            "rmse": 0,
            "mape": 0
        })

    return forecast