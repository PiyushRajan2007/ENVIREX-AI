EVENTS = {
    "Warehouse Fire": 0.40,
    "Port Strike": 0.30,
    "Supplier Delay": 0.20,
    "Flood": 0.25
}


def simulate_event(forecast, event):

    impact = EVENTS[event]

    new_supply = forecast * (1 - impact)

    return new_supply


forecast = 1000

for event in EVENTS:

    result = simulate_event(
        forecast,
        event
    )

    print(
        event,
        "->",
        result
    )