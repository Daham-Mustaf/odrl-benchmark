#!/usr/bin/env python3
"""
gen_e4_crossds.py — E4 Cross-Dataspace False Positive Validation
=================================================================
Tests two architectures:

CASE 1 — Shared Hub KB (Gaia-X/IDSA model)
  Both parties use the SAME shared federated KB.
  Tests: no false positives on truly compatible policy pairs.
  10 problems: 5 true conflicts + 5 true compat.

CASE 2 — Asymmetric KB (per-participant, cross-dataspace)
  Provider KB_A: full GEO (all disjointness)
  Consumer KB_B: minimal GEO (only root: westernEurope ⊥ easternEurope)

  TRUE CONFLICT  (both KBs derive it):
    germany  vs poland   → de≤wE, pl≤eE, wE⊥eE   ✓ in KB_A and KB_B
    bavaria  vs poland   → bav≤de≤wE, pl≤eE, wE⊥eE ✓ in both
    ...

  FALSE POSITIVE RISK (KB_A has it, KB_B does NOT):
    germany  vs france   → direct sibling pair in KB_A only
                           KB_B: de≤wE, fr≤wE — NO sibling disjointness
    belgium  vs spain    → KB_A sibling, KB_B cannot derive
    ...

  Our system, grounded against KB_B, correctly returns Unknown
  rather than importing KB_A's richer disjointness. No false positive.

Usage:
    python3 gen_e4_crossds.py [--outdir Problems/ODRL/CrossDS]
"""
import argparse, os
from datetime import date
from pathlib import Path

ODRL_INCLUDE = "include('Axioms/Layer1-ODRLCore/ODRL000-0.ax')."

# ── GEO KB data ───────────────────────────────────────────────────────────────

GEO_CONCEPTS = [
    "europe", "westernEurope", "easternEurope",
    "germany", "france", "italy", "belgium", "netherlands", "spain",
    "poland", "czechia", "bavaria",
]

GEO_HIERARCHY = """\
fof(geo_c_eu,  axiom, concept(europe)).
fof(geo_c_wE,  axiom, concept(westernEurope)).
fof(geo_c_eE,  axiom, concept(easternEurope)).
fof(geo_c_de,  axiom, concept(germany)).
fof(geo_c_fr,  axiom, concept(france)).
fof(geo_c_it,  axiom, concept(italy)).
fof(geo_c_be,  axiom, concept(belgium)).
fof(geo_c_nl,  axiom, concept(netherlands)).
fof(geo_c_es,  axiom, concept(spain)).
fof(geo_c_pl,  axiom, concept(poland)).
fof(geo_c_cz,  axiom, concept(czechia)).
fof(geo_c_bav, axiom, concept(bavaria)).
fof(geo_leq_wE_eu,  axiom, leq(westernEurope, europe)).
fof(geo_leq_eE_eu,  axiom, leq(easternEurope, europe)).
fof(geo_leq_de_wE,  axiom, leq(germany, westernEurope)).
fof(geo_leq_fr_wE,  axiom, leq(france, westernEurope)).
fof(geo_leq_it_wE,  axiom, leq(italy, westernEurope)).
fof(geo_leq_be_wE,  axiom, leq(belgium, westernEurope)).
fof(geo_leq_nl_wE,  axiom, leq(netherlands, westernEurope)).
fof(geo_leq_es_wE,  axiom, leq(spain, westernEurope)).
fof(geo_leq_pl_eE,  axiom, leq(poland, easternEurope)).
fof(geo_leq_cz_eE,  axiom, leq(czechia, easternEurope)).
fof(geo_leq_bav_de, axiom, leq(bavaria, germany)).
fof(geo_refl_eu,  axiom, leq(europe, europe)).
fof(geo_refl_wE,  axiom, leq(westernEurope, westernEurope)).
fof(geo_refl_eE,  axiom, leq(easternEurope, easternEurope)).
fof(geo_refl_de,  axiom, leq(germany, germany)).
fof(geo_refl_fr,  axiom, leq(france, france)).
fof(geo_refl_it,  axiom, leq(italy, italy)).
fof(geo_refl_be,  axiom, leq(belgium, belgium)).
fof(geo_refl_nl,  axiom, leq(netherlands, netherlands)).
fof(geo_refl_es,  axiom, leq(spain, spain)).
fof(geo_refl_pl,  axiom, leq(poland, poland)).
fof(geo_refl_cz,  axiom, leq(czechia, czechia)).
fof(geo_refl_bav, axiom, leq(bavaria, bavaria)).
fof(geo_trans, axiom, ![X,Y,Z]: (leq(X,Y) & leq(Y,Z) => leq(X,Z))).
fof(geo_una, axiom, $distinct(europe, westernEurope, easternEurope,
    germany, france, italy, belgium, netherlands, spain,
    poland, czechia, bavaria))."""

