"""
gen_signature.py
================
Generates TWO signature files for the FOIS 2026 deontic grounding:

  Problems/DeonticOntology/Axioms/GRND000-0.ax     — FOF/TPTP  (Vampire)
  Problems/DeonticOntology/Axioms/GRND000-0.smt2   — SMT-LIB   (Z3)

FOF file:
  Used via include() at the top of every .p problem file.

SMT-LIB file:
  SMT-LIB has NO include directive.
  This file is a PREAMBLE TEMPLATE embedded verbatim by every
  problem generator into each .smt2 problem file.

Usage:
    uv run Generators/DeonticOntology/gen_signature.py \
  --out-dir Problems/DeonticOntology/Axioms
"""

import argparse
import textwrap
from pathlib import Path
from datetime import date

META = {
    "domain":  "Deontic Ontology / ODRL Grounding ",
    "source":  "Mohammed et al., What Does ODRL Mean? ",
    "version": "1.0",
}

# ============================================================================
# FOF
# ============================================================================

def fof_header() -> str:
    return textwrap.dedent(f"""\
        %--------------------------------------------------------------------------
        % File     : GRND000-0.ax
        % Domain   : {META['domain']}
        % Problem  : Signature — sorts, predicates, rfr/decl functions
        % Version  : {META['version']}
        % English  : FOF signature. Include in ALL DeonticOntology .p files via:
        %              include('Axioms/GRND000-0.ax').
        %
        % Source   : {META['source']}
        % Generated: {date.today().isoformat()} by gen_signature.py
        %
        % SZS status: Not a conjecture file — axiom library only
        %
        % Sorts (unary guard predicates — FOF has no native sorts):
        %   agent, action, target, rule, position, legal_relator, event,
        %   forbearance
        %
        % Functions:
        %   rfr/1  : Act -> Forbearance   (refrain from action)
        %   pos/1  : Forbearance -> Act   (left-inverse of rfr)
        %   decl/1 : Act -> Act           (declare-violation institutional act)
        %--------------------------------------------------------------------------
    """)

FOF_SORT_GUARDS = """\
%--------------------------------------------------------------------------
% SORT GUARDS
% FOF has no native sorts. We use unary predicates as type guards.
% Guards are NOT asserted here — problem files assert them for constants.
%
%   agent(X)         — X is an agent (assigner or assignee)
%   action(X)        — X is an action  in Act
%   target(X)        — X is a target asset
%   rule(X)          — X is an ODRL rule (perm / proh / duty)
%   position(X)      — X is a Hohfeldian position (UFO moment)
%   legal_relator(X) — X is a UFO legal relator
%   event(X)         — X is an activation event
%   forbearance(X)   — X is a forbearance in rfr(Act)
%--------------------------------------------------------------------------
"""

FOF_RULE_PREDICATES = """\
%--------------------------------------------------------------------------
% ODRL RULE TYPE PREDICATES
%   perm(R)    — R is an odrl:Permission
%   proh(R)    — R is an odrl:Prohibition
%   obl(R)     — R is an odrl:Duty  [CANONICAL NAME]
%                Paper uses ODRLDuty(d) in Ax5.4 — must be changed to obl(d)
%   has_rem(R) — R is a prohibition carrying odrl:remedy  [CANONICAL NAME]
%                Paper uses rem(f) in Ax5.7 — must be changed to has_rem(f)
%
% ODRL STRUCTURAL ROLE PREDICATES
%   aee(R, X)  — assignee of R is X
%   aer(R, Y)  — assigner of R is Y
%   act(R, A)  — action  of R is A
%   tgt(R, T)  — target  of R is T
%
% ACTIVATION PREDICATE
%   activates(E, R) — event E activates rule R
%                     Source: ODRL Formal Semantics §3.1
%--------------------------------------------------------------------------
"""

