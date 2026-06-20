"""
gen_axioms.py
=============
Generates all 9 .ax axiom files in Problems/ODRL/AxisDecomposition/Axioms/.
Each file is a TPTP-format FOF axiom set. The Axioms directory is shared
by every problem .p file via include('Axioms/<name>.ax').

Files:
  ORD000-0.ax   Linear order over val/2 with less/2
  ORD001-0.ax   Density extension (forall x,y. less(x,y) -> exists z. less(x,z) & less(z,y))
  AXIS000-0.ax  Interval denotations (in_open, in_lopen, in_ropen, in_closed)
                + verdict algebra (box_verdict)
  PREC000-0.ax  Endpoint precedence (prec/4), disjointness criterion
                (disjoint/8), operator-to-tag mapping (upper_tag, lower_tag).
                Encodes Definition 5 and Theorem 2 of the ODAX paper.
  WF000-0.ax    Well-formedness predicates
  PROJ000-0.ax  Projection axioms
  COMP000-0.ax  Composition (or_verdict, xone_verdict)
  COMPL000-0.ax Completion axioms
  SUBS000-0.ax  Subsumption (axis_subsumes, subs_verdict, box_subs)

Change log:
  v1.1  PREC000-0.ax: added prec/4 biconditionals for cc/oc/co/oo cases,
        disjoint/8 biconditional, lower_tag/2 facts, tag sort with c != o,
        functionality of both tag families. Removed semantically wrong
        upper_tag(gteq, c) and upper_tag(gt, c) facts -- neither operator
        constrains the upper side of the interval.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from header import AXHeader, _ax_comment

OUT = Path("Problems/ODRL/AxisDecomposition/Axioms")
OUT.mkdir(parents=True, exist_ok=True)


def write_ax(filename, title, english, comments, fof_text):
    """Write an .ax file with proper header + FOF body."""
    hdr = AXHeader(
        file     = filename,
        domain   = "axis",
        title    = title,
        version  = "1.0",
        english  = english,
        refs     = ["axis2026"],
        comments = _ax_comment(fof_text, comments, ""),
        fof_text = fof_text,
    ).render()
    path = OUT / filename
    path.write_text(hdr + fof_text)
    n_axioms = fof_text.count("fof(")
    print(f"  Wrote {filename}  ({n_axioms} formulae)")
    return path


# ---------------------------------------------------------------------------
# ORD000-0.ax  --  Strict linear order axioms
# ---------------------------------------------------------------------------
ORD000 = """\
% Strict linear order: less/2 is irreflexive, transitive, and asymmetric
% over the val/1 sort. val(X) marks X as an axis value.

fof(less_irreflexive, axiom,
    ! [X] : ~ less(X, X)).

fof(less_transitive, axiom,
    ! [X,Y,Z] : ((less(X, Y) & less(Y, Z)) => less(X, Z))).

fof(less_asymmetric, axiom,
    ! [X,Y] : (less(X, Y) => ~ less(Y, X))).

% leq is reflexive closure of less
fof(leq_def, axiom,
    ! [X,Y] : (leq(X, Y) <=> (less(X, Y) | X = Y))).
"""

write_ax(
    "ORD000-0.ax",
    "Strict linear order over axis values",
    "Irreflexivity, transitivity, asymmetry of less/2; leq is reflexive closure.",
    "ord-irrefl + ord-trans + ord-asym + leq-def",
    ORD000,
)

# ---------------------------------------------------------------------------
# ORD001-0.ax  --  Density extension
# ---------------------------------------------------------------------------
ORD001 = """\
% Density axiom: between any two distinct ordered values there is another.
% Used only by problems with open-open intervals where no named witness exists.

fof(less_dense, axiom,
    ! [X,Y] : (less(X, Y) => ? [Z] : (less(X, Z) & less(Z, Y)))).
