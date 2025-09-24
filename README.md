# SocialSupport-AI

Prototype AI Workflow Automation for Social Security Applications.

This repository contains a minimal, runnable prototype to satisfy the CloudJune case study submission requirements:
- FastAPI backend exposing ingest, eligibility and chatbot endpoints.
- Streamlit frontend with a basic chatbot and file uploader demo.
- A simple scikit-learn eligibility model trained on synthetic data (`models/eligibility_model.pkl`).
- Instructions to run locally and with Docker.

## Quickstart (local)

```bash
# (optional) create venv
python -m venv venv
source venv/bin/activate   # windows: venv\\Scripts\\activate

pip install -r requirements.txt

# Start backend (FastAPI)
uvicorn app.main:app --reload --port 8000

# In a new terminal start frontend (Streamlit)
streamlit run frontend/Home.py
```

Backend runs on http://localhost:8000 by default. Streamlit UI runs on http://localhost:8501 by default.

## Files & Structure

- `app/` - FastAPI backend and services (OCR and LLM are mocked for the prototype)
- `frontend/` - Streamlit demo UI
- `models/` - Pre-trained mock eligibility model
- `data/` - Synthetic example inputs
- `README.md` - this file
- `requirements.txt` - Python dependencies
- `Dockerfile` & `docker-compose.yml` - simple service composition (postgres omitted in this minimal prototype)
