import pandas as pd
import numpy as np

sales = pd.read_csv(
    "Data/sales_train_validation.csv"
)

calendar = pd.read_csv(
    "Data/calendar.csv"
)

prices = pd.read_csv(
    "Data/sell_prices.csv"
)

print(sales.shape)

SKU = "HOBBIES_1_004"
STORE = "CA_1"

item = sales[
    (sales["item_id"] == SKU) &
    (sales["store_id"] == STORE)
]

days = [c for c in sales.columns if c.startswith("d_")]

series = item[days].T

series.columns = ["sales"]

series.reset_index(inplace=True)

series.rename(
    columns={"index":"d"},
    inplace=True
)


series["lag_7"] = series["sales"].shift(7)

series["lag_14"] = series["sales"].shift(14)

series["rolling_mean_7"] = (
    series["sales"]
    .rolling(7)
    .mean()
)

series["rolling_std_7"] = (
    series["sales"]
    .rolling(7)
    .std()
)

series.dropna(inplace=True)

from sklearn.model_selection import train_test_split

X = series[
    [
        "lag_7",
        "lag_14",
        "rolling_mean_7",
        "rolling_std_7"
    ]
]

y = series["sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    shuffle=False,
    test_size=0.2
)

from xgboost import XGBRegressor

model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05
)

model.fit(
    X_train,
    y_train
)

