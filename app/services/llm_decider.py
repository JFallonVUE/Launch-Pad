from typing import Dict, Any, List
from pydantic import BaseModel, Field, ValidationError
from app.services import kb_store
from app.config import settings

def _enforce_rules(answers: dict, proposed_services: List[dict]) -> List[dict]:
    out = []
    vacant = answers.get("occupancy") == "vacant"
    tight = bool(answers.get("tightRooms"))
    likely_remote = answers.get("likelyBuyer") == "remote_buyer"
    for s in proposed_services:
        sid = s.get("service_id","")
        if sid == "virtual_staging" and not vacant and not answers.get("explicitVirtualStagingOK", False):
            continue
        if sid == "exterior_only" and not answers.get("busy_street_special_case", False):
            continue
        out.append(s)
    if tight and all(s.get("service_id")!="2d_floor_plan" for s in out):
        out.insert(0, {"service_id":"2d_floor_plan","name":"2D Floor Plan","rationale":"Tight rooms benefit from schematic clarity."})
    if likely_remote and all(s.get("service_id")!="zillow_3d" for s in out):
        out.insert(0, {"service_id":"zillow_3d","name":"Zillow 3D Tour","rationale":"Remote buyers need spatial continuity."})
    return out

class _BiasMini(BaseModel):
    key: str
    name: str
    definition: str
    why: str
    executionBullets: List[str] = Field(min_length=2, max_length=3)

class _ServiceItem(BaseModel):
    service_id: str
    name: str
    rationale: str

class _Stack(BaseModel):
    tier: str
    services: List[_ServiceItem]
    rationale: str

class _Decision(BaseModel):
    stacks: List[_Stack]
    biases: List[_BiasMini]

def _call_llm(intake: dict, sigs: dict, context: dict) -> dict:
    # Offline deterministic sample if no API key
    if not settings.OPENAI_API_KEY:
        return {
            "stacks":[
                {"tier":"High","services":[
                    {"service_id":"show_stopper","name":"Show Stopper","rationale":"Flagship visuals."},
                    {"service_id":"aerials","name":"Aerials","rationale":"Context and scale."}
                ],"rationale":"Max impact"},
                {"tier":"Medium","services":[
                    {"service_id":"zillow_3d","name":"Zillow 3D","rationale":"Continuity."},
                    {"service_id":"2d_floor_plan","name":"2D Floor Plan","rationale":"Clarity."}
                ],"rationale":"Core remote-friendly"},
                {"tier":"Low","services":[
                    {"service_id":"2d_floor_plan","name":"2D Floor Plan","rationale":"Clarity."},
                    {"service_id":"quick_snaps","name":"Quick Snaps","rationale":"Speed."}
                ],"rationale":"Lean, fast"}
            ],
            "biases":[
                {"key":"fluency","name":"Fluency","definition":"Ease","why":"Tight rooms / remote buyers","executionBullets":["Chunk specs","Simple headlines"]},
                {"key":"mere_exposure","name":"Mere Exposure","definition":"Familiarity","why":"Build repetition","executionBullets":["Series posts","Retargeting"]},
                {"key":"anchoring","name":"Anchoring","definition":"Lead with best","why":"Signature feature","executionBullets":["Lead with hero","Frame comparisons"]}
            ]
        }
    # Real LLM call (if key present)
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    sys = ("You are a marketing-production planner for residential listings. "
           "Compliance: schools/safety language must be factual; post-production limited to non-material removals + sky/grass. "
           "Return structured JSON only.")
    prompt = {"intake_facts": intake, "signals": sigs, "catalog_snippets": context,
              "instructions":{"always_three_tiers":True,"tiers":["High","Medium","Low"],"bias_count":3}}
    resp = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        response_format={"type":"json_object"},
        messages=[{"role":"system","content":sys},{"role":"user","content":str(prompt)}],
        temperature=0.3,
    )
    import json
    return json.loads(resp.choices[0].message.content)

def decide(answers: dict, sigs: dict, mode: str) -> dict:
    ctx = kb_store.retrieve_context(answers, k=8)
    raw = _call_llm(answers, sigs, ctx)
    try:
        dec = _Decision.model_validate(raw)
    except Exception:
        dec = _Decision.model_validate(_call_llm(answers, sigs, ctx))

    stacks = []
    for st in dec.stacks:
        pruned = _enforce_rules(answers, [s.model_dump() for s in st.services])
        stacks.append({"tier":st.tier, "services": pruned, "rationale": st.rationale})
    biases = [b.model_dump() for b in dec.biases]
    return {"stacks": stacks, "biases": biases}
