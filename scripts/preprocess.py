import os, re, json
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

# Download punkt tokenizer if not already present
nltk.download('punkt')

# Setup manual tokenizer fallback
punkt_param = PunktParameters()
sentence_tokenizer = PunktSentenceTokenizer(punkt_param)

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

def extract_sections(text):
    sections = {}
    patterns = {
        "Introduction": r"(?:^|\n)(Introduction|Background|Objective)(.*?)(?=\n[A-Z][a-zA-Z ]{3,}|$)",
        "Results": r"(?:^|\n)(Results|Findings|Observations)(.*?)(?=\n[A-Z][a-zA-Z ]{3,}|$)",
        "Conclusion": r"(?:^|\n)(Conclusion|Discussion|Summary|Interpretation)(.*?)(?=\n[A-Z][a-zA-Z ]{3,}|$)"
    }
    for name, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            sections[name] = match.group(2).strip()
    return sections

def chunk_text(text, max_tokens=500):
    try:
        sentences = sentence_tokenizer.tokenize(text)
    except Exception as e:
        print(f"⚠️ Tokenization failed: {e}")
        return []

    chunks, current = [], []
    token_count = 0
    for sentence in sentences:
        tokens = sentence.split()
        token_count += len(tokens)
        current.append(sentence)
        if token_count >= max_tokens:
            chunks.append(" ".join(current))
            current, token_count = [], 0
    if current:
        chunks.append(" ".join(current))
    return chunks

processed_count = 0

for filename in os.listdir(RAW_DIR):
    if not filename.endswith(".txt"):
        continue

    pmc_id = filename.replace(".txt", "")
    with open(os.path.join(RAW_DIR, filename), "r", encoding="utf-8") as f:
        text = f.read()

    sections = extract_sections(text)
    if not sections:
        print(f"⚠️ No sections found in {pmc_id}, chunking full text.")
        sections["FullText"] = text  # ✅ fallback to full text

    all_chunks = []
    for section_name, section_text in sections.items():
        chunks = chunk_text(section_text)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "pmc_id": pmc_id,
                "section": section_name,
                "chunk_id": f"{pmc_id}_{section_name}_{i}",
                "text": chunk
            })

    if all_chunks:
        with open(os.path.join(PROCESSED_DIR, f"{pmc_id}_chunks.json"), "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, indent=2)
        processed_count += 1

print(f"✅ Preprocessed {processed_count} articles.")
