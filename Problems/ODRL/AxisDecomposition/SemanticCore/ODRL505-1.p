%--------------------------------------------------------------------------
% File     : ODRL505-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : lem:normalisation — same-axis lteq intersection reduces to tighter bound
% Expected : Theorem
% Verdict  : Compatible
% Category : SemanticCore
% Tests    : lem:normalisation, def:box-denotation
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-04-05
% Gen      : gen_semantic_core.py
%--------------------------------------------------------------------------
include('Axioms/AXIS000-0.ax').
% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v400, v600)).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl505, conjecture,
    ?[X]: (in_lopen(X, v0, v400) & in_lopen(X, v0, v600))).
%--------------------------------------------------------------------------