FOF_RELATOR_PREDICATES = """\
%--------------------------------------------------------------------------
% UFO RELATOR AND POSITION PREDICATES
%   founds(E, Rho)    — E founds relator Rho        (UFO axiom a77)
%   part_of(Pos, Rho) — Pos is part of Rho          (UFO §2.10)
%   bearer(Pos, X)    — Pos inheres in agent X       (UFO moment)
%   cnt(Pos, A, T)    — Pos has content A on target T  [CANONICAL]
%                       A in Act union Forbearance
%                       Used for ALL rule types: perm, proh, obl.
%                       Paper uses about(l,a,t) in Ax5.1 for Liberty/NoRight
%                       content — must be unified to cnt(l,a,t) everywhere.
%
% HOHFELDIAN POSITION TYPE PREDICATES
%   Conduct:    liberty   no_right   duty   claim
%   Competence: power     subjection immunity disability
%
% Source: UFO-L (griffo2018conceptual, griffo2023powers), Paper Def 5.3
%--------------------------------------------------------------------------
"""

FOF_RFR = """\
%--------------------------------------------------------------------------
% RFR FUNCTION  rfr : Act -> Forbearance
% rfr(A) = forbearance of performing A (duty to refrain).
% pos : Forbearance -> Act  is the left-inverse (uninterpreted function).
%
% RFR1  rfr(A) != A                      (irreflexivity)
% RFR2  rfr(A)=rfr(B) => A=B             (injectivity)
% RFR3  pos(rfr(A)) = A                  (left-inverse)
% RFR4  action(A) => forbearance(rfr(A)) (range guard)
% RFR5  forbearance(F) => ~action(F)     (sort disjointness)
%--------------------------------------------------------------------------

fof(rfr_irreflexive, axiom,
    ! [A] : ( action(A) => rfr(A) != A )).

fof(rfr_injective, axiom,
    ! [A, B] : ( ( action(A) & action(B) & rfr(A) = rfr(B) ) => A = B )).

fof(rfr_left_inverse, axiom,
    ! [A] : ( action(A) => pos(rfr(A)) = A )).

fof(rfr_range_forbearance, axiom,
    ! [A] : ( action(A) => forbearance(rfr(A)) )).

fof(forbearance_not_action, axiom,
    ! [F] : ( forbearance(F) => ~ action(F) )).

"""

FOF_DECL = """\
%--------------------------------------------------------------------------
% DECL FUNCTION  decl : Act -> Act
% decl(A) = institutional act of declaring a violation on action A.
% Used in Ax5.7 (Violation Authority).
%
% DECL1  action(A) => action(decl(A))    (range guard)
% DECL2  decl(A)=decl(B) => A=B          (injectivity)
% DECL3  action(A) => decl(A) != A       (distinctness)
%--------------------------------------------------------------------------

fof(decl_range_action, axiom,
    ! [A] : ( action(A) => action(decl(A)) )).

fof(decl_injective, axiom,
    ! [A, B] : ( ( action(A) & action(B) & decl(A) = decl(B) ) => A = B )).

fof(decl_distinct, axiom,
    ! [A] : ( action(A) => decl(A) != A )).

"""

FOF_NORMCONTENT = """\
%--------------------------------------------------------------------------
% NORMCONTENT TYPE DISTINCTION
% NormContent ::= Act | Forbearance  (paper, between Ax5.1 and Ax5.2)
% A position cannot have both action content and forbearance content.
%--------------------------------------------------------------------------

fof(action_forbearance_content_disjoint, axiom,
    ! [Pos, A, F, T1, T2] :
      ( ( cnt(Pos, A, T1) & cnt(Pos, F, T2) & action(A) & forbearance(F) )
     => A != F )).

"""