"""

write_ax(
    "ORD001-0.ax",
    "Density of the linear order",
    "Between any two distinct ordered values there is another.",
    "1 density axiom",
    ORD001,
)
# ---------------------------------------------------------------------------
# AXIS000-0.ax  --  Interval denotations, per-axis predicates, verdict algebra
#
# REWRITTEN v1.1: extends the previous version with three additions:
#   - axis_subsumes/4  (per-axis containment, paper Def 21)
#   - axis_conflict/4  (per-axis disjointness, paper Thm 13, closed-closed)
#   - box_verdict_total (robustness, analogous to box_subs_total in SUBS000)
#
# Sections A, B, C of v1.0 are unchanged.  Section D is new.
#
# Note on axis_subsumes: SUBS000 v1.1 also defines axis_subsumes_def with the
# same biconditional.  When a problem includes both AXIS000 and SUBS000 (as
# BoxContainment does), the duplicate is harmless redundancy.  Cleaner would
# be to remove the SUBS000 copy in a future refactor.
#
# Note on axis_conflict: the closed-closed form (less(U1, L2) | less(U2, L1))
# is correct for problems whose intervals are all closed-closed.  Mixed
# open/closed endpoint precedence (paper's $\prec$ relation) is handled by
# PREC000-0.ax instead.
# ---------------------------------------------------------------------------
AXIS000 = """\
% =================================================================
% Section A: Interval membership predicates (Def 14)
% in_open(X, L, U)   <=>  L < X < U     (open at both ends)
% in_lopen(X, L, U)  <=>  L < X <= U    (left-open, right-closed)
% in_ropen(X, L, U)  <=>  L <= X < U    (left-closed, right-open)
% in_closed(X, L, U) <=>  L <= X <= U   (closed at both ends)
% =================================================================
fof(in_open_def, axiom,
    ! [X,L,U] : (in_open(X, L, U) <=> (less(L, X) & less(X, U)))).
fof(in_lopen_def, axiom,
    ! [X,L,U] : (in_lopen(X, L, U) <=> (less(L, X) & leq(X, U)))).
fof(in_ropen_def, axiom,
    ! [X,L,U] : (in_ropen(X, L, U) <=> (leq(L, X) & less(X, U)))).
fof(in_closed_def, axiom,
    ! [X,L,U] : (in_closed(X, L, U) <=> (leq(L, X) & leq(X, U)))).

% =================================================================
% Section B: Three-valued verdict constants (Def 27)
% =================================================================
fof(verdicts_distinct, axiom,
    $distinct(compatible, conflict, unknown)).
fof(verdict_total, axiom,
    ! [V] : (is_verdict(V) <=> (V = compatible | V = conflict | V = unknown))).
fof(is_verdict_compatible, axiom, is_verdict(compatible)).
fof(is_verdict_conflict,   axiom, is_verdict(conflict)).
fof(is_verdict_unknown,    axiom, is_verdict(unknown)).

% =================================================================
% Section C: box_verdict (per-axis verdict combinator, Def 22)
%   Compatible iff every V_k = Compatible
%   Conflict iff some V_k = Conflict
%   Unknown otherwise
% =================================================================
fof(box_conflict, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2) &
                  (V1 = conflict | V2 = conflict))
                 => box_verdict(V1, V2) = conflict)).
fof(box_compatible, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2) &
                  V1 = compatible & V2 = compatible)
                 => box_verdict(V1, V2) = compatible)).
fof(box_unknown, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2) &
                  (V1 = unknown | V2 = unknown) &
                  V1 != conflict & V2 != conflict)
                 => box_verdict(V1, V2) = unknown)).
fof(box_verdict_total, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2))
                 => (box_verdict(V1, V2) = compatible |
                     box_verdict(V1, V2) = conflict |
                     box_verdict(V1, V2) = unknown))).

% =================================================================
% Section D: Per-axis containment and disjointness (Def 21, Thm 13)
%
% axis_subsumes(L1, U1, L2, U2): [L1, U1] subseteq [L2, U2]
%   closed-closed form: leq(L2, L1) & leq(U1, U2)
%
% axis_conflict(L1, U1, L2, U2): [L1, U1] cap [L2, U2] = empty
%   closed-closed form (Conflict Criterion, Thm 13 with strict <):
%   less(U1, L2) | less(U2, L1)
%
% These are the closed-closed instantiations of the paper's
% endpoint-precedence-based definitions.  Mixed open/closed cases
% use prec/2 from PREC000-0.ax instead.
% =================================================================
fof(axis_subsumes_def, axiom,
    ! [L1, U1, L2, U2] :
      ( axis_subsumes(L1, U1, L2, U2)
    <=> ( leq(L2, L1) & leq(U1, U2) ) )).

fof(axis_conflict_def, axiom,
    ! [L1, U1, L2, U2] :
      ( axis_conflict(L1, U1, L2, U2)
    <=> ( less(U1, L2) | less(U2, L1) ) )).
