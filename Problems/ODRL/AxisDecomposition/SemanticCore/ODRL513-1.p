%--------------------------------------------------------------------------
% File     : ODRL513-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : def:profile well-formedness (iii) — gt at effective upper bound yields empty denotation
% Expected : Theorem
% Verdict  : Conflict
% Category : SemanticCore
% Tests    : def:profile condition (iii), lem:totality violation
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-04-05
% Gen      : gen_semantic_core.py
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl513, conjecture,
    ~?[X]: (less(v600, X) & in_lopen(X, v0, v600))).
%--------------------------------------------------------------------------
