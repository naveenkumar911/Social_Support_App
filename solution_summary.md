# Solution Summary — CloudJune Social Support AI Prototype

## 1. Executive Summary
This prototype automates the evaluation of social support applications using a modular AI workflow. It ingests multimodal documents, extracts and validates applicant information, computes eligibility via a local ML model, stores semantic artifacts in a vector store, and provides LLM-based recommendations. The system is privacy-first (local model hosting), modular, and designed for deployment in government environments requiring data protection and auditability.

---

## 2. High-Level Architecture

```mermaid
flowchart LR
  subgraph Applicant
    A[Applicant Portal / Chatbot (Streamlit)]
    A -->|Uploads files + fills form| B[API Gateway (FastAPI)]
  end

  subgraph Backend
    B --> C[Ingest Module (OCR / Parser)]
    C --> D[Validation Module]
    D --> E[Feature Store / Postgres]
    C --> V[Embedding Service] --> Q[Vector Store (Qdrant mock)]
    D --> M[Eligibility ML (scikit-learn)]
    M --> R[Recommendation Agent (Local LLM via Ollama/OpenWebUI)]
    B --> O[Orchestrator Agent (Agentic controller)]
    O --> M
    O --> R
    O --> Q
  end

  subgraph Observability
    M --> Langfuse[Langfuse]
    R --> Langfuse
  end

  subgraph FrontendAdmin
    Admin[Reviewer Dashboard (Streamlit)]
    Admin --> B
  end
```
*(Use the Mermaid diagram above in README or slide deck; a PNG is included as placeholder.)*

---

## 3. Component Design & Responsibilities

### Frontend (Streamlit)
- Applicant-facing Chatbot & form for file uploads.
- Reviewer Dashboard that displays parsed documents, ML scores, and allows manual override.

### API Gateway (FastAPI)
- Routes: `/ingest/upload`, `/eligibility/predict`, `/chatbot/ask`, `/orchestrator/submit`.
- Stateless endpoints; delegates heavy-lifting to modular services.

### Ingest Module
- **OCR Service**: Extract text from images/PDFs (EasyOCR or Tesseract fallback).
- **Tabular Parser**: Parse CSV/XLSX into structured rows (pandas).
- **Sanitizer**: Normalize dates, currency, and names.

### Embedding & Vector Store
- **Embedding Service**: Uses `sentence-transformers` (all-MiniLM-L6-v2) with TF-IDF fallback.
- **Vector store**: Qdrant recommended for production; prototype includes a JSON-backed mock for local use.

### Eligibility ML
- **Model**: Scikit-learn RandomForest (explainable, fast inference). Stored as `models/eligibility_model.pkl`.
- **Features**: income, family_size, employment_years, assets_value + engineered features (debt-to-income, dependents ratio).
- **Explainability**: SHAP or permutation importance can be added for per-decision reasoning.

### Recommendation Agent (LLM)
- **Local LLM hosting**: Ollama or OpenWebUI to keep PII on-prem. The LLM produces upskilling and job-match suggestions based on applicant profile and regional training catalogs.
- **Agent orchestration**: A master orchestrator coordinates the validation, ML inference, and LLM recommendation steps. ReAct-like reasoning can be used for chain-of-thought where needed.

### Observability & Logging
- Langfuse for traces of LLM calls and agent actions.
- Structured logs for GDPR/audit compliance with request IDs and redaction of PII in logs.

---

## 4. Justification of Tool Choices

### Python
- **Suitability**: Rich ecosystem for ML, NLP, and web APIs.
- **Scalability**: Mature frameworks (FastAPI) and WSGI/ASGI deployment options.
- **Maintainability**: Widely adopted in government and enterprise contexts.

### FastAPI
- **Performance**: ASGI-based, supports async I/O for file uploads and concurrent processing.
- **Developer productivity**: Auto docs and type-safety with Pydantic.

### Streamlit
- **Rapid prototyping**: Enables an interactive UI for demos and reviewers.
- **Limitations**: Not a production-grade frontend; recommended to replace with React for full deployments.

### Scikit-learn (RandomForest)
- **Suitability**: Tabular, structured decision-making; interpretable with feature importances.
- **Performance/Maintainability**: Lightweight, fast inference, easy to retrain and version.

