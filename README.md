
# SEO Content Quality & Duplicate Detector

An end‑to‑end pipeline to analyze web pages for SEO readability, keyword usage, on‑page signals, and near‑duplicate detection, with an interactive Streamlit app for live URL analysis and corpus‑level similarity search.

## Live app

- Streamlit: https://seo-content-detector.streamlit.app

If the app is rebuilding, wait a minute and refresh.

## Features

- URL scraping and HTML parsing (requests, BeautifulSoup, lxml).
- Text cleaning and normalization (lowercasing, punctuation/HTML removal, Unicode fix, stopword handling).
- SEO metrics: title/description length, H1/H2 stats, word/unique counts, keyword density, outbound links count.
- Readability: textstat indices (Flesch Reading Ease, SMOG, Gunning Fog, Coleman–Liau, Automated Readability).
- Quality scoring: weighted composite score from readability + structural SEO features.
- Duplicate/similarity detection:
  - MinHash + LSH for fast near‑duplicates (datasketch).
  - Embedding‑based cosine similarity (sentence‑transformers) for semantic duplicates.
  - Optional fuzzy overlap (rapidfuzz).
- Advanced NLP (optional, toggle in code if installed): NER (spaCy), topic hints (BERTopic), sentiment (VADER).
- Visualizations: score gauges, distribution plots, word clouds, top duplicate pairs table.
- Batch processing notebook to build features.csv for your corpus and upload into the app.

## Repository structure

- streamlit_app/
  - app.py — Streamlit entrypoint
  - utils/
    - parser.py — fetching, HTML parsing, on‑page extractions
    - features.py — text preprocessing, feature engineering, embeddings
    - scorer.py — composite scoring, thresholds, display helpers
  - models/
    - quality_model.pkl — optional saved components (if used)
- data/ — optional example CSVs (features.csv, duplicates.csv)
- models/ — optional additional artifacts
- requirements.txt — dependencies
- README.md — this file

## Quick start (local)

1) Create environment and install:
- Python 3.11 recommended
- pip install -r requirements.txt

2) Run the app:
- streamlit run streamlit_app/app.py
- Open http://localhost:8501

3) Optional: Build corpus features (in notebook or script) to produce data/features.csv, then use the “Upload features.csv” widget to enable duplicate search against your corpus.

## Deploy to Streamlit Cloud

- Push this repo to GitHub (public).
- In Streamlit Community Cloud:
  - Repo: mansiisapariya/SEO-Content-Detector
  - Branch: main
  - Main file path: streamlit_app/app.py
  - Python version: 3.11 recommended
- Ensure requirements.txt is at the repository root.
- Deploy, wait for “App is running,” then use the live URL.

Tip: If build fails on heavy packages, temporarily remove bertopic, umap‑learn, and hdbscan from requirements.txt and comment their imports in app.py, then redeploy. Re‑add after the base app is stable.

## Usage walkthrough (app)

- Analyze a single URL
  - Enter page URL → Analyze.
  - View:
    - On‑page signals (title/meta length, headings, links).
    - Readability indices.
    - Keyword stats, wordcloud, basic sentiment (if enabled).
    - Composite quality score with recommendations.

- Duplicate detection
  - Upload features.csv (generated from your crawl).
  - The app computes candidate pairs by MinHash/LSH and/or cosine similarity of embeddings; shows top matches with similarity scores and links.

- Real‑time tweaks
  - Toggle “Advanced NLP” to enable NER/topic hints if dependencies are available.
  - Adjust similarity threshold sliders to broaden/narrow duplicate matches.

## Data preparation (batch)

- Crawl or list URLs to analyze.
- For each page:
  - Fetch HTML → parse text, title, meta, headings.
  - Clean text → compute features/readability.
  - Generate n‑gram shingles → MinHash signatures.
  - Optionally compute sentence‑transformer embeddings.
- Save per‑URL rows to data/features.csv with columns such as:
  - url, title, meta_desc, word_count, unique_terms, h1_count, h2_count, link_out_count
  - flesch, gunning_fog, smog, coleman_liau, automated_readability
  - keyword_density, stopword_ratio, char_len, avg_sentence_len
  - minhash_sig (or bands), embed_384/768 (if serialized), quality_score

## Configuration

- Thresholds: adjust duplicate similarity cutoffs (e.g., cosine ≥ 0.85, Jaccard ≥ 0.8) in scorer.py.
- Weighting: tune the quality score weights across readability vs. structural signals.
- Caching: heavy models/embedders are wrapped in st.cache_resource to reduce reloads.
- Timeouts: requests timeouts/retries configurable in parser.py.

## Requirements

Core:
- streamlit
- beautifulsoup4
- lxml
- requests
- pandas, numpy
- textstat
- scikit‑learn
- sentence‑transformers
- rapidfuzz
- unidecode
- nltk
- datasketch
- matplotlib, seaborn, wordcloud, plotly

Optional (advanced NLP):
- spacy
- bertopic
- umap‑learn
- hdbscan

If deploying to Streamlit Cloud, prefer Python 3.11 and consider commenting advanced packages initially.

## Troubleshooting

- File not found / wrong entrypoint
  - Main file path must be streamlit_app/app.py and requirements.txt at repo root.
- Missing packages (e.g., ModuleNotFoundError: bs4)
  - Confirm requirements.txt is at root and the build logs show installation lines; Reboot/Re‑deploy.
- Nested repo path in logs (…/repo/repo/streamlit_app/app.py)
  - Flatten the repo; remove extra nested folder layer; update Main file path.
- App URL access error
  - Ensure app visibility is Public in Streamlit settings; open from Your apps and copy that URL.

## Roadmap

- Crawl scheduler and sitemap ingestion.
- Richer on‑page audits (canonical, robots, structured data hints).
- Multilingual models and i18n readabilities.
- Incremental LSH index for large corpora.
- Export reports (PDF/CSV) per URL with charts.
