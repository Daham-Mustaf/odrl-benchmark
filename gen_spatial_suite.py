#!/usr/bin/env python3
"""
Generate & run TPTP problem files for ODRL benchmark suite (spatial domain).

Usage:
  # Generate prover-friendly (ALL Theorem) — default
  uv run python gen_spatial_suite.py -o Problems/ODRL/KBGrounding/Spatial

  # Generate + run Vampire
  uv run python gen_spatial_suite.py -o Problems/ODRL/KBGrounding/Spatial --run

  # Generate original encoding (mixed Theorem/CSA)
  uv run python gen_spatial_suite.py --encoding original

  # Custom timeout & prover
  uv run python gen_spatial_suite.py --run --timeout 30 --prover eprover

  # Dry run
  uv run python gen_spatial_suite.py --dry-run
"""
import os, sys, argparse, subprocess, re, csv, time
from datetime import datetime

PROBLEMS = []

# ═══════════════════════════════════════════════════════════════════════════
# HELPER: LIST CLOSURE GENERATION
# ═══════════════════════════════════════════════════════════════════════════
def generate_list_closure(list_id, elements):
    """Generate: ∀G. in_value_list(G, list_id) ⇒ (G = e₁ ∨ ... ∨ G = eₙ)"""
    disjuncts = " | ".join(f"G = {e}" for e in elements)
    return f"fof(list_{list_id}_closed, axiom,\n    ![G]: (in_value_list(G, {list_id}) => ({disjuncts})))."


def P(fn, exp, vrd, paper, diff, ttl, den, conj, flip_conj=None,
      extra="", inc=("GEO","ODRL"), pl=None):
    PROBLEMS.append(dict(fn=fn, exp=exp, vrd=vrd, paper=paper, diff=diff,
        ttl=ttl, den=den, conj=conj, flip_conj=flip_conj,
        extra=extra, inc=inc, pl=pl))

def tc(op, oper, val, ind="    "):
    return (f"{ind}odrl:constraint [\n%   {ind}  odrl:leftOperand odrl:{op} ;\n"
            f"%   {ind}  odrl:operator odrl:{oper} ;\n%   {ind}  odrl:rightOperand {val} ]")

def tp(name, rt, act, cs):
    lines = [f"ex:{name} a odrl:Set ;", f"  odrl:{rt} [", f"    odrl:action odrl:{act} ;"]
    for i,c in enumerate(cs):
        lines.append(tc(*c) + (" ;" if i<len(cs)-1 else " ] ."))
    return "\n%   ".join(lines)

# === CATEGORY 1: BASIC (010-019) ===

P("ODRL010-1.p","Theorem","Valid","Definition 2 (KB: leq transitivity)","Trivial",
  "(No ODRL policy — pure KB property test)",
  "leq(germany, westernEurope) ∧ leq(westernEurope, europe) ⟹ leq(germany, europe)",
  "fof(odrl010, conjecture, leq(germany, europe)).",
  pl="Transitive spatial containment: germany ⪯ europe")

