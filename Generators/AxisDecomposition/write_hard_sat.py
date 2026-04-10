"""
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
% Comments : SAT companion for HARD001+1.p.
%           : No conjecture — prover finds a model of the hypothesis set.
%           : Policy source: Policies/HARD001-policy.ttl
""" + SEP + """
include('Axioms/ORD000-0.ax').
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/COMPL000-0.ax').
% Ordering chain: n0 < n3 < n5 < n10 < n20
fof(h_0_3,    axiom, less(n0,n3)).
fof(h_3_5,    axiom, less(n3,n5)).
fof(h_5_10,   axiom, less(n5,n10)).
fof(h_10_20,  axiom, less(n10,n20)).
% Domain bounds
fof(h_inf_lb, axiom, ![X]: leq(ninf,X)).
fof(h_sup_ub, axiom, ![X]: leq(X,nsup)).
% SAT witness: the ordering chain is satisfiable in any dense total order.
% No conjecture — model finder confirms consistency.
fof(sat_witness, axiom, less(n0,n20)).
""")

# ── NFV001-SAT+1.p ────────────────────────────────────────────────────────
write(f"{base}/NFV001-SAT+1.p", SEP + """\
% File     : NFV001-SAT+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : axis_conflict hypothesis set is self-consistent (SAT companion)
% Version  : 1.0
% English  : The ordering n0<n5<n10<n15 with axis_conflict(n0,n5,n10,n15)
%           : is satisfiable — the hypotheses of NFV001 do not self-contradict.
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
% Comments : SAT companion for NFV001+1.p.
%           : Confirms axis_conflict hypothesis is consistent before THM proof.
%           : Policy source: Policies/NFV001-policy.ttl
""" + SEP + """
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').
fof(order_0_5,   axiom, less(n0,n5)).
fof(order_5_10,  axiom, less(n5,n10)).
fof(order_10_15, axiom, less(n10,n15)).
fof(conflict_hyp, axiom, axis_conflict(n0,n5,n10,n15)).
% No conjecture — model finder confirms consistency.
fof(sat_witness, axiom, less(n0,n15)).
""")

# ── NFV002-SAT+1.p ────────────────────────────────────────────────────────
write(f"{base}/NFV002-SAT+1.p", SEP + """\
% File     : NFV002-SAT+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : axis_compatible hypothesis set is self-consistent (SAT companion)
% Version  : 1.0
% English  : The ordering n0<n5<n10 with axis_compatible(n0,n10,n5,n10)
%           : is satisfiable — the hypotheses of NFV002 do not self-contradict.
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
% Comments : SAT companion for NFV002+1.p.
%           : Confirms axis_compatible hypothesis is consistent before THM proof.
%           : Policy source: Policies/NFV002-policy.ttl
""" + SEP + """
include('Axioms/ORD000-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PROJ000-0.ax').
fof(order_0_5,  axiom, less(n0,n5)).
fof(order_5_10, axiom, less(n5,n10)).
fof(compatible_hyp, axiom, axis_compatible(n0,n10,n5,n10)).
% No conjecture — model finder confirms consistency.
fof(sat_witness, axiom, less(n0,n10)).
""")

print("Done — 3 SAT companion files written.")
