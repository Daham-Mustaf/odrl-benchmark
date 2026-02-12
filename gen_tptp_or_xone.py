#!/usr/bin/env python3
"""Generate TPTP files for OR (080-084) and XONE (085-088) benchmarks."""

import os

OUTDIR = "/Users/dahammhamad/Desktop/tptp-odrl/Problems/ODRL/KBGrounding"

def header(pid, desc, status, scenario):
    return f"""%--------------------------------------------------------------------------
% File     : {pid}.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : {desc}
% Status   : {status}
%
{scenario}
%--------------------------------------------------------------------------
"""

def includes(*kbs):
    lines = []
    for kb in kbs:
        lines.append(f"include('Axioms/Layer0-DomainKB/{kb}').")
    lines.append("include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').")
    lines.append("include('Axioms/Layer2-Grounding/GROUND000-1.ax').")
    return "\n".join(lines)

def con(name, label, operand, operator, value):
    return f"fof({name}_{label}, axiom, has_operand({name}, {operand}) & has_operator({name}, {operator}) & has_value({name}, {value}))."

problems = []

# ===========================================================================
# OR (080-084)
# ===========================================================================

# ODRL080-1: or(isA de, isA ar) vs eq arz → arz ⊑ ar → Compatible
problems.append(("LogicalOr", "ODRL080-1", "Theorem", 
    "OR compatible: second branch (ar) covers arz",
"""% or(isA de, isA ar) vs eq arz
%   Branch 1: ⟦isA de⟧ ∩ ⟦eq arz⟧ = ∅ (arz ⊄ de)
%   Branch 2: ⟦isA ar⟧ ∩ ⟦eq arz⟧ = {arz} (arz ⊑ ar) ✓
%   or: at least one branch → Compatible""",
    ["LNG000-0.ax"],
    [con("c1","def","language","isA","de"),
     con("c2","def","language","isA","ar"),
     con("c3","def","language","eq","arz")],
    "fof(or_compatible, conjecture,\n"
    "    (?[X]: (in_denotation(X, c1) & in_denotation(X, c3)))\n"
    "  | (?[Y]: (in_denotation(Y, c2) & in_denotation(Y, c3))))."
))

# ODRL081-1: or(isA de, isA en) vs eq fr → Conflict (neither branch)
problems.append(("LogicalOr", "ODRL081-1", "Theorem",
    "OR conflict: neither branch covers fr",
"""% or(isA de, isA en) vs eq fr
%   Branch 1: ⟦isA de⟧ ∩ ⟦eq fr⟧ = ∅ (fr ⊄ de)
%   Branch 2: ⟦isA en⟧ ∩ ⟦eq fr⟧ = ∅ (fr ⊄ en)
%   or: both branches empty → Conflict""",
    ["LNG000-0.ax"],
    [con("c1","def","language","isA","de"),
     con("c2","def","language","isA","en"),
     con("c3","def","language","eq","fr")],
    "fof(or_conflict, conjecture,\n"
    "    ~((?[X]: (in_denotation(X, c1) & in_denotation(X, c3)))\n"
    "    | (?[Y]: (in_denotation(Y, c2) & in_denotation(Y, c3)))))."
))

# ODRL082-1: or(isA nonComm, isA marketing) vs eq sciRes → Unknown
problems.append(("LogicalOr", "ODRL082-1", "CounterSatisfiable",
    "OR Unknown: both branches indeterminate",
"""% or(isA nonCommercialPurpose, isA marketing) vs eq scientificResearch
%   Branch 1: sciRes ⊑? nonComm → Unknown (KB gap)
%   Branch 2: sciRes ⊑? marketing → Unknown (KB gap)
%   or: both indeterminate → Unknown""",
    ["DPV000-0.ax"],
    [con("c1","def","purpose","isA","nonCommercialPurpose"),
     con("c2","def","purpose","isA","marketing"),
     con("c3","def","purpose","eq","scientificResearch")],
    "fof(or_compatible, conjecture,\n"
    "    (?[X]: (in_denotation(X, c1) & in_denotation(X, c3)))\n"
    "  | (?[Y]: (in_denotation(Y, c2) & in_denotation(Y, c3))))."
))

