import pytest

def test_tight_room_condo_remote(client):
    payload = {"answers":{"propertyType":"Condo","beds":1,"baths":1.0,"interiorSizeSqft":620,"conditionBand":"updated",
                          "tightRooms":True,"naturalLight":"good","occupancy":"occupied","quirkyFlow":False,"signatureFeature":"Skyline peek",
                          "likelyBuyer":"remote_buyer","locationPerk":"walkable","timelinePressure":"medium","agentOnCamComfort":"medium","showingWindow":"morning"}}
    r = client.post("/intake/lighting", json=payload)
    js = r.json()
    assert r.status_code==200
    flat_services = [s["service_id"] for st in js["stacks"] for s in st["services"]]
    assert "2d_floor_plan" in flat_services and "zillow_3d" in flat_services
