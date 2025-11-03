
import re, numpy as np, textstat, spacy
from nltk.tokenize import sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer
from collections import Counter

# Load spaCy & VADER once at module import; in Streamlit, use cache in app for heavy models if needed
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import spacy.cli as spcli
    spcli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

sia = SentimentIntensityAnalyzer()

def clean_text_basic(s: str) -> str:
    s = (s or "").lower().strip()
    s = re.sub(r'\s+', ' ', s)
    return s

def sentence_count(s: str) -> int:
    try:
        return len(sent_tokenize(s)) if s else 0
    except Exception:
        return 0

def flesch_reading_ease(s: str) -> float:
    try:
        return float(textstat.flesch_reading_ease(s)) if s and len(s.split()) >= 5 else 0.0
    except Exception:
        return 0.0

def vader_compound(text: str) -> float:
    try:
        return sia.polarity_scores(text or '')['compound']
    except Exception:
        return 0.0

def ner_top(text: str):
    try:
        doc = nlp((text or "")[:30000])
        labels = [ent.label_ for ent in doc.ents]
        return len(labels), dict(Counter(labels).most_common(5))
    except Exception:
        return 0, {}

def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

def vectorize_texts(embedder, texts):
    return embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
