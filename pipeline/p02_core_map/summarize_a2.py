"""Tóm tắt output A2 (merge_stats, map_stats*, annot_stats) thành Markdown. stdlib only.
Dùng: python -B summarize_a2.py --dir data/a2 [--label chr1]
"""
import argparse, os, csv, sys
sys.stdout.reconfigure(encoding="utf-8")
ap=argparse.ArgumentParser(); ap.add_argument("--dir",required=True); ap.add_argument("--label",default="")
a=ap.parse_args(); D=a.dir
def kv(path):
    d={}
    if not os.path.exists(path): return d
    for row in csv.reader(open(path,encoding="utf-8"),delimiter="\t"):
        if len(row)>=2 and row[0]!="metric": d.setdefault(row[0],row[1:])
    return d
def section(path,header):
    rows=[]; on=False
    if not os.path.exists(path): return rows
    for row in csv.reader(open(path,encoding="utf-8"),delimiter="\t"):
        if row[:len(header)]==header: on=True; continue
        if on:
            if not row or len(row)<len(header): on=False; continue
            rows.append(row)
    return rows
m=kv(os.path.join(D,"merge_stats.tsv"))
print(f"## Tóm tắt A2 {a.label}\n")
if m: print(f"- Khoảng vào: {int(m['intervals_in'][0]):,} → phần tử: {int(m['elements_out'][0]):,}; bp vào {int(m['bp_in'][0]):,}, span ra {int(m['bp_out'][0]):,}")
for name,lab in (("map_stats.tsv","coverage ≥0,8"),("map_stats.cov50.tsv","coverage ≥0,5")):
    p=os.path.join(D,name); s=kv(p)
    if not s: continue
    bed=os.path.join(D,"bulbul_core.bed" if "cov50" not in name else "bulbul_core.cov50.bed"); bp=0
    if os.path.exists(bed):
        for l in open(bed,encoding="utf-8"):
            f=l.split("\t"); bp+=int(f[2])-int(f[1])
    print(f"\n### {lab}: {int(s['mapped'][0]):,} / {int(s['total_queries'][0]):,} phần tử ({s['mapped_pct'][0]} %), {bp:,} bp trên chào mào")
    rows=section(p,["qlen_bin","mapped","total","mapped_pct"])
    if rows:
        print("| nhóm bp | căn được | tổng | % |"); print("|---|---|---|---|")
        for r in rows: print(f"| {r[0]} | {int(r[1]):,} | {int(r[2]):,} | {r[3]} |")
an=os.path.join(D,"annot_stats.tsv")
rows=section(an,["feature_class","regions","bp"])
if rows:
    tot=sum(int(r[2]) for r in rows) or 1
    print("\n### Annotation (bộ coverage ≥0,8)\n| lớp | vùng | bp | % bp |\n|---|---|---|---|")
    for r in rows: print(f"| {r[0]} | {int(r[1]):,} | {int(r[2]):,} | {100*int(r[2])/tot:.1f} |")
    genes=section(an,["gene_id","gene_name","bp"])[:10]
    if genes:
        print("\nTop 10 gene theo bp lõi: " + ", ".join(f"{g[1]} ({int(g[2]):,})" for g in genes))
