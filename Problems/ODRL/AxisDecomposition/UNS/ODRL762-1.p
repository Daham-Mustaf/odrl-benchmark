%--------------------------------------------------------------------------
% File     : ODRL762-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : intra-policy: wf(lt) with V=InfD violates condition (ii) — empty denotation
% Version  : 1.0
% English  : Remark 3.4 intra-policy self-contradiction via WF000 wf_lt condition (ii).
%           : def:profile condition (ii): Op=lt ⇒ V ≠ InfD.
%           : Policy asserts wf(lt, v0, v0, v1200) where V = InfD = v0. By the wf_lt
%           : equivalence in WF000, this forces v0 ≠ v0 — a direct contradiction with
%           : equality reflexivity. The proof genuinely exercises WF000 rather than
%           : reducing to ORD irreflexivity.
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL762-1.p
%
% Status   : Unsatisfiable
% Verdict  : Unsatisfiable
% SPC      : FOF_UNS_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL762-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/WF000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(distinct, axiom, $distinct(v0, v1200)).
fof(policy_assertion, axiom, wf(lt, v0, v0, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl762, conjecture,
    None).
%--------------------------------------------------------------------------
