"""
Template: web_scraper_optimized.py
Pattern: Filtered HTML Extraction (Pattern 1) + Pre-Computed Selectors (Pattern 2)
Customize: TARGET_URL, SELECTORS, MAX_ITEMS, OUTPUT_PATH
"""

import json
import os
import sys
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

# --- CUSTOMIZE THESE ---
TARGET_URL  = "https://example.com"
OUTPUT_PATH = os.path.expanduser("~/.claude/skill-cache/scrape_output.json")
MAX_ITEMS   = 20

# CSS selectors — compute once with Claude, then hard-code
SELECTORS = {
    "title":   ".item-title",   # replace with actual selector
    "url":     ".item-link",    # replace with actual selector
    "summary": ".item-summary", # replace with actual selector
}

STRIP_TAGS = [
    "script","style","nav","footer","header","aside",
    "noscript","iframe","svg","form","meta","link",
]
# --- END CUSTOMIZE ---

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_page(url: str, timeout: int = 10) -> Optional[str]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"[ERROR] fetch failed: {e}", file=sys.stderr)
        return None


def filter_html(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(STRIP_TAGS):
        tag.decompose()
    return soup


def extract_items(soup: BeautifulSoup) -> list[dict]:
    items = []
    containers = soup.select(SELECTORS["title"])[:MAX_ITEMS]
    for el in containers:
        item: dict = {}
        title_el = el.select_one(SELECTORS["title"])
        item["title"] = title_el.get_text(strip=True) if title_el else ""
        url_el = el.select_one(SELECTORS["url"])
        item["url"] = url_el.get("href", "") if url_el else ""
        summary_el = el.select_one(SELECTORS["summary"])
        item["summary"] = summary_el.get_text(strip=True)[:200] if summary_el else ""
        if item["title"]:
            items.append(item)
    return items


def build_output(items: list[dict]) -> dict:
    return {
        "source":      TARGET_URL,
        "fetched_at":  datetime.now().isoformat(),
        "items":       items,
        "total_items": len(items),
        "truncated":   len(items) >= MAX_ITEMS,
    }


def main():
    html = fetch_page(TARGET_URL)
    if not html:
        print(json.dumps({"error": "fetch failed", "source": TARGET_URL}))
        sys.exit(1)

    soup   = filter_html(html)
    items  = extract_items(soup)
    output = build_output(items)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
