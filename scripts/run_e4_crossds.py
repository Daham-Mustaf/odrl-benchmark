#!/usr/bin/env python3
"""
run_e4_crossds.py — E4 Cross-Dataspace False Positive Validation Runner
========================================================================
Usage:
    uv run python run_e4_crossds.py
    uv run python run_e4_crossds.py --z3
    uv run python run_e4_crossds.py --timeout 60
"""
import argparse, csv, subprocess, time
from datetime import datetime
from pathlib import Path

G="\033[32m"; R="\033[31m"; Y="\033[33m"; B="\033[36m"; X="\033[0m"
ok  = lambda s: f"{G}{s}{X}"
err = lambda s: f"{R}{s}{X}"
dim = lambda s: f"{Y}{s}{X}"

# ── Grounded Z3 encoder ───────────────────────────────────────────────────────
try:
    from e3_z3_fix import (
        transitive_closure, disjoint_closure,
        build_grounded_smt2_preamble,
        encode_conflict_conjecture, encode_compat_conjecture,
    )
    Z3_FIX_AVAILABLE = True
except ImportError:
    Z3_FIX_AVAILABLE = False

# ── GEO KB data (shared between cases) ───────────────────────────────────────

GEO_CONCEPTS = [
    "europe", "westernEurope", "easternEurope",
    "germany", "france", "italy", "belgium", "netherlands", "spain",
    "poland", "czechia", "bavaria",
]
GEO_LEQ_BASE = [
    ("westernEurope", "europe"), ("easternEurope", "europe"),
    ("germany", "westernEurope"), ("france", "westernEurope"),
    ("italy", "westernEurope"), ("belgium", "westernEurope"),
    ("netherlands", "westernEurope"), ("spain", "westernEurope"),
    ("poland", "easternEurope"), ("czechia", "easternEurope"),
    ("bavaria", "germany"),
]
GEO_DISJ_FULL = [
    ("westernEurope", "easternEurope"),
    ("germany",  "france"),   ("germany",  "italy"),
    ("germany",  "belgium"),  ("germany",  "netherlands"),
    ("germany",  "spain"),    ("france",   "italy"),
    ("france",   "belgium"),  ("france",   "netherlands"),
    ("france",   "spain"),    ("italy",    "belgium"),
    ("italy",    "netherlands"), ("italy", "spain"),
    ("belgium",  "netherlands"), ("belgium", "spain"),
    ("netherlands", "spain"), ("poland",  "czechia"),
    ("germany",  "poland"),   ("germany",  "czechia"),
    ("france",   "poland"),   ("france",   "czechia"),
    ("italy",    "poland"),   ("italy",    "czechia"),
    ("belgium",  "poland"),   ("belgium",  "czechia"),
    ("netherlands", "poland"), ("netherlands", "czechia"),
    ("spain",    "poland"),   ("spain",    "czechia"),
    ("bavaria",  "france"),   ("bavaria",  "poland"),
    ("bavaria",  "italy"),
]
GEO_DISJ_ROOT = [("westernEurope", "easternEurope")]

# ── Problem definitions ───────────────────────────────────────────────────────
# Each: (prob_id, prob_type, a, b, subtype, chain, expected, verdict_label, note)

CASE1_PROBS = [
    # 5 true conflicts (shared full KB)
    ("E4_C1_01", "conflict", "westernEurope",  "easternEurope",  "existential", None,
     "Theorem", "TRUE-CONFLICT", "D1 root pair wE⊥eE"),
    ("E4_C1_02", "conflict", "germany",        "france",         "existential", None,
     "Theorem", "TRUE-CONFLICT", "D1 sibling de⊥fr"),
    ("E4_C1_03", "conflict", "germany",        "poland",         "existential", None,
     "Theorem", "TRUE-CONFLICT", "D2 cross-region de→wE⊥eE←pl"),
    ("E4_C1_04", "conflict", "bavaria",        "czechia",        "existential", None,
     "Theorem", "TRUE-CONFLICT", "D3 chain bav→de→wE⊥eE←cz"),
    ("E4_C1_05", "conflict", "italy",          "easternEurope",  "existential", None,
     "Theorem", "TRUE-CONFLICT", "D2 it→wE⊥eE"),
    # 5 true compat (no false positive)
    ("E4_C1_06", "compat",   "germany",        "westernEurope",  "existential", None,
     "Theorem", "TRUE-COMPAT",   "subsumption de≤wE"),
    ("E4_C1_07", "compat",   "bavaria",        "europe",         "existential", None,
     "Theorem", "TRUE-COMPAT",   "chain bav≤de≤wE≤eu"),
    ("E4_C1_08", "compat",   "germany",        "westernEurope",  "universal",   None,
     "Theorem", "TRUE-COMPAT",   "universal subsumption ↓de⊆↓wE"),
    ("E4_C1_09", "compat",   "germany",        "europe",         "chain",
     ["germany", "westernEurope", "europe"],
     "Theorem", "TRUE-COMPAT",   "3-way chain de≤wE≤eu"),
    ("E4_C1_10", "compat",   "bavaria",        "westernEurope",  "universal",   None,
     "Theorem", "TRUE-COMPAT",   "universal bav≤de≤wE"),
]