# Full disjointness (KB_A)
GEO_DISJ_FULL = [
    ("geo_disj_wE_eE", "westernEurope", "easternEurope"),  # ROOT
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

# Minimal disjointness (KB_B) — only root pair
GEO_DISJ_ROOT_ONLY = [
    ("geo_disj_wE_eE", "westernEurope", "easternEurope"),
]

def disj_block(pairs):
    lines = []
    for name, a, b in pairs:
        lines.append(f"fof({name}, axiom, disjoint({a},{b})).")
        lines.append(f"fof({name}_sym, axiom, disjoint({b},{a})).")
    return "\n".join(lines)

def write_tptp(path, prob_id, kb_block, conjecture, expected, case_desc, operator="isPartOf"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    content = f"""\
%--------------------------------------------------------------------------
% File     : {os.path.basename(path)} : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection — E4 Cross-Dataspace
% Problem  : {prob_id}
% Expected : {expected}
% Operator : {operator}
% Case     : {case_desc}
% Date     : {date.today().isoformat()}
% Purpose  : E4 — Validate no false positives across dataspace boundaries
%--------------------------------------------------------------------------
{ODRL_INCLUDE}
{kb_block}
% ─── Conjecture ─────────────────────────────────────────────────────────────
fof({prob_id.lower()}, conjecture, {conjecture}).
%--------------------------------------------------------------------------
"""
    with open(path, "w") as f:
        f.write(content)

# ── CASE 1: Shared Hub KB problems ───────────────────────────────────────────

# Policy pair semantics:
#   CONFLICT conjecture: ![X]: ~(in_denotation(X,A,op) & in_denotation(X,B,op))
#   COMPAT  conjecture:  ?[X]:  (in_denotation(X,A,op) & in_denotation(X,B,op))
#                    or: ![X]:  (in_denotation(X,A,op) => in_denotation(X,B,op))

CASE1_PROBLEMS = [
    # TRUE CONFLICTS — KB_shared has disjointness, conflict must be Theorem
    ("E4_C1_01", "conflict",
     "![X]: ~(in_denotation(X,westernEurope,isPartOf) & in_denotation(X,easternEurope,isPartOf))",
     "Theorem", "D1-direct: wE⊥eE root pair",
     "Permit location=westernEurope vs Prohibit location=easternEurope"),
    ("E4_C1_02", "conflict",
     "![X]: ~(in_denotation(X,germany,isPartOf) & in_denotation(X,france,isPartOf))",
     "Theorem", "D1-direct: de⊥fr sibling pair",
     "Permit location=germany vs Prohibit location=france"),
    ("E4_C1_03", "conflict",
     "![X]: ~(in_denotation(X,germany,isPartOf) & in_denotation(X,poland,isPartOf))",
     "Theorem", "D2-derived: de≤wE, pl≤eE, wE⊥eE",
     "Permit location=germany vs Prohibit location=poland"),
    ("E4_C1_04", "conflict",
     "![X]: ~(in_denotation(X,bavaria,isPartOf) & in_denotation(X,czechia,isPartOf))",
     "Theorem", "D3-derived: bav≤de≤wE, cz≤eE, wE⊥eE",
     "Permit location=bavaria vs Prohibit location=czechia"),
    ("E4_C1_05", "conflict",
     "![X]: ~(in_denotation(X,italy,isPartOf) & in_denotation(X,easternEurope,isPartOf))",
     "Theorem", "D2-derived: it≤wE, wE⊥eE",
     "Permit location=italy vs Prohibit location=easternEurope"),
    # TRUE COMPAT — no disjointness between these, must NOT fire as conflict
    ("E4_C1_06", "compat",
     "?[X]: (in_denotation(X,germany,isPartOf) & in_denotation(X,westernEurope,isPartOf))",
     "Theorem", "compat: de≤wE — subsumption witness",
     "Permit location=germany vs Permit location=westernEurope"),
    ("E4_C1_07", "compat",
     "?[X]: (in_denotation(X,bavaria,isPartOf) & in_denotation(X,europe,isPartOf))",
     "Theorem", "compat: bav≤de≤wE≤eu — chain witness",
     "Permit location=bavaria vs Permit location=europe"),
    ("E4_C1_08", "compat",
     "![X]: (in_denotation(X,germany,isPartOf) => in_denotation(X,westernEurope,isPartOf))",
     "Theorem", "compat: universal subsumption de⊆wE",
     "Provider allows germany ⊆ consumer requires westernEurope"),
    ("E4_C1_09", "compat",
     "?[X]: (in_denotation(X,germany,isPartOf) & in_denotation(X,westernEurope,isPartOf) & in_denotation(X,europe,isPartOf))",
     "Theorem", "compat: 3-way chain de≤wE≤eu",
     "Three-party chain: germany ∩ westernEurope ∩ europe"),
    ("E4_C1_10", "compat",
     "![X]: (in_denotation(X,bavaria,isPartOf) => in_denotation(X,westernEurope,isPartOf))",
     "Theorem", "compat: bav≤de≤wE universal",
     "Permit location=bavaria implies westernEurope allowed"),
]

# ── CASE 2: Asymmetric KB problems ───────────────────────────────────────────
# KB_A (Provider): full GEO
# KB_B (Consumer): only root disjointness (wE⊥eE)
#
# The conjecture is evaluated AGAINST KB_B (consumer's view).
# True conflicts: derivable even from KB_B's root alone.
# FP risks: only in KB_A, KB_B cannot derive → must return Unknown.

CASE2_PROBLEMS = [
    # TRUE CONFLICTS — derivable from KB_B (root wE⊥eE + transitive leq)
    ("E4_C2_01", "conflict",
     "![X]: ~(in_denotation(X,germany,isPartOf) & in_denotation(X,poland,isPartOf))",
     "Theorem", "TRUE-CONFLICT KB_B: de≤wE, pl≤eE, root wE⊥eE sufficient",
     "Provider: Permit location=germany / Consumer: Prohibit location=poland"),
    ("E4_C2_02", "conflict",
     "![X]: ~(in_denotation(X,westernEurope,isPartOf) & in_denotation(X,easternEurope,isPartOf))",
     "Theorem", "TRUE-CONFLICT KB_B: root pair directly",
     "Provider: Permit location=westernEurope / Consumer: Prohibit location=easternEurope"),
    ("E4_C2_03", "conflict",
     "![X]: ~(in_denotation(X,france,isPartOf) & in_denotation(X,czechia,isPartOf))",
     "Theorem", "TRUE-CONFLICT KB_B: fr≤wE, cz≤eE, root wE⊥eE",
     "Provider: Permit location=france / Consumer: Prohibit location=czechia"),
    ("E4_C2_04", "conflict",
     "![X]: ~(in_denotation(X,bavaria,isPartOf) & in_denotation(X,poland,isPartOf))",
     "Theorem", "TRUE-CONFLICT KB_B: bav≤de≤wE, pl≤eE, root wW⊥eE",
     "Provider: Permit location=bavaria / Consumer: Prohibit location=poland"),
    ("E4_C2_05", "conflict",
     "![X]: ~(in_denotation(X,italy,isPartOf) & in_denotation(X,easternEurope,isPartOf))",
     "Theorem", "TRUE-CONFLICT KB_B: it≤wE, root wE⊥eE",
     "Provider: Permit location=italy / Consumer: Prohibit location=easternEurope"),
    # FALSE POSITIVE RISKS — KB_A has sibling disjointness, KB_B does NOT
    # System grounded against KB_B must return Unknown (sound abstention)
    ("E4_C2_06", "conflict",
     "![X]: ~(in_denotation(X,germany,isPartOf) & in_denotation(X,france,isPartOf))",
     "Unknown", "FP-RISK: de⊥fr in KB_A only; KB_B: both≤wE, no sibling disj",
     "Provider: Permit location=germany / Consumer: Prohibit location=france"),
    ("E4_C2_07", "conflict",
     "![X]: ~(in_denotation(X,belgium,isPartOf) & in_denotation(X,spain,isPartOf))",
     "Unknown", "FP-RISK: be⊥es in KB_A only; KB_B: both≤wE, no sibling disj",
     "Provider: Permit location=belgium / Consumer: Prohibit location=spain"),
    ("E4_C2_08", "conflict",
     "![X]: ~(in_denotation(X,poland,isPartOf) & in_denotation(X,czechia,isPartOf))",
     "Unknown", "FP-RISK: pl⊥cz in KB_A only; KB_B: both≤eE, no sibling disj",
     "Provider: Permit location=poland / Consumer: Prohibit location=czechia"),
    ("E4_C2_09", "conflict",
     "![X]: ~(in_denotation(X,bavaria,isPartOf) & in_denotation(X,france,isPartOf))",
     "Unknown", "FP-RISK: bav⊥fr in KB_A only (bav≤de, de⊥fr); KB_B: no de⊥fr",
     "Provider: Permit location=bavaria / Consumer: Prohibit location=france"),
    ("E4_C2_10", "conflict",
     "![X]: ~(in_denotation(X,netherlands,isPartOf) & in_denotation(X,spain,isPartOf))",
     "Unknown", "FP-RISK: nl⊥es in KB_A only; KB_B: both≤wE, no sibling disj",
     "Provider: Permit location=netherlands / Consumer: Prohibit location=spain"),
]


def generate_case1(outdir):
    """Case 1: shared hub KB — full GEO for all problems."""
    kb_block = f"% ─── Shared Hub KB (GEO, complete) ────────────────────────────────────\n"
    kb_block += GEO_HIERARCHY + "\n"
    kb_block += disj_block(GEO_DISJ_FULL)

    for prob_id, ptype, conj, expected, note, policy_desc in CASE1_PROBLEMS:
        path = os.path.join(outdir, "Case1_SharedHub", f"{prob_id}.p")
        full_kb = f"% Policy pair: {policy_desc}\n% Note: {note}\n{kb_block}"
        write_tptp(path, prob_id, full_kb, conj, expected,
                   "Case1-SharedHub: both parties use full GEO KB")

    print(f"  Case 1: {len(CASE1_PROBLEMS)} problems → {outdir}/Case1_SharedHub/")


def generate_case2(outdir):
    """Case 2: asymmetric KBs — conjecture evaluated against KB_B (consumer, minimal)."""
    # Provider KB_A header (informational, not used for proof)
    kbA_info = "% KB_A (Provider, full GEO — NOT used for proof — shown for reference)\n"
    kbA_info += "% " + "\n% ".join(f"disj({a},{b})" for _, a, b in GEO_DISJ_FULL) + "\n"

    # Consumer KB_B (minimal — only root)
    kbB_block  = "% ─── KB_B Consumer KB (GEO, root disjointness only) ───────────────────\n"
    kbB_block += "% Architecture: conflict detection grounded against Consumer KB_B.\n"
    kbB_block += "% KB_A richer disjointness is NOT imported (no false positive by design).\n"
    kbB_block += GEO_HIERARCHY + "\n"
    kbB_block += disj_block(GEO_DISJ_ROOT_ONLY)

    for prob_id, ptype, conj, expected, note, policy_desc in CASE2_PROBLEMS:
        path = os.path.join(outdir, "Case2_AsymmetricKB", f"{prob_id}.p")
        full_kb = f"% Policy pair: {policy_desc}\n% Note: {note}\n"
        full_kb += kbA_info + "\n"
        full_kb += kbB_block
        write_tptp(path, prob_id, full_kb, conj, expected,
                   "Case2-AsymmetricKB: proof grounded against Consumer KB_B only")

    print(f"  Case 2: {len(CASE2_PROBLEMS)} problems → {outdir}/Case2_AsymmetricKB/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="Problems/ODRL/CrossDS")
    args = ap.parse_args()

    outdir = args.outdir
    print(f"\nE4 Cross-Dataspace False Positive Experiment")
    print(f"=" * 55)
    generate_case1(outdir)
    generate_case2(outdir)
    print(f"\nTotal: {len(CASE1_PROBLEMS) + len(CASE2_PROBLEMS)} TPTP problems")
    print(f"  Case 1 (shared hub): {sum(1 for p in CASE1_PROBLEMS if p[1]=='conflict')} conflicts + "
          f"{sum(1 for p in CASE1_PROBLEMS if p[1]=='compat')} compat")
    print(f"  Case 2 (asymmetric): {sum(1 for p in CASE2_PROBLEMS if p[3]=='Theorem')} true conflicts + "
          f"{sum(1 for p in CASE2_PROBLEMS if p[3]=='Unknown')} FP-risk pairs")


if __name__ == "__main__":
    main()
