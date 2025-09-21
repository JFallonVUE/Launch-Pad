import os, json, pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session", autouse=True)
def build_kb():
    os.makedirs("./data", exist_ok=True)
    if not os.path.exists("./data/catalog.json"):
        with open("./data/catalog.json","w") as f:
            json.dump({"services":[
                {"service_id":"show_stopper","name":"Show Stopper","deliverables":["Hero set"],"constraints":[],"compatible_biases":["anchoring","novelty"],"price_band":"high"},
                {"service_id":"aerials","name":"Aerials","deliverables":["Drone stills"],"constraints":[],"compatible_biases":["authority","social_proof"],"price_band":"medium"},
                {"service_id":"2d_floor_plan","name":"2D Floor Plan","deliverables":["Schematic plan"],"constraints":[],"compatible_biases":["fluency"],"price_band":"low"},
                {"service_id":"zillow_3d","name":"Zillow 3D","deliverables":["Tour"],"constraints":[],"compatible_biases":["fluency","mere_exposure"],"price_band":"medium"},
                {"service_id":"virtual_staging","name":"Virtual Staging","deliverables":["Staged photos"],"constraints":["vacant_only"],"compatible_biases":["anchoring"],"price_band":"low"},
                {"service_id":"quick_snaps","name":"Quick Snaps","deliverables":["Fast-turn images"],"constraints":[],"compatible_biases":["mere_exposure","loss_aversion"],"price_band":"low"}
            ]}, f)
    if not os.path.exists("./data/biases.json"):
        with open("./data/biases.json","w") as f:
            json.dump({"biases":[
                {"key":"fluency","name":"Fluency / Cognitive Ease","definition":"Reduce cognitive load.",
                 "copy_patterns":["Clear, short lines","Chunk specs"],"cadence_patterns":["Morning","Evening"],
                 "compatible_services":["2d_floor_plan","zillow_3d"]},
                {"key":"anchoring","name":"Anchoring","definition":"Lead with signature value.",
                 "copy_patterns":["Start with the best"],"cadence_patterns":["Lunch"],"compatible_services":["show_stopper","luxe"]},
                {"key":"mere_exposure","name":"Mere Exposure","definition":"Repeat to build familiarity.",
                 "copy_patterns":["Series posts"],"cadence_patterns":["Evening"],"compatible_services":["quick_snaps","zillow_3d"]},
                {"key":"loss_aversion","name":"Loss Aversion","definition":"Highlight what buyers miss.",
                 "copy_patterns":["Don't miss..."],"cadence_patterns":["Morning"],"compatible_services":["quick_snaps"]}
            ]}, f)
    yield

@pytest.fixture
def client():
    return TestClient(app)
