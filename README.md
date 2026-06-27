# Prithvex

Uncertainty-aware risk intelligence for global supply chains.

Prithvex is a hackathon prototype that moves supply chain planning from passive forecasting to active decision intelligence. It forecasts operational inventory pressure, simulates disruption scenarios, classifies risk, and recommends an action through an interactive Streamlit dashboard.

The project is aligned with the pitch deck theme: making supply chains predictable, trustworthy, and resilient by combining machine learning, uncertainty estimation, explainability, and decision automation.

## Problem

Supply chains often fail because teams receive point forecasts without reliability signals. During disruptions, this creates three expensive problems:

- Teams over-order or under-order because the forecast does not show uncertainty.
- Analysts need too much time to translate risk signals into action.
- Supplier and logistics shocks can cascade before buyers see the impact.

Prithvex compresses that uncertainty-to-action workflow into an interactive dashboard where a user can test scenarios and immediately see risk level, business impact, and the recommended response.

## What This Repo Implements

- XGBoost forecasting model trained on inventory and demand features.
- Streamlit dashboard with a modern neon command-center interface.
- Disruption simulation for warehouse fire, port strike, supplier delay, and flood scenarios.
- Risk triage engine with Low, Medium, and High risk levels.
- Recommendation engine for operational actions.
- Forecast confidence interval display.
- Plotly visualization for demand versus remaining supply.
- Feature importance table from the trained model.
- Supporting scripts for conformal prediction, SHAP analysis, event simulation, and uncertainty estimation.

## Demo Dashboard

Run the app from the project root:

```powershell
streamlit run Dashboard\app.py
```

Or specify a port:

```powershell
streamlit run Dashboard\app.py --server.port=8502
```

Then open:

```text
http://localhost:8502
```

In the sidebar, choose one of the fixed disruption events and adjust severity and demand surge. The dashboard updates the forecast, remaining supply, risk score, risk level, recommended action, confidence range, and impact chart.

## Current Demo Flow

1. Load the trained forecasting model from `Models/forecast_model.pkl`.
2. Read the dashboard dataset from `Data/tableau_dashboard_master_universidad.csv`.
3. Predict the latest inventory cost / demand-pressure signal.
4. Apply a user-selected disruption scenario.
5. Calculate remaining supply and risk score.
6. Classify the scenario as Low, Medium, or High risk.
7. Recommend an action:
   - High risk: Emergency Replenishment
   - Medium risk: Increase Safety Stock
   - Low risk: Normal Operations
8. Show the result in the Streamlit dashboard.

## Technology Stack

| Layer | Tools Used | Purpose |
| --- | --- | --- |
| Data processing | Python, Pandas, NumPy | Load and transform tabular supply chain data |
| Forecasting | XGBoost, Scikit-learn | Train the core predictive model |
| Model persistence | Joblib | Save and reload trained models |
| Uncertainty | Residual interval logic, MAPIE script | Estimate prediction confidence ranges |
| Explainability | SHAP script | Inspect model feature impact |
| Risk simulation | Python rule engine | Convert disruptions into risk levels |
| Dashboard | Streamlit | Interactive user interface |
| Visualization | Plotly | Supply impact chart and dashboard visuals |

## Project Structure

```text
AIhackathon/
|-- Dashboard/
|   `-- app.py
|-- Data/
|   |-- tableau_dashboard_master_universidad.csv
|   |-- global_supply_chain_risk_2026.csv
|   |-- Delivery_Logistics.csv
|   |-- DataCoSupplyChainDataset.csv
|   `-- calendar.csv
|-- Models/
|   |-- forecast_model.pkl
|   `-- conformal_model.pkl
|-- Outputs/
|   |-- forecasts.csv
|   |-- risks.csv
|   `-- recommendations.csv
|-- src/
|   |-- train_xgboost.py
|   |-- uncertainty.py
|   |-- conformal_prediction.py
|   |-- shap_explainer.py
|   |-- event_simulator.py
|   |-- risk_engine.py
|   |-- recommendation_engine.py
|   |-- m5_forecasting.py
|   |-- feature_engineering.py
|   `-- data_loader.py
`-- README.md
```

## Key Files

