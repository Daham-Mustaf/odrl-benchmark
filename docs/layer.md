Now I recall the full picture. You have two DPV KB variants:

DPV000-0.ax — with 279 sibling disjointness pairs (multi-inheritance safe) — the "golden" KB
DPV000-full.ax — full hierarchy, 0 disjointness assertions — a "flat" variant

The next step in the PAAR 2026 pipeline is to generate TPTP benchmark problem files — these combine:

Layer 0 (DPV000-0.ax or DPV000-full.ax) — the domain KB
Layer 1 (ODRL000-0.ax) — generic axioms you already have (leq_refl, leq_trans, disj_sym, disj_downward, disj_irrefl, disj_implies_not_leq — 31 axioms)
Layer 2 — ODRL denotation semantics (den/2, sat/2, policy conflict definitions)
Conjecture — the specific query (e.g., "do policy P1 and P2 conflict?")