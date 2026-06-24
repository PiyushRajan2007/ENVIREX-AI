# src/uncertainty.py

import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

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

model = joblib.load(
    "models/forecast_model.pkl"
)

pred = model.predict(X_test)

residual_std = np.std(y_test - pred)

lower = pred - 1.96 * residual_std
upper = pred + 1.96 * residual_std

for i in range(min(5, len(pred))):
    print(
        f"Prediction={pred[i]:.2f}, "
        f"95% CI=({lower[i]:.2f}, {upper[i]:.2f})"
    )