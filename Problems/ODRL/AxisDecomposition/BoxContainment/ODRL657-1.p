%--------------------------------------------------------------------------
% File     : ODRL657-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : 4-axis box: absent width axis propagates Unknown
% Version  : 1.0
% English  : Width:  C1 absent -> subs_verdict = unknown
%           : Height: (0,400] subseteq (0,800]  Compatible
%           : Depth:  (0,16]  subseteq (0,32]   Compatible
%           : Alt:    (0,150] subseteq (0,300]  Compatible
%           : box_subs(box_subs(box_subs(unknown,C),C),C) = unknown
%
% Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL657-1.p
%
% Status   : Theorem
% Verdict  : Unknown
% Relation : verdict_algebra
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. ISWC 2026.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL657-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/SUBS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,   axiom, val(v0)).
fof(val_v16,  axiom, val(v16)).
fof(val_v32,  axiom, val(v32)).
fof(val_v150, axiom, val(v150)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v16,    axiom, less(v0,   v16)).
fof(ord_v0_v32,    axiom, less(v0,   v32)).
fof(ord_v0_v150,   axiom, less(v0,   v150)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v16_v32,   axiom, less(v16,  v32)).
fof(ord_v16_v150,  axiom, less(v16,  v150)).
fof(ord_v16_v300,  axiom, less(v16,  v300)).
fof(ord_v16_v400,  axiom, less(v16,  v400)).
fof(ord_v16_v800,  axiom, less(v16,  v800)).
fof(ord_v32_v150,  axiom, less(v32,  v150)).
fof(ord_v32_v300,  axiom, less(v32,  v300)).
fof(ord_v32_v400,  axiom, less(v32,  v400)).
fof(ord_v32_v800,  axiom, less(v32,  v800)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v400, axiom, less(v150, v400)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v16, v32, v150, v300, v400, v800)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl657, conjecture,
    box_subs(
    box_subs(
      box_subs(
        subs_verdict(v0,v800,absent,v0,v800,present),
        subs_verdict(v0,v400,present,v0,v800,present)),
      subs_verdict(v0,v16,present,v0,v32,present)),
    subs_verdict(v0,v150,present,v0,v300,present))
  = unknown).
%--------------------------------------------------------------------------