CASE2_PROBS = [
    # 5 true conflicts — derivable from KB_B (root only) via transitive leq
    ("E4_C2_01", "conflict", "germany",        "poland",         "existential", None,
     "Theorem", "TRUE-CONFLICT", "de≤wE, pl≤eE, root wE⊥eE — KB_B sufficient"),
    ("E4_C2_02", "conflict", "westernEurope",  "easternEurope",  "existential", None,
     "Theorem", "TRUE-CONFLICT", "root pair — directly in KB_B"),
    ("E4_C2_03", "conflict", "france",         "czechia",        "existential", None,
     "Theorem", "TRUE-CONFLICT", "fr≤wE, cz≤eE, root wE⊥eE — KB_B sufficient"),
    ("E4_C2_04", "conflict", "bavaria",        "poland",         "existential", None,
     "Theorem", "TRUE-CONFLICT", "bav≤de≤wE, pl≤eE, root — KB_B sufficient"),
    ("E4_C2_05", "conflict", "italy",          "easternEurope",  "existential", None,
     "Theorem", "TRUE-CONFLICT", "it≤wE, root wE⊥eE — KB_B sufficient"),
    # 5 false positive risks — KB_A has it, KB_B cannot derive
    # System MUST return Unknown (sound abstention — no false positive)
    ("E4_C2_06", "conflict", "germany",        "france",         "existential", None,
     "Unknown", "FP-RISK→OK",  "de⊥fr: KB_A only; KB_B both≤wE, no sibling"),
    ("E4_C2_07", "conflict", "belgium",        "spain",          "existential", None,
     "Unknown", "FP-RISK→OK",  "be⊥es: KB_A only; KB_B both≤wE, no sibling"),
    ("E4_C2_08", "conflict", "poland",         "czechia",        "existential", None,
     "Unknown", "FP-RISK→OK",  "pl⊥cz: KB_A only; KB_B both≤eE, no sibling"),
    ("E4_C2_09", "conflict", "bavaria",        "france",         "existential", None,
     "Unknown", "FP-RISK→OK",  "bav⊥fr: KB_A only via bav≤de⊥fr; KB_B no de⊥fr"),
    ("E4_C2_10", "conflict", "netherlands",    "spain",          "existential", None,
     "Unknown", "FP-RISK→OK",  "nl⊥es: KB_A only; KB_B both≤wE, no sibling"),
]


# ── Prover helpers ────────────────────────────────────────────────────────────

