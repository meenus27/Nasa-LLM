import os
import json
from transformers import pipeline, AutoTokenizer

CHUNK_DIR = "data/processed"
SUMMARY_DIR = "data/summaries"
os.makedirs(SUMMARY_DIR, exist_ok=True)

# Use a fast model for CPU
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
summarizer = pipeline("summarization", model=MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

MAX_TOKENS = 1024  # model input limit
MAX_SEGMENTS = 5   # limit segments per chunk

def split_text_by_tokens(text, max_tokens=MAX_TOKENS):
    tokens = tokenizer.encode(text)
    segments = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(seg, skip_special_tokens=True) for seg in segments]

for filename in os.listdir(CHUNK_DIR):
    if not filename.endswith("_chunks.json"):
        continue

    pmc_id = filename.replace("_chunks.json", "")
    print(f"\n🔄 Summarizing {pmc_id}...")

    with open(os.path.join(CHUNK_DIR, filename), "r", encoding="utf-8") as f:
        chunks = json.load(f)

    summaries = []
    for chunk in chunks:
        text = chunk["text"]
        segments = split_text_by_tokens(text)[:MAX_SEGMENTS]

        combined_summary = ""
        for i, segment in enumerate(segments):
            input_tokens = len(tokenizer.encode(segment))
            max_len = max(30, min(80, input_tokens // 2))  # dynamic max_length

            try:
                result = summarizer(
                    segment,
                    max_length=max_len,
                    min_length=25,
                    do_sample=False,
                    num_beams=2
                )
                combined_summary += result[0]["summary_text"] + " "
            except Exception as e:
                print(f"⚠️ Failed to summarize segment {i} of {chunk['chunk_id']}: {e}")

        if combined_summary.strip():
            summaries.append({
                "chunk_id": chunk["chunk_id"],
                "section": chunk["section"],
                "summary": combined_summary.strip()
            })

    if summaries:
        with open(os.path.join(SUMMARY_DIR, f"{pmc_id}_summary.json"), "w", encoding="utf-8") as f:
            json.dump(summaries, f, indent=2)
        print(f"✅ Saved {len(summaries)} summaries to {pmc_id}_summary.json")
    else:
        print(f"⚠️ No valid summaries for {pmc_id}. Skipping save.")

print("\n🏁 All articles summarized.")

