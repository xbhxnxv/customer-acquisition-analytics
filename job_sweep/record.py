"""Append one or more company results (JSON objects, one per line on stdin) to progress.jsonl.

Each record: {"n", "company", "region", "status", "method", "careers_url", "notes",
              "roles": [...], "opening": [...], "closed": [...]}
Re-recording a company number replaces the earlier entry (last write wins in build_workbook).
"""
import json
import sys
from pathlib import Path

REQUIRED = {"n", "company", "region", "status", "method", "careers_url"}
ROLE_REQUIRED = {"title", "family", "seniority", "loc", "link", "deadline", "dl_text", "dl_source"}

out = Path(__file__).with_name("progress.jsonl")
count = 0
with out.open("a") as f:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        missing = REQUIRED - rec.keys()
        assert not missing, f"{rec.get('company')}: missing {missing}"
        for r in rec.get("roles", []):
            m = ROLE_REQUIRED - r.keys()
            assert not m, f"{rec['company']} / {r.get('title')}: missing {m}"
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        count += 1
        print(f"[{rec['n']}/259] {rec['company']} ({rec['region']}) — {len(rec.get('roles', []))} roles — {rec['method']}")
print(f"recorded {count}")