def run_vampire(fp, inc_dir, timeout):
    try:
        t0 = time.time()
        r = subprocess.run(
            ["vampire", "--input_syntax", "tptp",
             "--include", str(inc_dir),
             "--time_limit", str(timeout), str(fp)],
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


def build_smt2(prob_id, prob_type, a, b, concepts, leq_base, disj_base,
               operator="isPartOf", subtype="existential", chain=None):
    """Build grounded SMT2 using e3_z3_fix primitives."""
    preamble, leq_tc, disj_tc = build_grounded_smt2_preamble(
        concepts, leq_base, disj_base, operator)

    if prob_type == "conflict":
        conj = encode_conflict_conjecture(a, b, concepts, leq_tc, disj_tc, prob_id)
    else:
        conj = encode_compat_conjecture(a, b, concepts, leq_tc, prob_id, subtype, chain)

    header = f"""\
; ─────────────────────────────────────────────────────────────────────────────
; E4 Cross-Dataspace  —  {prob_id}
; Grounded SMT2 (no forall axioms — E-matching safe)
; ─────────────────────────────────────────────────────────────────────────────
"""
    return header + preamble + "\n\n" + conj


def run_z3_smt2(smt2_content, timeout):
    """Write temp file and run Z3."""
    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".smt2", mode="w",
                                     delete=False) as f:
        f.write(smt2_content)
        tmp = f.name
    try:
        t0 = time.time()
        r = subprocess.run(["z3", f"-T:{timeout}", tmp],
                           capture_output=True, text=True, timeout=timeout + 10)
        elapsed = time.time() - t0
        out = (r.stdout + r.stderr).lower()
        if "unsat" in out:
            return "Theorem", elapsed
        if "sat" in out:
            return "Unknown", elapsed
        return "unknown", elapsed
    except FileNotFoundError:
        return "NoZ3", 0.0
    except subprocess.TimeoutExpired:
        return "Timeout", float(timeout)
    finally:
        os.unlink(tmp)


def is_pass(actual, expected):
    ok_map = {
        "Theorem":  {"Theorem"},
        "Unknown":  {"Unknown", "GaveUp", "Timeout"},
    }
    return actual in ok_map.get(expected, {expected})


def verdict_colour(v, expected):
    passed = is_pass(v, expected)
    label = f"{v:>10}"
    return ok(label) if passed else err(label)


# ── Main ──────────────────────────────────────────────────────────────────────

