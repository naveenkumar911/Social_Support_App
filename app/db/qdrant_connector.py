from pathlib import Path
import json, os
STORE = Path('data/qdrant_store.json')

def upsert_embeddings(records):
    # records: list of dicts {id: str, vector: list, payload: dict}
    store = []
    if STORE.exists():
        store = json.loads(STORE.read_text())
    ids = {r['id'] for r in store}
    for r in records:
        # replace if exists else append
        store = [s for s in store if s['id'] != r['id']]
        store.append(r)
    STORE.write_text(json.dumps(store, indent=2))
    return {'status':'ok', 'upserted': len(records)}

def search_similar(vector, top_k=5):
    # naive cosine similarity over stored vectors
    import numpy as np
    if not STORE.exists():
        return []
    store = json.loads(STORE.read_text())
    def cos(a,b):
        a = np.array(a); b = np.array(b)
        return float((a@b)/((np.linalg.norm(a)*np.linalg.norm(b))+1e-9))
    scored = []
    for item in store:
        score = cos(vector, item['vector'])
        scored.append({'id': item['id'], 'score': score, 'payload': item.get('payload')})
    scored = sorted(scored, key=lambda x: x['score'], reverse=True)[:top_k]
    return scored