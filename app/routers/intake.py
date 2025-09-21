from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel, Field
from typing import Dict, Any
from app.deps import get_session, init_db
from app.services import signals, llm_decider
from app.models import Intake

router = APIRouter()

class LightingPayload(BaseModel):
    answers: Dict[str, Any] = Field(..., description="15 answers per schemas/lighting.json")

class DeepDivePayload(BaseModel):
    answers: Dict[str, Any] = Field(..., description="40–50 answers per schemas/deep_dive.json")

@router.post("/lighting")
def intake_lighting(payload: LightingPayload, session: Session = Depends(get_session)):
    init_db()
    sigs = signals.compute(payload.answers)
    result = llm_decider.decide(payload.answers, sigs, mode="lighting")
    intake = Intake(mode="lighting", answers=payload.answers, signals=sigs,
                    stacks=result["stacks"], biases=result["biases"])
    session.add(intake); session.commit()
    return {"stacks": result["stacks"], "biases": result["biases"]}

@router.post("/deep-dive")
def intake_deep_dive(payload: DeepDivePayload, session: Session = Depends(get_session)):
    init_db()
    sigs = signals.compute(payload.answers)
    result = llm_decider.decide(payload.answers, sigs, mode="deep_dive")
    intake = Intake(mode="deep_dive", answers=payload.answers, signals=sigs,
                    stacks=result["stacks"], biases=result["biases"])
    session.add(intake); session.commit(); session.refresh(intake)
    return {"intake_id": intake.id, "stacks": result["stacks"], "biases": result["biases"]}