def run_case(case_name, probs, kb_disj, inc_dir, timeout, use_z3,
             case_description, fp_semantics):
    """Run one case. kb_disj = disjointness pairs for the proof KB."""
    print(f"\n{'='*72}")
    print(f"  {B}{case_name}{X}  —  {case_description}")
    print(f"{'='*72}")
    print(f"  {'Problem':<14} {'Label':<18} {'Expect':>9}  {'Vampire':>10}"
          + (f"  {'Z3':>10}" if use_z3 else "") + "  Note")
    print(f"  {'-'*70}")

    rows = []
    passed_total = 0
    fp_prevented = 0
    tp_found = 0

    for (prob_id, ptype, a, b, subtype, chain,
         expected, vlabel, note) in probs:

        # Vampire (uses TPTP file)
        fp = inc_dir / "CrossDS" / case_name / f"{prob_id}.p"
        if fp.exists():
            vstatus, vtime = run_vampire(fp, inc_dir, timeout)
        else:
            vstatus, vtime = "NoFile", 0.0

        # Z3 grounded
        zstatus = ""
        if use_z3 and Z3_FIX_AVAILABLE:
            smt2 = build_smt2(prob_id, ptype, a, b,
                              GEO_CONCEPTS, GEO_LEQ_BASE, kb_disj,
                              "isPartOf", subtype, chain)
            zstatus, _ = run_z3_smt2(smt2, timeout)

        z_ok = is_pass(zstatus, expected) if zstatus else False
        v_ok = is_pass(vstatus, expected) if vstatus != 'NoFile' else z_ok
        overall = v_ok if not (use_z3) else (v_ok and z_ok)
        passed_total += overall

        if vlabel == "TRUE-CONFLICT" and overall:
            tp_found += 1
        if "FP-RISK" in vlabel and overall:
            fp_prevented += 1

        vcol = verdict_colour(vstatus, expected)
        zcol = verdict_colour(zstatus, expected) if use_z3 else ""

        sym = ok("✓") if overall else err("✗")
        print(f"  {prob_id:<14} {vlabel:<18} {expected:>9}  {vcol}"
              + (f"  {zcol}" if use_z3 else "") + f"  {sym}  {note}")

        rows.append({
            "case": case_name, "prob_id": prob_id, "type": ptype,
            "a": a, "b": b, "expected": expected, "label": vlabel,
            "vampire": vstatus, "z3": zstatus, "pass": overall, "note": note,
            "fp_semantics": fp_semantics,
        })

    print(f"\n  Pass: {passed_total}/{len(probs)}")
    if fp_prevented:
        print(ok(f"  ✓ FALSE POSITIVES PREVENTED: {fp_prevented}/5 FP-risk pairs → Unknown (sound)"))
    if tp_found:
        print(ok(f"  ✓ TRUE POSITIVES DETECTED:   {tp_found}/5 genuine conflicts → Theorem"))

    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--z3",     action="store_true")
    ap.add_argument("--base-dir", default=".")
    ap.add_argument("--generate", action="store_true",
                    help="Generate TPTP files before running")
    args = ap.parse_args()

    base    = Path(args.base_dir).resolve()
    inc_dir = base / "Problems" / "ODRL"

    if args.generate:
        import subprocess as sp
        sp.run(["python3", str(base / "gen_e4_crossds.py"),
                "--outdir", str(base / "Problems/ODRL/CrossDS")], check=True)

    if not Z3_FIX_AVAILABLE and args.z3:
        print(err("Warning: e3_z3_fix.py not found — Z3 columns unavailable"))

    print(f"\n{B}E4 Cross-Dataspace False Positive Validation{X}"
          f"  timeout={args.timeout}s  z3={'yes' if args.z3 else 'no'}")

    all_rows = []

    # Case 1: shared hub KB (full GEO)
    rows1 = run_case(
        "Case1_SharedHub", CASE1_PROBS, GEO_DISJ_FULL, inc_dir, args.timeout, args.z3,
        "Shared Hub KB — both parties use full GEO (Gaia-X/IDSA model)",
        "shared_hub",
    )
    all_rows.extend(rows1)

    # Case 2: asymmetric KB — proof grounded against KB_B (root only)
    rows2 = run_case(
        "Case2_AsymmetricKB", CASE2_PROBS, GEO_DISJ_ROOT, inc_dir, args.timeout, args.z3,
        "Asymmetric KB — Consumer KB_B has root disjointness only",
        "asymmetric_consumer_grounded",
    )
    all_rows.extend(rows2)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*72}")
    print(f"  E4 SUMMARY — Cross-Dataspace False Positive Analysis")
    print(f"{'='*72}")

    c1_pass = sum(r["pass"] for r in rows1)
    c2_pass = sum(r["pass"] for r in rows2)
    fp_rows = [r for r in rows2 if "FP-RISK" in r["label"]]
    tp_rows = [r for r in rows2 if r["label"] == "TRUE-CONFLICT"]

    print(f"\n  Case 1 (Shared Hub KB):    {c1_pass}/{len(rows1)} pass")
    c1_compat = [r for r in rows1 if r["type"] == "compat"]
    if all(r["vampire"] == "Theorem" for r in c1_compat):
        print(ok(f"  ✓ No false positives on compatible pairs (all {len(c1_compat)} → Theorem)"))
    if all(r["vampire"] == "Theorem" for r in rows1 if r["label"] == "TRUE-CONFLICT"):
        print(ok(f"  ✓ All true conflicts detected (5/5 → Theorem)"))

    print(f"\n  Case 2 (Asymmetric KB):    {c2_pass}/{len(rows2)} pass")
    fp_ok = [r for r in fp_rows if r["pass"]]
    tp_ok = [r for r in tp_rows if r["pass"]]
    if len(fp_ok) == len(fp_rows):
        print(ok(f"  ✓ ALL false positive risks correctly abstained ({len(fp_ok)}/5 → Unknown)"))
        print(ok(f"    Provider's richer KB_A disjointness NOT imported into Consumer proof"))
    else:
        print(err(f"  ✗ {len(fp_rows)-len(fp_ok)} false positives detected!"))
    if len(tp_ok) == len(tp_rows):
        print(ok(f"  ✓ All cross-region true conflicts still detected ({len(tp_ok)}/5 → Theorem)"))

    overall = sum(r["pass"] for r in all_rows)
    print(f"\n  Total: {overall}/{len(all_rows)} pass  "
          + (ok("ALL CORRECT") if overall == len(all_rows) else err("FAILURES")))

    # ── CSV ───────────────────────────────────────────────────────────────────
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = base / "results" / "hierarchies" / f"e4_crossds_{ts}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "case", "prob_id", "type", "a", "b", "expected", "label",
            "vampire", "z3", "pass", "note", "fp_semantics"])
        w.writeheader()
        w.writerows(all_rows)
    print(f"\n  {ok('CSV →')} {out}")


if __name__ == "__main__":
    main()