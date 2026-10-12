"""Guess which applicant-tracking system a careers URL uses (Section 3, Step A)."""
import re

PATTERNS = [
    ("greenhouse", r"greenhouse\.io/(?:v1/boards/)?([\w-]+)"),
    ("lever", r"lever\.co/([\w-]+)"),
    ("ashby", r"ashbyhq\.com/([\w-]+)"),
    ("smartrecruiters", r"smartrecruiters\.com/([\w-]+)"),
    ("workday", r"([\w-]+)\.(wd\d+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([\w-]+)"),
    ("eightfold", r"([\w-]+)\.eightfold\.ai"),
]


def detect(url: str):
    """Return (ats_name, match_groups) or (None, None) when no API-backed ATS is recognised."""
    for name, pat in PATTERNS:
        m = re.search(pat, url or "")
        if m:
            return name, m.groups()
    return None, None


if __name__ == "__main__":
    import csv
    with open("companies.csv") as f:
        for row in csv.DictReader(f):
            ats, g = detect(row["Careers URL"])
            if ats:
                print(row["#"], row["Company"], ats, g)
