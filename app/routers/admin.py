from fastapi import APIRouter
from app.services import ingest_docx, kb_store

router = APIRouter()

@router.post("/reload-kb")
def reload_kb():
    ingest_docx.build_kb_files()
    kb_store.build_or_refresh()
    return {"status": "reloaded"}
