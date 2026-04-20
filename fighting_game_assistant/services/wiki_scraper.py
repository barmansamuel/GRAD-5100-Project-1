# services/wiki_scraper.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {"User-Agent": "FGC-RAG-Bot/1.0"}

SOURCES = {
    "supercombo": "https://wiki.supercombo.gg/w/",
    "dustloop":   "https://www.dustloop.com/wiki/index.php?title=",
    "mizuumi":    "https://wiki.gbl.gg/w/",
}

# Phrases that appear in MediaWiki "page not found" pages
NOT_FOUND_SIGNALS = [
    "there is currently no text in this page",
    "this page does not exist",
    "no text in this page",
    "page does not exist",
    "search for this page title",
]


def _page_is_missing(soup: BeautifulSoup) -> bool:
    """Return True if the wiki served a 'page not found' placeholder."""
    text = soup.get_text(separator=" ").lower()
    return any(signal in text for signal in NOT_FOUND_SIGNALS)


def build_urls(game: str, character: str) -> list[str]:
    page = f"{game}/{character}"
    return [base + quote(page, safe="/") for base in SOURCES.values()]


def scrape(game: str, character: str) -> list[str]:
    """
    Scrape wiki pages for the given game/character.
    Returns a list of text chunks, or an empty list if nothing useful was found.
    """
    texts: list[str] = []

    for url in build_urls(game, character):
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
        except requests.RequestException:
            # Network error — skip this source silently
            continue

        # Treat any non-200 status as "not found" for this source
        if r.status_code != 200:
            continue

        soup = BeautifulSoup(r.text, "lxml")

        # Detect wiki's own "page not found" pages (they still return HTTP 200)
        if _page_is_missing(soup):
            continue

        # Remove noise
        for tag in soup(["script", "style"]):
            tag.decompose()

        content = soup.find("div", {"id": "mw-content-text"})
        if not content:
            continue

        # Keep tables — they contain frame data which is valuable
        for tag in content.find_all(["p", "li", "td", "th"]):
            text = tag.get_text(separator=" ", strip=True)
            if len(text) > 40:
                texts.append(text)

    return texts