# src/feature_engineering.py

df["lag_7"] = df["sales"].shift(7)

df["lag_14"] = df["sales"].shift(14)

df["rolling_mean_7"] = (
    df["sales"]
    .rolling(7)
    .mean()
)