"""

write_ax(
    "AXIS000-0.ax",
    "Interval denotations, per-axis predicates, verdict algebra (v1.1)",
    "Section A: in_open/in_lopen/in_ropen/in_closed biconditionals. "
    "Section B: three-valued Verdict constants. "
    "Section C: box_verdict combinator + totality. "
    "Section D: axis_subsumes + axis_conflict biconditionals (closed-closed).",
    "4 intervals + 5 verdict facts + 4 box_verdict cases + 2 axis predicates = 15 formulae "
    "(generator output reports +3 vs prior version: +box_verdict_total, +axis_subsumes_def, +axis_conflict_def)",
    AXIS000,
)
# ---------------------------------------------------------------------------
# PREC000-0.ax  --  Endpoint precedence, disjointness criterion, tag mapping
#
# REWRITTEN v1.1: the previous version was incomplete -- it defined only
# upper_tag/2 (with two semantically wrong facts for gteq and gt), and did
# not define prec/4 or disjoint/8 at all, even though those predicates are
# used throughout problem_data_prec.py.
#
# This version adds:
#   - Tag sort with c != o
#   - prec/4 biconditionals for cc, oc, co, oo (encodes Definition 5)
#   - disjoint/8 biconditional (encodes Theorem 2)
#   - lower_tag/2 facts for eq, gteq, gt
#   - Removal of the wrong upper_tag facts for gteq and gt
#   - Functionality axioms for both tag families
#
# Biconditionals (not forward implications) are required: positive
# Theorem problems close on the forward direction, but negative problems
# (ODRL601, ODRL606) need the backward direction via contrapositive on
# irreflexivity of less.
# ---------------------------------------------------------------------------
PREC000 = """\
% Section 1: Tag sort
% prec/4's third and fourth arguments are openness tags drawn from {c, o}.
% Without c != o, a model can collapse the two and silently merge
% prec_cc with prec_oc; negative problems will misbehave.

fof(tag_c,         axiom, tag(c)).
fof(tag_o,         axiom, tag(o)).
fof(tags_distinct, axiom, c != o).

% Section 2: Endpoint precedence (Definition 5)
% u prec l iff (u < l) OR (u = l AND at least one endpoint is open).
%
% Case split by (upper_tag, lower_tag):
%   (c,c) both closed -> u prec l iff u < l       (strict)
%   (o,c) upper open  -> u prec l iff u <= l
%   (c,o) lower open  -> u prec l iff u <= l
%   (o,o) both open   -> u prec l iff u <= l
%
% Used by: ODRL600 (cc fwd), ODRL601 (cc bwd), ODRL602 (oc fwd),
%          ODRL603 (co fwd), ODRL604 (oo fwd), ODRL605 (cc fwd via disjoint),
%          ODRL606 (cc bwd via disjoint), ODRL607 (co fwd via disjoint).

fof(prec_cc, axiom,
    ! [U,L] : (prec(U, L, c, c) <=> less(U, L))).

fof(prec_oc, axiom,
    ! [U,L] : (prec(U, L, o, c) <=> leq(U, L))).

fof(prec_co, axiom,
    ! [U,L] : (prec(U, L, c, o) <=> leq(U, L))).

fof(prec_oo, axiom,
    ! [U,L] : (prec(U, L, o, o) <=> leq(U, L))).

% Section 3: Disjointness criterion (Theorem 2)
% disjoint([L1,U1] tagged (CL1,CU1), [L2,U2] tagged (CL2,CU2)) iff
%   prec(U1, L2, CU1, CL2)  OR  prec(U2, L1, CU2, CL1).
%
% Biconditional needed for ODRL606 (non-disjoint at shared closed endpoint)
% and ODRL608 (symmetry of disjoint via OR-commutativity).

fof(disjoint_def, axiom,
    ! [L1,U1,CL1,CU1,L2,U2,CL2,CU2] :
      ( disjoint(L1, U1, CL1, CU1, L2, U2, CL2, CU2)
    <=> ( prec(U1, L2, CU1, CL2)
        | prec(U2, L1, CU2, CL1) ) )).

