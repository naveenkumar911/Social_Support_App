from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatReq(BaseModel):
    message: str

@router.post('/ask')
def ask(req: ChatReq):
    # Mock chatbot: echo + simple rule-based guidance
    msg = req.message.lower()
    if 'upskill' in msg or 'training' in msg:
        return {'reply': 'Recommended programs: Basic Data Entry, Retail Customer Service, Digital Marketing short courses.'}
    if 'eligibility' in msg:
        return {'reply': 'Upload your documents and run eligibility check via /eligibility/predict'}
    return {'reply': f'ECHO: {req.message}'}