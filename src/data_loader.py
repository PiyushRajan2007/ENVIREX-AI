# src/data_loader.py

import pandas as pd

sales = pd.read_csv("data/raw/sales_train_validation.csv")
calendar = pd.read_csv("data/raw/calendar.csv")
prices = pd.read_csv("data/raw/sell_prices.csv")

print(sales.shape)