from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from fastapi.responses import JSONResponse
from app.orchestrator.agent_orchestrator import AgentOrchestrator
import os

router = APIRouter()
orch = AgentOrchestrator()

@router.post('/submit')
async def submit_application(applicant_id: str = Form(...), income: float = Form(...), family_size: int = Form(...),
                             employment_years: float = Form(...), assets_value: float = Form(...), files: List[UploadFile] = File(None)):
    saved = {}
    upload_dir = 'data/uploads'
    os.makedirs(upload_dir, exist_ok=True)
    for f in files or []:
        content = await f.read()
        path = os.path.join(upload_dir, f.filename)
        with open(path, 'wb') as fh:
            fh.write(content)
        saved[f.filename] = path
    form = {'applicant_id': applicant_id, 'income': income, 'family_size': family_size, 'employment_years': employment_years, 'assets_value': assets_value}
    result = orch.process_application(saved, form)
    return JSONResponse(result)