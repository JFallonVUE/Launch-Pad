import json, math
from typing import List, Tuple, Dict, Any

def _read_kb() -> Tuple[List[Dict[str,Any]], List[Dict[str,Any]]]:
    with open("./data/catalog.json", "r", encoding="utf-8") as f:
        services = json.load(f).get("services", [])
    with open("./data/biases.json", "r", encoding="utf-8") as f:
        biases = json.load(f).get("biases", [])
    return services, biases

def _bofe(text: str) -> Dict[str, float]:
    words = [w.lower() for w in text.split()]
    vec = {}
    for w in words:
        vec[w] = vec.get(w,0)+1.0
    return vec

def _cos(a: Dict[str,float], b: Dict[str,float]) -> float:
    dot = sum(a.get(k,0.0)*b.get(k,0.0) for k in set(a)|set(b))
    na = math.sqrt(sum(v*v for v in a.values())) or 1.0
    nb = math.sqrt(sum(v*v for v in b.values())) or 1.0
    return dot/(na*nb)

def build_or_refresh():
    return True

def retrieve_context(intake_facts: Dict[str,Any], k: int = 8) -> Dict[str,Any]:
    services, biases = _read_kb()
    query = " ".join([f"{k}:{v}" for k,v in intake_facts.items() if isinstance(v,(str,int,float))])
    qv = _bofe(query or "query")
    scored_s = sorted(
        [(s, _cos(qv, _bofe(s.get('name','')+' '+ ' '.join(s.get('deliverables',[]))))) for s in services],
        key=lambda x: x[1], reverse=True
    )[:max(3, min(k,8))]
    scored_b = sorted(
        [(b, _cos(qv, _bofe(b.get('name','')+' '+ b.get('definition','')+' '+' '.join(b.get('copy_patterns',[]))))) for b in biases],
        key=lambda x: x[1], reverse=True
    )[:max(3, min(k,8))]
    return {"services": [s for s,_ in scored_s], "biases": [b for b,_ in scored_b]}
