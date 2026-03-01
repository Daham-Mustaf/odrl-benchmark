#!/usr/bin/env python3
"""Full benchmark audit with category breakdown."""
import os
from pathlib import Path
from collections import defaultdict

G="\033[32m"; Y="\033[33m"; B="\033[36m"; R="\033[31m"; X="\033[0m"

repo = Path(".")
stats = defaultdict(lambda: {"p":0,"thm":0,"unk":0,"other":0})
total_p = total_thm = total_unk = total_other = 0

for root, dirs, files in os.walk(repo / "Problems"):
    dirs.sort()
    p_files = [f for f in sorted(files) if f.endswith(".p")]
    if not p_files:
        continue
    folder = str(Path(root).relative_to(repo))
    parts = folder.replace("Problems/ODRL/","").split("/")
    category = parts[0] if parts else folder

    t = u = o = 0
    for f in p_files:
        for line in open(Path(root)/f):
            if "% Expected" in line:
                v = line.split(":")[-1].strip()
                if   "Theorem" in v: t += 1
                elif "Unknown" in v: u += 1
                else:                o += 1
                break
    n = len(p_files)
    stats[category]["p"]     += n
    stats[category]["thm"]   += t
    stats[category]["unk"]   += u
    stats[category]["other"] += o
    total_p += n; total_thm += t; total_unk += u; total_other += o

print(f"\n{B}{'='*65}{X}")
print(f"{B}  FULL BENCHMARK AUDIT — {repo.resolve().name}{X}")
print(f"{B}{'='*65}{X}")
print(f"  {'Category':<35} {'Files':>6}  {'Thm':>5}  {'Unk':>5}  {'Other':>5}")
print(f"  {'-'*60}")
for cat, s in sorted(stats.items()):
    print(f"  {cat:<35} {s['p']:>6}  "
          f"{G}{s['thm']:>5}{X}  "
          f"{Y}{s['unk']:>5}{X}  "
          f"{R if s['other'] else X}{s['other']:>5}{X}")
print(f"  {'-'*60}")
print(f"  {'TOTAL':<35} {B}{total_p:>6}{X}  {G}{total_thm:>5}{X}  {Y}{total_unk:>5}{X}  {R}{total_other:>5}{X}")

print(f"\n{B}{'='*65}{X}")
print(f"  SUMMARY FOR PAPER")
print(f"{B}{'='*65}{X}")
print(f"  Total benchmark problems  : {B}{total_p}{X}")
print(f"  Expected Theorem (proved) : {G}{total_thm}{X}  ({100*total_thm//total_p}%)")
print(f"  Expected Unknown (sound)  : {Y}{total_unk}{X}  ({100*total_unk//total_p}%)")
print(f"  Other / needs review      : {R}{total_other}{X}  ({100*total_other//total_p}%)")

e3  = sum(s["p"] for k,s in stats.items() if "Incompleteness" in k)
e4  = sum(s["p"] for k,s in stats.items() if "CrossDS" in k)
ax  = sum(s["p"] for k,s in stats.items() if "Axis" in k)
oth = total_p - e3 - e4 - ax
print(f"\n  By experiment:")
print(f"    E3 Incompleteness Sweep : {G}{e3:>4}{X}  (3 KBs x 5 levels x 13 problems)")
print(f"    E4 Cross-Dataspace      : {G}{e4:>4}{X}  (2 architectures x 10 problems)")
print(f"    Axis Decomposition      : {G}{ax:>4}{X}  (multi-axis conflict taxonomy)")
print(f"    Other KB / grounding    : {G}{oth:>4}{X}  (spatial, DAG, alignment, ...)")
print(f"    {'─'*40}")
print(f"    GRAND TOTAL             : {B}{total_p:>4}{X}  problems")
print(f"{B}{'='*65}{X}\n")