FOF_POSITION_DISJOINTNESS = """\
%--------------------------------------------------------------------------
% POSITION SORT DISJOINTNESS — all 8 types mutually disjoint
%--------------------------------------------------------------------------

% Within conduct level
fof(liberty_not_duty,     axiom, ! [P] : ~ ( liberty(P)  & duty(P)     )).
fof(liberty_not_claim,    axiom, ! [P] : ~ ( liberty(P)  & claim(P)    )).
fof(liberty_not_no_right, axiom, ! [P] : ~ ( liberty(P)  & no_right(P) )).
fof(duty_not_claim,       axiom, ! [P] : ~ ( duty(P)     & claim(P)    )).
fof(duty_not_no_right,    axiom, ! [P] : ~ ( duty(P)     & no_right(P) )).
fof(claim_not_no_right,   axiom, ! [P] : ~ ( claim(P)    & no_right(P) )).

% Within competence level
fof(power_not_subjection,     axiom, ! [P] : ~ ( power(P)      & subjection(P) )).
fof(power_not_immunity,       axiom, ! [P] : ~ ( power(P)      & immunity(P)   )).
fof(power_not_disability,     axiom, ! [P] : ~ ( power(P)      & disability(P) )).
fof(subjection_not_immunity,  axiom, ! [P] : ~ ( subjection(P) & immunity(P)   )).
fof(subjection_not_disability,axiom, ! [P] : ~ ( subjection(P) & disability(P) )).
fof(immunity_not_disability,  axiom, ! [P] : ~ ( immunity(P)   & disability(P) )).

% Conduct vs competence (16 pairs)
fof(cn_1,  axiom, ! [P] : ~ ( liberty(P)  & power(P)      )).
fof(cn_2,  axiom, ! [P] : ~ ( liberty(P)  & subjection(P) )).
fof(cn_3,  axiom, ! [P] : ~ ( liberty(P)  & immunity(P)   )).
fof(cn_4,  axiom, ! [P] : ~ ( liberty(P)  & disability(P) )).
fof(cn_5,  axiom, ! [P] : ~ ( duty(P)     & power(P)      )).
fof(cn_6,  axiom, ! [P] : ~ ( duty(P)     & subjection(P) )).
fof(cn_7,  axiom, ! [P] : ~ ( duty(P)     & immunity(P)   )).
fof(cn_8,  axiom, ! [P] : ~ ( duty(P)     & disability(P) )).
fof(cn_9,  axiom, ! [P] : ~ ( claim(P)    & power(P)      )).
fof(cn_10, axiom, ! [P] : ~ ( claim(P)    & subjection(P) )).
fof(cn_11, axiom, ! [P] : ~ ( claim(P)    & immunity(P)   )).
fof(cn_12, axiom, ! [P] : ~ ( claim(P)    & disability(P) )).
fof(cn_13, axiom, ! [P] : ~ ( no_right(P) & power(P)      )).
fof(cn_14, axiom, ! [P] : ~ ( no_right(P) & subjection(P) )).
fof(cn_15, axiom, ! [P] : ~ ( no_right(P) & immunity(P)   )).
fof(cn_16, axiom, ! [P] : ~ ( no_right(P) & disability(P) )).

% End of GRND000-0.ax
"""

def generate_fof() -> str:
    return "\n".join([
        fof_header(),
        FOF_SORT_GUARDS, FOF_RULE_PREDICATES, FOF_RELATOR_PREDICATES,
        FOF_RFR, FOF_DECL, FOF_NORMCONTENT, FOF_POSITION_DISJOINTNESS,
    ])


# ============================================================================
# SMT-LIB
# ============================================================================

def smt2_header() -> str:
    return textwrap.dedent(f"""\
        ; --------------------------------------------------------------------------
        ; File     : GRND000-0.smt2
        ; Domain   : {META['domain']}
        ; Problem  : Signature preamble — sorts, functions, rfr/decl axioms
        ; Version  : {META['version']}
        ; English  : SMT-LIB preamble. SMT-LIB has NO include directive.
        ;            Embedded verbatim at the top of every .smt2 problem file
        ;            by the problem generators. Do NOT add (check-sat) here.
        ;
        ; Source   : {META['source']}
        ; Generated: {date.today().isoformat()} by gen_signature.py
        ;
        ; Correspondence with GRND000-0.ax (FOF):
        ;   FOF guard predicate agent(X)  <->  (declare-sort Agent 0)
        ;   FOF perm(R)                   <->  (declare-fun perm (Rule) Bool)
        ;   FOF fof(rfr_irreflexive,...)  <->  (assert (forall ((a Action)) ...))
        ;   cnt/3 dual-sort              <->  cnt (Action) + cnt-f (Forbearance)
        ; --------------------------------------------------------------------------

        (set-logic UF)
        (set-info :source |{META['source']}|)
        (set-info :status unknown)

    """)

