import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from xgboost import XGBRegressor

# Load dataset
df = pd.read_csv(
    "Data/tableau_dashboard_master_universidad.csv"
)

print(df.head())
print(df.info())

# Target column
y = df["Total_Inventory_Cost"]

# Features
X = df.drop(
    "Total_Inventory_Cost",
    axis=1
)

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = XGBRegressor(
    n_estimators=100,
    max_depth=4,
    random_state=42
)

# Train
model.fit(
    X_train,
    y_train
)

# Predict
pred = model.predict(X_test)

print(
    "MAE =",
    mean_absolute_error(
        y_test,
        pred
    )
)

# Save model

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/forecast_model.pkl"
)

print("Model saved successfully")
