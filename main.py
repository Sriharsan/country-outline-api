from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_country_outline(country: str = Query(..., description="Country name")):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Could not fetch Wikipedia page for {country}"}

    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    markdown = ["## Contents", f"# {country}"]
    for heading in headings:
        level = int(heading.name[1])
        title = heading.get_text().strip()
        if title.lower() != "references":
            markdown.append(f"{'#' * level} {title}")

    return {"markdown": "\n\n".join(markdown)}
