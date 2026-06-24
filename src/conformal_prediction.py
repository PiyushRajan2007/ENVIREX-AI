import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from mapie.regression import MapieRegressor

# Load data
df = pd.read_csv(
    "Data/tableau_dashboard_master_universidad.csv"
)

y = df["Total_Inventory_Cost"]

X = df.drop(
    "Total_Inventory_Cost",
    axis=1
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Load trained model
model = joblib.load(
    "models/forecast_model.pkl"
)

# MAPIE
mapie = MapieRegressor(
    estimator=model,
    method="plus"
)

mapie.fit(
    X_train,
    y_train
)

pred, intervals = mapie.predict(
    X_test,
    alpha=0.1
)

print(pred[:5])
print(intervals[:5])