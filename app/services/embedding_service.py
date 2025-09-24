from pathlib import Path
import numpy as np
try:
    from sentence_transformers import SentenceTransformer
    MODEL = SentenceTransformer('all-MiniLM-L6-v2')
except Exception:
    MODEL = None
    from sklearn.feature_extraction.text import TfidfVectorizer
    VECT = TfidfVectorizer(max_features=512)
    FITTED = False

def embed_texts(texts):
    global FITTED
    if MODEL is not None:
        emb = MODEL.encode(texts, show_progress_bar=False)
        return [e.tolist() for e in emb]
    # TF-IDF fallback: fit-transform then pad/truncate to 512 dims
    if not FITTED:
        VECT.fit(texts)
        FITTED = True
    vecs = VECT.transform(texts).toarray()
    # pad/truncate
    dim = 512
    out = []
    for v in vecs:
        if len(v) < dim:
            v = list(v) + [0.0]*(dim - len(v))
        else:
            v = list(v[:dim])
        out.append(v)
    return out