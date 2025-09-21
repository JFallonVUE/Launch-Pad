def compute(answers: dict) -> dict:
    size = float(answers.get("interiorSizeSqft", 1500))
    condition = answers.get("conditionBand", "average")
    tight = bool(answers.get("tightRooms", False))
    natural = answers.get("naturalLight", "good")
    timeline = answers.get("timelinePressure", answers.get("priority", "medium"))

    def map_condition(c):
        m = {"pristine":0.2,"updated":0.4,"average":0.5,"dated":0.7,"needs_work":0.9}
        return m.get(c,0.5)
    def map_natural(n):
        m = {"excellent":0.2,"good":0.4,"mixed":0.6,"poor":0.8}
        return m.get(n,0.5)
    def map_timeline(t):
        m = {"low":0.3,"medium":0.5,"high":0.7,"urgent":0.9,
             "speed":0.9,"balance":0.6,"maximize_price":0.4}
        return m.get(t,0.5)

    complexity = 0.3*map_condition(condition) + 0.2*(1.0-map_natural(natural)) + 0.2*(1.0 if tight else 0) + 0.3*(size/4000.0)
    clarity_need = 0.6*map_condition(condition) + 0.4*(1.0 if tight else 0.0)
    momentum = map_timeline(timeline)
    brand_lift = 0.2 + (size/5000.0) + (0.2 if answers.get("propertyType")=="Luxury" else 0.0)
    location_eff = 0.5

    return {
        "complexity": round(min(1.0, complexity), 3),
        "clarityNeed": round(min(1.0, clarity_need), 3),
        "momentumPressure": round(min(1.0, momentum), 3),
        "brandLift": round(min(1.0, brand_lift), 3),
        "locationEfficiency": round(min(1.0, location_eff), 3),
    }
