"""Kiem tra file research/raw/R*.md: du 6 muc, moi dong bang phat hien co nhan bang chung.
Chay: python -B research/validate_raw.py  -> exit 0 = PASS, 1 = NEEDS_FIX
"""
import re, sys, glob, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REQUIRED = ["## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6."]
LABELS = ("CONFIRMED", "STRONG_INFERENCE", "UNVERIFIED")
fail = 0
for path in sorted(glob.glob("research/raw/R[0-9]*-*.md")):
    txt = open(path, encoding="utf-8").read()
    missing = [h for h in REQUIRED if h not in txt]
    # rows of section 2 table: lines starting with '|' between '## 2.' and '## 3.'
    m = re.search(r"## 2\..*?(?=## 3\.)", txt, re.S)
    rows = [l for l in (m.group(0).splitlines() if m else []) if l.startswith("|")][2:]
    unlabeled = [r for r in rows if not any(l in r for l in LABELS)]
    counts = {l: sum(l in r for r in rows) for l in LABELS}
    pplx = len(re.findall(r"pplx_smart_query", txt))
    status = "PASS" if not missing and not unlabeled and rows else "NEEDS_FIX"
    fail |= status != "PASS"
    print(f"{status} {path} | rows={len(rows)} {counts} | missing={missing} | unlabeled={len(unlabeled)} | pplx_mentions={pplx}")
for path in glob.glob("research/raw/R6*.md"):
    txt = open(path, encoding="utf-8").read()
    ok = len(txt) > 2000 and "Search log" in txt
    fail |= not ok
    print(f"{'PASS' if ok else 'NEEDS_FIX'} {path} | bytes={len(txt)} | search_log={'Search log' in txt} | urls={len(re.findall(r'https?://', txt))}")
sys.exit(1 if fail else 0)
