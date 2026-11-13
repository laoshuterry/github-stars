#!/usr/bin/env python3
"""Fetch all stars of a user, merge with data/curation.json, write docs/stars.json (+ data/uncurated.json).

Env: GITHUB_TOKEN (optional, raises rate limit), STARS_USER (default laoshuterry).
Curated content (category / summary_zh / tags) lives in data/curation.json; taxonomy in data/categories.json.
"""
import json, os, sys, time, re, datetime, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER = os.environ.get("STARS_USER", "laoshuterry")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
UNCAT = {"id": "uncategorized", "name_zh": "待整理", "description_zh": "新 Star 的仓库，尚未分类和撰写中文简介"}


def get(url):
    h = {"Accept": "application/vnd.github.star+json", "User-Agent": "github-stars-builder",
         "X-GitHub-Api-Version": "2022-11-28"}
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60) as r:
                return json.load(r), r.headers.get("Link", "")
        except (urllib.error.URLError, TimeoutError) as e:
            code = getattr(e, "code", None)
            if code in (401, 404):
                raise
            wait = 5 * (attempt + 1)
            if code in (403, 429):
                wait = 60
            print(f"retry {attempt + 1} after error {e}; sleep {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"failed: {url}")


def fetch_all():
    url = f"https://api.github.com/users/{USER}/starred?per_page=100"
    out = []
    while url:
        data, link = get(url)
        out.extend(data)
        m = re.search(r'<([^>]+)>;\s*rel="next"', link or "")
        url = m.group(1) if m else None
    return out


def main():
    stars = fetch_all()
    if not stars:
        sys.exit("no stars fetched; refusing to overwrite")
    cats = json.load(open(f"{ROOT}/data/categories.json", encoding="utf-8"))
    cur = json.load(open(f"{ROOT}/data/curation.json", encoding="utf-8"))
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(days=365)
    ids = {c["id"] for c in cats}
    repos, uncurated = [], []
    for s in stars:
        r = s["repo"]
        c = cur.get(r["full_name"])
        if c is None:
            # tolerate renamed repos: match by case-insensitive name
            c = next((v for k, v in cur.items() if k.lower() == r["full_name"].lower()), None)
        if c is None or c.get("category") not in ids:
            uncurated.append({"full_name": r["full_name"], "html_url": r["html_url"],
                              "description": r.get("description") or "", "topics": r.get("topics", []),
                              "language": r.get("language"), "starred_at": s["starred_at"]})
        pushed = r.get("pushed_at")
        pdt = datetime.datetime.fromisoformat(pushed.replace("Z", "+00:00")) if pushed else None
        repos.append({
            "full_name": r["full_name"], "name": r["name"], "owner": r["owner"]["login"],
            "html_url": r["html_url"], "description": r.get("description") or "",
            "summary_zh": (c or {}).get("summary_zh", "") if c and c.get("category") in ids else "",
            "category": c["category"] if c and c.get("category") in ids else UNCAT["id"],
            "tags": (c or {}).get("tags", []) if c and c.get("category") in ids else [],
            "language": r.get("language"), "stargazers_count": r["stargazers_count"],
            "forks_count": r["forks_count"], "topics": r.get("topics", []),
            "homepage": r.get("homepage") or "", "license": (r.get("license") or {}).get("spdx_id"),
            "archived": r["archived"], "stale": bool(pdt and pdt < cutoff), "fork": r["fork"],
            "pushed_at": pushed, "created_at": r.get("created_at"), "updated_at": r.get("updated_at"),
            "starred_at": s["starred_at"], "owner_avatar_url": r["owner"]["avatar_url"],
        })
    all_cats = cats + ([UNCAT] if uncurated else [])
    categories = [dict(c, count=sum(1 for x in repos if x["category"] == c["id"])) for c in all_cats]
    content = {"user": USER, "total": len(repos),
               "stats": {"archived": sum(x["archived"] for x in repos), "stale": sum(x["stale"] for x in repos),
                         "uncurated": len(uncurated), "stale_cutoff": cutoff.date().isoformat()},
               "categories": categories, "repos": repos}
    path = f"{ROOT}/docs/stars.json"
    # only bump generated_at when content actually changed (avoids daily no-op commits)
    try:
        old = json.load(open(path, encoding="utf-8"))
        old_gen = old.pop("generated_at", None)
    except Exception:
        old, old_gen = None, None
    gen = old_gen if old == content and old_gen else now.isoformat(timespec="seconds")
    json.dump({"generated_at": gen, **content}, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(uncurated, open(f"{ROOT}/data/uncurated.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"total={len(repos)} uncurated={len(uncurated)} archived={content['stats']['archived']} "
          f"stale={content['stats']['stale']} changed={gen != old_gen}")


if __name__ == "__main__":
    main()
