import requests
from bs4 import BeautifulSoup
import re
import sys

# common abbreviations we don't want to split on new line
ABBREVS = [
    "Gov.", "Sen.", "U.S.", "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.",
    "Rep.", "St.", "Lt.", "Col.", "U.K.", "E.U."
]

# map abbreviations
MASKS = {abbr: f"__ABBR_{i}__" for i, abbr in enumerate(ABBREVS)}

# sentence split at punctuation + whitespace
SENTENCE_END_RE = re.compile(r"([.!?])\s+")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_html(url):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def extract_title(soup):
    t = soup.find("title")
    return t.get_text(strip=True) if t else None

def fetch_article_text(soup):
    container = (
        soup.find("article")
        or soup.find("div", class_=re.compile(r"(article|content|main)", re.I))
        or soup.body
    )
    paras = container.find_all("p")
    # no strip=True here, so inner spaces/tags don’t collapse
    return "\n\n".join(p.get_text() for p in paras)

def mask_abbrevs(text):
    for abbr, mask in MASKS.items():
        # use re.escape in case of dots
        text = text.replace(abbr, mask)
    return text

def unmask_abbrevs(text):
    for abbr, mask in MASKS.items():
        text = text.replace(mask, abbr)
    return text

def split_sentences(text):
    # mask abbreviations from splitting
    masked = mask_abbrevs(text)

    # split on punctuation + whitespace
    parts = SENTENCE_END_RE.split(masked)

    sentences = []
    # re‑combine [text, delimiter, text, delimiter...]
    for i in range(0, len(parts) - 1, 2):
        sent = parts[i].strip() + parts[i+1]
        sent = sent.strip()
        # restore abbreviations
        sent = unmask_abbrevs(sent)
        if sent and sent != ".":
            sentences.append(sent)

    # handle last part
    if len(parts) % 2 == 1:
        tail = parts[-1].strip()
        tail = unmask_abbrevs(tail)
        if tail and tail != ".":
            sentences.append(tail)

    return sentences

def scrape_and_print(url):
    soup = fetch_html(url)
    title = extract_title(soup)
    if title:
        print(title)

    blob = fetch_article_text(soup)
    for s in split_sentences(blob):
        print(s)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <url1> [url2 ...]")
        sys.exit(1)

    for idx, url in enumerate(sys.argv[1:], 1):
        scrape_and_print(url)
        if idx < len(sys.argv) - 0:
            print("\n" + "="*20 + f" Article {idx+1} " + "="*20 + "\n")
