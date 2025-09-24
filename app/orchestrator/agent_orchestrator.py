from typing import Dict, Any
from app.services import ocr_service, tabular_service, embedding_service, eligibility_service
from app.db import qdrant_connector

class AgentOrchestrator:
    \"\"\"Simple orchestrator coordinating ingestion -> validation -> eligibility -> recommendation.\"\"\"
    def __init__(self):
        pass

    def process_application(self, files: Dict[str, str], form: Dict[str, Any]):
        # files: dict of filename -> path
        # form: structured form fields
        # 1. Ingest and extract text/tabular
        extracted = {}
        for fname, path in files.items():
            if fname.lower().endswith(('.png','.jpg','.jpeg','.tiff')):
                extracted[fname] = ocr_service.extract_text_from_image(path)
            elif fname.lower().endswith(('.csv','.xls','.xlsx')):
                extracted[fname] = tabular_service.parse_file(path)
            else:
                try:
                    extracted[fname] = open(path).read()
                except:
                    extracted[fname] = 'unreadable'
        # 2. Create embeddings for textual content to store in vector DB
        texts = []
        for k,v in extracted.items():
            if isinstance(v, list):
                # tabular preview to string
                texts.append(str(v))
            else:
                texts.append(v)
        embs = embedding_service.embed_texts(texts)
        records = []
        for i, t in enumerate(texts):
            records.append({'id': f\"{form.get('applicant_id','unknown')}_{i}\", 'vector': embs[i], 'payload': {'source': list(files.keys())[i], 'text': t[:200]}})
        qdrant_connector.upsert_embeddings(records)
        # 3. Validate & run eligibility ML
        features = {
            'income': form.get('income', 0.0),
            'family_size': form.get('family_size', 1),
            'employment_years': form.get('employment_years', 0.0),
            'assets_value': form.get('assets_value', 0.0)
        }
        eligibility = eligibility_service.predict_eligibility(features)
        # 4. Return a combined response
        return {'extracted_preview': {k:(v[:200] if isinstance(v,str) else v[:3] if isinstance(v,list) else str(v)) for k,v in extracted.items()}, 'eligibility': eligibility}