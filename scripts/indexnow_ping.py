#!/usr/bin/env python3
"""Ping IndexNow (api.indexnow.org) with every URL in sitemap.xml.
Bing's index powers ChatGPT web search; 200/202 = accepted.
Key file lives at the repo root and is deployed at https://oneiromusic.com/<key>.txt
"""
import glob, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "oneiromusic.com"

key_files = [f for f in glob.glob(os.path.join(ROOT, "*.txt"))
             if re.fullmatch(r"[0-9a-f]{32}\.txt", os.path.basename(f))]
if not key_files:
    sys.exit("No IndexNow key file (32-hex .txt) found at repo root")
key = os.path.basename(key_files[0])[:-4]

sitemap = open(os.path.join(ROOT, "sitemap.xml")).read()
urls = re.findall(r"<loc>(.*?)</loc>", sitemap)
if not urls:
    sys.exit("No URLs found in sitemap.xml")

payload = {
    "host": HOST,
    "key": key,
    "keyLocation": f"https://{HOST}/{key}.txt",
    "urlList": urls,
}
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json; charset=utf-8"},
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow: HTTP {r.status} for {len(urls)} URLs: {', '.join(urls)}")
except urllib.error.HTTPError as e:
    print(f"IndexNow: HTTP {e.code} — {e.read().decode()[:200]}")
    sys.exit(1)