SMT2_SORTS = """\
; --------------------------------------------------------------------------
; SORTS — uninterpreted (closest to FOF guard predicates)
; --------------------------------------------------------------------------

(declare-sort Agent       0)
(declare-sort Action      0)
(declare-sort Forbearance 0)
(declare-sort Target      0)
(declare-sort Rule        0)
(declare-sort Position    0)
(declare-sort Relator     0)
(declare-sort Event       0)

"""

SMT2_RULE_PREDICATES = """\
; --------------------------------------------------------------------------
; ODRL RULE TYPE PREDICATES
; --------------------------------------------------------------------------

(declare-fun perm    (Rule) Bool)
(declare-fun proh    (Rule) Bool)
(declare-fun obl     (Rule) Bool)   ; CANONICAL — paper Ax5.4 uses ODRLDuty, must change to obl
(declare-fun has-rem (Rule) Bool)   ; CANONICAL — paper Ax5.7 uses rem, must change to has-rem

(declare-fun aee (Rule Agent)  Bool)
(declare-fun aer (Rule Agent)  Bool)
(declare-fun act (Rule Action) Bool)
(declare-fun tgt (Rule Target) Bool)

(declare-fun activates (Event Rule) Bool)

"""

SMT2_RELATOR_PREDICATES = """\
; --------------------------------------------------------------------------
; UFO RELATOR AND POSITION PREDICATES
; --------------------------------------------------------------------------

(declare-fun founds  (Event    Relator)            Bool)
(declare-fun part-of (Position Relator)            Bool)
(declare-fun bearer  (Position Agent)              Bool)
(declare-fun cnt     (Position Action      Target) Bool)  ; action content — CANONICAL
(declare-fun cnt-f   (Position Forbearance Target) Bool)  ; forbearance content
; cnt   = action content (permissions, obligations). Used in Ax5.1 for Liberty/NoRight too.
;         Paper uses about(l,a,t) in Ax5.1 — must be unified to cnt everywhere.
; cnt-f = forbearance content (prohibitions, Ax5.2).
; Two predicates because Action and Forbearance are distinct SMT-LIB sorts.
; In FOF (GRND000-0.ax), a single cnt/3 handles both via type guards.

(declare-fun liberty    (Position) Bool)
(declare-fun no-right   (Position) Bool)
(declare-fun duty       (Position) Bool)
(declare-fun claim      (Position) Bool)
(declare-fun power      (Position) Bool)
(declare-fun subjection (Position) Bool)
(declare-fun immunity   (Position) Bool)
(declare-fun disability (Position) Bool)

"""

SMT2_RFR = """\
; --------------------------------------------------------------------------
; RFR FUNCTION  rfr : Action -> Forbearance
; pos : Forbearance -> Action  (left-inverse of rfr)
;
; RFR1 holds automatically — Action and Forbearance are distinct sorts.
; RFR4, RFR5 hold by sort separation.
; --------------------------------------------------------------------------

(declare-fun rfr (Action)      Forbearance)
(declare-fun pos (Forbearance) Action)

; RFR2: Injectivity
(assert (forall ((a Action) (b Action))
  (=> (= (rfr a) (rfr b)) (= a b))))

; RFR3: Left-inverse
(assert (forall ((a Action))
  (= (pos (rfr a)) a)))

"""

SMT2_DECL = """\
; --------------------------------------------------------------------------
; DECL FUNCTION  decl : Action -> Action
; --------------------------------------------------------------------------

(declare-fun decl (Action) Action)

; DECL2: Injectivity
(assert (forall ((a Action) (b Action))
  (=> (= (decl a) (decl b)) (= a b))))

; DECL3: Distinctness
(assert (forall ((a Action))(not (= (decl a) a))))

"""

