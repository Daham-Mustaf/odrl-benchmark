#!/usr/bin/env python3
"""
run_e3_sweep.py — Run E3 Incompleteness Sweep with Vampire + Z3
================================================================
Usage (from repo root):
    uv run python run_e3_sweep.py                     # Vampire only
    uv run python run_e3_sweep.py --z3                # Vampire + Z3 (grounded)
    uv run python run_e3_sweep.py --kb GEO            # one KB only
    uv run python run_e3_sweep.py --kb DPV --z3
    uv run python run_e3_sweep.py --timeout 60
"""
import argparse, csv, os, re, subprocess, time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

G="\033[32m"; R="\033[31m"; Y="\033[33m"; B="\033[36m"; X="\033[0m"
ok  = lambda s: f"{G}{s}{X}"
err = lambda s: f"{R}{s}{X}"
dim = lambda s: f"{Y}{s}{X}"

# ── Z3 grounded encoder ───────────────────────────────────────────────────────
try:
    from e3_z3_fix import (
        build_e3_smt2, run_z3_on_smt2,
        transitive_closure, disjoint_closure, get_kept_disjoints,
    )
    Z3_FIX_AVAILABLE = True
except ImportError:
    Z3_FIX_AVAILABLE = False

# ── KB registry ───────────────────────────────────────────────────────────────
# Each entry: (concepts, leq_base, disjoints_ordered, operator)
# disjoints_ordered: list of (name, a, b) — removal proceeds from END

GEO_CONCEPTS = [
    "europe", "westernEurope", "easternEurope", "germany", "france",
    "italy", "belgium", "netherlands", "spain", "poland", "czechia", "bavaria",
]
GEO_LEQ_BASE = [
    ("westernEurope", "europe"), ("easternEurope", "europe"),
    ("germany", "westernEurope"), ("france", "westernEurope"),
    ("italy", "westernEurope"), ("belgium", "westernEurope"),
    ("netherlands", "westernEurope"), ("spain", "westernEurope"),
    ("poland", "easternEurope"), ("czechia", "easternEurope"),
    ("bavaria", "germany"),
]
GEO_DISJOINTS_ORDERED = [
    ("geo_disj_wE_eE", "westernEurope", "easternEurope"),
    ("geo_disj_de_fr",  "germany",  "france"),
    ("geo_disj_de_it",  "germany",  "italy"),
    ("geo_disj_de_be",  "germany",  "belgium"),
    ("geo_disj_de_nl",  "germany",  "netherlands"),
    ("geo_disj_de_es",  "germany",  "spain"),
    ("geo_disj_fr_it",  "france",   "italy"),
    ("geo_disj_fr_be",  "france",   "belgium"),
    ("geo_disj_fr_nl",  "france",   "netherlands"),
    ("geo_disj_fr_es",  "france",   "spain"),
    ("geo_disj_it_be",  "italy",    "belgium"),
    ("geo_disj_it_nl",  "italy",    "netherlands"),
    ("geo_disj_it_es",  "italy",    "spain"),
    ("geo_disj_be_nl",  "belgium",  "netherlands"),
    ("geo_disj_be_es",  "belgium",  "spain"),
    ("geo_disj_nl_es",  "netherlands", "spain"),
    ("geo_disj_pl_cz",  "poland",   "czechia"),
    ("geo_disj_de_pl",  "germany",  "poland"),
    ("geo_disj_de_cz",  "germany",  "czechia"),
    ("geo_disj_fr_pl",  "france",   "poland"),
    ("geo_disj_fr_cz",  "france",   "czechia"),
    ("geo_disj_it_pl",  "italy",    "poland"),
    ("geo_disj_it_cz",  "italy",    "czechia"),
    ("geo_disj_be_pl",  "belgium",  "poland"),
    ("geo_disj_be_cz",  "belgium",  "czechia"),
    ("geo_disj_nl_pl",  "netherlands", "poland"),
    ("geo_disj_nl_cz",  "netherlands", "czechia"),
    ("geo_disj_es_pl",  "spain",    "poland"),
    ("geo_disj_es_cz",  "spain",    "czechia"),
    ("geo_disj_bav_fr", "bavaria",  "france"),
    ("geo_disj_bav_pl", "bavaria",  "poland"),
    ("geo_disj_bav_it", "bavaria",  "italy"),
]

