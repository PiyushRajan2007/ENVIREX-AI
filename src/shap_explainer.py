import joblib
import pandas as pd
import shap

from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv(
    "Data/tableau_dashboard_master_universidad.csv"
)

# Target
y = df["Total_Inventory_Cost"]

# Features
X = df.drop(
    "Total_Inventory_Cost",
    axis=1
)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Load model
model = joblib.load(
    "models/forecast_model.pkl"
)

# SHAP Explainer
explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X_test)

print("SHAP calculated successfully")

# Summary plot
shap.summary_plot(
    shap_values,
    X_test
)