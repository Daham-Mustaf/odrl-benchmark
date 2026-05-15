"""
smt_axioms.py
=============
Reusable SMT-LIB axiom snippets for the AxisDecomposition benchmark.

Mirrors the FOF axioms in:
  - AXIS000-0.ax (Section D: box_verdict)
  - COMP000-0.ax (or_verdict, xone_verdict)
  - SUBS000-0.ax (subs_verdict, box_subs)
  - PREC000-0.ax (upper_tag)

Every axiom block is a verbatim translation of the corresponding FOF axiom
into SMT-LIB UF logic, verified to derive unsat under Z3 and cvc5 against
the ground-instance and Skolemized conjectures used in the .p files.
"""

PREAMBLE_VERDICT = """\
; Three-valued Verdict sort (mirrors AXIS000-0.ax Section D)
(declare-sort Verdict 0)
(declare-fun conflict   () Verdict)
(declare-fun compatible () Verdict)
(declare-fun unknown    () Verdict)
(declare-fun is_verdict (Verdict) Bool)
(assert (distinct conflict compatible unknown))
(assert (is_verdict conflict))
(assert (is_verdict compatible))
(assert (is_verdict unknown))
(assert (forall ((v Verdict))
    (=> (is_verdict v)
        (or (= v conflict) (= v compatible) (= v unknown)))))
"""

PREAMBLE_PRESENCE = """\
; Presence sort (mirrors SUBS000-0.ax presence tags)
(declare-sort Presence 0)
(declare-fun present () Presence)
(declare-fun absent  () Presence)
(declare-fun is_presence (Presence) Bool)
(assert (distinct present absent))
(assert (is_presence present))
(assert (is_presence absent))
(assert (forall ((p Presence)) (=> (is_presence p) (or (= p present) (= p absent)))))
"""

PREAMBLE_BOUND_SORT = """\
; Bound sort: uninterpreted endpoints of intervals
(declare-sort Bound 0)
"""

DECL_OR_VERDICT   = "(declare-fun or_verdict (Verdict Verdict) Verdict)\n"
DECL_XONE_VERDICT = "(declare-fun xone_verdict (Verdict Verdict) Verdict)\n"
DECL_BOX_VERDICT  = "(declare-fun box_verdict (Verdict Verdict) Verdict)\n"
DECL_BOX_SUBS     = "(declare-fun box_subs (Verdict Verdict) Verdict)\n"
DECL_AXIS_SUBSUMES = "(declare-fun axis_subsumes (Bound Bound Bound Bound) Bool)\n"
DECL_SUBS_VERDICT = "(declare-fun subs_verdict (Bound Bound Presence Bound Bound Presence) Verdict)\n"

AXIOM_OR_COMPAT = """\
; or_compat (COMP000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (or (= v1 compatible) (= v2 compatible)))
        (= (or_verdict v1 v2) compatible))))
"""

AXIOM_OR_CONFLICT = """\
; or_conflict (COMP000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (and (= v1 conflict) (= v2 conflict)))
        (= (or_verdict v1 v2) conflict))))
"""

AXIOM_OR_UNKNOWN = """\
; or_unknown (COMP000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (not (= v1 compatible)) (not (= v2 compatible))
             (not (and (= v1 conflict) (= v2 conflict))))
        (= (or_verdict v1 v2) unknown))))
"""

AXIOM_OR_TOTAL = """\
; or_verdict_total (COMP000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2))
        (or (= (or_verdict v1 v2) compatible)
            (= (or_verdict v1 v2) conflict)
            (= (or_verdict v1 v2) unknown)))))
"""

AXIOM_XONE_COMPAT = """\
; xone_compat (COMP000-0.ax)
(assert (forall ((vm Verdict) (vr Verdict))
    (=> (and (is_verdict vm) (is_verdict vr)
             (= vm compatible) (= vr conflict))
        (= (xone_verdict vm vr) compatible))))
"""

AXIOM_XONE_CONFLICT = """\
; xone_conflict (COMP000-0.ax)
(assert (forall ((vm Verdict) (vr Verdict))
    (=> (and (is_verdict vm) (is_verdict vr)
             (= vm conflict) (= vr conflict))
        (= (xone_verdict vm vr) conflict))))
"""

AXIOM_XONE_UNKNOWN = """\
; xone_unknown (COMP000-0.ax) - residual case
(assert (forall ((vm Verdict) (vr Verdict))
    (=> (and (is_verdict vm) (is_verdict vr)
             (not (and (= vm compatible) (= vr conflict)))
             (not (and (= vm conflict)  (= vr conflict))))
        (= (xone_verdict vm vr) unknown))))
"""

AXIOM_XONE_TOTAL = """\
; xone_verdict_total (COMP000-0.ax)
(assert (forall ((vm Verdict) (vr Verdict))
    (=> (and (is_verdict vm) (is_verdict vr))
        (or (= (xone_verdict vm vr) compatible)
            (= (xone_verdict vm vr) conflict)
            (= (xone_verdict vm vr) unknown)))))
"""

