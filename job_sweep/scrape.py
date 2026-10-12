"""Playwright fallback for careers sites without a usable API (Section 3, Step B).

Usage: python scrape.py "<Company>" "<careers search URL containing {q}>"
Untested against live sites from the authoring session (network policy blocked egress).
Stops and reports when it sees a CAPTCHA or login wall; it never tries to bypass one.
"""
import json
import sys
import time

from playwright.sync_api import sync_playwright

from ats_fetch import KEYWORDS, UA, CACHE, slug

BLOCK_MARKERS = ("captcha", "are you a robot", "verify you are human", "sign in to continue")


def scrape(company, url_template):
    results, blocked = {}, None
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", headless=True)
        page = browser.new_page(user_agent=UA)
        for kw in KEYWORDS:
            page.goto(url_template.format(q=kw.replace(" ", "+")), wait_until="networkidle", timeout=45000)
            text = page.content().lower()
            if any(m in text for m in BLOCK_MARKERS):
                blocked = "Blocked — CAPTCHA/login, check manually"
                break
            for a in page.query_selector_all("a"):
                title = (a.inner_text() or "").strip()
                href = a.get_attribute("href") or ""
                if title and any(k in title.lower() for k in ("analyst", "graduate", "associate", "consultant")):
                    results[page.urljoin(href) if hasattr(page, "urljoin") else href] = title
            time.sleep(2)
        browser.close()
    d = CACHE / slug(company)
    d.mkdir(parents=True, exist_ok=True)
    (d / "playwright.json").write_text(json.dumps({"blocked": blocked, "links": results}, indent=1))
    return blocked, results


if __name__ == "__main__":
    blocked, res = scrape(sys.argv[1], sys.argv[2])
    print(blocked or f"{len(res)} candidate links")
    for href, t in res.items():
        print(t, "|", href)