SMT2_POSITION_DISJOINTNESS = """\
; --------------------------------------------------------------------------
; POSITION SORT DISJOINTNESS
; --------------------------------------------------------------------------

; Within conduct level
(assert (forall ((p Position)) (not (and (liberty p)  (duty p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (claim p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (no-right p)))))
(assert (forall ((p Position)) (not (and (duty p)     (claim p)))))
(assert (forall ((p Position)) (not (and (duty p)     (no-right p)))))
(assert (forall ((p Position)) (not (and (claim p)    (no-right p)))))

; Within competence level
(assert (forall ((p Position)) (not (and (power p)      (subjection p)))))
(assert (forall ((p Position)) (not (and (power p)      (immunity p)))))
(assert (forall ((p Position)) (not (and (power p)      (disability p)))))
(assert (forall ((p Position)) (not (and (subjection p) (immunity p)))))
(assert (forall ((p Position)) (not (and (subjection p) (disability p)))))
(assert (forall ((p Position)) (not (and (immunity p)   (disability p)))))

; Conduct vs competence
(assert (forall ((p Position)) (not (and (liberty p)  (power p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (subjection p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (immunity p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (disability p)))))
(assert (forall ((p Position)) (not (and (duty p)     (power p)))))
(assert (forall ((p Position)) (not (and (duty p)     (subjection p)))))
(assert (forall ((p Position)) (not (and (duty p)     (immunity p)))))
(assert (forall ((p Position)) (not (and (duty p)     (disability p)))))
(assert (forall ((p Position)) (not (and (claim p)    (power p)))))
(assert (forall ((p Position)) (not (and (claim p)    (subjection p)))))
(assert (forall ((p Position)) (not (and (claim p)    (immunity p)))))
(assert (forall ((p Position)) (not (and (claim p)    (disability p)))))
(assert (forall ((p Position)) (not (and (no-right p) (power p)))))
(assert (forall ((p Position)) (not (and (no-right p) (subjection p)))))
(assert (forall ((p Position)) (not (and (no-right p) (immunity p)))))
(assert (forall ((p Position)) (not (and (no-right p) (disability p)))))

; --------------------------------------------------------------------------
; END OF PREAMBLE — problem files append axioms + conjecture after this
; --------------------------------------------------------------------------
"""

def generate_smt2() -> str:
    return "\n".join([
        smt2_header(),
        SMT2_SORTS, SMT2_RULE_PREDICATES, SMT2_RELATOR_PREDICATES,
        SMT2_RFR, SMT2_DECL, SMT2_POSITION_DISJOINTNESS,
    ])


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate GRND000-0.ax (FOF) and GRND000-0.smt2 (SMT-LIB) signatures."
    )
    parser.add_argument("--out-dir", default="../../Problems/DeonticOntology/Axioms")
    parser.add_argument("--stdout-fof",  action="store_true")
    parser.add_argument("--stdout-smt2", action="store_true")
    args = parser.parse_args()

    fof_content  = generate_fof()
    smt2_content = generate_smt2()

    if args.stdout_fof:
        print(fof_content); return
    if args.stdout_smt2:
        print(smt2_content); return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    fof_path  = out_dir / "GRND000-0.ax"
    smt2_path = out_dir / "GRND000-0.smt2"

    fof_path.write_text(fof_content,  encoding="utf-8")
    smt2_path.write_text(smt2_content, encoding="utf-8")

    print(f"Written: {fof_path}")
    print(f"  Lines: {fof_content.count(chr(10))}  FOF axioms: {fof_content.count('fof(')}")
    print(f"Written: {smt2_path}")
    print(f"  Lines: {smt2_content.count(chr(10))}  (assert): {smt2_content.count('(assert')}  (declare-): {smt2_content.count('(declare-')}")


if __name__ == "__main__":
    main()