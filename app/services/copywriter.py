from app.config import settings
from app.services.kb_store import retrieve_context

def _offline_pack():
    return {
        "core_listing_print":{
            "MLS description":"Neutral, factual description...",
            "Flyer/Brochure":{"headline":"Crisp Headline","short narrative":"Neutral lines.","bulleted specs":["3 beds","2 baths","1,800 sqft"]},
            "Feature Sheet":{"Rooms":{"Kitchen":"Quartz, SS","Living":"View window"},"Upgrades/Brands":["Bosch","Kohler"]}
        },
        "digital_social":{
            "Just Listed":["Post A","Post B"],
            "Open House":["Post A","Post B"],
            "Feature Highlights":["Highlight 1","Highlight 2","Highlight 3"],
            "Under Contract/Sold":["Wrap post"],
            "Video scripts":{"walkthrough_60_120s":"Script...","reels_15_60s":"Short script..."},
            "Single-property website copy":"SPW block...",
            "Ads":["Variant1","Variant2","Variant3","Variant4","Variant5"]
        },
        "direct_outreach":{
            "New Listing email blast":"Email...",
            "Inquiry response templates":{"SMS":"SMS...", "Email":"Email..."},
            "Open House follow-up email":"Follow-up..."
        },
        "cadence":{"Phase I":["Morning 9–11a","Lunch 12–2p","Evening 5–8p"],
                   "Phase II":["Morning 9–11a","Lunch 12–2p","Evening 5–8p"]},
        "ops_checklists":{"Homeowner Prep":["Declutter","Lights on"],"Run of Show":["Arrival","Coverage"],"Gallery Order":["Exteriors first"],"3D/Plan Placement":["Embed in SPW"],"Retouch Notes":["Non-material removals only"]},
        "kpis":["CTR","Video completion","Lead replies"],
        "disclaimers":{"schools_safety":"School and safety references must remain factual only—use names, distances, links.","post_production":"Post-production limited to non-material item removals and sky/grass adjustments."}
    }

def _call_llm(intake, chosen_stack, chosen_bias, kb_context):
    if not settings.OPENAI_API_KEY:
        return _offline_pack()
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    sys = ("You write neutral, factual, bias-aware listing content. "
           "Compliance: schools/safety factual only. Post-production limited. Return JSON.")
    prompt = {"intake": intake, "chosen_stack": chosen_stack, "chosen_bias": chosen_bias, "kb_context": kb_context}
    resp = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        response_format={"type":"json_object"},
        temperature=0.3,
        messages=[{"role":"system","content":sys},{"role":"user","content":str(prompt)}]
    )
    import json
    return json.loads(resp.choices[0].message.content)

def generate(intake, chosen_tier, chosen_bias):
    stacks = intake.stacks
    chosen_stack = next(s for s in stacks if s["tier"].lower()==chosen_tier.lower())
    kb = retrieve_context(intake.answers, k=6)
    bias = next((b for b in intake.biases if b["key"]==chosen_bias), intake.biases[0])
    pack = _call_llm(intake={"answers":intake.answers,"signals":intake.signals}, chosen_stack=chosen_stack, chosen_bias=bias, kb_context=kb)
    pack.setdefault("disclaimers",{})
    pack["disclaimers"].setdefault("schools_safety","School and safety references must remain factual only—use names, distances, and links.")
    pack["disclaimers"].setdefault("post_production","Post-production limited to non-material item removals and sky/grass adjustments.")
    return pack
