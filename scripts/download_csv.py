import requests

url = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publications_PMC.csv"
r = requests.get(url)
with open("data/raw/SB_publications_PMC.csv", "wb") as f:
    f.write(r.content)