### Sentence-Transformers + Qdrant
- **Suitability**: Text semantic search, similarity queries for cross-document reconciliation and retrieving similar applicant patterns.
- **Scalability**: Qdrant scales horizontally; supports hybrid search and payload filters.
- **Security**: Can be self-hosted on government infrastructure.

### Ollama / OpenWebUI (Local LLM hosting)
- **Suitability**: Ensures PII stays on-prem and aligns with data residency requirements.
- **Performance**: Modern local LLMs (Llama2-family derivatives) run well on GPU-enabled servers; CPU-only can be used for smaller models.

### Langfuse
- **Observability**: Tracks LLM prompts, agent decisions, and helps in debugging, auditing, and monitoring model drift.

---

## 5. AI Workflow: Step-by-step

1. **Applicant interaction**: Applicant uploads forms and attachments via Streamlit Chatbot/Form.
2. **Ingestion**: Files saved and parsed by Ingest Module (OCR for images, pandas for tabular files).
3. **Data normalization**: Currency, date, and name normalization; deduplication of family members.
4. **Embeddings stored**: Extracted text embedded and upserted to Vector Store for retrieval and evidence linking.
5. **Validation checks**: Cross-document consistency checks (addresses, incomes). Violations flagged for reviewer or probabilistic correction.
6. **Eligibility inference**: ML model returns approve/soft-decline with probability. Explainability metadata attached.
7. **LLM recommendations**: For approved/soft-decline cases, the LLM suggests training, job matches, or both.
8. **Decision record**: Full decision payload stored in Postgres (or other RDBMS) for audit and downstream workflows.
9. **Reviewer UI**: Human reviewer inspects and can override; actions are logged.

---

## 6. Integration & API Design Considerations

### API Patterns
- Keep REST endpoints stateless and idempotent where possible.
- `/orchestrator/submit` accepts multipart form data for files and applicant metadata.
- Provide endpoints for async polling for long-running tasks (e.g., `/orchestrator/status/{id}`).
- Webhooks for downstream systems (benefits disbursement, case management).

### Data Pipeline
- Raw uploads stored in an immutable object store (S3 or government object store) with hashed filenames.
- ETL pipeline to normalize and project features into a feature store (e.g., Feast or simple Postgres tables).
- Use message queues (RabbitMQ/Kafka) for scaling ingestion and for decoupled processing.

### Privacy & Security
- Encrypt data at rest & in transit (TLS).
- PII redaction in logs and access controls for reviewer dashboards (role-based access).
- Local LLM hosting to meet data residency and privacy constraints.

---

## 7. Future Improvements

1. **Full production-grade Vector DB**: Replace JSON mock with Qdrant/Redis vector store; enable filtered retrieval and metadata queries.
2. **Document-level provenance**: Track source and timestamp for each extracted fact; use Neo4j for complex family/relationship graphs.
3. **Explainability**: Integrate SHAP/LIME for per-decision explanations and expose them in the reviewer UI.
4. **ModelOps**: CI/CD for models, automated retraining pipelines, and bias detection scans.
5. **Agent orchestration**: Integrate LangGraph or Crew.AI to support complex multi-agent flows with monitoring.
6. **Fraud detection**: Graph-based anomaly detection for repeated patterns, mismatched IDs, or synthetic identities.
7. **Localization**: Multi-language OCR and LLM prompt templates for Arabic and other local languages.

---

## 8. How to run the Prototype (local)
1. Install requirements: `pip install -r requirements.txt`
2. Start backend: `uvicorn app.main:app --reload --port 8000`
3. Start frontend: `streamlit run frontend/Home.py`
4. Use the Home UI to upload files, run eligibility, or call `/orchestrator/submit` to run the full pipeline.

---

## 9. Deliverables in Repo
- Full source code (FastAPI + Streamlit)
- `models/eligibility_model.pkl`
- `data/` with sample inputs
- `diagrams/` mermaid diagram (in README) and placeholders
- `README.md` with run instructions

---

## 10. Closing Notes
This prototype focuses on delivering the **core functionality** asked in the brief: multimodal ingestion, local ML + LLM usage, agent orchestration, and end-to-end demoability. The architecture supports replacing mock components with production-grade systems (Qdrant, Neo4j, Ollama) without structural changes.