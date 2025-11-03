
import re, requests
from bs4 import BeautifulSoup
from unidecode import unidecode

headers = {"User-Agent": "Mozilla/5.0 (compatible; SEOContentDetector/1.0; +https://example.com/bot)"}

def extract_main_text(html):
    try:
        soup = BeautifulSoup(html or "", "lxml")
        container = soup.find('main') or soup.find('article') or soup.body or soup
        for tag in container.find_all(['script','style','nav','footer','header','form','aside']):
            tag.decompose()
        paragraphs = [p.get_text(" ", strip=True) for p in container.find_all('p')]
        text = " ".join(paragraphs) if paragraphs else container.get_text(" ", strip=True)
        text = re.sub(r'\s+', ' ', text).strip()
        return unidecode(text)
    except Exception:
        return ""

def extract_title(html):
    try:
        soup = BeautifulSoup(html or "", "lxml")
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            return og.get("content").strip()
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(" ", strip=True)
        return ""
    except Exception:
        return ""

def scrape_url(url: str, timeout=12):
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            return "", ""
        return extract_title(resp.text), extract_main_text(resp.text)
    except Exception:
        return "", ""
