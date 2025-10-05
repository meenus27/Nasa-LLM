from scripts.summarize import summarize

def summarize_chunks(chunks):
    return [summarize(chunk) for chunk in chunks]
