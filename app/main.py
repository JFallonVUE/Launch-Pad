from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, json
from app.config import settings
from app.routers import intake, export, admin

app = FastAPI(title="LaunchPad AI Decision Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

app.include_router(intake.router, prefix="/intake", tags=["intake"])
app.include_router(export.router, prefix="/export", tags=["export"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/schemas", tags=["meta"])
def get_schemas():
    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "schemas")
    def load(name):
        with open(os.path.join(base, name), "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "lighting": load("lighting.json"),
        "deep_dive": load("deep_dive.json"),
        "stacks": load("stacks.json"),
        "bias_plan": load("bias_plan.json"),
        "export_request": load("export_request.json"),
    }