# ODRL083-1: spatial AND or(purpose₁, purpose₂) — both work
problems.append(("LogicalOr", "ODRL083-1", "Theorem",
    "Cross-DS AND-OR: spatial compatible AND or(purpose) compatible",
"""% spatial: isPartOf europe vs eq france → Compatible (france ⊑ europe)
% or(isA nonCommPurpose, isA R&D) vs eq academicResearch
%   Branch 2: acadRes ⊑ R&D → Compatible
% Conjunction: spatial ∧ or(purpose) → Compatible""",
    ["GEO000-0.ax", "DPV000-0.ax"],
    [con("c_s1","def","spatial","isPartOf","europe"),
     con("c_s2","def","spatial","eq","france"),
     con("c_p1","def","purpose","isA","nonCommercialPurpose"),
     con("c_p2","def","purpose","isA","researchAndDevelopment"),
     con("c_p3","def","purpose","eq","academicResearch")],
    "fof(and_or_compatible, conjecture,\n"
    "    (?[X]: (in_denotation(X, c_s1) & in_denotation(X, c_s2)))\n"
    "  & ((?[Y]: (in_denotation(Y, c_p1) & in_denotation(Y, c_p3)))\n"
    "   | (?[Z]: (in_denotation(Z, c_p2) & in_denotation(Z, c_p3)))))."
))

# ODRL084-1: spatial AND or(purpose) — spatial ok, or(purpose) unknown
problems.append(("LogicalOr", "ODRL084-1", "CounterSatisfiable",
    "Cross-DS AND-OR blocked: or(purpose) indeterminate",
"""% spatial: isPartOf europe vs eq france → Compatible
% or(isA nonCommPurpose, isA marketing) vs eq scientificResearch
%   Both branches indeterminate → Unknown
% Conjunction blocked by purpose Unknown""",
    ["GEO000-0.ax", "DPV000-0.ax"],
    [con("c_s1","def","spatial","isPartOf","europe"),
     con("c_s2","def","spatial","eq","france"),
     con("c_p1","def","purpose","isA","nonCommercialPurpose"),
     con("c_p2","def","purpose","isA","marketing"),
     con("c_p3","def","purpose","eq","scientificResearch")],
    "fof(and_or_compatible, conjecture,\n"
    "    (?[X]: (in_denotation(X, c_s1) & in_denotation(X, c_s2)))\n"
    "  & ((?[Y]: (in_denotation(Y, c_p1) & in_denotation(Y, c_p3)))\n"
    "   | (?[Z]: (in_denotation(Z, c_p2) & in_denotation(Z, c_p3)))))."
))

# ===========================================================================
# XONE (085-088)
# ===========================================================================

# ODRL085-1: xone(comm, nonComm) vs nonCommRes → exactly one branch → Compatible
problems.append(("LogicalXone", "ODRL085-1", "Theorem",
    "XONE compatible: exactly one branch (nonComm) holds",
"""% xone(isA commercialPurpose, isA nonCommercialPurpose) vs eq nonCommRes
%   nonCommRes ⊑ nonCommPurpose ✓ (branch 2)
%   nonCommRes ⊄ commercialPurpose ✓ (explicit in KB)
%   Exactly one branch holds → Compatible""",
    ["DPV000-0.ax"],
    [con("c1","def","purpose","isA","commercialPurpose"),
     con("c2","def","purpose","isA","nonCommercialPurpose"),
     con("c3","def","purpose","eq","nonCommercialResearch")],
    "fof(xone_compatible, conjecture,\n"
    "    (?[X]: (in_denotation(X, c1) & ~in_denotation(X, c2) & in_denotation(X, c3)))\n"
    "  | (?[Y]: (in_denotation(Y, c2) & ~in_denotation(Y, c1) & in_denotation(Y, c3))))."
))