DPV_CONCEPTS = [
    "purpose", "commercialPurpose", "researchAndDevelopment",
    "serviceProvision", "legalCompliance", "marketing",
    "commercialResearch", "academicResearch", "publicResearch", "productDevelopment",
]
DPV_LEQ_BASE = [
    ("commercialPurpose",       "purpose"),
    ("researchAndDevelopment",  "purpose"),
    ("serviceProvision",        "purpose"),
    ("legalCompliance",         "purpose"),
    ("marketing",               "purpose"),
    ("commercialResearch",      "commercialPurpose"),
    ("commercialResearch",      "researchAndDevelopment"),
    ("academicResearch",        "researchAndDevelopment"),
    ("publicResearch",          "researchAndDevelopment"),
    ("productDevelopment",      "commercialPurpose"),
]
DPV_DISJOINTS_ORDERED = [
    ("dpv_disj_cP_sP",   "commercialPurpose",      "serviceProvision"),
    ("dpv_disj_cP_leg",  "commercialPurpose",      "legalCompliance"),
    ("dpv_disj_cP_mkt",  "commercialPurpose",      "marketing"),
    ("dpv_disj_RD_sP",   "researchAndDevelopment", "serviceProvision"),
    ("dpv_disj_RD_leg",  "researchAndDevelopment", "legalCompliance"),
    ("dpv_disj_RD_mkt",  "researchAndDevelopment", "marketing"),
    ("dpv_disj_sP_leg",  "serviceProvision",       "legalCompliance"),
    ("dpv_disj_sP_mkt",  "serviceProvision",       "marketing"),
    ("dpv_disj_leg_mkt", "legalCompliance",        "marketing"),
    ("dpv_disj_cR_sP",   "commercialResearch",     "serviceProvision"),
    ("dpv_disj_cR_leg",  "commercialResearch",     "legalCompliance"),
    ("dpv_disj_cR_mkt",  "commercialResearch",     "marketing"),
    ("dpv_disj_acR_sP",  "academicResearch",       "serviceProvision"),
    ("dpv_disj_acR_cP",  "academicResearch",       "commercialPurpose"),
    ("dpv_disj_acR_leg", "academicResearch",       "legalCompliance"),
    ("dpv_disj_acR_mkt", "academicResearch",       "marketing"),
    ("dpv_disj_pubR_cP", "publicResearch",         "commercialPurpose"),
    ("dpv_disj_pubR_sP", "publicResearch",         "serviceProvision"),
    ("dpv_disj_pubR_leg","publicResearch",         "legalCompliance"),
    ("dpv_disj_prod_RD", "productDevelopment",     "researchAndDevelopment"),
    ("dpv_disj_prod_sP", "productDevelopment",     "serviceProvision"),
    ("dpv_disj_prod_leg","productDevelopment",     "legalCompliance"),
]