% Section 4: Operator-to-tag mapping (Definition 3)
% Each ODRL operator defines an upper boundary, a lower boundary, or both:
%
%   eq v   denotes {v}        -- defines both upper (closed) and lower (closed).
%   lteq v denotes (-inf, v]  -- defines upper (closed) only.
%   gteq v denotes [v, +inf)  -- defines lower (closed) only.
%   lt v   denotes (-inf, v)  -- defines upper (open) only.
%   gt v   denotes (v, +inf)  -- defines lower (open) only.
%
% The previous version asserted upper_tag(gteq, c) and upper_tag(gt, c);
% those are wrong because neither operator constrains the upper side.
% Used by: ODRL609 (operator-tag unit facts directly).

% Upper-tag facts
fof(upper_tag_eq,   axiom, upper_tag(eq,   c)).
fof(upper_tag_lteq, axiom, upper_tag(lteq, c)).
fof(upper_tag_lt,   axiom, upper_tag(lt,   o)).

% Lower-tag facts
fof(lower_tag_eq,   axiom, lower_tag(eq,   c)).
fof(lower_tag_gteq, axiom, lower_tag(gteq, c)).
fof(lower_tag_gt,   axiom, lower_tag(gt,   o)).

% Functionality: each operator has at most one tag per side
fof(upper_tag_functional, axiom,
    ! [OP,T1,T2] : ((upper_tag(OP, T1) & upper_tag(OP, T2)) => T1 = T2)).

fof(lower_tag_functional, axiom,
    ! [OP,T1,T2] : ((lower_tag(OP, T1) & lower_tag(OP, T2)) => T1 = T2)).
"""

write_ax(
    "PREC000-0.ax",
    "Endpoint precedence, disjointness criterion, and operator-tag mapping",
    "prec/4 biconditionals for cc/oc/co/oo (Definition 5); "
    "disjoint/8 biconditional (Theorem 2); "
    "upper_tag/lower_tag facts for the five ODRL dimensional operators.",
    "3 tag-sort + 4 prec biconditionals + 1 disjoint biconditional + "
    "6 tag facts + 2 functionality axioms",
    PREC000,
)

# ---------------------------------------------------------------------------
# WF000-0.ax  --  Well-formedness predicates (Definition 4)
#
# REWRITTEN v1.1: the previous version defined well_formed/2 with five
# forward-only implications.  None of the 8 WellFormedness problems use
# well_formed/2; they all use wf/4 and sem_nonempty/4 (paper-faithful
# signatures with explicit InfD, SupD parameters).  Same dead-predicate
# problem as the original COMPL000.
#
# This version:
#   - Replaces well_formed/2 with wf/4, biconditional, mirroring Def 4
#   - Adds sem_nonempty/4, biconditional, mirroring Lemma "Well-formed
#     denotation" case analysis
#   - Removes the existential `(?[X]: less(X,V))` proxy for the boundary
#     exclusions; uses the direct V != InfD / V != SupD form
#
# Biconditionals are needed by negative problems (ODRL614, ODRL616) which
# derive ~wf from the boundary equalities.
# ---------------------------------------------------------------------------
WF000 = """\
% Section 1: wf/4  (Definition 4, Well-formed constraint)
%
% wf(Op, V, InfD, SupD) holds iff (Op V) is a well-formed constraint
% over domain [InfD, SupD]:
%   eq, lteq, gteq: V in [InfD, SupD]
%   lt:             V in [InfD, SupD] AND V != InfD
%   gt:             V in [InfD, SupD] AND V != SupD
%
% Used by: ODRL610-616 (positive and negative wf cases per operator).

fof(wf_eq_def, axiom,
    ! [V, InfD, SupD] :
      ( wf(eq, V, InfD, SupD)
    <=> ( leq(InfD, V) & leq(V, SupD) ) )).

fof(wf_lteq_def, axiom,
    ! [V, InfD, SupD] :
      ( wf(lteq, V, InfD, SupD)
    <=> ( leq(InfD, V) & leq(V, SupD) ) )).

fof(wf_gteq_def, axiom,
    ! [V, InfD, SupD] :
      ( wf(gteq, V, InfD, SupD)
    <=> ( leq(InfD, V) & leq(V, SupD) ) )).

fof(wf_lt_def, axiom,
    ! [V, InfD, SupD] :
      ( wf(lt, V, InfD, SupD)
    <=> ( leq(InfD, V) & leq(V, SupD) & V != InfD ) )).

fof(wf_gt_def, axiom,
    ! [V, InfD, SupD] :
      ( wf(gt, V, InfD, SupD)
    <=> ( leq(InfD, V) & leq(V, SupD) & V != SupD ) )).

