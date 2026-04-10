%--------------------------------------------------------------------------
% File     : ODRL635-1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : unknown_sound: box verdict is Unknown when axis unconstrained
% Version  : 1.0
% English  : thm:unknown-sound: box_verdict(compatible, unknown) = unknown.
%           : One axis compatible, one axis unconstrained => Unknown overall.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : ODRL635-1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Axis decomposition tier. arXiv:2602.19878.
%           : Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.
%           : Policy source: Policies/ODRL635-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/COMPL000-0.ax').
include('Axioms/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
% ─── Conjecture ────────────────────────────────────────────────────
fof(odrl635, conjecture,
    box_verdict(compatible, unknown) = unknown).
%--------------------------------------------------------------------------
