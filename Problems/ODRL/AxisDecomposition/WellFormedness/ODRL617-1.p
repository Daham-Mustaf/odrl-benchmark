%--------------------------------------------------------------------------
% File     : ODRL617-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : nonempty: wf(lt) implies sem_nonempty(lt)
% Version  : 1.0
% English  : lem:totality: wf(lt,V,InfD,SupD) => sem_nonempty(lt,V,InfD,SupD)
%           : Every well-formed constraint has a non-empty denotation.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL617-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL617-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/WF000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl617, conjecture,
    wf(lt, v600, v0, v1200) => sem_nonempty(lt, v600, v0, v1200)).
%--------------------------------------------------------------------------