% Section 2: sem_nonempty/4  (Lemma "Well-formed denotation" case analysis)
%
% sem_nonempty(Op, V, InfD, SupD) holds iff the denotation of (Op V),
% intersected with [InfD, SupD], is non-empty:
%   eq:    V in [InfD, SupD]               (the singleton {V} hits the domain)
%   lteq:  V >= InfD                       ([InfD, min(V, SupD)] non-empty)
%   gteq:  V <= SupD                       ([max(V, InfD), SupD] non-empty)
%   lt:    V >  InfD                       ([InfD, V) non-empty)
%   gt:    V <  SupD                       ((V, SupD] non-empty)
%
% Lemma "Well-formed denotation" says wf => sem_nonempty.
%
% Used by: ODRL617 (the wf(lt) => sem_nonempty(lt) implication).

fof(sem_nonempty_eq_def, axiom,
    ! [V, InfD, SupD] :
      ( sem_nonempty(eq, V, InfD, SupD)
    <=> ( leq(InfD, V) & leq(V, SupD) ) )).

fof(sem_nonempty_lteq_def, axiom,
    ! [V, InfD, SupD] :
      ( sem_nonempty(lteq, V, InfD, SupD)
    <=> leq(InfD, V) )).

fof(sem_nonempty_gteq_def, axiom,
    ! [V, InfD, SupD] :
      ( sem_nonempty(gteq, V, InfD, SupD)
    <=> leq(V, SupD) )).

fof(sem_nonempty_lt_def, axiom,
    ! [V, InfD, SupD] :
      ( sem_nonempty(lt, V, InfD, SupD)
    <=> less(InfD, V) )).

fof(sem_nonempty_gt_def, axiom,
    ! [V, InfD, SupD] :
      ( sem_nonempty(gt, V, InfD, SupD)
    <=> less(V, SupD) )).
"""

write_ax(
    "WF000-0.ax",
    "Well-formedness predicates (Definition 4, Lemma 5)",
    "wf/4 biconditionals (Def 4) and sem_nonempty/4 biconditionals (Lemma 5) "
    "for all 5 ODRL dimensional operators.",
    "5 wf biconditionals + 5 sem_nonempty biconditionals = 10 axioms",
    WF000,
)

# ---------------------------------------------------------------------------
# PROJ000-0.ax  --  Box Denotation and Projection (Def. 14 / Thm. 17)
#
# REWRITTEN v1.1: the previous version defined box_member/6 and
# box_member3/9, neither of which any problem references.  The 10
# Projection problems actually use in_box2/6, in_box3/9, box2_compatible/8,
# and box2_conflict/8 -- four predicates that were not defined anywhere.
# Same dead-predicate problem as the original PREC000/COMPL000/WF000/SUBS000.
#
# This version defines all four problem-referenced predicates as
# biconditional axioms.  box_member predicates are dropped (no problem
# uses them).
# ---------------------------------------------------------------------------
PROJ000 = """\
% =================================================================
% in_box2/6  -- 2D box membership (Def. 14, Thm. 17 projection)
%   in_box2(X, Y, L1, U1, L2, U2) iff (X, Y) is in [L1,U1] x [L2,U2],
%   equivalently iff per-axis closed-interval membership holds.
% =================================================================
fof(in_box2_def, axiom,
    ! [X, Y, L1, U1, L2, U2] :
      ( in_box2(X, Y, L1, U1, L2, U2)
    <=> ( in_closed(X, L1, U1) & in_closed(Y, L2, U2) ) )).

% =================================================================
% in_box3/9  -- 3D box membership (Def. 14, Thm. 17 projection)
% =================================================================
fof(in_box3_def, axiom,
    ! [X, Y, Z, L1, U1, L2, U2, L3, U3] :
      ( in_box3(X, Y, Z, L1, U1, L2, U2, L3, U3)
    <=> ( in_closed(X, L1, U1)
        & in_closed(Y, L2, U2)
        & in_closed(Z, L3, U3) ) )).

