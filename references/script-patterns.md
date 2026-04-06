# Script Patterns for Skills

Eight patterns for token-efficient, high-performance skill scripts.
Read by the Script Engineer agent during Phase 2 design.
Also read during Audit mode for Type A and D skills.

---

## Pattern 1: Filtered HTML Extraction

Never return raw HTML to the model. Filter before returning.

Tags to always strip: `script`, `style`, `nav`, `footer`, `header`, `aside`,
`noscript`, `iframe`, `svg`, `form`, `meta`, `link`

Result: typically 85-95% token reduction on standard web pages.
A page that returns 8,000 tokens raw returns under 1,000 filtered.

```python
from bs4 import BeautifulSoup

STRIP_TAGS = ['script','style','nav','footer','header','aside',
              'noscript','iframe','svg','form','meta','link']

def extract_clean_text(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(STRIP_TAGS):
        tag.decompose()
    return soup.get_text(separator='\n', strip=True)
```

When to use: any skill that fetches web pages (Pattern 1 is always on).

---

## Pattern 2: Pre-Computed Selectors

If you know the structure of a page you will scrape repeatedly,
compute the CSS selectors once and hard-code them. Never re-analyze
page structure on every run — that burns tokens and introduces variance.

How to get selectors: paste the page HTML into Claude once and ask:
"Extract the CSS class selectors for [field 1], [field 2], [field 3]."
Then hard-code the result in the script.

```python
# Computed once, hard-coded forever
SELECTORS = {
    'title':    '.story-link .titleline > a',
    'score':    '.score',
    'user':     '.hnuser',
    'comments': '.subtext a:last-child',
}
```

When to use: any skill that scrapes the same site repeatedly.

---

## Pattern 3: Script as Heavy Lifter

The model decides what to fetch and what to do with the result.
The script does the fetching, filtering, parsing, and formatting.
No data processing logic should live in model instructions.

Decision boundary:
- Model: "Go get the top 10 Hacker News stories from the last 6 hours"
- Script: fetches, filters, parses, returns structured JSON
- Model: "Here are the stories. Summarize the two most relevant to my project."

If the model is making decisions about data shape or structure on every run,
that logic belongs in a script.

When to use: all Type A and Type D skills.

---

## Pattern 4: Strict Output Schema

Every script must return data in a defined schema. Define it before writing the script.
Reject any script output that doesn't conform. Prefer JSON for structured data.

```python
import json
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Item:
    title: str
    url: str
    summary: str

@dataclass
class ScriptOutput:
    source: str
    fetched_at: str
    items: List[Item]
    total_items: int
    truncated: bool

def to_json(output: ScriptOutput) -> str:
    return json.dumps(asdict(output), indent=2)
```

When to use: all scripts. No exceptions.

---

## Pattern 5: Limits and Stop Conditions

Never let a script paginate or loop without a hard ceiling.
Every loop needs a max_pages or max_items constant at the top of the script.

```python
MAX_PAGES = 3
MAX_ITEMS = 30
MAX_API_CALLS = 5

# In the loop:
if page_count >= MAX_PAGES or len(items) >= MAX_ITEMS:
    output.truncated = True
    break
```

Without stop conditions, a skill will fill the context window on edge cases.
Define the limit in the script, not in SKILL.md instructions.

When to use: any script that paginates or loops.

---

## Pattern 6: Incremental Runs

For skills that run repeatedly on the same source, track state.
On each run, load the last checkpoint and only process new items.

```python
import json, os
from datetime import datetime

STATE_FILE = os.path.expanduser('~/.claude/skill-state/{skill_name}.json')

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {'last_run': None, 'last_id': None}

def save_state(last_id: str):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump({'last_run': datetime.now().isoformat(), 'last_id': last_id}, f)
```

When to use: any skill that monitors a source over time (daily briefings, news monitors,
feed trackers, etc.).

---

## Pattern 7: Parallel Batch Execution

For skills that call 3+ sources or run 3+ searches, use threading.
Each sequential call adds the full conversation context to the next turn.
Batching eliminates the compounding overhead.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Any

def batch_fetch(tasks: List[dict], fetch_fn: Callable, max_workers: int = 5) -> List[Any]:
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_fn, task): task for task in tasks}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append({'error': str(e), 'task': futures[future]})
    return results
```

When to use: any skill with 3+ parallel fetches (multi-source briefings, batch searches,
competitive monitoring, etc.).

---

## Pattern 8: Hard-Coded Configuration

Bake known values directly into the script. Never ask the model to supply
configuration it can't know at runtime.

Things to hard-code:
- Site URLs you always scrape
- CSS selectors (see Pattern 2)
- Field names and category labels
- Username or account identifiers
- Proxy settings
- Output file paths

```python
# Configuration block at top of every script
CONFIG = {
    'target_url':  'https://news.ycombinator.com',
    'output_path': os.path.expanduser('~/.claude/skill-cache/hn.json'),
    'max_items':   20,
    'fields':      ['title', 'url', 'score', 'comments'],
}
```

When to use: any script that hits a known endpoint.

---

## Retrofit Candidates — Identifying Skills That Need Scripts

When auditing an existing skill library, flag any skill that:

| Signal | Action |
|--------|--------|
| Makes 3+ sequential API/MCP calls | Apply Pattern 7 (parallel) |
| Fetches web pages and passes raw HTML | Apply Pattern 1 (filter) |
| Re-analyzes page structure on every run | Apply Pattern 2 (selectors) |
| Runs daily/periodically with no state | Apply Pattern 6 (incremental) |
| Has no hard limits on pagination or loops | Apply Pattern 5 (stop conditions) |
| Returns unstructured text from scripts | Apply Pattern 4 (schema) |

Start with the highest-frequency skills — the ones that run daily will see the biggest
token savings from even small efficiency improvements.
