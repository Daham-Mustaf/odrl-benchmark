"""
write_hard_sat.py

Writes SAT companion problems for the Hard tier.
Run from ~/Desktop/tptp-odrl:
    python3 write_hard_sat.py
"""
from pathlib import Path

SEP = "%--------------------------------------------------------------------------\n"

def write(path, content):
    Path(path).write_text(content, encoding="utf-8")
    print(f"Written: {path}")

base = "Problems/ODRL/AxisDecomposition/Hard"

# ── HARD001-SAT+1.p ────────────────────────────────────────────────────────
write(f"{base}/HARD001-SAT+1.p", SEP + """\
% File     : HARD001-SAT+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Hypothesis set of HARD001 is self-consistent (SAT companion)
% Version  : 1.0
% English  : The ordering chain n0<n3<n5<n10<n20 with universal domain bounds
%           : is satisfiable — the hypotheses of HARD001 do not self-contradict.
%           : This is the SAT companion of HARD001+1.p (THM).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : HARD001-SAT+1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : SAT companion for HARD001+1.p. No conjecture — a model finder
%           : (Mace4, Paradox, Vampire-FMB) should return a finite model
%           : establishing satisfiability of the hypothesis set.
%           : Policy source: Policies/HARD001-policy.ttl
""" + SEP + """
include('Axioms/ORD000-0.ax').
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/COMPL000-0.ax').

% Ordering chain: n0 < n3 < n5 < n10 < n20
fof(h_0_3,   axiom, less(n0,n3)).
fof(h_3_5,   axiom, less(n3,n5)).
fof(h_5_10,  axiom, less(n5,n10)).
fof(h_10_20, axiom, less(n10,n20)).

% Domain bounds (sentinel infimum/supremum used by HARD001)
fof(h_inf_lb, axiom, ![X]: leq(ninf,X)).
fof(h_sup_ub, axiom, ![X]: leq(X,nsup)).

% 7 distinct domain elements needed: n0, n3, n5, n10, n20, ninf, nsup
fof(distinct, axiom, $distinct(ninf, n0, n3, n5, n10, n20, nsup)).
""")

# ── NFV001-SAT+1.p ────────────────────────────────────────────────────────
write(f"{base}/NFV001-SAT+1.p", SEP + """\
% File     : NFV001-SAT+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : axis_conflict hypothesis set is self-consistent (SAT companion)
% Version  : 1.0
% English  : The ordering n0<n5<n10<n15 with axis_conflict(n0,n5,n10,n15)
%           : is satisfiable — the disjointness of [n0,n5] and [n10,n15]
%           : is consistent with the strict chain (since less(n5,n10) holds).
%           : This is the SAT companion of NFV001+1.p (THM).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : NFV001-SAT+1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : SAT companion for NFV001+1.p. No conjecture.
%           : Run with Mace4 -n 4 -N 6, Paradox, or Vampire-FMB.
%           : Policy source: Policies/NFV001-policy.ttl
""" + SEP + """
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').

fof(order_0_5,   axiom, less(n0,n5)).
fof(order_5_10,  axiom, less(n5,n10)).
fof(order_10_15, axiom, less(n10,n15)).
fof(distinct,    axiom, $distinct(n0,n5,n10,n15)).
fof(conflict_hyp, axiom, axis_conflict(n0,n5,n10,n15)).
""")

# ── NFV002-SAT+1.p ────────────────────────────────────────────────────────
write(f"{base}/NFV002-SAT+1.p", SEP + """\
% File     : NFV002-SAT+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : axis_compatible hypothesis set is self-consistent (SAT companion)
% Version  : 1.0
% English  : The ordering n0<n5<n10 with axis_compatible(n0,n10,n5,n10)
%           : is satisfiable — the intervals [n0,n10] and [n5,n10] overlap
%           : in [n5,n10], so a witness exists (X=n5 or X=n10).
%           : This is the SAT companion of NFV002+1.p (THM).
%
% Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : NFV002-SAT+1.p
%
% Status   : Satisfiable
% SPC      : FOF_SAT_RFN
%
% Comments : SAT companion for NFV002+1.p. No conjecture.
%           : Policy source: Policies/NFV002-policy.ttl
""" + SEP + """
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').

fof(order_0_5,  axiom, less(n0,n5)).
fof(order_5_10, axiom, less(n5,n10)).
fof(distinct,   axiom, $distinct(n0,n5,n10)).
fof(compatible_hyp, axiom, axis_compatible(n0,n10,n5,n10)).
""")

print("Done — 3 SAT companion files written.")