% =================================================================
% box2_compatible/8  -- two 2D boxes overlap (Def. 21 box-verdict)
%   box A = [L1A, U1A] x [L2A, U2A]
%   box B = [L1B, U1B] x [L2B, U2B]
%   overlap iff per-axis intersections are non-empty,
%   equivalently iff max(L_A, L_B) <= min(U_A, U_B) per axis,
%   equivalently iff (L_A <= U_B) AND (L_B <= U_A) per axis.
% =================================================================
fof(box2_compatible_def, axiom,
    ! [L1A, U1A, L2A, U2A, L1B, U1B, L2B, U2B] :
      ( box2_compatible(L1A, U1A, L2A, U2A, L1B, U1B, L2B, U2B)
    <=> ( leq(L1A, U1B) & leq(L1B, U1A)
        & leq(L2A, U2B) & leq(L2B, U2A) ) )).

% =================================================================
% box2_conflict/8  -- two 2D boxes disjoint (Conflict Criterion, Thm. 13)
%   Disjoint iff some axis has disjoint intervals,
%   equivalently iff (U_A < L_B) OR (U_B < L_A) for some axis,
%   where < captures endpoint precedence for closed-closed intervals.
% =================================================================
fof(box2_conflict_def, axiom,
    ! [L1A, U1A, L2A, U2A, L1B, U1B, L2B, U2B] :
      ( box2_conflict(L1A, U1A, L2A, U2A, L1B, U1B, L2B, U2B)
    <=> ( less(U1A, L1B) | less(U1B, L1A)
        | less(U2A, L2B) | less(U2B, L2A) ) )).
"""

write_ax(
    "PROJ000-0.ax",
    "Box Denotation and Projection (Def. 14, Thm. 17)",
    "in_box2/6 + in_box3/9 + box2_compatible/8 + box2_conflict/8 biconditionals.",
    "4 biconditionals (was 2 unused box_member axioms in v1.0)",
    PROJ000,
)

# ---------------------------------------------------------------------------
# COMP000-0.ax  --  Composition: or_verdict, xone_verdict
# ---------------------------------------------------------------------------
COMP000 = """\
% or_verdict/2: ODRL `or` composition of two verdicts.
%   Rule: any compatible -> compatible
%         both conflict  -> conflict
%         otherwise      -> unknown

fof(or_compat, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2) &
                  (V1 = compatible | V2 = compatible))
                 => or_verdict(V1, V2) = compatible)).

fof(or_conflict, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2) &
                  V1 = conflict & V2 = conflict)
                 => or_verdict(V1, V2) = conflict)).

fof(or_unknown, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2) &
                  V1 != compatible & V2 != compatible &
                  ~(V1 = conflict & V2 = conflict))
                 => or_verdict(V1, V2) = unknown)).

fof(or_verdict_total, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2))
                 => (or_verdict(V1, V2) = compatible |
                     or_verdict(V1, V2) = conflict |
                     or_verdict(V1, V2) = unknown))).

% xone_verdict/2: ODRL `xone` (exactly one) reduction.
%   Conservative reduction:
%     match(compat) when remainder all-conflict   -> compatible
%     no match + all-conflict                     -> conflict
%     all other cases                             -> unknown

fof(xone_compat, axiom,
    ! [VM,VR] : ((is_verdict(VM) & is_verdict(VR) &
                  VM = compatible & VR = conflict)
                 => xone_verdict(VM, VR) = compatible)).

fof(xone_conflict, axiom,
    ! [VM,VR] : ((is_verdict(VM) & is_verdict(VR) &
                  VM = conflict & VR = conflict)
                 => xone_verdict(VM, VR) = conflict)).

fof(xone_unknown, axiom,
    ! [VM,VR] : ((is_verdict(VM) & is_verdict(VR) &
                  ~(VM = compatible & VR = conflict) &
                  ~(VM = conflict   & VR = conflict))
                 => xone_verdict(VM, VR) = unknown)).

fof(xone_verdict_total, axiom,
    ! [VM,VR] : ((is_verdict(VM) & is_verdict(VR))
                 => (xone_verdict(VM, VR) = compatible |
                     xone_verdict(VM, VR) = conflict |
                     xone_verdict(VM, VR) = unknown))).
