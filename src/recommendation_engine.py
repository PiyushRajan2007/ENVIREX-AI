# src/recommendation_engine.py

def recommend(risk):

    if risk == "HIGH":
        return "Emergency Replenishment"

    elif risk == "MEDIUM":
        return "Increase Safety Stock"

    return "Normal Operations"


print(recommend("HIGH"))
print(recommend("MEDIUM"))
print(recommend("LOW"))