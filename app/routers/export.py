from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from app.deps import get_session, init_db
from app.models import Intake, ExportJob
from app.services import copywriter, export_docx

router = APIRouter()

class ExportRequest(BaseModel):
    intake_id: str
    chosen_tier: str  # High|Medium|Low
    chosen_bias_key: str

@router.post("/docx")
def export_docx_endpoint(req: ExportRequest, session: Session = Depends(get_session)):
    init_db()
    intake = session.exec(select(Intake).where(Intake.id == req.intake_id)).first()
    if not intake:
        raise HTTPException(status_code=404, detail="intake not found")
    job = ExportJob(intake_id=intake.id, chosen_tier=req.chosen_tier, chosen_bias_key=req.chosen_bias_key)
    session.add(job); session.commit(); session.refresh(job)

    copy_pack = copywriter.generate(intake=intake, chosen_tier=req.chosen_tier, chosen_bias=req.chosen_bias_key)
    outpath = export_docx.build_doc(intake=intake, copy_pack=copy_pack, chosen_tier=req.chosen_tier,
                                    chosen_bias=req.chosen_bias_key, job_id=job.id)
    job.status = "done"; job.file_path = outpath
    session.add(job); session.commit()

    url = f"/exports/{os.path.basename(outpath)}" if outpath else None
    return {"downloadUrl": url, "jobId": job.id}