| File | Description |
| --- | --- |
| `Dashboard/app.py` | Main Streamlit dashboard and interactive demo |
| `src/train_xgboost.py` | Trains the XGBoost forecasting model |
| `src/uncertainty.py` | Computes residual-based confidence intervals |
| `src/conformal_prediction.py` | MAPIE conformal prediction experiment |
| `src/shap_explainer.py` | SHAP feature attribution script |
| `src/event_simulator.py` | Disruption event impact simulator |
| `src/risk_engine.py` | Low / Medium / High risk classifier |
| `src/recommendation_engine.py` | Converts risk level into recommended action |
| `Models/forecast_model.pkl` | Saved forecasting model used by the dashboard |

## Dataset Used by Dashboard

The dashboard currently uses:

```text
Data/tableau_dashboard_master_universidad.csv
```

Main columns:

- `Order_Quantity`
- `Holding_Cost`
- `Ordering_Cost`
- `Total_Inventory_Cost`
- `Annual_Demand`
- `Daily_Demand`
- `Daily_Std_Dev`
- `Base_Unit_Price`
- `Default_Lead_Time`

The current model trains on all columns except `Total_Inventory_Cost`, which is used as the target.

## Model Training

To retrain the forecasting model:

```powershell
python src\train_xgboost.py
```

The script:

- Loads `Data/tableau_dashboard_master_universidad.csv`
- Splits data into train and test sets
- Trains an `XGBRegressor`
- Prints mean absolute error
- Saves the model as `models/forecast_model.pkl`

Note: the dashboard also checks `Models/forecast_model.pkl`, which is the current saved model location in this repo.

## Optional Analysis Scripts

Run residual uncertainty estimation:

```powershell
python src\uncertainty.py
```

Run conformal prediction experiment:

```powershell
python src\conformal_prediction.py
```

Run SHAP explainability:

```powershell
python src\shap_explainer.py
```

Run disruption simulation:

```powershell
python src\event_simulator.py
```

## Suggested Environment

Install the main dependencies:

```powershell
pip install streamlit pandas numpy scikit-learn xgboost joblib plotly shap mapie
```

If you want to extend the full pitch-deck vision, also consider:

```powershell
pip install lightgbm networkx
```

## Pitch Deck Alignment

The presentation frames Prithvex as a five-layer system:

| Pitch Layer | Current Repo Status |
| --- | --- |
| Data ingestion | Implemented through CSV-based data loading |
| Ensemble ML | XGBoost implemented; LightGBM is part of the stated future stack |
| Conformal prediction | MAPIE experiment included in `src/conformal_prediction.py` |
| Risk + SHAP | Rule-based risk engine and SHAP script included |
| Dashboard | Streamlit + Plotly dashboard implemented |

The deck also describes a broader production roadmap:

- Multi-horizon 7 day, 30 day, and 90 day forecasts
- Multi-tier supplier graph intelligence
- Monte Carlo shock propagation
- KL-divergence based shift detection
- ROI-ranked action recommendations
- Sector expansion across pharma, FMCG, automotive, and semiconductors

Those items are represented in the product concept and can be built on top of the current prototype.

## Business Impact Story

Prithvex is designed around four impact goals from the deck:

- Reduce emergency procurement costs by surfacing risk earlier.
- Reduce stockouts without excessive overstock.
- Shorten crisis response time from days to seconds.
- Provide explainable recommendations instead of black-box scores.

The prototype demonstrates this through an interactive disruption simulator and a decision dashboard that turns forecast output into operational action.

## Limitations

This is a hackathon prototype, not a production deployment. The current implementation uses a compact dashboard dataset and a saved local model. Some pitch-deck capabilities, such as full multi-tier supplier graphs, LightGBM stacking, Monte Carlo propagation, and ROI optimization, are documented as the next product layer rather than fully implemented in this repo.

## Future Improvements

- Add full `requirements.txt` with pinned package versions.
- Standardize model output paths between `models/` and `Models/`.
- Expand the dashboard from one latest prediction to SKU-level risk tables.
- Add SHAP explanations directly inside the Streamlit UI.
- Add MAPIE conformal intervals to the live dashboard flow.
- Build supplier network graphs using NetworkX.
- Add cost-of-action versus cost-of-inaction calculations.
- Export scenario results into `Outputs/forecasts.csv`, `Outputs/risks.csv`, and `Outputs/recommendations.csv`.

## One-Line Summary

Prithvex is a local, reproducible supply chain resilience prototype that combines forecasting, uncertainty awareness, disruption simulation, risk triage, and prescriptive recommendations in a Streamlit decision dashboard.
