
# SEO Content Detector

End-to-end pipeline for SEO content quality scoring and duplicate detection with a Colab notebook and optional Streamlit app.

## Setup
git clone https://github.com/MansiiSapariya/SEO-Content-Detector
cd seo-content-detector
pip install -r requirements.txt
jupyter notebook notebooks/seo_pipeline.ipynb

## Quick Start
- Place data.csv under data/ with columns: url, html_content.
- Run the notebook cells.
- Outputs:
  - data/extracted_content.csv
  - data/features.csv
  - data/duplicates.csv
  - models/quality_model.pkl

## Key Decisions
- Parsing: <main>/<article> preferred; boilerplate stripped via tag removal.
- Similarity: MinHash LSH for lexical candidates + cosine on MiniLM embeddings; tuned thresholds.
- Classifier: RandomForest on content + structure features; baseline = word_count rule.
- Advanced NLP: VADER sentiment, spaCy NER, BERTopic topics; TF-IDF keyword improvements.

## Results Summary
- See classification report & confusion matrix in notebook.
- Duplicates: data/duplicates.csv and heatmap in notebook.
- Real-time: analyze_url(url) returns quality & similar pages.

## Limitations
- Extraction varies by site template and language.
- Readability is advisory; pair with structure and intent.
- LSH/cosine thresholds require corpus-specific tuning.

## Streamlit
- Deployed URL: https://seo-content-detector-gh7ewkbschvgcjm7wnscbv.streamlit.app/