# ODRL086-1: xone(comm, nonComm) vs commRes → Unknown (missing disjointness)
problems.append(("LogicalXone", "ODRL086-1", "CounterSatisfiable",
    "XONE Unknown: missing explicit disjointness for commRes",
"""% xone(isA commercialPurpose, isA nonCommercialPurpose) vs eq commRes
%   commRes ⊑ commercialPurpose ✓ (branch 1)
%   commRes ⊄ nonCommPurpose? NOT explicit in KB!
%   Open world: commRes COULD be under both → can't confirm exclusivity
%   → Unknown
%
%   Contrast with ODRL085: nonCommRes HAS explicit ¬⊑ commercialPurpose.
%   Insight: xone requires explicit disjointness axioms.""",
    ["DPV000-0.ax"],
    [con("c1","def","purpose","isA","commercialPurpose"),
     con("c2","def","purpose","isA","nonCommercialPurpose"),
     con("c3","def","purpose","eq","commercialResearch")],
    "fof(xone_compatible, conjecture,\n"
    "    (?[X]: (in_denotation(X, c1) & ~in_denotation(X, c2) & in_denotation(X, c3)))\n"
    "  | (?[Y]: (in_denotation(Y, c2) & ~in_denotation(Y, c1) & in_denotation(Y, c3))))."
))

# ODRL087-1: xone(R&D, nonComm) vs nonCommRes → both branches → Unknown
problems.append(("LogicalXone", "ODRL087-1", "CounterSatisfiable",
    "XONE both-in: nonCommRes satisfies both branches",
"""% xone(isA researchAndDevelopment, isA nonCommercialPurpose) vs eq nonCommRes
%   nonCommRes ⊑ R&D ✓ (branch 1)
%   nonCommRes ⊑ nonCommPurpose ✓ (branch 2)
%   BOTH branches hold → violates exclusive-or
%   Open world: maybe other values satisfy exactly one? → Unknown""",
    ["DPV000-0.ax"],
    [con("c1","def","purpose","isA","researchAndDevelopment"),
     con("c2","def","purpose","isA","nonCommercialPurpose"),
     con("c3","def","purpose","eq","nonCommercialResearch")],
    "fof(xone_compatible, conjecture,\n"
    "    (?[X]: (in_denotation(X, c1) & ~in_denotation(X, c2) & in_denotation(X, c3)))\n"
    "  | (?[Y]: (in_denotation(Y, c2) & ~in_denotation(Y, c1) & in_denotation(Y, c3))))."
))

# ODRL088-1: xone(isA de, isA en) vs eq fr → neither branch → Conflict
problems.append(("LogicalXone", "ODRL088-1", "Theorem",
    "XONE conflict: neither branch holds (fr ⊄ de, fr ⊄ en)",
"""% xone(isA de, isA en) vs eq fr
%   fr ⊄ de → branch 1 fails
%   fr ⊄ en → branch 2 fails
%   Neither branch holds → Conflict""",
    ["LNG000-0.ax"],
    [con("c1","def","language","isA","de"),
     con("c2","def","language","isA","en"),
     con("c3","def","language","eq","fr")],
    "fof(xone_conflict, conjecture,\n"
    "    ~((?[X]: (in_denotation(X, c1) & ~in_denotation(X, c2) & in_denotation(X, c3)))\n"
    "    | (?[Y]: (in_denotation(Y, c2) & ~in_denotation(Y, c1) & in_denotation(Y, c3)))))."
))

# ===========================================================================
# Write files
# ===========================================================================
for subdir, pid, status, desc, scenario, kbs, constraints, conjecture in problems:
    d = os.path.join(OUTDIR, subdir)
    os.makedirs(d, exist_ok=True)
    
    h = header(pid, desc, status, scenario)
    inc = includes(*kbs)
    cons = "\n".join(constraints)
    
    content = f"{h}\n{inc}\n\n{cons}\n\n{conjecture}\n%--------------------------------------------------------------------------\n"
    
    path = os.path.join(d, f"{pid}.p")
    with open(path, "w") as f:
        f.write(content)
    print(f"  {pid}.p -> {status}")

print(f"\nGenerated {len(problems)} TPTP files in {OUTDIR}/")
