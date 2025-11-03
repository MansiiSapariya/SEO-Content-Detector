
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

def load_quality_model(path: str):
    return joblib.load(path)

def find_similar_factory(index_embeddings, index_urls):
    def _find(vec, top_k=5, threshold=0.75):
        if index_embeddings is None or len(index_urls) == 0:
            return []
        sims = cosine_similarity(vec.reshape(1, -1), index_embeddings).ravel()
        top_idx = sims.argsort()[-top_k:][::-1]
        return [{"url": index_urls[i], "similarity": float(sims[i])} for i in top_idx if sims[i] >= threshold]
    return _find