"""

write_ax(
    "COMP000-0.ax",
    "Composition: or_verdict and xone_verdict",
    "ODRL `or` and `xone` reductions over three-valued verdicts.",
    "4 or_verdict cases + 4 xone_verdict cases",
    COMP000,
)

# ---------------------------------------------------------------------------
# COMPL000-0.ax  --  Completion axioms (Theorem 6.10, Unknown Soundness)
#
# REWRITTEN v1.1: the previous version defined completed/3 with six
# identity-shape axioms.  That predicate is not used by any of the 8
# Completion problems.  The problems use completion_compatible/3 and
# completion_conflict/4 (both undefined in v1.0), and ODRL634 uses
# axis_conflict/4 (also undefined).  This rewrite replaces the dead
# axioms with three biconditionals matching what the problems actually
# need, derived directly from Theorem 6.10 (Unknown Soundness):
#
#   Compatible completion: add (eq V) to both policies for some V in D_k.
#   Well-formed iff V in [InfD, SupD].
#
#   Conflict completion: add (lteq U) to one and (gteq V) to the other,
#   with U < V both in D_k.  Yields disjoint intervals by Thm 5.8.
#
#   Axis-level conflict: [L1,U1] and [L2,U2] conflict iff one ends strictly
#   before the other begins (the cc case of Thm 5.8's disjoint criterion,
#   encoded directly so Completion problems do not need to include PREC000).
# ---------------------------------------------------------------------------
COMPL000 = """\
% Section 1: completion_compatible/3  (Theorem 6.10, compatible completion)
%
% completion_compatible(V, InfD, SupD) holds iff value V can serve as the
% witness in the (eq V) compatible completion -- i.e., V lies in the
% effective axis domain [InfD, SupD].
%
% Used by: ODRL630 (interior), ODRL632 (sharpness), ODRL636 (boundary V=InfD).

fof(completion_compatible_def, axiom,
    ! [V, InfD, SupD] :
      ( completion_compatible(V, InfD, SupD)
    <=> ( leq(InfD, V) & leq(V, SupD) ) )).

% Section 2: completion_conflict/4  (Theorem 6.10, conflict completion)
%
% completion_conflict(U, V, InfD, SupD) holds iff (U, V) can serve as the
% pair in the (lteq U) / (gteq V) conflict completion: U < V strictly, and
% both U and V lie in [InfD, SupD].  The strictness is essential -- equal
% endpoints with both intervals closed share that point and do not
% conflict (cf. Theorem 5.8 prec_cc case).
%
% Used by: ODRL631 (witness pair), ODRL633 (sharpness), ODRL637 (strictness).

fof(completion_conflict_def, axiom,
    ! [U, V, InfD, SupD] :
      ( completion_conflict(U, V, InfD, SupD)
    <=> ( leq(InfD, U) & less(U, V) & leq(V, SupD) ) )).

% Section 3: axis_conflict/4  (Theorem 5.8 cc-case, encoded directly)
%
% Two closed intervals are in conflict iff either ends strictly before
% the other begins.  This duplicates the cc case of disjoint/8 from
% PREC000-0.ax in order to keep Completion problems self-contained.
%
% Used by: ODRL634 (monotone_conflict / ground instance).

fof(axis_conflict_def, axiom,
    ! [L1, U1, L2, U2] :
      ( axis_conflict(L1, U1, L2, U2)
    <=> ( less(U1, L2) | less(U2, L1) ) )).
"""

write_ax(
    "COMPL000-0.ax",
    "Completion axioms (Theorem 6.10, Unknown Soundness)",
    "completion_compatible: V in [InfD,SupD] suffices for compatible completion. "
    "completion_conflict: U<V in [InfD,SupD] witnesses conflict completion. "
    "axis_conflict: two intervals conflict iff one ends strictly before the other begins.",
    "3 biconditionals: completion_compatible + completion_conflict + axis_conflict",
    COMPL000,
)

# ---------------------------------------------------------------------------
# SUBS000-0.ax  --  Subsumption / Box Containment (Definition 23)
#
# Defines axis_subsumes/4 biconditionally (paper-faithful sem(c1) subseteq
# sem(c2) for the closed-interval case), then composes per-axis verdicts
# under box_subs/2 (the box-level combinator from Def. 23).
#
# v1.1: added axis_subsumes_def biconditional.  Previously axis_subsumes/4
# was declared but never defined; problems supplied ground hints in their
# .p files (which is brittle and fails for ODRL650 / ODRL651 where no hint
# is provided).  With the biconditional, axis_subsumes is derivable from
# the leq ordering and the hint axioms in ODRL652/653/657 become harmless
# redundancy.
# ---------------------------------------------------------------------------
SUBS000 = """\
% =================================================================
% axis_subsumes/4 - paper Def. 23: sem(c1_k) subseteq sem(c2_k)
% Closed-interval form: [L1, U1] subseteq [L2, U2] iff
%   L2 <= L1 AND U1 <= U2.
% (lteq constraints on D_k = (0, inf) all share lower bound 0, so
% the lower-bound clause reduces to leq(0, 0) = true and the test
% becomes upper-bound comparison.)
% =================================================================
fof(axis_subsumes_def, axiom,
    ! [L1, U1, L2, U2] :
      ( axis_subsumes(L1, U1, L2, U2)
    <=> ( leq(L2, L1) & leq(U1, U2) ) )).

