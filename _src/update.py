"""Fetch the latest publication data and metrics into _src/data.json.

Sources
- ORCID public API: journal articles (new DOIs are added to the site) and peer-review count.
- Crossref: author list, journal, volume and pages for newly found DOIs.
- Google Scholar profile page: citations, h-index, i10-index. If Scholar cannot be reached,
  the last known values are kept (OpenAlex is used only if no Scholar value exists yet).

Run by .github/workflows/update.yml 3 times a day. Standard library only.
"""
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ORCID = "0000-0001-5032-292X"
SCHOLAR_USER = "-c7W-o0AAAAJ"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data.json")
BUILD = os.path.join(HERE, "build.py")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def log(*a):
    print("[update]", *a, file=sys.stderr)


def fetch(url, accept=None, timeout=30):
    headers = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
    if accept:
        headers["Accept"] = accept
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def fetch_json(url):
    return json.loads(fetch(url, accept="application/json"))


def curated_dois():
    """DOIs already curated by hand in build.py (keys of the METRICS dict)."""
    src = open(BUILD, encoding="utf-8").read()
    return {d.lower() for d in re.findall(r'^\s*"(10\.[^"]+)":\s*\(', src, re.M)}


# ---------------------------------------------------------------- ORCID
def orcid_journal_articles(works_json):
    out = []
    for g in works_json.get("group", []):
        s = g["work-summary"][0]
        if s.get("type") != "journal-article":
            continue
        ids = (g.get("external-ids") or {}).get("external-id") or []
        doi = next((e["external-id-value"] for e in ids if e.get("external-id-type") == "doi"), None)
        if not doi:
            continue
        year = ((s.get("publication-date") or {}).get("year") or {}).get("value")
        out.append({"doi": doi.strip().lower(),
                    "year": int(year) if year else None,
                    "title": s["title"]["title"]["value"],
                    "journal": (s.get("journal-title") or {}).get("value") or ""})
    return out


def orcid_peer_review_count(pr_json):
    n = 0
    for g in pr_json.get("group", []):
        for pg in g.get("peer-review-group", []):
            n += len(pg.get("peer-review-summary", []))
    return n


# ---------------------------------------------------------------- Crossref
def initials(given):
    parts = []
    for word in given.replace(".", " ").split():
        parts.append("-".join(p[0].upper() + "." for p in word.split("-") if p))
    return "".join(parts)


def crossref_details(doi):
    m = fetch_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
    authors = []
    for a in m.get("author", []):
        if a.get("family"):
            ini = initials(a.get("given", ""))
            authors.append(f"{ini} {a['family']}".strip())
        elif a.get("name"):
            authors.append(a["name"])
    journal = (m.get("short-container-title") or m.get("container-title") or [""])[0]
    pages = m.get("page") or m.get("article-number") or ""
    year = None
    for key in ("published-print", "published-online", "issued"):
        dp = (m.get(key) or {}).get("date-parts") or [[None]]
        if dp[0] and dp[0][0]:
            year = dp[0][0]
            break
    title = re.sub(r"<[^>]+>", "", (m.get("title") or [""])[0]).strip()
    return {"authors": ", ".join(authors), "journal": journal, "volume": m.get("volume", ""),
            "pages": pages, "year": year, "title": title}


# ---------------------------------------------------------------- Google Scholar
def scholar_metrics(page):
    vals = re.findall(r'<td class="gsc_rsb_std">(\d+)</td>', page)
    if len(vals) < 6:
        raise ValueError("citation table not found (blocked or layout changed)")
    return {"citations": int(vals[0]), "h_index": int(vals[2]), "i10_index": int(vals[4])}


def openalex_metrics():
    a = fetch_json(f"https://api.openalex.org/authors/orcid:{ORCID}")
    s = a.get("summary_stats") or {}
    return {"citations": a.get("cited_by_count"), "h_index": s.get("h_index"), "i10_index": s.get("i10_index")}


# ---------------------------------------------------------------- main
def main():
    data = json.load(open(DATA, encoding="utf-8")) if os.path.exists(DATA) else {}
    before = json.dumps(data, sort_keys=True)
    today = datetime.date.today()

    # ORCID works -> new journal articles not yet curated in build.py
    try:
        works = orcid_journal_articles(fetch_json(f"https://pub.orcid.org/v3.0/{ORCID}/works"))
        known = curated_dois()
        cache = {w["doi"]: w for w in data.get("extra_works", [])}
        extra = []
        for w in works:
            if w["doi"] in known:
                continue
            if w["doi"] in cache:
                extra.append(cache[w["doi"]])
                continue
            entry = {"doi": w["doi"], "year": w["year"], "title": w["title"], "journal": w["journal"],
                     "authors": "", "volume": "", "pages": ""}
            try:
                cr = crossref_details(w["doi"])
                entry.update({k: v for k, v in cr.items() if v})
            except Exception as e:  # keep ORCID data only
                log("Crossref failed for", w["doi"], e)
            log("new article:", w["doi"])
            extra.append(entry)
        data["extra_works"] = sorted(extra, key=lambda e: (-(e.get("year") or 0), e["doi"]))
    except Exception as e:
        log("ORCID works failed, keeping previous list:", e)

    try:
        data["peer_reviews"] = orcid_peer_review_count(
            fetch_json(f"https://pub.orcid.org/v3.0/{ORCID}/peer-reviews"))
    except Exception as e:
        log("ORCID peer reviews failed, keeping previous value:", e)

    # Citation metrics
    metrics = data.get("metrics") or {}
    try:
        m = scholar_metrics(fetch(f"https://scholar.google.com/citations?user={SCHOLAR_USER}&hl=en"))
        metrics = {"source": "Google Scholar", **m}
        log("Google Scholar:", m)
    except Exception as e:
        log("Google Scholar unavailable:", e)
        if metrics.get("source") != "Google Scholar":
            try:
                metrics = {"source": "OpenAlex", **openalex_metrics()}
                log("OpenAlex:", metrics)
            except Exception as e2:
                log("OpenAlex failed:", e2)
    if metrics:
        data["metrics"] = metrics

    # Month of the latest check; only changes once a month, so unchanged data means no commit.
    data["checked"] = today.strftime("%Y-%m")

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    log("done; changed =", json.dumps(data, sort_keys=True) != before)


if __name__ == "__main__":
    main()
