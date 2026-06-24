# src/risk_engine.py

def risk_score(forecast, available_supply):

    ratio = available_supply / forecast

    if ratio < 0.7:
        return "HIGH"

    elif ratio < 0.9:
        return "MEDIUM"

    return "LOW"


print(risk_score(1000, 600))
print(risk_score(1000, 850))
print(risk_score(1000, 1000))