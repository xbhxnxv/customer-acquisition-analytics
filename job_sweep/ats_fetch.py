"""One fetch function per ATS public JSON API (Section 3, Step A).

Untested against live endpoints: the session that wrote this had all outbound
careers-site traffic blocked by its network policy. Responses are cached under
cache/{company_slug}/ so a re-run does not refetch.
"""
import hashlib
import json
import re
import time
from pathlib import Path

import httpx

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
KEYWORDS = ["graduate", "analyst", "associate", "business analyst", "consultant", "data analyst",
            "early careers", "entry level"]
CACHE = Path(__file__).with_name("cache")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def cached(company, key, fn):
    d = CACHE / slug(company)
    d.mkdir(parents=True, exist_ok=True)
    p = d / (hashlib.sha1(key.encode()).hexdigest()[:16] + ".json")
    if p.exists():
        return json.loads(p.read_text())
    data = fn()
    p.write_text(json.dumps(data))
    time.sleep(2)  # politeness delay per Section 3
    return data


def _get(url, **kw):
    r = httpx.get(url, headers={"User-Agent": UA}, timeout=30, follow_redirects=True, **kw)
    r.raise_for_status()
    return r.json()


def greenhouse(company, token):
    data = cached(company, f"gh:{token}", lambda: _get(
        f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"))
    return [{"title": j["title"], "loc": j.get("location", {}).get("name", ""), "link": j["absolute_url"],
             "posted": j.get("updated_at", "")[:10], "desc": j.get("content", "")} for j in data["jobs"]]


def lever(company, org):
    data = cached(company, f"lever:{org}", lambda: _get(f"https://api.lever.co/v0/postings/{org}?mode=json"))
    return [{"title": j["text"], "loc": j.get("categories", {}).get("location", ""), "link": j["hostedUrl"],
             "posted": "", "desc": j.get("descriptionPlain", "")} for j in data]


def ashby(company, org):
    data = cached(company, f"ashby:{org}", lambda: _get(
        f"https://api.ashbyhq.com/posting-api/job-board/{org}?includeCompensation=true"))
    return [{"title": j["title"], "loc": j.get("location", ""), "link": j["jobUrl"],
             "posted": j.get("publishedAt", "")[:10], "desc": j.get("descriptionPlain", "")} for j in data["jobs"]]


def smartrecruiters(company, cid):
    out = []
    for kw in KEYWORDS:
        data = cached(company, f"sr:{cid}:{kw}", lambda: _get(
            f"https://api.smartrecruiters.com/v1/companies/{cid}/postings", params={"q": kw}))
        for j in data.get("content", []):
            out.append({"title": j["name"], "loc": j.get("location", {}).get("city", ""),
                        "link": f"https://jobs.smartrecruiters.com/{cid}/{j['id']}",
                        "posted": j.get("releasedDate", "")[:10], "desc": ""})
    return out


def workday(company, tenant, wd, site):
    base = f"https://{tenant}.{wd}.myworkdayjobs.com"
    out = {}
    for kw in KEYWORDS:
        def call():
            r = httpx.post(f"{base}/wday/cxs/{tenant}/{site}/jobs", headers={"User-Agent": UA},
                           json={"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": kw}, timeout=30)
            r.raise_for_status()
            return r.json()
        for j in cached(company, f"wd:{tenant}:{site}:{kw}", call).get("jobPostings", []):
            out[j["externalPath"]] = {"title": j["title"], "loc": j.get("locationsText", ""),
                                      "link": f"{base}/{site}{j['externalPath']}",
                                      "posted": j.get("postedOn", ""), "desc": ""}
    for path, job in out.items():  # detail call carries the description and any closing date
        detail = cached(company, f"wd-detail:{path}", lambda: _get(f"{base}/wday/cxs/{tenant}/{site}{path}"))
        info = detail.get("jobPostingInfo", {})
        job["desc"] = info.get("jobDescription", "")
        job["deadline"] = info.get("endDate", "")
    return list(out.values())


def eightfold(company, sub, domain, location="United Kingdom"):
    out = []
    for kw in KEYWORDS:
        data = cached(company, f"ef:{sub}:{kw}:{location}", lambda: _get(
            f"https://{sub}.eightfold.ai/api/apply/v2/jobs",
            params={"domain": domain, "query": kw, "location": location}))
        for j in data.get("positions", []):
            out.append({"title": j["name"], "loc": j.get("location", ""), "link": j.get("canonicalPositionUrl", ""),
                        "posted": "", "desc": j.get("job_description", "")})
    return out