AXIOM_BOX_CONFLICT = """\
; box_conflict (AXIS000-0.ax Section D)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (or (= v1 conflict) (= v2 conflict)))
        (= (box_verdict v1 v2) conflict))))
"""

AXIOM_BOX_COMPATIBLE = """\
; box_compatible (AXIS000-0.ax Section D)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (= v1 compatible) (= v2 compatible))
        (= (box_verdict v1 v2) compatible))))
"""

AXIOM_BOX_UNKNOWN = """\
; box_unknown (AXIS000-0.ax Section D)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (or (= v1 unknown) (= v2 unknown))
             (not (= v1 conflict)) (not (= v2 conflict)))
        (= (box_verdict v1 v2) unknown))))
"""

AXIOM_SUBS_C1_ABSENT = """\
; subs_c1_absent (SUBS000-0.ax)
(assert (forall ((l1 Bound) (h1 Bound) (l2 Bound) (h2 Bound))
    (= (subs_verdict l1 h1 absent l2 h2 present) unknown)))
"""

AXIOM_SUBS_C2_ABSENT = """\
; subs_c2_absent (SUBS000-0.ax)
(assert (forall ((l1 Bound) (h1 Bound) (l2 Bound) (h2 Bound))
    (= (subs_verdict l1 h1 present l2 h2 absent) unknown)))
"""

AXIOM_SUBS_BOTH_ABSENT = """\
; subs_both_absent (SUBS000-0.ax)
(assert (forall ((l1 Bound) (h1 Bound) (l2 Bound) (h2 Bound))
    (= (subs_verdict l1 h1 absent l2 h2 absent) unknown)))
"""

AXIOM_SUBS_PRESENT_YES = """\
; subs_present_yes (SUBS000-0.ax)
(assert (forall ((l1 Bound) (h1 Bound) (l2 Bound) (h2 Bound))
    (=> (axis_subsumes l1 h1 l2 h2)
        (= (subs_verdict l1 h1 present l2 h2 present) compatible))))
"""

AXIOM_SUBS_PRESENT_NO = """\
; subs_present_no (SUBS000-0.ax)
(assert (forall ((l1 Bound) (h1 Bound) (l2 Bound) (h2 Bound))
    (=> (not (axis_subsumes l1 h1 l2 h2))
        (= (subs_verdict l1 h1 present l2 h2 present) conflict))))
"""

AXIOM_SUBS_TOTAL = """\
; subs_verdict_total (SUBS000-0.ax)
(assert (forall ((l1 Bound) (h1 Bound) (p1 Presence) (l2 Bound) (h2 Bound) (p2 Presence))
    (=> (and (is_presence p1) (is_presence p2))
        (or (= (subs_verdict l1 h1 p1 l2 h2 p2) compatible)
            (= (subs_verdict l1 h1 p1 l2 h2 p2) conflict)
            (= (subs_verdict l1 h1 p1 l2 h2 p2) unknown)))))
"""

AXIOM_BOX_SUBS_COMPAT = """\
; box_subs_compat (SUBS000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (= v1 compatible) (= v2 compatible))
        (= (box_subs v1 v2) compatible))))
"""

AXIOM_BOX_SUBS_CONFLICT = """\
; box_subs_conflict (SUBS000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (or (= v1 conflict) (= v2 conflict)))
        (= (box_subs v1 v2) conflict))))
"""

AXIOM_BOX_SUBS_UNKNOWN = """\
; box_subs_unknown (SUBS000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (not (and (= v1 compatible) (= v2 compatible)))
             (not (= v1 conflict)) (not (= v2 conflict)))
        (= (box_subs v1 v2) unknown))))
"""

AXIOM_BOX_SUBS_TOTAL = """\
; box_subs_total (SUBS000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2))
        (or (= (box_subs v1 v2) compatible)
            (= (box_subs v1 v2) conflict)
            (= (box_subs v1 v2) unknown)))))
"""

PREAMBLE_UPPER_TAG = """\
; Op and Tag sorts (PREC000-0.ax)
(declare-sort Op 0)
(declare-sort Tag 0)
(declare-fun eq   () Op)
(declare-fun lteq () Op)
(declare-fun gteq () Op)
(declare-fun lt   () Op)
(declare-fun gt   () Op)
(declare-fun c () Tag)
(declare-fun o () Tag)
(declare-fun upper_tag (Op Tag) Bool)
(assert (distinct c o))
"""

AXIOM_UPPER_TAG_GROUND = """\
; upper_tag ground facts (PREC000-0.ax)
(assert (upper_tag eq c))
(assert (upper_tag lteq c))
(assert (upper_tag gteq c))
(assert (upper_tag lt o))
(assert (upper_tag gt c))
; Functionality: upper_tag is single-valued on Op
(assert (forall ((op Op) (t1 Tag) (t2 Tag))
    (=> (and (upper_tag op t1) (upper_tag op t2)) (= t1 t2))))
"""


def declare_bounds(names):
    """Emit `(declare-fun NAME () Bound)` lines for each name in `names`."""
    return "".join(f"(declare-fun {n} () Bound)\n" for n in names)
