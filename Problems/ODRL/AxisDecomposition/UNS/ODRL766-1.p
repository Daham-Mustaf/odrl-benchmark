%--------------------------------------------------------------------------
% File     : ODRL766-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : intra-policy: eq 600 AND eq 800 on same axis empty
% Version  : 1.0
% English  : Remark 3.4: single constraint eq 600 AND eq 800 on width.
%           : {600} ∩ {800} = ∅ — self-contradictory.
%           : Contradiction via fresh witness w=v600 and w=v800:
%           : by transitivity v600=v800, contradicting $distinct(v600,v800).
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL766-1.p
%
% Status   : Unsatisfiable
% Verdict  : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL766-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v600, v800)).
fof(wit_eq1, axiom, w = v600).
fof(wit_eq2, axiom, w = v800).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl766, conjecture,
    None).
%--------------------------------------------------------------------------