LANG_CONCEPTS = [
    "allLanguages", "en", "deLang", "frLang", "nlLang", "esLang",
    "enGB", "enUS", "enAU", "deAT", "deCH", "frCH", "frBE",
]
LANG_LEQ_BASE = [
    ("en",     "allLanguages"), ("deLang", "allLanguages"),
    ("frLang", "allLanguages"), ("nlLang", "allLanguages"),
    ("esLang", "allLanguages"),
    ("enGB", "en"), ("enUS", "en"), ("enAU", "en"),
    ("deAT", "deLang"), ("deCH", "deLang"),
    ("frCH", "frLang"), ("frBE", "frLang"),
]
LANG_DISJOINTS_ORDERED = [
    ("lang_disj_en_de",    "en",    "deLang"),
    ("lang_disj_en_fr",    "en",    "frLang"),
    ("lang_disj_en_nl",    "en",    "nlLang"),
    ("lang_disj_en_es",    "en",    "esLang"),
    ("lang_disj_de_fr",    "deLang","frLang"),
    ("lang_disj_de_nl",    "deLang","nlLang"),
    ("lang_disj_de_es",    "deLang","esLang"),
    ("lang_disj_fr_nl",    "frLang","nlLang"),
    ("lang_disj_fr_es",    "frLang","esLang"),
    ("lang_disj_nl_es",    "nlLang","esLang"),
    ("lang_disj_enGB_enUS","enGB",  "enUS"),
    ("lang_disj_enGB_enAU","enGB",  "enAU"),
    ("lang_disj_enUS_enAU","enUS",  "enAU"),
    ("lang_disj_deAT_deCH","deAT",  "deCH"),
    ("lang_disj_frCH_frBE","frCH",  "frBE"),
    ("lang_disj_enGB_de",  "enGB",  "deLang"),
    ("lang_disj_enUS_de",  "enUS",  "deLang"),
    ("lang_disj_enGB_fr",  "enGB",  "frLang"),
    ("lang_disj_enUS_fr",  "enUS",  "frLang"),
    ("lang_disj_deAT_en",  "deAT",  "en"),
    ("lang_disj_deCH_en",  "deCH",  "en"),
    ("lang_disj_frCH_en",  "frCH",  "en"),
    ("lang_disj_frBE_en",  "frBE",  "en"),
    ("lang_disj_frCH_de",  "frCH",  "deLang"),
    ("lang_disj_frBE_de",  "frBE",  "deLang"),
]

# KB registry: kb_name -> (concepts, leq_base, disjoints_ordered, operator)
KB_REGISTRY = {
    "GEO":  (GEO_CONCEPTS,  GEO_LEQ_BASE,  GEO_DISJOINTS_ORDERED,  "isPartOf"),
    "DPV":  (DPV_CONCEPTS,  DPV_LEQ_BASE,  DPV_DISJOINTS_ORDERED,  "isA"),
    "LANG": (LANG_CONCEPTS, LANG_LEQ_BASE, LANG_DISJOINTS_ORDERED, "isPartOf"),
}

