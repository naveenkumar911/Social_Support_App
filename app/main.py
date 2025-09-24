from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ingest, eligibility, chatbot, orchestrator

app = FastAPI(title="CloudJune Social Support API - Prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])\napp.include_router(orchestrator.router, prefix="/orchestrator", tags=["orchestrator"])
app.include_router(eligibility.router, prefix="/eligibility", tags=["eligibility"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])

@app.get('/health')
def health():
    return {'status':'ok'}