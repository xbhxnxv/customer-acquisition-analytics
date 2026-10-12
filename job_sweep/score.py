"""Fit scoring per Section 5 of the brief (score out of 100)."""

FAMILY_POINTS = {"consulting": 35, "ba": 30, "data": 25, "other": 18}
SENIORITY_POINTS = {"grad": 25, "0-2": 18, "unclear": 10}
# Skills/areas from the candidate profile; each overlap is worth 5 points, capped at 25.
PROFILE_SKILLS = {"sql", "python", "powerbi", "tableau", "excel", "stakeholder",
                  "requirements", "esg", "fintech", "modelling", "analytics", "consulting"}
TOP_METROS = ("london", "bengaluru", "bangalore", "gurugram", "gurgaon", "delhi", "noida",
              "mumbai", "pune", "hyderabad", "chennai")
DOMAIN_BONUS = {"fs", "fintech", "esg", "consulting"}

ROLE_TYPE_LABEL = {"consulting": "Consulting", "ba": "Business Analyst", "data": "Data Analyst"}


def location_points(loc: str) -> int:
    l = (loc or "").lower()
    if any(m in l for m in TOP_METROS):
        return 10
    if "remote" in l:
        return 8
    return 6


def fit_score(role: dict) -> int:
    s = FAMILY_POINTS[role["family"]]
    s += SENIORITY_POINTS[role["seniority"]]
    skills = {x.lower() for x in role.get("skills", [])} & PROFILE_SKILLS
    s += min(25, 5 * len(skills))
    s += location_points(role.get("loc", ""))
    if role.get("domain") in DOMAIN_BONUS:
        s += 5
    return s


def role_type(role: dict) -> str:
    return role.get("type") or ROLE_TYPE_LABEL.get(role["family"], "Graduate Programme")