% =================================================================
% Presence sort: present | absent
% =================================================================
fof(presence_distinct, axiom, present != absent).
fof(presence_total, axiom,
    ! [P] : (is_presence(P) <=> (P = present | P = absent))).
fof(is_presence_present, axiom, is_presence(present)).
fof(is_presence_absent,  axiom, is_presence(absent)).

% =================================================================
% subs_verdict/6 - paper Def. 23 per-axis containment status S_k
%   S_k = Unknown    if either policy does not constrain a_k
%   S_k = Compatible if both constrain AND sem(c1_k) subseteq sem(c2_k)
%   S_k = Conflict   otherwise
% Forward-only axioms suffice: classical case analysis on the two
% presence tags and on axis_subsumes (which is total since classical)
% gives exhaustive coverage; subs_verdict is a function so the result
% is unique under verdict distinctness from AXIS000.
% =================================================================
fof(subs_c1_absent, axiom,
    ! [L1,U1,L2,U2] :
        subs_verdict(L1, U1, absent, L2, U2, present) = unknown).
fof(subs_c2_absent, axiom,
    ! [L1,U1,L2,U2] :
        subs_verdict(L1, U1, present, L2, U2, absent) = unknown).
fof(subs_both_absent, axiom,
    ! [L1,U1,L2,U2] :
        subs_verdict(L1, U1, absent, L2, U2, absent) = unknown).
fof(subs_present_yes, axiom,
    ! [L1,U1,L2,U2] :
        (axis_subsumes(L1, U1, L2, U2) =>
         subs_verdict(L1, U1, present, L2, U2, present) = compatible)).
fof(subs_present_no, axiom,
    ! [L1,U1,L2,U2] :
        (~ axis_subsumes(L1, U1, L2, U2) =>
         subs_verdict(L1, U1, present, L2, U2, present) = conflict)).
fof(subs_verdict_total, axiom,
    ! [L1,U1,P1,L2,U2,P2] :
        ((is_presence(P1) & is_presence(P2))
         => (subs_verdict(L1, U1, P1, L2, U2, P2) = compatible |
             subs_verdict(L1, U1, P1, L2, U2, P2) = conflict   |
             subs_verdict(L1, U1, P1, L2, U2, P2) = unknown))).

% =================================================================
% box_subs/2 - paper Def. 23 box-level combinator
%   Compatible iff every S_k = Compatible
%   Conflict   iff some  S_k = Conflict
%   Unknown    otherwise
% Binary; multi-axis combination is a left-associative chain.
% =================================================================
fof(box_subs_compat, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2) &
                  V1 = compatible & V2 = compatible)
                 => box_subs(V1, V2) = compatible)).
fof(box_subs_conflict, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2) &
                  (V1 = conflict | V2 = conflict))
                 => box_subs(V1, V2) = conflict)).
fof(box_subs_unknown, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2) &
                  ~(V1 = compatible & V2 = compatible) &
                  V1 != conflict & V2 != conflict)
                 => box_subs(V1, V2) = unknown)).
fof(box_subs_total, axiom,
    ! [V1,V2] : ((is_verdict(V1) & is_verdict(V2))
                 => (box_subs(V1, V2) = compatible |
                     box_subs(V1, V2) = conflict |
                     box_subs(V1, V2) = unknown))).
"""

write_ax(
    "SUBS000-0.ax",
    "Subsumption / Box Containment (Def. 23)",
    "axis_subsumes/4 biconditional + subs_verdict/6 case analysis + box_subs/2 combinator.",
    "1 axis_subsumes def + 4 presence + 5 subs_verdict cases + 4 box_subs cases = 14 formulae "
    "(generator output reports +1 vs prior version due to axis_subsumes_def addition)",
    SUBS000,
)

print(f"\nDone. 9 axiom files in {OUT.resolve()}")