# Problem parameter lookup: prob_id -> (prob_type, a, b, subtype, chain)
PROB_PARAMS = {
    # GEO
    "GEO_C01": ("conflict", "westernEurope",  "easternEurope",         "existential", None),
    "GEO_C02": ("conflict", "germany",        "france",                "existential", None),
    "GEO_C03": ("conflict", "germany",        "poland",                "existential", None),
    "GEO_C04": ("conflict", "bavaria",        "poland",                "existential", None),
    "GEO_C05": ("conflict", "france",         "czechia",               "existential", None),
    "GEO_C06": ("conflict", "italy",          "easternEurope",         "existential", None),
    "GEO_C07": ("conflict", "spain",          "czechia",               "existential", None),
    "GEO_C08": ("conflict", "belgium",        "poland",                "existential", None),
    "GEO_M01": ("compat",   "germany",        "westernEurope",         "existential", None),
    "GEO_M02": ("compat",   "bavaria",        "europe",                "existential", None),
    "GEO_M03": ("compat",   "germany",        "westernEurope",         "existential", None),
    "GEO_M04": ("compat",   "germany",        "westernEurope",         "universal",   None),
    "GEO_M05": ("compat",   "germany",        "europe",                "chain",
                ["germany", "westernEurope", "europe"]),
    # DPV
    "DPV_C01": ("conflict", "commercialPurpose",      "serviceProvision",       "existential", None),
    "DPV_C02": ("conflict", "researchAndDevelopment", "serviceProvision",       "existential", None),
    "DPV_C03": ("conflict", "academicResearch",       "serviceProvision",       "existential", None),
    "DPV_C04": ("conflict", "commercialResearch",     "serviceProvision",       "existential", None),
    "DPV_C05": ("conflict", "legalCompliance",        "marketing",              "existential", None),
    "DPV_C06": ("conflict", "productDevelopment",     "researchAndDevelopment", "existential", None),
    "DPV_C07": ("conflict", "publicResearch",         "commercialPurpose",      "existential", None),
    "DPV_C08": ("conflict", "academicResearch",       "legalCompliance",        "existential", None),
    "DPV_M01": ("compat",   "commercialPurpose",      "researchAndDevelopment", "existential", None),
    "DPV_M02": ("compat",   "commercialResearch",     "researchAndDevelopment", "existential", None),
    "DPV_M03": ("compat",   "commercialResearch",     "commercialPurpose",      "existential", None),
    "DPV_M04": ("compat",   "academicResearch",       "researchAndDevelopment", "universal",   None),
    "DPV_M05": ("compat",   "academicResearch",       "researchAndDevelopment", "existential", None),
    # LANG
    "LANG_C01": ("conflict", "en",    "deLang", "existential", None),
    "LANG_C02": ("conflict", "enGB",  "enUS",   "existential", None),
    "LANG_C03": ("conflict", "enGB",  "frLang", "existential", None),
    "LANG_C04": ("conflict", "deAT",  "frLang", "existential", None),
    "LANG_C05": ("conflict", "frCH",  "en",     "existential", None),
    "LANG_C06": ("conflict", "enUS",  "deLang", "existential", None),
    "LANG_C07": ("conflict", "deLang","frLang", "existential", None),
    "LANG_C08": ("conflict", "frBE",  "deLang", "existential", None),
    "LANG_M01": ("compat",   "enGB",  "en",           "existential", None),
    "LANG_M02": ("compat",   "deAT",  "deLang",        "existential", None),
    "LANG_M03": ("compat",   "frCH",  "frLang",        "existential", None),
    "LANG_M04": ("compat",   "enGB",  "en",            "universal",   None),
    "LANG_M05": ("compat",   "enGB",  "allLanguages",  "chain",
                 ["enGB", "en", "allLanguages"]),
}

LEVEL_TO_PCT = {"full": 0, "pct25": 25, "pct50": 50, "pct75": 75, "empty": 100}

# ── Prover helpers ────────────────────────────────────────────────────────────

def run_vampire(path, inc_dir, timeout):
    try:
        t0 = time.time()
        r = subprocess.run(
            ["vampire", "--input_syntax", "tptp",
             "--include", str(inc_dir),
             "--time_limit", str(timeout), str(path)],
            capture_output=True, text=True, timeout=timeout + 10)
        elapsed = time.time() - t0
        for line in r.stdout.splitlines():
            if "SZS status" in line:
                return line.split("SZS status")[1].strip().split()[0], elapsed
        return "Unknown", elapsed
    except FileNotFoundError:
        return "NoVampire", 0.0
    except subprocess.TimeoutExpired:
        return "Timeout", float(timeout)


def run_z3_grounded(prob_id, kb_name, level, timeout):
    """Run Z3 using the grounded SMT2 encoder (avoids E-matching unknown)."""
    if not Z3_FIX_AVAILABLE:
        return "NoFix", 0.0

    params = PROB_PARAMS.get(prob_id)
    if params is None:
        return "NoParams", 0.0

    kb_data = KB_REGISTRY.get(kb_name)
    if kb_data is None:
        return "NoKB", 0.0

    prob_type, a, b, subtype, chain = params
    concepts, leq_base, disjoints_ordered, operator = kb_data
    pct = LEVEL_TO_PCT[level]

    disj_kept = get_kept_disjoints(disjoints_ordered, pct)

    smt2 = build_e3_smt2(
        prob_id=prob_id,
        prob_type=prob_type,
        a=a, b=b,
        concepts=concepts,
        leq_base=leq_base,
        disj_base=disj_kept,
        kb_name=kb_name,
        pct=pct,
        operator=operator,
        conjecture_subtype=subtype,
        chain=chain,
    )
    result, elapsed = run_z3_on_smt2(smt2, timeout=timeout)
    # Normalise to Vampire-style labels for display
    if result == "unsat":
        return "Theorem", elapsed
    if result == "sat":
        return "Unknown", elapsed
    return result, elapsed


