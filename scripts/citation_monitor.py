#!/usr/bin/env python3
"""Weekly AI-citation monitor for oneiromusic.com.
Runs real buyer queries through Perplexity (sonar), records whether oneiromusic.com
is cited or mentioned, which rival domains ARE cited, and appends JSONL history.
Key: PERPLEXITY_API_KEY from ~/agentforge/.env (never printed).
"""
import json, os, re, sys, time, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, "scripts", "citation-history.jsonl")
DOMAIN = "oneiromusic.com"

QUERIES = [
    "best Greek band for a wedding in Michigan",
    "Greek wedding band Detroit",
    "live Greek band for hire in the Midwest",
    "Greek band for a baptism reception",
    "who should I hire for live music at a Greek festival in the US",
    "Greek bouzouki band for weddings",
    "Greek American wedding entertainment band",
    "band that plays laika and dimotika for events",
    "Greek band for a glendi",
    "hire a Greek band for a destination wedding",
    "live Greek music for a corporate event in Michigan",
    "best live Greek bands in the United States",
]

def api_key():
    for line in open(os.path.expanduser("~/agentforge/.env")):
        m = re.match(r"\s*PERPLEXITY_API_KEY\s*=\s*(.+)\s*", line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    sys.exit("PERPLEXITY_API_KEY not found in ~/agentforge/.env")

def ask(key, q):
    body = json.dumps({
        "model": "sonar",
        "messages": [{"role": "user", "content": q}],
    }).encode()
    req = urllib.request.Request(
        "https://api.perplexity.ai/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def domains_of(urls):
    out = []
    for u in urls or []:
        m = re.match(r"https?://(?:www\.)?([^/]+)", u)
        if m:
            out.append(m.group(1).lower())
    return out

def main():
    key = api_key()
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    rows = []
    for q in QUERIES:
        try:
            resp = ask(key, q)
        except Exception as e:
            rows.append({"ts": ts, "query": q, "error": str(e)[:120]})
            continue
        cites = resp.get("citations") or resp.get("search_results") or []
        urls = [c if isinstance(c, str) else c.get("url", "") for c in cites]
        doms = domains_of(urls)
        answer = (resp.get("choices") or [{}])[0].get("message", {}).get("content", "")
        cited = any(DOMAIN in d for d in doms)
        mentioned = ("oneiro" in answer.lower())
        rows.append({"ts": ts, "query": q, "cited": cited, "mentioned": mentioned,
                     "cited_domains": doms[:10]})
        time.sleep(1)

    with open(HIST, "a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    ok = [r for r in rows if r.get("cited")]
    men = [r for r in rows if r.get("mentioned") and not r.get("cited")]
    absent = [r for r in rows if not r.get("cited") and not r.get("mentioned") and "error" not in r]
    errs = [r for r in rows if "error" in r]
    print(f"=== Citation monitor {ts} — {DOMAIN} ===")
    print(f"CITED: {len(ok)}/{len(QUERIES)}")
    for r in ok: print(f"  + {r['query']}")
    print(f"MENTIONED (no citation): {len(men)}")
    for r in men: print(f"  ~ {r['query']}")
    print(f"ABSENT: {len(absent)}")
    for r in absent: print(f"  - {r['query']}")
    if errs: print(f"ERRORS: {len(errs)}: " + "; ".join(r['query'] for r in errs))
    rivals = {}
    for r in rows:
        for d in r.get("cited_domains", []):
            if DOMAIN not in d:
                rivals[d] = rivals.get(d, 0) + 1
    top = sorted(rivals.items(), key=lambda x: -x[1])[:12]
    print("TOP CITED RIVAL DOMAINS:")
    for d, n in top: print(f"  {n:2d}x {d}")

if __name__ == "__main__":
    main()
