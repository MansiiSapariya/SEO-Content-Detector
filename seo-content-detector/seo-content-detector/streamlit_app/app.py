
import streamlit as st
import pandas as pd
import numpy as np
import json
from utils.parser import scrape_url
from utils.features import (clean_text_basic, sentence_count, flesch_reading_ease,
                            load_embedder, vectorize_texts, vader_compound, ner_top)
from utils.scorer import load_quality_model, find_similar_factory

st.set_page_config(page_title="SEO Content Detector", layout="wide")
st.title("SEO Content Detector")
st.write("Analyze quality, duplicates, readability, sentiment, and entities.")

# Cache heavy resources for faster subsequent runs
@st.cache_resource
def get_model():
    return load_quality_model("models/quality_model.pkl")

@st.cache_resource
def get_embedder():
    return load_embedder()

model = get_model()
embedder = get_embedder()

uploaded_feats = st.file_uploader("Optional: Upload features.csv (to enable similarity to known pages)", type=["csv"])

index_urls, index_embeddings = [], None
if uploaded_feats:
    feats = pd.read_csv(uploaded_feats)
    emb = feats['embedding'].apply(lambda s: np.array(json.loads(s)))
    index_embeddings = np.vstack(emb.values)
    index_urls = feats['url'].tolist()

find_similar = find_similar_factory(index_embeddings, index_urls)

url = st.text_input("Enter a URL to analyze")
if st.button("Analyze") and url:
    title, body = scrape_url(url)
    ct = clean_text_basic(body)
    wc = len(ct.split()); sc = sentence_count(body); fre = flesch_reading_ease(body)
    sent = vader_compound(body)
    ner_total, ner_top5 = ner_top(body)
    vec = vectorize_texts(embedder, [ct])[0]
    similar = find_similar(vec, top_k=5, threshold=0.75) if index_embeddings is not None else []

    X_one = pd.DataFrame([{"word_count": wc, "sentence_count": sc, "flesch_reading_ease": fre,
                           "avg_paragraph_len": float(len(ct.split())/(sc or 1)), "list_density": 0.0}])
    try:
        pred = model.predict(X_one)[0]
    except:
        pred = "Medium"

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Core Metrics")
        st.json({
            "url": url, "title": title, "word_count": wc, "sentence_count": sc,
            "readability": fre, "quality_label": pred, "is_thin": bool(wc < 500)
        })
    with col2:
        st.subheader("Advanced NLP")
        st.json({
            "sentiment_vader_compound": sent,
            "ner_total": ner_total,
            "ner_top5": ner_top5
        })

    st.subheader("Similar Pages")
    st.json(similar if similar else [{"info":"Upload features.csv to enable similarity search"}])