def is_pass(actual, expected):
    ok_map = {
        "Theorem":            {"Theorem"},
        "Unknown":            {"Unknown", "GaveUp", "Timeout"},
        "Unknown_or_Theorem": {"Unknown", "Theorem", "GaveUp", "Timeout"},
        "Unsatisfiable":      {"Unsatisfiable", "CounterSatisfiable"},
    }
    return actual in ok_map.get(expected, {expected})


def cell_colour(v):
    if v == "Theorem":
        return ok(f"{v:>9}")
    if v in ("Unknown", "GaveUp", "Timeout", "unknown", "timeout"):
        return dim(f"{v:>9}")
    return err(f"{v:>9}")


def read_expected(fp):
    with open(fp) as f:
        for line in f:
            if "% Expected" in line:
                return line.split(":")[-1].strip()
    return "Unknown"


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb",      default=None, choices=["GEO", "DPV", "LANG"])
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--z3",      action="store_true")
    ap.add_argument("--base-dir", default=".")
    args = ap.parse_args()

    if args.z3 and not Z3_FIX_AVAILABLE:
        print(err("Warning: e3_z3_fix.py not found — Z3 rows will show 'NoFix'"))

    base    = Path(args.base_dir).resolve()
    e3_dir  = base / "Problems" / "ODRL" / "KBGrounding" / "IncompletenessWeep"
    inc_dir = base / "Problems" / "ODRL"

    if not e3_dir.exists():
        print(err(f"Not found: {e3_dir}"))
        print("Run: python3 gen_e3_sweep.py --outdir Problems/ODRL/KBGrounding/IncompletenessWeep")
        return

    KBS    = [args.kb] if args.kb else ["GEO", "DPV", "LANG"]
    LEVELS = ["full", "pct25", "pct50", "pct75", "empty"]
    PCT    = {"full": "0%", "pct25": "25%", "pct50": "50%", "pct75": "75%", "empty": "100%"}

    print(f"\n{B}E3 Incompleteness Sweep{X}  timeout={args.timeout}s  z3={'yes' if args.z3 else 'no'}")
    all_rows = []
    total = total_pass = 0

    for kb in KBS:
        kb_dir = e3_dir / kb
        if not kb_dir.exists():
            print(err(f"  missing: {kb_dir}")); continue

        problems = sorted(set(
            re.sub(r"_(full|pct25|pct50|pct75|empty)$", "", f.stem)
            for f in (kb_dir / "full").glob("*.p")))

        print(f"\n{'='*72}")
        print(f"  {B}{kb}{X}  ({len(problems)} problems × 5 levels = {len(problems)*5} runs)")
        print(f"{'='*72}")
        print(f"  {'Problem':<16}  {'0%':>10}  {'25%':>10}  {'50%':>10}  {'75%':>10}  {'100%':>10}  Type")
        print(f"  {'-'*70}")

        kb_pass = kb_total = 0

        for prob in problems:
            ptype  = "CONFLICT" if "_C" in prob else "COMPAT  "
            vcells = []
            zcells = []
            row_data = []

            for level in LEVELS:
                fp = kb_dir / level / f"{prob}_{level}.p"
                if not fp.exists():
                    vcells.append(dim("  missing "))
                    zcells.append(dim("  missing "))
                    continue

                expected = read_expected(fp)

                # Vampire
                vstatus, vtime = run_vampire(fp, inc_dir, args.timeout)
                passed = is_pass(vstatus, expected)
                vsym   = ok(f"{vstatus:>9}") if passed else err(f"{vstatus:>9}")
                vcells.append(vsym)
                kb_pass += passed; kb_total += 1
                total_pass += passed; total += 1

                # Z3 (grounded)
                zstatus = ""
                if args.z3:
                    zstatus, _ = run_z3_grounded(prob, kb, level, args.timeout)
                    zcells.append(cell_colour(zstatus))

                row_data.append({
                    "kb": kb, "problem": prob, "level": level, "pct": PCT[level],
                    "type": ptype.strip(), "expected": expected,
                    "vampire": vstatus, "vampire_t": f"{vtime:.2f}",
                    "z3": zstatus, "pass": passed,
                })

            print(f"  {prob:<16}  " + "  ".join(f"{c:>10}" for c in vcells) + f"  {ptype}")
            if args.z3 and zcells:
                print(f"  {'[Z3]':<16}  " + "  ".join(f"{c:>10}" for c in zcells))

            all_rows.extend(row_data)

        sym = ok("✓") if kb_pass == kb_total else err("✗")
        print(f"\n  {sym}  {kb}: {kb_pass}/{kb_total} passed")

    # ── Summary table ─────────────────────────────────────────────────────────
    print(f"\n{'='*72}")
    print(f"  DEGRADATION TABLE (Vampire verdicts by level)")
    print(f"{'='*72}")
    print(f"  {'Problem':<18}  {'0%':>9}  {'25%':>9}  {'50%':>9}  {'75%':>9}  {'100%':>9}  Type")
    print(f"  {'-'*70}")
    grid = defaultdict(dict)
    ptype_map = {}
    for row in all_rows:
        grid[row["problem"]][row["pct"]] = row["vampire"]
        ptype_map[row["problem"]] = row["type"]
    for prob in sorted(grid.keys()):
        cells = [grid[prob].get(p, "?") for p in ["0%", "25%", "50%", "75%", "100%"]]
        ptype = ptype_map.get(prob, "")
        print(f"  {prob:<18}  " + "  ".join(cell_colour(c) for c in cells) + f"  {ptype}")

    # ── Soundness check ───────────────────────────────────────────────────────
    print(f"\n{'='*72}")
    false_c = [r for r in all_rows
               if r["type"] == "COMPAT"
               and r["vampire"] not in ("Theorem", "Unknown", "GaveUp", "Timeout", "NoVampire", "")]
    if false_c:
        print(err(f"  ⚠ SOUNDNESS VIOLATION: {len(false_c)} Compatible → Conflict!"))
        for r in false_c:
            print(f"    {r['kb']}/{r['problem']}/{r['level']}: got {r['vampire']}")
    else:
        print(ok("  ✓ SOUNDNESS OK") + " — no Compatible ever became Conflict")

    compat_rows = [r for r in all_rows if r["type"] == "COMPAT" and r["vampire"] != "NoVampire"]
    compat_ok   = all(r["vampire"] == "Theorem" for r in compat_rows)
    if compat_ok:
        print(ok("  ✓ STABILITY OK") + " — all Compatible → Theorem at ALL 5 levels")
    else:
        unstable = [r for r in compat_rows if r["vampire"] != "Theorem"]
        print(err(f"  ⚠ STABILITY: {len(unstable)} Compatible gave non-Theorem"))

    c = G if total_pass == total else R
    print(f"\n  Total: {total}   {ok('Pass')}: {c}{total_pass}{X}   {err('Fail')}: {total - total_pass}")

    # ── CSV ───────────────────────────────────────────────────────────────────
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag = f"_{args.kb}" if args.kb else "_all"
    out = base / "results" / "hierarchies" / f"e3{tag}_{ts}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "kb", "problem", "level", "pct", "type", "expected",
            "vampire", "vampire_t", "z3", "pass"])
        w.writeheader(); w.writerows(all_rows)
    print(f"\n  {ok('CSV →')} {out}")


if __name__ == "__main__":
    main()