P("ODRL011-1.p","Theorem","Compatible","Definition 3, Definition 5","Easy",
  tp("policy1","permission","use",[("spatial","isPartOf","geo:europe")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","eq","geo:germany")]),
  "⟦isPartOf(europe)⟧ ⊇ {germany}, ⟦eq(germany)⟧ = {germany}\n%   Witness: germany",
  "fof(odrl011, conjecture,\n    ?[X]: ( in_denotation(X, europe, isPartOf)\n          & in_denotation(X, germany, eq) )).",
  pl="Compatible: isPartOf(europe) ∩ eq(germany) ≠ ∅")

P("ODRL012-1.p","CounterSatisfiable","Conflict","Definition 3, Definition 5","Trivial",
  tp("policy1","permission","use",[("spatial","eq","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","eq","geo:france")]),
  "⟦eq(germany)⟧={germany}, ⟦eq(france)⟧={france}, germany≠france (UNA) → ∅",
  "fof(odrl012, conjecture,\n    ?[X]: ( in_denotation(X, germany, eq)\n          & in_denotation(X, france, eq) )).",
  flip_conj="fof(odrl012, conjecture,\n    ![X]: ~( in_denotation(X, germany, eq)\n           & in_denotation(X, france, eq) )).",
  pl="Conflict: eq(germany) ∩ eq(france) = ∅")

P("ODRL013-1.p","CounterSatisfiable","Conflict","Definition 2 (disj_downward), Definition 5","Medium",
  tp("policy1","permission","use",[("spatial","isPartOf","geo:westernEurope")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:easternEurope")]),
  "disjoint(wE, eE) → disj_downward + disj_irrefl → ∅ → Conflict",
  "fof(odrl013, conjecture,\n    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n          & in_denotation(X, easternEurope, isPartOf) )).",
  flip_conj="fof(odrl013, conjecture,\n    ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n           & in_denotation(X, easternEurope, isPartOf) )).",
  pl="Conflict: isPartOf(westernEurope) ∩ isPartOf(easternEurope) = ∅")

P("ODRL014-1.p","Theorem","Compatible","Definition 3 (hasPart/isPartOf), Definition 5","Medium",
  tp("policy1","permission","use",[("spatial","hasPart","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:europe")]),
  "⟦hasPart(de)⟧={de,wE,europe,world}, ⟦isPartOf(eu)⟧={eu,...,de,...}\n%   Witnesses: westernEurope, europe",
  "fof(odrl014, conjecture,\n    ?[X]: ( in_denotation(X, germany, hasPart)\n          & in_denotation(X, europe, isPartOf) )).",
  pl="Compatible: hasPart(germany) ∩ isPartOf(europe) ≠ ∅")

P("ODRL015-1.p","CounterSatisfiable","Conflict","Definition 3, Definition 5, Lemma 1","Hard",
  tp("policy1","permission","use",[("spatial","hasPart","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","eq","geo:poland")]),
  "disj(eE,wE) → disj(poland,germany) → poland ∉ ⟦hasPart(de)⟧ → ∅",
  "fof(odrl015, conjecture,\n    ?[X]: ( in_denotation(X, germany, hasPart)\n          & in_denotation(X, poland, eq) )).",
  flip_conj="fof(odrl015, conjecture,\n    ![X]: ~( in_denotation(X, germany, hasPart)\n           & in_denotation(X, poland, eq) )).",
  pl="Conflict: hasPart(germany) ∩ eq(poland) = ∅")

P("ODRL016-1.p","Theorem","Compatible","Definition 3 (neq/isPartOf), Definition 5","Medium",
  tp("policy1","permission","use",[("spatial","neq","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:westernEurope")]),
  "⟦neq(de)⟧=C\\{de}, Witness: france",
  "fof(odrl016, conjecture,\n    ?[X]: ( in_denotation(X, germany, neq)\n          & in_denotation(X, westernEurope, isPartOf) )).",
  pl="Compatible: neq(germany) ∩ isPartOf(westernEurope) ≠ ∅")

P("ODRL017-1.p","CounterSatisfiable","Conflict","Definition 3 (eq/neq), Definition 5","Easy",
  tp("policy1","permission","use",[("spatial","neq","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","eq","geo:germany")]),
  "X=germany ∧ X≠germany → contradiction → ∅",
  "fof(odrl017, conjecture,\n    ?[X]: ( in_denotation(X, germany, neq)\n          & in_denotation(X, germany, eq) )).",
  flip_conj="fof(odrl017, conjecture,\n    ![X]: ~( in_denotation(X, germany, neq)\n           & in_denotation(X, germany, eq) )).",
  pl="Conflict: neq(germany) ∩ eq(germany) = ∅")

P("ODRL018-1.p","Theorem","Compatible","Definition 2, Definition 3","Medium-Hard",
  tp("policy1","permission","use",[("spatial","isPartOf","geo:northernEurope")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","hasPart","geo:channelIslands")]),
  "Witness: northernEurope (reflexivity + L0 edge)",
  "fof(odrl018, conjecture,\n    ?[X]: ( in_denotation(X, northernEurope, isPartOf)\n          & in_denotation(X, channelIslands, hasPart) )).",
  pl="Compatible: isPartOf(northernEurope) ∩ hasPart(channelIslands) ≠ ∅")

P("ODRL019-1.p","CounterSatisfiable","Conflict","Definition 2 (disj_downward), Definition 5","Medium",
  tp("policy1","permission","use",[("spatial","isPartOf","geo:northernEurope")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:southernEurope")]),
  "disjoint(nE, sE) [siblings] → ∅ → Conflict",
  "fof(odrl019, conjecture,\n    ?[X]: ( in_denotation(X, northernEurope, isPartOf)\n          & in_denotation(X, southernEurope, isPartOf) )).",
  flip_conj="fof(odrl019, conjecture,\n    ![X]: ~( in_denotation(X, northernEurope, isPartOf)\n           & in_denotation(X, southernEurope, isPartOf) )).",
  pl="Conflict: isPartOf(northernEurope) ∩ isPartOf(southernEurope) = ∅")

# === CATEGORY 2: SET-VALUED (020-025) ===

P("ODRL020-1.p","Theorem","Compatible","Definition 3 (isAnyOf), Definition 5","Medium",
  tp("policy1","permission","use",[("spatial","isAnyOf","( geo:westernEurope geo:northernEurope )")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","eq","geo:germany")]),
  "⟦isAnyOf({wE,nE})⟧=↓wE∪↓nE, Witness: germany∈↓wE",
  "fof(odrl020, conjecture,\n    ?[X]: ( in_denotation_set(X, regions020, isAnyOf)\n          & in_denotation(X, germany, eq) )).",
  extra=(
      "fof(list_020_1, axiom, in_value_list(westernEurope, regions020)).\n"
      "fof(list_020_2, axiom, in_value_list(northernEurope, regions020)).\n" +
      generate_list_closure("regions020", ["westernEurope", "northernEurope"])
  ),
  pl="Compatible: isAnyOf({westernEurope, northernEurope}) ∩ eq(germany) ≠ ∅")

P("ODRL021-1.p","Theorem","Compatible","Definition 3 (isNoneOf), Definition 5","Hard",
  tp("policy1","permission","use",[("spatial","isNoneOf","( geo:easternEurope geo:southernEurope )")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:westernEurope")]),
  "Witness: germany — ≤wE, ¬≤eE (disj), ¬≤sE (disj)",
  "fof(odrl021, conjecture,\n    ?[X]: ( in_denotation_set(X, excluded021, isNoneOf)\n          & in_denotation(X, westernEurope, isPartOf) )).",
  extra=(
      "fof(list_021_1, axiom, in_value_list(easternEurope, excluded021)).\n"
      "fof(list_021_2, axiom, in_value_list(southernEurope, excluded021)).\n" +
      generate_list_closure("excluded021", ["easternEurope", "southernEurope"])
  ),
  pl="Compatible: isNoneOf({easternEurope, southernEurope}) ∩ isPartOf(westernEurope) ≠ ∅")

P("ODRL022-1.p","CounterSatisfiable","Conflict","Definition 3 (isNoneOf), Definition 5","Very Hard",
  tp("policy1","permission","use",[("spatial","isNoneOf","( geo:europe )")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:westernEurope")]),
  "∀x: x≤wE ⟹ x≤europe (trans) → excluded by isNoneOf → ∅",
  "fof(odrl022, conjecture,\n    ?[X]: ( in_denotation_set(X, excluded022, isNoneOf)\n          & in_denotation(X, westernEurope, isPartOf) )).",
  flip_conj="fof(odrl022, conjecture,\n    ![X]: ~( in_denotation_set(X, excluded022, isNoneOf)\n           & in_denotation(X, westernEurope, isPartOf) )).",
  extra=(
      "fof(list_022_1, axiom, in_value_list(europe, excluded022)).\n" +
      generate_list_closure("excluded022", ["europe"])
  ),
  pl="Conflict: isNoneOf({europe}) ∩ isPartOf(westernEurope) = ∅")

P("ODRL023-1.p","CounterSatisfiable","Conflict","Definition 3 (isAllOf), Definition 5","Hard",
  tp("policy1","permission","use",[("spatial","isAllOf","( geo:westernEurope geo:easternEurope )")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","eq","geo:germany")]),
  "disjoint(wE,eE) → ⟦isAllOf⟧=∅ → ∅∩{de}=∅",
  "fof(odrl023, conjecture,\n    ?[X]: ( in_denotation_set(X, allRegions023, isAllOf)\n          & in_denotation(X, germany, eq) )).",
  flip_conj="fof(odrl023, conjecture,\n    ![X]: ~( in_denotation_set(X, allRegions023, isAllOf)\n           & in_denotation(X, germany, eq) )).",
  extra=(
      "fof(list_023_1, axiom, in_value_list(westernEurope, allRegions023)).\n"
      "fof(list_023_2, axiom, in_value_list(easternEurope, allRegions023)).\n" +
      generate_list_closure("allRegions023", ["westernEurope", "easternEurope"])
  ),
  pl="Conflict: isAllOf({westernEurope, easternEurope}) ∩ eq(germany) = ∅")

P("ODRL024-1.p","Theorem","Compatible","Definition 3 (isAnyOf/isNoneOf), Definition 5","Hard",
  tp("policy1","permission","use",[("spatial","isAnyOf","( geo:france geo:germany )")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isNoneOf","( geo:easternEurope )")]),
  "Witness: france — ¬≤eE by disjointness (wE⊥eE)",
  "fof(odrl024, conjecture,\n    ?[X]: ( in_denotation_set(X, anyList024, isAnyOf)\n          & in_denotation_set(X, noneList024, isNoneOf) )).",
  extra=(
      "fof(list_024a_1, axiom, in_value_list(france, anyList024)).\n"
      "fof(list_024a_2, axiom, in_value_list(germany, anyList024)).\n" +
      generate_list_closure("anyList024", ["france", "germany"]) + "\n" +
      "fof(list_024b_1, axiom, in_value_list(easternEurope, noneList024)).\n" +
      generate_list_closure("noneList024", ["easternEurope"])
  ),
  pl="Compatible: isAnyOf({france,germany}) ∩ isNoneOf({easternEurope}) ≠ ∅")

P("ODRL025-1.p","CounterSatisfiable","Conflict","Definition 3 (isAnyOf/isNoneOf), Definition 5","Hard",
  tp("policy1","permission","use",[("spatial","isAnyOf","( geo:germany geo:france )")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isNoneOf","( geo:westernEurope )")]),
  "Both de≤wE and fr≤wE → both excluded → ∅",
  "fof(odrl025, conjecture,\n    ?[X]: ( in_denotation_set(X, anyList025, isAnyOf)\n          & in_denotation_set(X, noneList025, isNoneOf) )).",
  flip_conj="fof(odrl025, conjecture,\n    ![X]: ~( in_denotation_set(X, anyList025, isAnyOf)\n           & in_denotation_set(X, noneList025, isNoneOf) )).",
  extra=(
      "fof(list_025a_1, axiom, in_value_list(germany, anyList025)).\n"
      "fof(list_025a_2, axiom, in_value_list(france, anyList025)).\n" +
      generate_list_closure("anyList025", ["germany", "france"]) + "\n" +
      "fof(list_025b_1, axiom, in_value_list(westernEurope, noneList025)).\n" +
      generate_list_closure("noneList025", ["westernEurope"])
  ),
  pl="Conflict: isAnyOf({germany,france}) ∩ isNoneOf({westernEurope}) = ∅")

# === CATEGORY 3: SUBSUMPTION (030-037) ===

P("ODRL030-1.p","Theorem","Confirmed","Definition 7 (Constraint Subsumption)","Easy",
  "c1: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] .\n%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .",
  "{germany} ⊆ {x|x≤europe} → Confirmed",
  "fof(odrl030, conjecture,\n    ![X]: ( in_denotation(X, germany, isPartOf)\n          => in_denotation(X, europe, isPartOf) )).",
  pl="Subsumption: isPartOf(germany) ⊆ isPartOf(europe)")

P("ODRL031-1.p","CounterSatisfiable","Refuted","Definition 7","Medium",
  "c1: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .\n%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] .",
  "Counterexample: france ∈ ⟦c1⟧ but france ∉ ⟦c2⟧",
  "fof(odrl031, conjecture,\n    ![X]: ( in_denotation(X, europe, isPartOf)\n          => in_denotation(X, germany, isPartOf) )).",
  flip_conj="fof(odrl031, conjecture,\n    ?[X]: ( in_denotation(X, europe, isPartOf)\n          & ~in_denotation(X, germany, isPartOf) )).",
  pl="Subsumption refuted: isPartOf(europe) ⊄ isPartOf(germany)")

P("ODRL032-1.p","Theorem","Confirmed","Definition 7","Easy",
  "c1: [ odrl:operator odrl:eq ; odrl:rightOperand geo:germany ] .\n%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .",
  "\"Exactly germany\" refines \"anywhere in europe\".",
  "fof(odrl032, conjecture,\n    ![X]: ( in_denotation(X, germany, eq)\n          => in_denotation(X, europe, isPartOf) )).",
  pl="Cross-operator subsumption: eq(germany) ⊆ isPartOf(europe)")

P("ODRL033-1.p","Theorem","Confirmed","Definition 3 (isA=isPartOf), Definition 7","Trivial",
  "c1: [ odrl:operator odrl:isA ; odrl:rightOperand geo:germany ] .\n%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] .",
  "TAUTOLOGY: isA and isPartOf have identical denotation.",
  "fof(odrl033, conjecture,\n    ![X]: ( in_denotation(X, germany, isA)\n        <=> in_denotation(X, germany, isPartOf) )).",
  pl="Tautological equivalence: isA(germany) ≡ isPartOf(germany)")

P("ODRL034-1.p","Theorem","Confirmed","Definition 7, policy simplification","Easy",
  "Same rule, two constraints (redundancy):\n%   ex:rule1 a odrl:Permission ;\n%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] ;\n%     odrl:constraint [ odrl:operator odrl:eq ; odrl:rightOperand geo:germany ] .",
  "eq(de) ⊆ isPartOf(wE) → eq constraint is redundant.",
  "fof(odrl034, conjecture,\n    ![X]: ( in_denotation(X, germany, eq)\n          => in_denotation(X, westernEurope, isPartOf) )).",
  pl="Redundancy: eq(germany) ⊆ isPartOf(westernEurope)")

P("ODRL035-1.p","CounterSatisfiable","Conflict","Lemma 2 (Conflict Propagation)","Medium",
  "c1: isPartOf(germany), c2: isPartOf(westernEurope), c3: isPartOf(easternEurope)",
  "c1⊑c2 (ODRL030) ∧ conflict(c2,c3) (ODRL013) ⟹ conflict(c1,c3)",
  "fof(odrl035, conjecture,\n    ?[X]: ( in_denotation(X, germany, isPartOf)\n          & in_denotation(X, easternEurope, isPartOf) )).",
  flip_conj="fof(odrl035, conjecture,\n    ![X]: ~( in_denotation(X, germany, isPartOf)\n           & in_denotation(X, easternEurope, isPartOf) )).",
  pl="Conflict propagation: c1⊑c2 ∧ conflict(c2,c3) → conflict(c1,c3)")

P("ODRL036-1.p","Theorem","Confirmed","Definition 7","Medium",
  "c1: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] .\n%   c2: [ odrl:operator odrl:neq ; odrl:rightOperand geo:france ] .",
  "germany≠france (UNA) → {germany} ⊆ C\\{france}",
  "fof(odrl036, conjecture,\n    ![X]: ( in_denotation(X, germany, isPartOf)\n          => in_denotation(X, france, neq) )).",
  pl="Cross-operator subsumption: isPartOf(germany) ⊆ neq(france)")

P("ODRL037-1.p","CounterSatisfiable","Refuted","Definition 7","Medium",
  "c1: [ odrl:operator odrl:neq ; odrl:rightOperand geo:germany ] .\n%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] .",
  "Counterexample: poland ∈ ⟦neq(de)⟧ but poland ∉ ⟦isPartOf(wE)⟧",
  "fof(odrl037, conjecture,\n    ![X]: ( in_denotation(X, germany, neq)\n          => in_denotation(X, westernEurope, isPartOf) )).",
  flip_conj="fof(odrl037, conjecture,\n    ?[X]: ( in_denotation(X, germany, neq)\n          & ~in_denotation(X, westernEurope, isPartOf) )).",
  pl="Subsumption refuted: neq(germany) ⊄ isPartOf(westernEurope)")

# === CATEGORY 4: COMPOSITION (040-047) ===

P("ODRL040-1.p","Theorem","Compatible","Definition 6 (Composition, and)","Medium",
  tp("policy1","permission","use",[("spatial","isPartOf","geo:europe"),("hasPurpose","isA","dpv:ResearchAndDevelopment")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","eq","geo:germany"),("hasPurpose","isA","dpv:AcademicResearch")]),
  "V_spatial=Compatible, V_purpose=Compatible → AND-Compatible",
  "fof(odrl040, conjecture,\n    ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n             & in_denotation(Xs, germany, eq) )\n    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n             & in_denotation(Xp, academicResearch, isA) ) )).",
  inc=("GEO","DPV","ODRL"), pl="AND-Compatible: spatial ✓ ∧ purpose ✓ → Compatible")

P("ODRL041-1.p","CounterSatisfiable","Conflict","Definition 6 (Composition, and)","Hard",
  tp("policy1","permission","use",[("spatial","isPartOf","geo:europe"),("hasPurpose","isA","dpv:AcademicResearch")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","eq","geo:germany"),("hasPurpose","isA","dpv:Marketing")]),
  "V_spatial=Compatible, V_purpose=Conflict → AND-Conflict",
  "fof(odrl041, conjecture,\n    ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n             & in_denotation(Xs, germany, eq) )\n    & ?[Xp]: ( in_denotation(Xp, academicResearch, isA)\n             & in_denotation(Xp, marketing, isA) ) )).",
  flip_conj="fof(odrl041, conjecture,\n    ![Xp]: ~( in_denotation(Xp, academicResearch, isA)\n            & in_denotation(Xp, marketing, isA) )).",
  inc=("GEO","DPV","ODRL"), pl="AND-Conflict: spatial ✓ ∧ purpose ✗ → Conflict")

P("ODRL042-1.p","Theorem","Compatible","Definition 6 (Composition, or)","Hard",
  tp("policy1","permission","use",[("spatial","isPartOf","geo:westernEurope"),("hasPurpose","isA","dpv:ResearchAndDevelopment")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:easternEurope"),("hasPurpose","isA","dpv:AcademicResearch")]),
  "V_spatial=Conflict, V_purpose=Compatible → OR-Compatible",
  "fof(odrl042, conjecture,\n    ( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)\n             & in_denotation(Xs, easternEurope, isPartOf) )\n    | ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n             & in_denotation(Xp, academicResearch, isA) ) )).",
  inc=("GEO","DPV","ODRL"), pl="OR-Compatible: spatial ✗ ∨ purpose ✓ → Compatible")

P("ODRL043-1.p","CounterSatisfiable","Conflict","Definition 6 (Composition, or)","Hard",
  "V_spatial=Conflict(wE⊥eE), V_purpose=Conflict(AcadRes⊥Marketing)",
  "OR: ∀k:V_k=Conflict → Conflict",
  "fof(odrl043, conjecture,\n    ( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)\n             & in_denotation(Xs, easternEurope, isPartOf) )\n    | ?[Xp]: ( in_denotation(Xp, academicResearch, isA)\n             & in_denotation(Xp, marketing, isA) ) )).",
  flip_conj="fof(odrl043, conjecture,\n    ( ![Xs]: ~( in_denotation(Xs, westernEurope, isPartOf)\n              & in_denotation(Xs, easternEurope, isPartOf) )\n    & ![Xp]: ~( in_denotation(Xp, academicResearch, isA)\n              & in_denotation(Xp, marketing, isA) ) )).",
  inc=("GEO","DPV","ODRL"), pl="OR-Conflict: spatial ✗ ∨ purpose ✗ → Conflict")

P("ODRL044-1.p","CounterSatisfiable","Conflict",
  "Definition 5 (self-conflict within single rule)","Medium",
  "ex:policy1 a odrl:Set ;\n"
  "%     odrl:permission [\n"
  "%       odrl:action odrl:use ;\n"
  "%       odrl:constraint [\n"
  "%         odrl:leftOperand odrl:spatial ;\n"
  "%         odrl:operator odrl:isPartOf ;\n"
  "%         odrl:rightOperand geo:westernEurope ] ;\n"
  "%       odrl:constraint [\n"
  "%         odrl:leftOperand odrl:spatial ;\n"
  "%         odrl:operator odrl:isPartOf ;\n"
  "%         odrl:rightOperand geo:easternEurope ] ] .",
  "Same rule, same operand, two constraints: isPartOf(wE) ∧ isPartOf(eE)\n"
  "%   disjoint(wE, eE) → no X satisfies both → rule is vacuous",
  "fof(odrl044, conjecture,\n"
  "    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
  "          & in_denotation(X, easternEurope, isPartOf) )).",
  flip_conj=
  "fof(odrl044, conjecture,\n"
  "    ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
  "           & in_denotation(X, easternEurope, isPartOf) )).",
  pl="Self-conflict: single rule with contradictory constraints")

P("ODRL045-1.p","Theorem","Compatible","Definition 6 (Composition, xone)","Very Hard",
  "V_spatial=Conflict(provable), V_purpose=Compatible",
  "XONE: ∃!k:V_k=Compatible ∧ ∀j≠k:V_j=Conflict → Compatible",
  "fof(odrl045, conjecture,\n    ( ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n             & in_denotation(Xp, academicResearch, isA) )\n    & ~( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)\n                & in_denotation(Xs, easternEurope, isPartOf) ) ) )).",
  inc=("GEO","DPV","ODRL"), pl="XONE-Compatible: purpose ✓ ⊕ spatial ✗ → Compatible")

P("ODRL046-1.p","CounterSatisfiable","Unknown","Definition 6 (Composition, xone)","Very Hard",
  "V_spatial=Compatible, V_purpose=Compatible → exclusivity fails → Unknown",
  "XONE=(spatial∧¬purpose)∨(purpose∧¬spatial) — both disjuncts fail.",
  "fof(odrl046, conjecture,\n    ( ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n              & in_denotation(Xs, germany, eq) )\n      & ~( ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n                   & in_denotation(Xp, academicResearch, isA) ) ) )\n    | ( ?[Xp2]: ( in_denotation(Xp2, researchAndDevelopment, isA)\n                & in_denotation(Xp2, academicResearch, isA) )\n      & ~( ?[Xs2]: ( in_denotation(Xs2, europe, isPartOf)\n                    & in_denotation(Xs2, germany, eq) ) ) ) )).",
  flip_conj="fof(odrl046, conjecture,\n    ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n             & in_denotation(Xs, germany, eq) )\n    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n             & in_denotation(Xp, academicResearch, isA) ) )).",
  inc=("GEO","DPV","ODRL"), pl="XONE-Unknown: spatial ✓ ⊕ purpose ✓ → Unknown")

P("ODRL047-1.p","CounterSatisfiable","Conflict","Definition 6 (Composition, xone)","Hard",
  "V_spatial=Conflict, V_purpose=Conflict",
  "XONE: ∀k:V_k=Conflict → Conflict",
  "fof(odrl047, conjecture,\n    ( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)\n             & in_denotation(Xs, easternEurope, isPartOf) )\n    | ?[Xp]: ( in_denotation(Xp, academicResearch, isA)\n             & in_denotation(Xp, marketing, isA) ) )).",
  flip_conj="fof(odrl047, conjecture,\n    ( ![Xs]: ~( in_denotation(Xs, westernEurope, isPartOf)\n              & in_denotation(Xs, easternEurope, isPartOf) )\n    & ![Xp]: ~( in_denotation(Xp, academicResearch, isA)\n              & in_denotation(Xp, marketing, isA) ) )).",
  inc=("GEO","DPV","ODRL"), pl="XONE-Conflict: spatial ✗ ⊕ purpose ✗ → Conflict")

# === CATEGORY 5: EDGE CASES (050-055) ===

P("ODRL050-1.p","Theorem","Compatible","Definition 5 (identity)","Trivial",
  "Identical constraints on two rules.",
  "⟦isPartOf(eu)⟧ ∩ ⟦isPartOf(eu)⟧ = ⟦isPartOf(eu)⟧ ≠ ∅",
  "fof(odrl050, conjecture,\n    ?[X]: ( in_denotation(X, europe, isPartOf)\n          & in_denotation(X, europe, isPartOf) )).",
  pl="Self-compatible: isPartOf(europe) ∩ isPartOf(europe) ≠ ∅")

P("ODRL051-1.p","Theorem","Compatible","Definition 3 (hasPart)","Medium",
  tp("policy1","permission","use",[("spatial","hasPart","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","eq","geo:world")]),
  "Witness: world (3 transitivity steps: de→wE→eu→world)",
  "fof(odrl051, conjecture,\n    ?[X]: ( in_denotation(X, germany, hasPart)\n          & in_denotation(X, world, eq) )).",
  pl="Root reachability: hasPart(germany) ∩ eq(world) ≠ ∅")

P("ODRL052-1.p","Theorem","Compatible","Definition 3 (hasPart)","Medium",
  tp("policy1","permission","use",[("spatial","hasPart","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","hasPart","geo:france")]),
  "Common ancestors: {wE, europe, world}. Witness: westernEurope",
  "fof(odrl052, conjecture,\n    ?[X]: ( in_denotation(X, germany, hasPart)\n          & in_denotation(X, france, hasPart) )).",
  pl="Common ancestor: hasPart(germany) ∩ hasPart(france) ≠ ∅")

P("ODRL053-1.p","Theorem","Compatible","Definition 3 (hasPart)","Medium-Hard",
  tp("policy1","permission","use",[("spatial","hasPart","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","hasPart","geo:poland")]),
  "NOTE: isPartOf(de)∩isPartOf(pl)=Conflict, but hasPart looks UPWARD!\n%   Common ancestors: {europe, world}. Witness: europe",
  "fof(odrl053, conjecture,\n    ?[X]: ( in_denotation(X, germany, hasPart)\n          & in_denotation(X, poland, hasPart) )).",
  pl="Cross-branch hasPart: hasPart(germany) ∩ hasPart(poland) ≠ ∅")

P("ODRL054-1.p","Theorem","Confirmed","Definition 7","Medium",
  "c1: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] .\n%   c2: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:germany ] .",
  "⟦hasPart(eu)⟧={eu,world} ⊆ ⟦hasPart(de)⟧={de,wE,eu,world}\n%   Counterintuitive: MORE GENERAL concept → FEWER ancestors.",
  "fof(odrl054, conjecture,\n    ![X]: ( in_denotation(X, europe, hasPart)\n          => in_denotation(X, germany, hasPart) )).",
  pl="Counterintuitive: hasPart(europe) ⊆ hasPart(germany)")

P("ODRL055-1.p","CounterSatisfiable","Refuted","Definition 7","Medium",
  "c1: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:germany ] .\n%   c2: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] .",
  "Counterexample: germany ∈ ⟦c1⟧ but germany ∉ ⟦c2⟧\n%   Paired with ODRL054: hasPart subsumption asymmetry.",
  "fof(odrl055, conjecture,\n    ![X]: ( in_denotation(X, germany, hasPart)\n          => in_denotation(X, europe, hasPart) )).",
  flip_conj="fof(odrl055, conjecture,\n    ?[X]: ( in_denotation(X, germany, hasPart)\n          & ~in_denotation(X, europe, hasPart) )).",
  pl="Subsumption refuted: hasPart(germany) ⊄ hasPart(europe)")

# === CATEGORY 6: TAUTOLOGY / REDUNDANCY / REFINEMENT CONFLICT (060-069) ===

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 6A: TAUTOLOGY DETECTION (060-062)
# ═══════════════════════════════════════════════════════════════════════════

# 060: isPartOf(europe) = C because europe is root of GEO KB
P("ODRL060-1.p","Theorem","Tautological","Tautology Detection","Easy",
  "c: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .",
  "⟦isPartOf(europe)⟧ = {x ∈ C | x ≤ europe} = C\n"
  "%   europe is the root of GEO KB → every concept is ≤ europe\n"
  "%   via transitivity (country → sub-region → europe) → tautological",
  "fof(odrl060, conjecture,\n    ![X]: ( concept(X) => in_denotation(X, europe, isPartOf) )).",
  pl="Tautology: isPartOf(europe) = C (root covers all concepts)")

# 061: isPartOf(westernEurope) ⊂ C — only 10 of 58 concepts
P("ODRL061-1.p","CounterSatisfiable","Non-Tautological","Tautology Detection","Easy",
  "c: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] .",
  "⟦isPartOf(westernEurope)⟧ = ↓wE = {wE, austria, belgium, france,\n"
  "%     germany, liechtenstein, luxembourg, monaco, netherlands, switzerland}\n"
  "%   Only 10 of 58 concepts. Counterexample: poland (≤ eE, ¬≤ wE)",
  "fof(odrl061, conjecture,\n    ![X]: ( concept(X) => in_denotation(X, westernEurope, isPartOf) )).",
  flip_conj="fof(odrl061, conjecture,\n    ?[X]: ( concept(X) & ~in_denotation(X, westernEurope, isPartOf) )).",
  pl="Non-tautological: isPartOf(westernEurope) ⊂ C")

# 062: hasPart(europe) = {europe} ≠ C — only root satisfies hasPart(root)
P("ODRL062-1.p","CounterSatisfiable","Non-Tautological","Tautology Detection (hasPart root)","Easy",
  "c: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] .",
  "⟦hasPart(europe)⟧ = {x ∈ C | europe ≤ x} = {europe}\n"
  "%   europe is maximal (root) → only europe itself satisfies hasPart(europe)\n"
  "%   This is NOT tautological: |⟦hasPart(europe)⟧| = 1, |C| = 58\n"
  "%   Counterexample: germany — europe ¬≤ germany",
  "fof(odrl062, conjecture,\n    ![X]: ( concept(X) => in_denotation(X, europe, hasPart) )).",
  flip_conj="fof(odrl062, conjecture,\n    ?[X]: ( concept(X) & ~in_denotation(X, europe, hasPart) )).",
  pl="Non-tautological: hasPart(europe) = {europe} ≠ C")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 6B: REDUNDANCY DETECTION (063-065)
# ═══════════════════════════════════════════════════════════════════════════

# 063: isPartOf(germany) ⊆ isPartOf(europe) — europe constraint redundant
P("ODRL063-1.p","Theorem","Redundant","Redundancy Detection (intra-rule ∧)","Medium",
  "ex:rule a odrl:Permission ;\n"
  "%     odrl:action odrl:use ;\n"
  "%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] ;\n"
  "%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .",
  "Under conjunction: ⟦isPartOf(de)⟧ ⊆ ⟦isPartOf(eu)⟧\n"
  "%   Chain: leq(X, de) → leq(de, wE) [h_0017] → leq(wE, eu) [h_0056] → leq(X, eu)\n"
  "%   → the europe constraint adds no restriction → REDUNDANT\n"
  "%   The STRICTER constraint (germany) makes the WEAKER one (europe) redundant.",
  "fof(odrl063, conjecture,\n    ![X]: ( in_denotation(X, germany, isPartOf)\n          => in_denotation(X, europe, isPartOf) )).",
  pl="Redundancy: isPartOf(europe) redundant under ∧ with isPartOf(germany)")

# 064: isAnyOf({germany, france}) ⊆ isPartOf(westernEurope)
P("ODRL064-1.p","Theorem","Redundant","Redundancy Detection (set-valued)","Medium",
  "ex:rule a odrl:Permission ;\n"
  "%     odrl:constraint [ odrl:operator odrl:isAnyOf ;\n"
  "%                        odrl:rightOperand ( geo:germany geo:france ) ] ;\n"
  "%     odrl:constraint [ odrl:operator odrl:isPartOf ;\n"
  "%                        odrl:rightOperand geo:westernEurope ] .",
  "⟦isAnyOf({de,fr})⟧ = ↓de ∪ ↓fr ⊆ ↓wE = ⟦isPartOf(wE)⟧",
  "fof(odrl064, conjecture,\n    ![X]: ( in_denotation_set(X, anyList064, isAnyOf)\n          => in_denotation(X, westernEurope, isPartOf) )).",
  extra=(
      "fof(list_064_1, axiom, in_value_list(germany, anyList064)).\n"
      "fof(list_064_2, axiom, in_value_list(france, anyList064)).\n" +
      generate_list_closure("anyList064", ["germany", "france"])
  ),
  pl="Redundancy: isAnyOf({de,fr}) ⊆ isPartOf(wE) → wE constraint redundant")

# 065: isPartOf(europe) ⊄ neq(germany) — germany witnesses the failure
P("ODRL065-1.p","CounterSatisfiable","Non-Redundant","Redundancy Refuted","Medium",
  "ex:rule a odrl:Permission ;\n"
  "%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] ;\n"
  "%     odrl:constraint [ odrl:operator odrl:neq ; odrl:rightOperand geo:germany ] .",
  "⟦isPartOf(eu)⟧ ⊄ ⟦neq(de)⟧: germany ∈ ⟦isPartOf(eu)⟧ but germany ∉ ⟦neq(de)⟧\n"
  "%   → neq(germany) is NOT redundant; it genuinely restricts the rule\n"
  "%   (removes exactly germany from the europe scope)",
  "fof(odrl065, conjecture,\n    ![X]: ( in_denotation(X, europe, isPartOf)\n          => in_denotation(X, germany, neq) )).",
  flip_conj="fof(odrl065, conjecture,\n    ?[X]: ( in_denotation(X, europe, isPartOf)\n          & ~in_denotation(X, germany, neq) )).",
  pl="Non-redundant: isPartOf(europe) ⊄ neq(germany)")


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 6C: REFINEMENT CONFLICT / PARTIAL OVERLAP (066-069)
#
# Pattern: ∃X.(c1∧c2) ∧ ∃Y.(c1∧¬c2) ∧ ∃Z.(c2∧¬c1)
# ═══════════════════════════════════════════════════════════════════════════

# 066: hasPart(germany) vs isPartOf(westernEurope)
#   hasPart(de) = {de, wE, europe}   (3 concepts: ancestors of germany)
#   isPartOf(wE) = ↓wE               (10 concepts: wE + 9 countries)
#   Intersection = {de, wE}  ≠ ∅
#   {europe} = hasPart(de) \ isPartOf(wE)              → c1 ⊄ c2
#   {austria, belgium, france, ...} = isPartOf(wE) \ hasPart(de)  → c2 ⊄ c1
P("ODRL066-1.p","Theorem","Partial-Overlap","Refinement Conflict (hasPart vs isPartOf)","Hard",
  tp("policy1","permission","use",[("spatial","hasPart","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:westernEurope")]),
  "⟦hasPart(de)⟧ = {de, wE, europe}  (ancestors of germany)\n"
  "%   ⟦isPartOf(wE)⟧ = {wE, austria, belgium, france, de, ...}  (10 concepts)\n"
  "%   Intersection = {germany, westernEurope} ≠ ∅\n"
  "%   hasPart(de) \\ isPartOf(wE) = {europe}             → c1 ⊄ c2\n"
  "%   isPartOf(wE) \\ hasPart(de) = {austria, belgium, france, ...}  → c2 ⊄ c1\n"
  "%   → PARTIAL OVERLAP (modification conflict)",
  "fof(odrl066, conjecture,\n"
  "    ( ?[X]: ( in_denotation(X, germany, hasPart)\n"
  "           & in_denotation(X, westernEurope, isPartOf) )\n"
  "    & ?[Y]: ( in_denotation(Y, germany, hasPart)\n"
  "           & ~in_denotation(Y, westernEurope, isPartOf) )\n"
  "    & ?[Z]: ( in_denotation(Z, westernEurope, isPartOf)\n"
  "           & ~in_denotation(Z, germany, hasPart) ) )).",
  pl="Partial overlap: hasPart(germany) vs isPartOf(westernEurope)")

# 067: neq(germany) vs isPartOf(westernEurope)
#   neq(de) = C \ {de}  (57 concepts)
#   isPartOf(wE) = ↓wE   (10 concepts)
#   Intersection = ↓wE \ {de} = {wE, austria, belgium, france, ...} (9 concepts)
#   neq(de) \ isPartOf(wE) = {poland, eE, nE, sE, europe, ...}    → c1 ⊄ c2
#   isPartOf(wE) \ neq(de) = {germany}                             → c2 ⊄ c1
P("ODRL067-1.p","Theorem","Partial-Overlap","Refinement Conflict (neq vs isPartOf)","Hard",
  tp("policy1","permission","use",[("spatial","neq","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:westernEurope")]),
  "⟦neq(de)⟧ = C \\ {de}  (57 concepts)\n"
  "%   ⟦isPartOf(wE)⟧ = ↓wE  (10 concepts)\n"
  "%   Intersection = ↓wE \\ {de} = {wE, austria, belgium, france, ...} ≠ ∅\n"
  "%   neq(de) \\ isPartOf(wE) = {poland, eE, nE, sE, europe, ...} → c1 ⊄ c2\n"
  "%   isPartOf(wE) \\ neq(de) = {germany}                          → c2 ⊄ c1\n"
  "%   → PARTIAL OVERLAP",
  "fof(odrl067, conjecture,\n"
  "    ( ?[X]: ( in_denotation(X, germany, neq)\n"
  "           & in_denotation(X, westernEurope, isPartOf) )\n"
  "    & ?[Y]: ( in_denotation(Y, germany, neq)\n"
  "           & ~in_denotation(Y, westernEurope, isPartOf) )\n"
  "    & ?[Z]: ( in_denotation(Z, westernEurope, isPartOf)\n"
  "           & ~in_denotation(Z, germany, neq) ) )).",
  pl="Partial overlap: neq(germany) vs isPartOf(westernEurope)")


# 068: isNoneOf({easternEurope}) vs hasPart(poland)
#   isNoneOf({eE}) = C \ ↓eE  (47 concepts: all non-eastern + europe)
#   hasPart(pl) = {pl, eE, europe}  (3 concepts: ancestors of poland)
#   Intersection = {europe}  (europe ¬≤ eE, but pl ≤ europe)
#   isNoneOf({eE}) \ hasPart(pl) = {wE, nE, sE, france, ...}   → c1 ⊄ c2
#   hasPart(pl) \ isNoneOf({eE}) = {poland, eE}  (both ≤ eE)   → c2 ⊄ c1
P("ODRL068-1.p","Theorem","Partial-Overlap","Refinement Conflict (isNoneOf vs hasPart)","Very Hard",
  tp("policy1","permission","use",[("spatial","isNoneOf","( geo:easternEurope )")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","hasPart","geo:poland")]),
  "⟦isNoneOf({eE})⟧ = C \\ ↓eE  (47 concepts: all non-eastern + europe)",
  "fof(odrl068, conjecture,\n"
  "    ( ?[X]: ( in_denotation_set(X, excl068, isNoneOf)\n"
  "           & in_denotation(X, poland, hasPart) )\n"
  "    & ?[Y]: ( in_denotation_set(Y, excl068, isNoneOf)\n"
  "           & ~in_denotation(Y, poland, hasPart) )\n"
  "    & ?[Z]: ( in_denotation(Z, poland, hasPart)\n"
  "           & ~in_denotation_set(Z, excl068, isNoneOf) ) )).",
  extra=(
      "fof(list_068_1, axiom, in_value_list(easternEurope, excl068)).\n" +
      generate_list_closure("excl068", ["easternEurope"])
  ),
  pl="Partial overlap: isNoneOf({easternEurope}) vs hasPart(poland)")

# 069: eq(germany) ⊆ isPartOf(westernEurope) → NOT partial overlap
#   Second witness (Y ∈ eq(de) \ isPartOf(wE)) fails: de ≤ wE directly
P("ODRL069-1.p","CounterSatisfiable","Full-Subsumption","Refinement Conflict Refuted","Medium",
  tp("policy1","permission","use",[("spatial","eq","geo:germany")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:westernEurope")]),
  "⟦eq(de)⟧ = {de} ⊆ ↓wE = ⟦isPartOf(wE)⟧\n"
  "%   Three-part test fails at part 2:\n"
  "%     X: eq(de) ∩ isPartOf(wE) → germany ✓\n"
  "%     Y: eq(de) \\ isPartOf(wE) → NO witness! (de ≤ wE by h_0017)\n"
  "%     Z: isPartOf(wE) \\ eq(de) → france ✓\n"
  "%   → NOT partial overlap; this is full subsumption (cf. ODRL034)",
  "fof(odrl069, conjecture,\n"
  "    ( ?[X]: ( in_denotation(X, germany, eq)\n"
  "           & in_denotation(X, westernEurope, isPartOf) )\n"
  "    & ?[Y]: ( in_denotation(Y, germany, eq)\n"
  "           & ~in_denotation(Y, westernEurope, isPartOf) )\n"
  "    & ?[Z]: ( in_denotation(Z, westernEurope, isPartOf)\n"
  "           & ~in_denotation(Z, germany, eq) ) )).",
  flip_conj="fof(odrl069, conjecture,\n"
  "    ~( ?[Y]: ( in_denotation(Y, germany, eq)\n"
  "            & ~in_denotation(Y, westernEurope, isPartOf) ) )).",
  pl="NOT partial overlap: eq(germany) ⊆ isPartOf(wE) → full subsumption")


# ═══════════════════════════════════════════════════════════════════════════
# INLINE ALIGNMENT AXIOMS (for ODRL082 — derivability test)
# ═══════════════════════════════════════════════════════════════════════════
# Part A of ALIGN000-0.ax, inlined for problems that test derivability
# of Part B without loading the full alignment theory file.
ALIGN_PART_A_INLINE = """\
% --- Inline Part A of ALIGN000-0.ax (Definition 8) ---
% Included here to test derivability of Part B (Lemma 3).
fof(align_order_forward, axiom,
    ![X,Y,Xp,Yp]: ((align(X, Xp) & align(Y, Yp) & leq(X, Y))
        => leq(Xp, Yp))).
fof(align_order_backward, axiom,
    ![X,Y,Xp,Yp]: ((align(X, Xp) & align(Y, Yp) & leq(Xp, Yp))
        => leq(X, Y))).
fof(align_disj_forward, axiom,
    ![X,Y,Xp,Yp]: ((align(X, Xp) & align(Y, Yp) & disjoint(X, Y))
        => disjoint(Xp, Yp))).
fof(align_injective, axiom,
    ![X,Y,Z]: ((align(X, Z) & align(Y, Z)) => (X = Y))).
fof(align_functional, axiom,
    ![X,Y,Z]: ((align(X, Y) & align(X, Z)) => (Y = Z))).
fof(align_typed, axiom,
    ![X,Y]: (align(X, Y) => (concept(X) & concept(Y))))."""


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 7: CROSS-DATASPACE ALIGNMENT (080-087)
# Paper §3.3 — Definition 8, Lemma 3, Proposition 2, Corollary 1
#
# These problems load TWO KBs (GEO + ISO 3166) plus alignment axioms.
# They test verdict preservation, graceful degradation, and alignment
# theory derivability.
#
# Alignment: GEO (curated UN M49) → ISO 3166 (flat EU27)
#   Mapped: europe→europe, france→fR, germany→dE, poland→pL, italy→iT, spain→eS
#   Unmapped: westernEurope, easternEurope, northernEurope, southernEurope,
#             + all sub-national (bavaria, ileDeFrance, paris, etc.)
# ═══════════════════════════════════════════════════════════════════════════

# 080: Conflict preservation (Prop 2.1) — source-KB conflict still holds
#   with ISO 3166 + alignment axioms loaded. Baseline test: alignment
#   doesn't break existing single-KB reasoning.
P("ODRL080-1.p","CounterSatisfiable","Conflict",
  "Proposition 2(1) — Conflict Preservation (baseline)","Hard",
  tp("policy1","permission","use",[("spatial","isPartOf","geo:westernEurope")])+"\n%\n%   "+
  tp("policy2","prohibition","use",[("spatial","isPartOf","geo:easternEurope")]),
  "disjoint(wE, eE) in GEO → ∅ → Conflict.\n"
  "%   Tests: loading ISO3166 + alignment does NOT disrupt source-KB reasoning.",
  "fof(odrl080, conjecture,\n"
  "    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
  "          & in_denotation(X, easternEurope, isPartOf) )).",
  flip_conj=
  "fof(odrl080, conjecture,\n"
  "    ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
  "           & in_denotation(X, easternEurope, isPartOf) )).",
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="Conflict preservation: wE ⊥ eE holds with alignment loaded")

# 081: Aligned disjointness transfer (Def 8.ii + disj_downward)
#   germany ⊥ poland in GEO (via disj_downward from wE ⊥ eE)
#   align(germany, dE) + align(poland, pL) → disjoint(dE, pL) [align_disj_forward]
#   → ⟦isPartOf(dE)⟧ ∩ ⟦isPartOf(pL)⟧ = ∅ in ISO 3166
P("ODRL081-1.p","CounterSatisfiable","Conflict",
  "Def. 8(ii), Proposition 2(1) — Disjointness Transfer","Very Hard",
  "Dataspace A (GEO): permission spatial isPartOf germany\n"
  "%   Dataspace B (ISO): prohibition spatial isPartOf pL",
  "disj_downward(wE⊥eE, de≤wE, pl≤eE) → disjoint(de, pl)\n"
  "%   align_disj_forward(de→dE, pl→pL, disj(de,pl)) → disjoint(dE, pL)\n"
  "%   → ⟦isPartOf(dE)⟧ ∩ ⟦isPartOf(pL)⟧ = ∅ → Conflict",
  "fof(odrl081, conjecture,\n"
  "    ?[X]: ( in_denotation(X, dE, isPartOf)\n"
  "          & in_denotation(X, pL, isPartOf) )).",
  flip_conj=
  "fof(odrl081, conjecture,\n"
  "    ![X]: ~( in_denotation(X, dE, isPartOf)\n"
  "           & in_denotation(X, pL, isPartOf) )).",
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="Aligned conflict: disjoint(dE, pL) via alignment transfer")

# 082: Lemma 3 derivability test (review recommendation)
#   Load Part A axioms INLINE (not from ALIGN000-0.ax).
#   Do NOT load ALIGN000-0.ax.
#   Prove denotation transfer (Part B) as conjecture.
#   Expected: Theorem — Part B is derivable from Part A + ODRL000-0.ax.
P("ODRL082-1.p","Theorem","Derivable",
  "Lemma 3 — Denotation Transfer Derivability","Hard",
  "(Meta-test: Part B of ALIGN000-0.ax is derivable from Part A + ODRL000-0.ax)",
  "Prove: in_den(X,G,isPartOf) ∧ align(X,Xp) ∧ align(G,Gp)\n"
  "%          ⟹ in_den(Xp,Gp,isPartOf)\n"
  "%   Using only Part A axioms (inlined) + ODRL000-0.ax denotation rules.\n"
  "%   Proof: den_isPartOf_onlyif → leq(X,G) → align_order_forward → leq(Xp,Gp)\n"
  "%          → den_isPartOf_if → in_denotation(Xp,Gp,isPartOf)",
  "fof(odrl082, conjecture,\n"
  "    ![X,G,Xp,Gp]: ((in_denotation(X, G, isPartOf)\n"
  "                    & align(X, Xp)\n"
  "                    & align(G, Gp))\n"
  "        => in_denotation(Xp, Gp, isPartOf))).",
  extra=ALIGN_PART_A_INLINE,
  inc=("GEO","ISO","ALIGN_DATA","ODRL"),  # NOTE: no ALIGN_THEORY
  pl="Lemma 3 derivability: denotation transfer from Part A alone")

# 083: Aligned compatible — verdict preservation (Prop 2.1)
#   isPartOf(europe) ∩ eq(germany) = {germany} ≠ ∅ in GEO
#   Maps to: isPartOf(europe) ∩ eq(dE) via alignment
#   Witness: dE (leq(dE, europe) in ISO3166 + dE = dE)
P("ODRL083-1.p","Theorem","Compatible",
  "Proposition 2(1) — Compatible Verdict Preservation","Medium",
  "Dataspace A (GEO): permission spatial isPartOf europe\n"
  "%   Dataspace B (ISO): prohibition spatial eq dE",
  "GEO: isPartOf(europe) ∩ eq(germany) → Compatible (witness: germany)\n"
  "%   ISO: isPartOf(europe) ∩ eq(dE) → Compatible (witness: dE)\n"
  "%   Alignment preserves compatible verdict.",
  "fof(odrl083, conjecture,\n"
  "    ?[X]: ( in_denotation(X, europe, isPartOf)\n"
  "          & in_denotation(X, dE, eq) )).",
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="Aligned compatible: isPartOf(europe) ∩ eq(dE) ≠ ∅")

# 084: Subsumption preservation (Corollary 1)
#   isPartOf(germany) ⊆ isPartOf(europe) in GEO
#   Maps to: isPartOf(dE) ⊆ isPartOf(europe) in ISO
#   Proof: leq(X, dE) → align_order_backward → leq(pre(X), germany) [if aligned]
#   BUT simpler: leq(dE, europe) is directly in ISO3166-0.ax
#   So leq(X, dE) → leq(X, europe) by transitivity.
P("ODRL084-1.p","Theorem","Confirmed",
  "Corollary 1 — Subsumption Preservation","Medium",
  "c1: [ odrl:operator odrl:isPartOf ; odrl:rightOperand iso:dE ] .\n"
  "%   c2: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .",
  "⟦isPartOf(dE)⟧ ⊆ ⟦isPartOf(europe)⟧ in ISO3166\n"
  "%   leq(dE, europe) [ISO3166] → transitivity → subsumption\n"
  "%   Tests Corollary 1: subsumption preserved under alignment.",
  "fof(odrl084, conjecture,\n"
  "    ![X]: ( in_denotation(X, dE, isPartOf)\n"
  "          => in_denotation(X, europe, isPartOf) )).",
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="Subsumption preservation: isPartOf(dE) ⊆ isPartOf(europe)")

# 085: Graceful degradation (Prop 2.2) — unmapped concept
#   westernEurope has no ISO 3166 counterpart.
#   isPartOf(westernEurope) ∩ eq(dE) = ? in merged namespace
#   dE is an ISO concept. leq(dE, westernEurope) is NOT derivable
#   because align_order_backward requires align(???, westernEurope)
#   which doesn't exist. So: CounterSatisfiable (prover can't
#   find witness; verdicts degrades toward Unknown).
P("ODRL085-1.p","CounterSatisfiable","Unknown",
  "Proposition 2(2) — Graceful Degradation","Hard",
  "Dataspace A (GEO): permission spatial isPartOf westernEurope\n"
  "%   Dataspace B (ISO): prohibition spatial eq dE",
  "westernEurope has NO ISO 3166 counterpart (unmapped).\n"
  "%   leq(dE, westernEurope) NOT derivable — align_order_backward needs\n"
  "%   align(???, westernEurope) which doesn't exist.\n"
  "%   Verdict degrades to Unknown (Prop 2.2): cannot prove or refute overlap.",
  "fof(odrl085, conjecture,\n"
  "    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
  "          & in_denotation(X, dE, eq) )).",
  # No good flip — both directions are unprovable (genuine Unknown)
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="Graceful degradation: unmapped concept → Unknown")

# 086: Cross-KB conflict via UNA — eq(dE) ∩ eq(fR) = ∅
#   dE ≠ fR from ISO3166 $distinct (or UNA)
#   eq(dE) = {dE}, eq(fR) = {fR}, dE ≠ fR → ∅ → Conflict
#   Tests: UNA propagation across loaded KBs.
P("ODRL086-1.p","CounterSatisfiable","Conflict",
  "Definition 5 — Cross-KB Conflict via UNA","Easy",
  "Dataspace A (GEO): permission spatial eq germany\n"
  "%   Dataspace B (ISO): prohibition spatial eq fR",
  "eq(dE) = {dE}, eq(fR) = {fR}, dE ≠ fR (ISO $distinct) → ∅ → Conflict\n"
  "%   Basic test: UNA between ISO 3166 constants enables conflict detection.",
  "fof(odrl086, conjecture,\n"
  "    ?[X]: ( in_denotation(X, dE, eq)\n"
  "          & in_denotation(X, fR, eq) )).",
  flip_conj=
  "fof(odrl086, conjecture,\n"
  "    ![X]: ~( in_denotation(X, dE, eq)\n"
  "           & in_denotation(X, fR, eq) )).",
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="Cross-KB conflict: eq(dE) ∩ eq(fR) = ∅ via UNA")

# 087: Aligned set-valued — isAnyOf({dE, fR}) compatible with isPartOf(europe)
#   dE ≤ europe and fR ≤ europe in ISO3166
#   Witness: dE (or fR)
P("ODRL087-1.p","Theorem","Compatible",
  "Definition 3 (isAnyOf), Proposition 2(1)","Medium",
  "Dataspace A (GEO): permission spatial isAnyOf (germany france)\n"
  "%   Dataspace B (ISO): prohibition spatial isPartOf europe\n"
  "%   Via alignment: isAnyOf({dE, fR}) tested against isPartOf(europe)",
  "⟦isAnyOf({dE,fR})⟧ = ↓dE ∪ ↓fR ⊆ ↓europe = ⟦isPartOf(europe)⟧\n"
  "%   Witness: dE ∈ ↓dE ∩ ↓europe.",
  "fof(odrl087, conjecture,\n"
  "    ?[X]: ( in_denotation_set(X, isoRegions087, isAnyOf)\n"
  "          & in_denotation(X, europe, isPartOf) )).",
  extra=(
      "fof(list_087_1, axiom, in_value_list(dE, isoRegions087)).\n"
      "fof(list_087_2, axiom, in_value_list(fR, isoRegions087)).\n" +
      generate_list_closure("isoRegions087", ["dE", "fR"])
  ),
  inc=("GEO","ISO","ALIGN_DATA","ODRL","ALIGN_THEORY"),
  pl="Aligned compatible: isAnyOf({dE, fR}) ∩ isPartOf(europe) ≠ ∅")


"""
PATCH for gen_spatial_suite.py — Category 8: Runtime Semantics (090-095)

Instructions:
1. Add these problems AFTER Category 7 (alignment) problems
2. Add "RUNTIME" to the INC map

Design: Runtime encoding (7 axioms in RUNTIME000-0.ax).
  assigns(Omega, X)       — context ω assigns concept X to the operand
  satisfies(Omega, G, Op) — ω satisfies constraint (_, Op, v) where γ(v)=G
  ungrounded(G)           — G has no KB grounding (⟦c⟧ = ⊤)

Parts A-C are strictly EPR. Part D (satisfies_needs_assignment)
introduces one existential, Skolemized to a unary function. Required
for Theorem 3 proofs over arbitrary contexts.

Multi-operand: separate context constants per operand (Assumption 2).
"""

# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 8: RUNTIME SEMANTICS (090-095)
# Paper §3.2.1 — Definition 9, 10, Theorem 3
#
# Predicates (from RUNTIME000-0.ax):
#   assigns(Omega, X)       — context assigns concept X
#   satisfies(Omega, G, Op) — context satisfies (_, Op, v) where γ(v)=G
#   ungrounded(G)           — G has no KB grounding
# ═══════════════════════════════════════════════════════════════════════════

# 090: Theorem 3 (forward) — static Conflict → no runtime witness
#   Static: isPartOf(wE) ∩ isPartOf(eE) = ∅ (Conflict, from ODRL013)
#   Runtime: ∀ω: ¬(satisfies(ω, wE, isPartOf) ∧ satisfies(ω, eE, isPartOf))
#   Proof (by refutation):
#     Negated conjecture: ∃Omega: satisfies(Ω, wE, isPartOf) ∧ satisfies(Ω, eE, isPartOf)
#     Skolemize: satisfies(ω_sk, wE, isPartOf) ∧ satisfies(ω_sk, eE, isPartOf)
#     Step 1: satisfies_needs_assignment → assigns(ω_sk, X) for some X
#     Step 2: satisfaction_to_denotation (concept(wE) ✓, concept(eE) ✓):
#             in_denotation(X, wE, isPartOf) ∧ in_denotation(X, eE, isPartOf)
#     Step 3: context_functional → same X for both
#     Step 4: den_isPartOf_onlyif → leq(X, wE) ∧ leq(X, eE)
#     Step 5: disj_downward(wE ⊥ eE) → disjoint(X, X)
#     Step 6: disj_irrefl → contradiction □
P("ODRL090-1.p","Theorem","Sound",
  "Theorem 3 — Runtime Soundness (Conflict → no context)","Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:westernEurope")])+"\n%\n%   "+
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:easternEurope")]),
  "Static: ⟦isPartOf(wE)⟧ ∩ ⟦isPartOf(eE)⟧ = ∅ (Conflict)\n"
  "%   6-step refutation proof:\n"
  "%     1. satisfies_needs_assignment → assigns(ω_sk, X)\n"
  "%     2. satisfaction_to_denotation → in_den(X, wE/eE, isPartOf)\n"
  "%     3. context_functional → same X for both\n"
  "%     4. den_isPartOf_onlyif → leq(X, wE) ∧ leq(X, eE)\n"
  "%     5. disj_downward(wE ⊥ eE) → disjoint(X, X)\n"
  "%     6. disj_irrefl → contradiction",
  "fof(odrl090, conjecture,\n"
  "    ![Omega]: ~( satisfies(Omega, westernEurope, isPartOf)\n"
  "              & satisfies(Omega, easternEurope, isPartOf) )).",
  inc=("GEO","ODRL","RUNTIME"),
  pl="Runtime soundness: Conflict → no ω satisfies both")

# 091: Runtime witness for Compatible verdict
#   Static: isPartOf(europe) ∩ eq(germany) = {germany} ≠ ∅ (Compatible)
#   Runtime: Construct ω with assigns(ω, germany).
#   Prove: satisfies(ω, europe, isPartOf) ∧ satisfies(ω, germany, eq)
#   Proof:
#     assigns(omega091, germany) [given]
#     → leq(germany, europe) [leq_trans via westernEurope]
#     → in_denotation(germany, europe, isPartOf) [den_isPartOf_if]
#     → satisfies(omega091, europe, isPartOf) [denotation_to_satisfaction]
#     germany = germany → in_denotation(germany, germany, eq) [den_eq_if]
#     → satisfies(omega091, germany, eq) [denotation_to_satisfaction] □
P("ODRL091-1.p","Theorem","Sound",
  "Definition 10 — Runtime Witness for Compatible Verdict","Medium",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:europe")])+"\n%\n%   "+
  tp("policyB","prohibition","use",[("spatial","eq","geo:germany")]),
  "Static: Compatible (witness: germany ∈ both denotations).\n"
  "%   Runtime: assigns(ω, germany) → denotation_to_satisfaction\n"
  "%   → satisfies(ω, europe, isPartOf) ∧ satisfies(ω, germany, eq).",
  "fof(runtime_context_091, axiom, assigns(omega091, germany)).\n"
  "\n"
  "fof(odrl091, conjecture,\n"
  "    ( satisfies(omega091, europe, isPartOf)\n"
  "    & satisfies(omega091, germany, eq) )).",
  inc=("GEO","ODRL","RUNTIME"),
  pl="Runtime witness: Compatible verdict → satisfying context")

# 092: Theorem 3 (contrapositive) — runtime witness → ¬Conflict
#   If we construct a context satisfying both constraints,
#   then the static verdict cannot be Conflict.
#   Approach: assert assigns(ω, france), then prove static overlap.
#   Proof:
#     assigns(omega092, france) [given]
#     → leq(france, westernEurope) [from GEO KB]
#     → in_denotation(france, westernEurope, isPartOf) [den_isPartOf_if]
#     france ≠ germany [UNA in GEO KB]
#     → in_denotation(france, germany, neq) [den_neq_if]
#     → ∃X: in_denotation(X, wE, isPartOf) ∧ in_denotation(X, de, neq) □
P("ODRL092-1.p","Theorem","Sound",
  "Theorem 3 (contrapositive) — Runtime Witness → Static Compatible","Medium",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:westernEurope")])+"\n%\n%   "+
  tp("policyB","prohibition","use",[("spatial","neq","geo:germany")]),
  "Contrapositive of Theorem 3: ∃ω:(ω ⊨ c1 ∧ ω ⊨ c2) → verdict ≠ Conflict.\n"
  "%   Runtime witness: assigns(ω, france).\n"
  "%   france ∈ ⟦isPartOf(wE)⟧ ∧ france ∈ ⟦neq(de)⟧ → static overlap.",
  "fof(runtime_context_092, axiom, assigns(omega092, france)).\n"
  "\n"
  "fof(odrl092, conjecture,\n"
  "    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
  "          & in_denotation(X, germany, neq) )).",
  inc=("GEO","ODRL","RUNTIME"),
  pl="Contrapositive: runtime witness → verdict ≠ Conflict")

# 093: Permissive satisfaction for ungrounded constraint (⊤ case)
#   Def. 10: "When ⟦c⟧ = ⊤, any grounded context value satisfies
#   conservatively."
#   Setup: assigns(ω, germany) — grounded context
#          ungrounded(unknownConcept) — constraint value not in KB
#   Prove: satisfies(ω, unknownConcept, isPartOf)
#   Proof:
#     assigns(omega093, germany) ∧ ungrounded(unknownConcept)
#     → permissive_satisfaction → satisfies(omega093, unknownConcept, isPartOf) □
#   Backward bridge blocked: concept(unknownConcept) fails → no in_denotation.
P("ODRL093-1.p","Theorem","Permissive",
  "Definition 10 (⊤ case) — Permissive Satisfaction","Easy",
  tp("policyA","permission","use",[("spatial","isPartOf","<unknownConcept>")])+"\n%\n%   "+
  "ω(spatial) = germany (grounded), constraint value = unknownConcept (ungrounded)",
  "Def. 10 disjunction case 1: ⟦c⟧ = ⊤ → any grounded context satisfies.\n"
  "%   permissive_satisfaction: assigns(ω, germany) ∧ ungrounded(unknownConcept)\n"
  "%   → satisfies(ω, unknownConcept, isPartOf).\n"
  "%   Backward bridge blocked: concept(unknownConcept) fails → no in_denotation.\n"
  "%   NOTE: Enforcement policies may override with default-deny.",
  "fof(runtime_context_093, axiom, assigns(omega093, germany)).\n"
  "fof(unknown_ungrounded, axiom, ungrounded(unknownConcept)).\n"
  "\n"
  "fof(odrl093, conjecture,\n"
  "    satisfies(omega093, unknownConcept, isPartOf)).",
  inc=("GEO","ODRL","RUNTIME"),
  pl="Permissive ⊤: ungrounded constraint → satisfy by default")

# 094: Multi-operand runtime (Def 6 + Theorem 3)
#   AND composition: ω must satisfy ALL operand constraints.
#   Uses per-operand context constants (Assumption 2: operand independence):
#     omega094s — assigns germany to spatial
#     omega094p — assigns academicResearch to purpose
P("ODRL094-1.p","Theorem","Sound",
  "Theorem 2 + 3 — Multi-Operand Runtime Soundness","Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:europe"),("hasPurpose","isA","dpv:ResearchAndDevelopment")])+"\n%\n%   "+
  tp("policyB","prohibition","use",[("spatial","eq","geo:germany"),("hasPurpose","isA","dpv:AcademicResearch")]),
  "AND composition: V_spatial=Compatible, V_purpose=Compatible.\n"
  "%   Per-operand context constants (Assumption 2: operand independence):\n"
  "%     omega094s ↦ germany (spatial), omega094p ↦ academicResearch (purpose).",
  "% Per-operand contexts (Assumption 2: operand independence)\n"
  "fof(ctx_spatial, axiom, assigns(omega094s, germany)).\n"
  "fof(ctx_purpose, axiom, assigns(omega094p, academicResearch)).\n"
  "\n"
  "fof(odrl094, conjecture,\n"
  "    ( satisfies(omega094s, europe, isPartOf)\n"
  "    & satisfies(omega094s, germany, eq)\n"
  "    & satisfies(omega094p, researchAndDevelopment, isA)\n"
  "    & satisfies(omega094p, academicResearch, isA) )).",
  inc=("GEO","DPV","ODRL","RUNTIME"),
  pl="Multi-operand: AND composition at runtime")

# 095: Conflict propagation at runtime (Lemma 2 + Theorem 3)
#   Static: isPartOf(germany) ⊆ isPartOf(westernEurope) (subsumption)
#           isPartOf(westernEurope) ∩ isPartOf(easternEurope) = ∅ (conflict)
#           → by Lemma 2: isPartOf(germany) ∩ isPartOf(easternEurope) = ∅
#   Runtime: ∀ω: ¬(satisfies(ω, germany, isPartOf) ∧ satisfies(ω, eE, isPartOf))
#   Proof: Same 6-step structure as ODRL090, but with extra leq_trans step.
#     Step 4 becomes: leq(X, germany) → leq(X, wE) [leq_trans] ∧ leq(X, eE)
P("ODRL095-1.p","Theorem","Sound",
  "Lemma 2 + Theorem 3 — Runtime Conflict Propagation","Very Hard",
  tp("policyA","permission","use",[("spatial","isPartOf","geo:germany")])+"\n%\n%   "+
  tp("policyB","prohibition","use",[("spatial","isPartOf","geo:easternEurope")]),
  "Lemma 2: isPartOf(de) ⊑ isPartOf(wE) ∧ conflict(wE,eE) → conflict(de,eE).\n"
  "%   Theorem 3: conflict(de,eE) → ¬∃ω: (ω ⊨ isPartOf(de) ∧ ω ⊨ isPartOf(eE)).\n"
  "%   7-step proof (ODRL090 + one leq_trans step):\n"
  "%     1. satisfies_needs_assignment → assigns(ω_sk, X)\n"
  "%     2. satisfaction_to_denotation → in_den(X, de/eE, isPartOf)\n"
  "%     3. context_functional → same X\n"
  "%     4. den_onlyif → leq(X, de) ∧ leq(X, eE)\n"
  "%     5. leq_trans: leq(X, de) ∧ leq(de, wE) → leq(X, wE)\n"
  "%     6. disj_downward(wE ⊥ eE) → disjoint(X, X)\n"
  "%     7. disj_irrefl → contradiction",
  "fof(odrl095, conjecture,\n"
  "    ![Omega]: ~( satisfies(Omega, germany, isPartOf)\n"
  "              & satisfies(Omega, easternEurope, isPartOf) )).",
  inc=("GEO","ODRL","RUNTIME"),
  pl="Runtime propagation: subsumption + conflict → no ω")


# ═══════════════════════════════════════════════════════════════════════════
# INC MAP:
# ═══════════════════════════════════════════════════════════════════════════
INC = {
    "GEO":          "include('Axioms/Layer0-DomainKB/GEO000-0.ax').",
    "DPV":          "include('Axioms/Layer0-DomainKB/DPV000-0.ax').",
    "LANG":         "include('Axioms/Layer0-DomainKB/LANG000-0.ax').",
    "ODRL":         "include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').",
    "ISO":          "include('Axioms/Layer0-DomainKB/ISO3166-0.ax').",
    "ALIGN_DATA":   "include('Axioms/Alignment/ALIGN-GEO-ISO.ax').",
    "ALIGN_THEORY": "include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').",
    "RUNTIME":      "include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').",
}

# ═══════════════════════════════════════════════════════════════════════════
# GENERATE
# ═══════════════════════════════════════════════════════════════════════════
def generate(args):
    OUT = args.output
    os.makedirs(OUT, exist_ok=True)
    use_flip = (args.encoding == "prover")
    written = []

    for p in PROBLEMS:
        if use_flip and p["flip_conj"]:
            conj = p["flip_conj"]
            expected = "Theorem"
            enc_note = "% Encoding : prover-friendly (flipped for refutation provers)\n"
        else:
            conj = p["conj"]
            expected = p["exp"]
            enc_note = ""

        includes = "\n".join(INC[i] for i in p["inc"])
        extra = "\n" + p["extra"] + "\n" if p["extra"] else ""

        content = (
            f"%--------------------------------------------------------------------------\n"
            f"% File     : {p['fn']} : TPTP v0.1.0\n"
            f"% Domain   : ODRL Policy Conflict Detection\n"
            f"% Problem  : {p.get('pl') or p['vrd']}\n"
            f"% Expected : {expected}\n"
            f"% Verdict  : {p['vrd']}\n"
            f"% Paper    : {p['paper']}\n"
            f"{enc_note}"
            f"%\n"
            f"% ODRL Policy (Turtle):\n"
            f"%   {p['ttl']}\n"
            f"%\n"
            f"% Denotation analysis:\n"
            f"%   {p['den']}\n"
            f"%\n"
            f"% Difficulty: {p['diff']}\n"
            f"% Authors  : Mustafa, D. & Sutcliffe, G.\n"
            f"%--------------------------------------------------------------------------\n"
            f"{includes}\n"
            f"{extra}\n"
            f"{conj}\n"
            f"%--------------------------------------------------------------------------\n"
        )
        path = os.path.join(OUT, p["fn"])
        if args.dry_run:
            print(f"  [dry-run] {p['fn']}")
        else:
            with open(path, 'w') as f:
                f.write(content)
            written.append(path)
            print(f"  ✓ {p['fn']}")

    n = len(written) if not args.dry_run else len(PROBLEMS)
    enc_label = "prover (all Theorem)" if use_flip else "original (mixed)"
    print(f"\n{'='*60}")
    print(f"Generated {n} problems [{enc_label}] → {os.path.abspath(OUT)}")
    print(f"{'='*60}")
    return written

# ═══════════════════════════════════════════════════════════════════════════
# RUN PROVER
# ═══════════════════════════════════════════════════════════════════════════
def run_prover(args, paths):
    prover = args.prover
    timeout = args.timeout
    inc_path = args.include
    results = []
    counts = {"pass": 0, "fail": 0, "timeout": 0}

    GREEN, RED, YELLOW, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[0m"

    print(f"\n{'='*60}")
    print(f"Running {prover} (timeout={timeout}s, include={inc_path})")
    print(f"{'='*60}\n")

    for path in sorted(paths):
        fn = os.path.basename(path)
        with open(path) as f:
            text = f.read()
        m = re.search(r'^% Expected\s*:\s*(\w+)', text, re.MULTILINE)
        expected = m.group(1) if m else "?"
        m2 = re.search(r'^% Verdict\s*:\s*(\w+)', text, re.MULTILINE)
        verdict = m2.group(1) if m2 else "?"

        if prover == "vampire":
            cmd = ["vampire", "--include", inc_path,
                   "--time_limit", str(timeout), "--mode", "casc", path]
        else:
            cmd = ["eprover", f"--include={inc_path}",
                   f"--cpu-limit={timeout}", "--auto", path]

        t0 = time.time()
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=timeout + 10)
            output = proc.stdout + proc.stderr
        except subprocess.TimeoutExpired:
            output = ""
        elapsed = time.time() - t0

        m = re.search(r'SZS status (\w+)', output)
        actual = m.group(1) if m else "Timeout"

        if actual == expected:
            sym, col = "✓", GREEN; counts["pass"] += 1
        elif actual == "Timeout":
            sym, col = "⏱", YELLOW; counts["timeout"] += 1
        else:
            sym, col = "✗", RED; counts["fail"] += 1

        print(f"  {col}{sym}{RESET} {fn:<18} exp={expected:<20} got={actual:<20} "
              f"vrd={verdict:<12} {elapsed:.1f}s")
        results.append(dict(problem=fn, expected_szs=expected, actual_szs=actual,
                            verdict=verdict, time_s=f"{elapsed:.3f}",
                            passed=(actual == expected)))

    total = len(results)
    print(f"\n{'='*60}")
    print(f"  {GREEN}✓ {counts['pass']}{RESET} pass  "
          f"{RED}✗ {counts['fail']}{RESET} fail  "
          f"{YELLOW}⏱ {counts['timeout']}{RESET} timeout  "
          f"(total: {total})")
    print(f"{'='*60}")

    os.makedirs("results", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = f"results/benchmark_{args.encoding}_{ts}.csv"
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    print(f"CSV → {csv_path}")
    return results

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(
        description="Generate & run ODRL TPTP spatial benchmark.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -o Problems/ODRL/KBGrounding/Spatial
  %(prog)s -o Problems/ODRL/KBGrounding/Spatial --encoding prover --run
  %(prog)s -o Problems/ODRL/KBGrounding/Spatial --run --timeout 30
  %(prog)s --encoding original --run --prover eprover
""")
    ap.add_argument("-o", "--output", default="Problems/ODRL/KBGrounding/Spatial")
    ap.add_argument("--encoding", choices=["original","prover"], default="prover",
        help="original=mixed Theorem/CSA; prover=all Theorem (default: prover)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--run", action="store_true", help="Run prover after generating")
    ap.add_argument("--timeout", type=int, default=60, help="Prover timeout (s)")
    ap.add_argument("--prover", choices=["vampire","eprover"], default="vampire")
    ap.add_argument("--include", default="Problems/ODRL", help="TPTP include path")
    args = ap.parse_args()

    paths = generate(args)
    if args.run and not args.dry_run:
        run_prover(args, paths)

if __name__ == "__main__":
    main()