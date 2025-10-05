import csv, requests, os, json
from bs4 import BeautifulSoup


RAW_DIR = "data/raw"
META_DIR = "data/metadata"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)


def fetch_article(pmc_url, title):
    if not pmc_url.startswith("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC"):
        print(f"⚠️ Skipping malformed URL: {pmc_url}")
        return

    pmc_id = pmc_url.strip("/").split("/")[-1]
    plain_text_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/?report=plaintext"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(plain_text_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch {title}: {e}")
        return

    with open(f"{RAW_DIR}/{pmc_id}.txt", "w", encoding="utf-8") as f:
        f.write(response.text)

    metadata = {
        "pmc_id": pmc_id,
        "title": title,
        "source_url": pmc_url
    }

    with open(f"{META_DIR}/{pmc_id}.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Downloaded: {title}")





with open("data/raw/SB_publications_PMC.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 2:
            continue  # Skip rows with missing title or URL
        title, url = row
        fetch_article(url, title)
