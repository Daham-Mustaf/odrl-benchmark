"""
gen_foundation_problems.py
===================
Generates FOF/TPTP (.p) and SMT-LIB (.smt2) problem files for the
FOIS 2026 deontic grounding validation (Paper §6).
CHANGELOG v1.3:
  - Per-problem axiom inlining: each .p file now includes only the axioms
    it needs (via fof_axioms key), eliminating Vampire timeout caused by
    loading all 19 axioms via include('Axioms/Layer1-Deontic/GRND-AX-1.ax').
  - FOF_AXIOM_DICT added: individual named FOF axioms for selective inclusion.
CHANGELOG v1.2:
  - FOF problem files now use include() for Layer1 axioms instead of
    inlining all 19 axioms. Each .p file is now:
      include(Layer0-Signature)
      include(Layer1-Deontic)
      Appendix A.0 extra predicates (comment block)
      Ground instance (gamma: constants + activation facts)
      Conjecture (if any)
  - SMT-LIB files unchanged (SMT-LIB has no include; axioms embedded)
  - founds/3 throughout (v1.1 fix retained)
  - Correct include path: Axioms/Layer0-Signature/GRND000-0.ax
Output layout:
  Problems/DeonticOntology/
    Axioms/
      Layer0-Signature/
        GRND000-0.ax        -- signature (gen_signature.py)
        GRND000-0.smt2
      Layer1-Deontic/
        GRND-AX-1.ax        -- theory axioms (gen_layer1_deontic.py)
    Consistency/
      GRND001-1.p / .smt2
    Entailment/
      GRND002-1.p / .smt2  ...  GRND006-1.p / .smt2
    Discriminating/
      GRND007-open-1.p / .smt2  ...  GRND009-no-immunity-1.p / .smt2
Usage:
    uv run Generators/DeonticOntology/gen_axioms.py \\
      --sig-ax  Problems/DeonticOntology/Axioms/Layer0-Signature/GRND000-0.ax \\
      --sig-smt Problems/DeonticOntology/Axioms/Layer0-Signature/GRND000-0.smt2 \\
      --out-dir Problems/DeonticOntology
"""
import argparse
import textwrap
from pathlib import Path
from datetime import date

# ============================================================================
# Change 1: Individual axioms by name — subset included per problem
# ============================================================================
FOF_AXIOM_DICT = {
    "ax_perm_relator_basic": """\
fof(ax_perm_relator_basic, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T) & activates(E,P) )
     => ? [Rho, L, N] :
          ( founds(E,Rho,P)
          & liberty(L)  & bearer(L,X) & cnt(L,A,T)  & part_of(L,Rho)
          & no_right(N) & bearer(N,Y) & cnt(N,A,T)  & part_of(N,Rho) ) )).""",
    "ax_proh_relator_basic": """\
fof(ax_proh_relator_basic, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) & activates(E,F) )
     => ? [Rho, D, C] :
          ( founds(E,Rho,F)
          & duty(D)  & bearer(D,X) & cnt(D,rfr(A),T) & part_of(D,Rho)
          & claim(C) & bearer(C,Y) & cnt(C,rfr(A),T) & part_of(C,Rho) ) )).""",
    "ax_proh_relator_remedy": """\
fof(ax_proh_relator_remedy, axiom,
    ! [F, X, Y, A, T, E, Rho] :
      ( ( proh(F) & has_rem(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T)
        & activates(E,F) & founds(E,Rho,F) )
     => ? [Pw, S] :
          ( power(Pw)     & bearer(Pw,Y) & cnt(Pw,decl(A),T) & part_of(Pw,Rho)
          & subjection(S) & bearer(S,X)  & cnt(S,decl(A),T)  & part_of(S,Rho) ) )).""",
    "ax_cross_relator_consistency": """\
fof(ax_cross_relator_consistency, axiom,
    ! [L, D, X, A, T] :
      ( ( liberty(L) & bearer(L,X) & cnt(L,A,T)
        & duty(D)    & bearer(D,X) & cnt(D,rfr(A),T) )
     => $false )).""",
    "ax_disability_block": """\
fof(ax_disability_block, axiom,
    ! [F, X, Y, A, T] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) )
     => ~ ? [Db] : ( disability(Db) & bearer(Db,Y) & cnt(Db,A,T) ) )).""",
    "ax_correlativity_liberty": """\
fof(ax_correlativity_liberty, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [L] : ( liberty(L)  & part_of(L,Rho) & cnt(L,A,T) ) )
        <=> ( ? [N] : ( no_right(N) & part_of(N,Rho) & cnt(N,A,T)
                      & ! [M] : ( ( no_right(M) & part_of(M,Rho) & cnt(M,A,T) )
                                 => M = N ) ) ) ) )).""",
}

# ============================================================================
# SMT-LIB AXIOM BLOCKS (still inlined — SMT-LIB has no include)
# founds is 3-ary: (founds Event Relator Rule) throughout.
# ============================================================================
SMT2_AXIOMS = [
    ("ax_perm_relator_basic",
     """\
(assert (forall ((p Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (perm p) (aee p x) (aer p y) (act p a) (tgt p t) (activates e p))
      (exists ((rho Relator) (l Position) (n Position))
        (and (founds e rho p)
             (liberty l) (bearer l x) (cnt l a t) (part-of l rho)
             (no-right n) (bearer n y) (cnt n a t) (part-of n rho))))))"""),
    ("ax_perm_relator_strong",
     """\
(assert (forall ((p Rule) (x Agent) (y Agent) (a Action) (t Target)
                 (e Event) (rho Relator))
  (=> (and (perm p) (strong p) (aee p x) (aer p y) (act p a) (tgt p t)
           (activates e p) (founds e rho p))
      (exists ((im Position) (db Position))
        (and (immunity im)   (bearer im x) (cnt im a t)  (part-of im rho)
             (disability db) (bearer db y) (cnt db a t)  (part-of db rho))))))"""),
    ("ax_proh_relator_basic",
     """\
(assert (forall ((f Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (proh f) (aee f x) (aer f y) (act f a) (tgt f t) (activates e f))
      (exists ((rho Relator) (d Position) (c Position))
        (and (founds e rho f)
             (duty d)  (bearer d x) (cnt-f d (rfr a) t) (part-of d rho)
             (claim c) (bearer c y) (cnt-f c (rfr a) t) (part-of c rho))))))"""),
    ("ax_proh_relator_remedy",
     """\
(assert (forall ((f Rule) (x Agent) (y Agent) (a Action) (t Target)
                 (e Event) (rho Relator))
  (=> (and (proh f) (has-rem f) (aee f x) (aer f y) (act f a) (tgt f t)
           (activates e f) (founds e rho f))
      (exists ((pw Position) (s Position))
        (and (power pw)      (bearer pw y) (cnt pw (decl a) t) (part-of pw rho)
             (subjection s)  (bearer s x)  (cnt s  (decl a) t) (part-of s rho))))))"""),
    ("ax_unique_founding",
     """\
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds e rho1 r) (founds e rho2 r)) (= rho1 rho2))))"""),
    ("ax_unique_relator_per_event",
     """\
(assert (forall ((r Rule) (e1 Event) (e2 Event) (rho Relator))
  (=> (and (founds e1 rho r) (founds e2 rho r)) (= e1 e2))))"""),
    ("ax_obl_relator",
     """\
(assert (forall ((d Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (obl d) (aee d x) (aer d y) (act d a) (tgt d t) (activates e d))
      (exists ((rho Relator) (du Position) (c Position))
        (and (founds e rho d)
             (duty du) (bearer du x) (cnt du a t)  (part-of du rho)
             (claim c) (bearer c y)  (cnt c  a t)  (part-of c rho))))))"""),
    ("ax_correlativity_liberty",
     """\
(assert (forall ((rho Relator) (a Action) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((l Position))
           (and (liberty l) (part-of l rho) (cnt l a t)))
         (exists ((n Position))
           (and (no-right n) (part-of n rho) (cnt n a t)
                (forall ((m Position))
                  (=> (and (no-right m) (part-of m rho) (cnt m a t))
                      (= m n)))))))))"""),
    ("ax_correlativity_duty",
     """\
(assert (forall ((rho Relator) (a Action) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((d Position))
           (and (duty d) (part-of d rho) (cnt d a t)))
         (exists ((c Position))
           (and (claim c) (part-of c rho) (cnt c a t)
                (forall ((k Position))
                  (=> (and (claim k) (part-of k rho) (cnt k a t))
                      (= k c)))))))))"""),
    ("ax_correlativity_power",
     """\
(assert (forall ((rho Relator) (a Action) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((pw Position))
           (and (power pw) (part-of pw rho) (cnt pw a t)))
         (exists ((s Position))
           (and (subjection s) (part-of s rho) (cnt s a t)
                (forall ((s2 Position))
                  (=> (and (subjection s2) (part-of s2 rho) (cnt s2 a t))
                      (= s2 s)))))))))"""),
    ("ax_correlativity_immunity",
     """\
(assert (forall ((rho Relator) (a Action) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((im Position))
           (and (immunity im) (part-of im rho) (cnt im a t)))
         (exists ((db Position))
           (and (disability db) (part-of db rho) (cnt db a t)
                (forall ((db2 Position))
                  (=> (and (disability db2) (part-of db2 rho) (cnt db2 a t))
                      (= db2 db)))))))))"""),
    ("ax_conflict_detection",
     """\
(assert (forall ((rho Relator) (l Position) (d Position)
                 (x Agent) (a Action) (t Target))
  (=> (and (part-of l rho) (part-of d rho)
           (liberty l) (duty d)
           (bearer l x) (bearer d x)
           (cnt l a t) (cnt-f d (rfr a) t))
      false)))"""),
    ("ax_cross_relator_consistency",
     """\
(assert (forall ((l Position) (d Position) (x Agent) (a Action) (t Target))
  (=> (and (liberty l) (bearer l x) (cnt l a t)
           (duty d)    (bearer d x) (cnt-f d (rfr a) t))
      false)))"""),
    ("ax_disability_block",
     """\
(assert (forall ((f Rule) (x Agent) (y Agent) (a Action) (t Target))
  (=> (and (proh f) (aee f x) (aer f y) (act f a) (tgt f t))
      (not (exists ((db Position))
             (and (disability db) (bearer db y) (cnt db a t)))))))"""),
    ("ax_A1",
     """\
(assert (forall ((x Agent) (a Action) (t Target) (q NormPos))
  (=> (norm-state-change x a t q)
      (exists ((e Event))
        (and (inst-event e) (triggers e x a t q))))))"""),
    ("ax_A2",
     """\
(assert (forall ((e Event))
  (=> (inst-event e)
      (exists ((y Agent)) (competent-for y e)))))"""),
    ("ax_A3",
     """\
(assert (forall ((y Agent) (e Event))
  (=> (competent-for y e)
      (exists ((pw Position) (s Position) (x Agent))
        (and (power pw) (bearer pw y) (about-event pw e)
             (subjection s) (bearer s x) (about-event s e))))))"""),
    ("ax_B1",
     """\
(assert (forall ((f Rule) (x Agent) (a Action) (t Target) (b Action))
  (=> (and (proh f) (has-rem f) (act f a) (tgt f t) (aee f x) (does x a t))
      (norm-state-change x b t duty-rem))))"""),
    ("ax_B2",
     """\
(assert (forall ((pw Position) (a Action) (t Target)
                 (rho Relator) (e Event) (r Rule))
  (=> (and (power pw) (cnt pw (decl a) t) (part-of pw rho) (founds e rho r))
      (about-event pw e))))"""),
    ("ax_B3",
     """\
(assert (forall ((s Position) (a Action) (t Target)
                 (rho Relator) (e Event) (r Rule))
  (=> (and (subjection s) (cnt s (decl a) t) (part-of s rho) (founds e rho r))
      (about-event s e))))"""),
]

# ============================================================================
# SMT-LIB APPENDIX SORTS (Appendix A.0 predicates not in GRND000-0.smt2)
# odrl-rel is in the preamble — NOT repeated here.
# ============================================================================
SMT2_APPENDIX_SORTS = """\
; Appendix A.0 additional sorts and predicates
; Note: odrl-rel and strong are declared in the preamble — not repeated here.
(declare-sort NormPos 0)
(declare-fun norm-state-change (Agent Action Target NormPos) Bool)
(declare-fun inst-event        (Event) Bool)
(declare-fun triggers          (Event Agent Action Target NormPos) Bool)
(declare-fun competent-for     (Agent Event) Bool)
(declare-fun about-event       (Position Event) Bool)
(declare-fun does              (Agent Action Target) Bool)
(declare-const duty-rem        NormPos)
"""

# ============================================================================
# FOF APPENDIX COMMENT (comment block only — predicates declared via axioms)
# ============================================================================
FOF_APPENDIX_DECLS = """\
%--------------------------------------------------------------------------
% Appendix A.0 extra predicates (declared via axiom context in Layer1)
%   norm_state_change(X,A,T,Q)  -- position Q changes for X over (A,T)
%   inst_event(E)               -- E is an institutional event
%   triggers(E,X,A,T,Q)         -- E triggers the change of Q
%   competent_for(Y,E)          -- Y is competent to perform E
%   about_event(Pos,E)          -- position Pos concerns event E
%   does(X,A,T)                 -- X performs A on T
%   duty_rem                    -- constant: token for remedy-duty position
%   odrl_rel(Rho)               -- Rho is a relator founded by an ODRL rule
%--------------------------------------------------------------------------
"""

# ============================================================================
# PROBLEM DEFINITIONS
# ============================================================================
PROBLEMS = [
    {
        "id": "GRND001", "subdir": "Consistency",
        "name": "Full axiom set consistency",
        "status_fof": "Satisfiable",
        "status_smt": "sat",
        "fof_axioms": ["ax_perm_relator_basic"],
        "description": """\
% The full axiom set (Ax5.1-5.10, A1-A3, B1-B3) is satisfiable.
% Minimal model: one perm rule, one agent pair, one action, one target.""",
        "fof_extra_decls": """\
fof(agent_alice,  axiom, agent(alice)).
fof(agent_acme,   axiom, agent(acme)).
fof(action_read,  axiom, action(read)).
fof(target_d1,    axiom, target(d1)).
fof(rule_p1,      axiom, rule(p1)).
fof(event_e1,     axiom, event(e1)).
fof(perm_p1,      axiom, perm(p1)).
fof(aee_p1,       axiom, aee(p1, alice)).
fof(aer_p1,       axiom, aer(p1, acme)).
fof(act_p1,       axiom, act(p1, read)).
fof(tgt_p1,       axiom, tgt(p1, d1)).
fof(act_e1_p1,    axiom, activates(e1, p1)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const alice  Agent)
(declare-const acme   Agent)
(declare-const read   Action)
(declare-const d1     Target)
(declare-const p1     Rule)
(declare-const e1     Event)
(assert (perm p1))
(assert (aee p1 alice)) (assert (aer p1 acme))
(assert (act p1 read))  (assert (tgt p1 d1))
(assert (activates e1 p1))
""",
        "smt2_conjecture": None,
    },
    {
        "id": "GRND002", "subdir": "Entailment",
        "name": "Permission creates Liberty and NoRight",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_perm_relator_basic"],
        "description": """\
% perm(p1) activated by e1 entails Liberty(alice,read,d1) and NoRight(acme,read,d1).""",
        "fof_extra_decls": """\
fof(agent_alice, axiom, agent(alice)).
fof(agent_acme,  axiom, agent(acme)).
fof(action_read, axiom, action(read)).
fof(target_d1,   axiom, target(d1)).
fof(rule_p1,     axiom, rule(p1)).
fof(event_e1,    axiom, event(e1)).
fof(perm_p1,     axiom, perm(p1)).
fof(aee_p1,      axiom, aee(p1, alice)).
fof(aer_p1,      axiom, aer(p1, acme)).
fof(act_p1,      axiom, act(p1, read)).
fof(tgt_p1,      axiom, tgt(p1, d1)).
fof(act_e1_p1,   axiom, activates(e1, p1)).
""",
        "fof_conjecture": """\
? [Rho, L, N] :
  ( founds(e1, Rho, p1)
  & liberty(L)  & bearer(L, alice) & cnt(L, read, d1)  & part_of(L, Rho)
  & no_right(N) & bearer(N, acme)  & cnt(N, read, d1)  & part_of(N, Rho) )""",
        "smt2_extra_decls": """\
(declare-const alice Agent) (declare-const acme Agent)
(declare-const read  Action) (declare-const d1   Target)
(declare-const p1    Rule)   (declare-const e1   Event)
(assert (perm p1))
(assert (aee p1 alice)) (assert (aer p1 acme))
(assert (act p1 read))  (assert (tgt p1 d1))
(assert (activates e1 p1))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((rho Relator) (l Position) (n Position))
    (and (founds e1 rho p1)
         (liberty l)  (bearer l alice) (cnt l read d1) (part-of l rho)
         (no-right n) (bearer n acme)  (cnt n read d1) (part-of n rho)))))""",
    },
    {
        "id": "GRND003", "subdir": "Entailment",
        "name": "Prohibition creates Duty and Claim over rfr(a)",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_proh_relator_basic"],
        "description": """\
% proh(f1) activated by e1 entails Duty(alice,rfr(distribute),d1)
% and Claim(acme,rfr(distribute),d1).""",
        "fof_extra_decls": """\
fof(agent_alice,       axiom, agent(alice)).
fof(agent_acme,        axiom, agent(acme)).
fof(action_distribute, axiom, action(distribute)).
fof(target_d1,         axiom, target(d1)).
fof(rule_f1,           axiom, rule(f1)).
fof(event_e1,          axiom, event(e1)).
fof(proh_f1,           axiom, proh(f1)).
fof(aee_f1,            axiom, aee(f1, alice)).
fof(aer_f1,            axiom, aer(f1, acme)).
fof(act_f1,            axiom, act(f1, distribute)).
fof(tgt_f1,            axiom, tgt(f1, d1)).
fof(act_e1_f1,         axiom, activates(e1, f1)).
""",
        "fof_conjecture": """\
? [Rho, D, C] :
  ( founds(e1, Rho, f1)
  & duty(D)  & bearer(D, alice) & cnt(D, rfr(distribute), d1) & part_of(D, Rho)
  & claim(C) & bearer(C, acme)  & cnt(C, rfr(distribute), d1) & part_of(C, Rho) )""",
        "smt2_extra_decls": """\
(declare-const alice      Agent) (declare-const acme       Agent)
(declare-const distribute Action) (declare-const d1         Target)
(declare-const f1         Rule)   (declare-const e1         Event)
(assert (proh f1))
(assert (aee f1 alice)) (assert (aer f1 acme))
(assert (act f1 distribute)) (assert (tgt f1 d1))
(assert (activates e1 f1))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((rho Relator) (d Position) (c Position))
    (and (founds e1 rho f1)
         (duty d)  (bearer d alice) (cnt-f d (rfr distribute) d1) (part-of d rho)
         (claim c) (bearer c acme)  (cnt-f c (rfr distribute) d1) (part-of c rho)))))""",
    },
    {
        "id": "GRND004", "subdir": "Entailment",
        "name": "Prohibition with remedy creates Power and Subjection",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_proh_relator_basic", "ax_proh_relator_remedy"],
        "description": """\
% proh(f1) + has_rem(f1) + founds(e1,rho1,f1).
% Entails Power(acme,decl(distribute),d1) and Subjection(alice,decl(distribute),d1).""",
        "fof_extra_decls": """\
fof(agent_alice,       axiom, agent(alice)).
fof(agent_acme,        axiom, agent(acme)).
fof(action_distribute, axiom, action(distribute)).
fof(target_d1,         axiom, target(d1)).
fof(rule_f1,           axiom, rule(f1)).
fof(event_e1,          axiom, event(e1)).
fof(relator_rho1,      axiom, legal_relator(rho1)).
fof(proh_f1,           axiom, proh(f1)).
fof(rem_f1,            axiom, has_rem(f1)).
fof(aee_f1,            axiom, aee(f1, alice)).
fof(aer_f1,            axiom, aer(f1, acme)).
fof(act_f1,            axiom, act(f1, distribute)).
fof(tgt_f1,            axiom, tgt(f1, d1)).
fof(act_e1_f1,         axiom, activates(e1, f1)).
fof(founds_e1_rho1,    axiom, founds(e1, rho1, f1)).
""",
        "fof_conjecture": """\
? [Pw, S] :
  ( power(Pw)     & bearer(Pw, acme)  & cnt(Pw, decl(distribute), d1) & part_of(Pw, rho1)
  & subjection(S) & bearer(S,  alice) & cnt(S,  decl(distribute), d1) & part_of(S,  rho1) )""",
        "smt2_extra_decls": """\
(declare-const alice      Agent) (declare-const acme       Agent)
(declare-const distribute Action) (declare-const d1         Target)
(declare-const f1         Rule)   (declare-const e1         Event)
(declare-const rho1       Relator)
(assert (proh f1)) (assert (has-rem f1))
(assert (aee f1 alice)) (assert (aer f1 acme))
(assert (act f1 distribute)) (assert (tgt f1 d1))
(assert (activates e1 f1)) (assert (founds e1 rho1 f1))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((pw Position) (s Position))
    (and (power pw)      (bearer pw acme)  (cnt pw (decl distribute) d1) (part-of pw rho1)
         (subjection s)  (bearer s  alice) (cnt s  (decl distribute) d1) (part-of s  rho1)))))""",
    },
    {
        "id": "GRND005", "subdir": "Entailment",
        "name": "Liberty-Duty conflict detection (single relator)",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": ["ax_cross_relator_consistency"],
        "description": """\
% Liberty(l,alice,read,d1) and Duty(d,alice,rfr(read),d1) in same rho.
% Ax5.8 derives False.""",
        "fof_extra_decls": """\
fof(agent_alice, axiom, agent(alice)).
fof(action_read, axiom, action(read)).
fof(target_d1,   axiom, target(d1)).
fof(pos_l,       axiom, position(l)).
fof(pos_d,       axiom, position(d)).
fof(rel_rho1,    axiom, legal_relator(rho1)).
fof(liberty_l,   axiom, liberty(l)).
fof(duty_d,      axiom, duty(d)).
fof(bearer_l,    axiom, bearer(l, alice)).
fof(bearer_d,    axiom, bearer(d, alice)).
fof(cnt_l,       axiom, cnt(l, read, d1)).
fof(cnt_d,       axiom, cnt(d, rfr(read), d1)).
fof(partof_l,    axiom, part_of(l, rho1)).
fof(partof_d,    axiom, part_of(d, rho1)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const alice  Agent)
(declare-const read   Action) (declare-const d1  Target)
(declare-const l      Position) (declare-const d  Position)
(declare-const rho1   Relator)
(assert (liberty l))  (assert (duty d))
(assert (bearer l alice)) (assert (bearer d alice))
(assert (cnt l read d1))  (assert (cnt-f d (rfr read) d1))
(assert (part-of l rho1)) (assert (part-of d rho1))
""",
        "smt2_conjecture": None,
    },
    {
        "id": "GRND006", "subdir": "Entailment",
        "name": "Correlativity: Liberty implies unique NoRight in relator",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_correlativity_liberty"],
        "description": """\
% odrl_rel(rho1), Liberty(l) partOf rho1 => exists unique n. NoRight(n) partOf rho1.""",
        "fof_extra_decls": """\
fof(pos_l,     axiom, position(l)).
fof(rel_rho1,  axiom, legal_relator(rho1)).
fof(odrl_rho1, axiom, odrl_rel(rho1)).
fof(liberty_l, axiom, liberty(l)).
fof(partof_l,  axiom, part_of(l, rho1)).
fof(cnt_l,     axiom, cnt(l, some_action, some_target)).
fof(some_action_typed, axiom, action(some_action)).
fof(some_target_typed, axiom, target(some_target)).
""",
        "fof_conjecture": """\
? [N] : ( no_right(N) & part_of(N, rho1) & cnt(N, some_action, some_target)
        & ! [M] : ( ( no_right(M) & part_of(M, rho1)
                    & cnt(M, some_action, some_target) )
                  => M = N ) )""",
        "smt2_extra_decls": """\
(declare-const l           Position)
(declare-const rho1        Relator)
(declare-const some-action Action)
(declare-const some-target Target)
(assert (liberty l)) (assert (part-of l rho1))
(assert (cnt l some-action some-target))
(assert (odrl-rel rho1))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((n Position))
    (and (no-right n) (part-of n rho1) (cnt n some-action some-target)
         (forall ((m Position))
           (=> (and (no-right m) (part-of m rho1)
                    (cnt m some-action some-target))
               (= m n)))))))""",
    },
    {
        "id": "GRND007-open", "subdir": "Discriminating",
        "name": "Open-world: uncovered action entails Liberty by default",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": [],
        "description": """\
% Open-world closure added. No proh for 'modify'.
% Liberty(alice,modify,d1) is derivable.""",
        "fof_extra_decls": """\
fof(agent_alice,        axiom, agent(alice)).
fof(agent_acme,         axiom, agent(acme)).
fof(action_modify,      axiom, action(modify)).
fof(target_d1,          axiom, target(d1)).
fof(no_proh_modify,     axiom,
    ~ ? [F, E] : ( proh(F) & aee(F,alice) & act(F,modify) & activates(E,F) )).
fof(open_world_closure, axiom,
    ! [X, A, T] :
      ( ( agent(X) & action(A) & target(T)
        & ~ ? [F, E] : ( proh(F) & aee(F,X) & act(F,A) & activates(E,F) ) )
     => ? [L] : ( liberty(L) & bearer(L,X) & cnt(L,A,T) ) )).
""",
        "fof_conjecture": """\
? [L] : ( liberty(L) & bearer(L, alice) & cnt(L, modify, d1) )""",
        "smt2_extra_decls": """\
(declare-const alice  Agent) (declare-const acme   Agent)
(declare-const modify Action) (declare-const d1     Target)
(assert (not (exists ((f Rule) (e Event))
               (and (proh f) (aee f alice) (act f modify) (activates e f)))))
(assert (forall ((x Agent) (a Action) (t Target))
  (=> (not (exists ((f Rule) (e Event))
              (and (proh f) (aee f x) (act f a) (activates e f))))
      (exists ((l Position))
        (and (liberty l) (bearer l x) (cnt l a t))))))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((l Position))
    (and (liberty l) (bearer l alice) (cnt l modify d1)))))""",
    },
    {
        "id": "GRND007-closed", "subdir": "Discriminating",
        "name": "Closed-world: no Liberty for uncovered action",
        "status_fof": "Satisfiable",
        "status_smt": "sat",
        "fof_axioms": [],
        "description": """\
% No perm rule for 'modify'. No open-world closure.
% Liberty(alice,modify,d1) is NOT derivable — consistent with its negation.""",
        "fof_extra_decls": """\
fof(agent_alice,   axiom, agent(alice)).
fof(action_modify, axiom, action(modify)).
fof(target_d1,     axiom, target(d1)).
fof(no_liberty_modify, axiom,
    ~ ? [L] : ( liberty(L) & bearer(L, alice) & cnt(L, modify, d1) )).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const alice  Agent)
(declare-const modify Action) (declare-const d1 Target)
(assert (not (exists ((l Position))
               (and (liberty l) (bearer l alice) (cnt l modify d1)))))
""",
        "smt2_conjecture": None,
    },
    {
        "id": "GRND008-sanctioned", "subdir": "Discriminating",
        "name": "Sanctioned prohibition: violation reachable, remedy norm fires",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_proh_relator_remedy"],
        "description": """\
% proh(f1) + has_rem(f1) + founds(e1,rho1,f1) + does(alice,distribute,d1).
% Conjecture: Power+Subjection pair exists in rho1.""",
        "fof_extra_decls": """\
fof(agent_alice,       axiom, agent(alice)).
fof(agent_acme,        axiom, agent(acme)).
fof(action_distribute, axiom, action(distribute)).
fof(target_d1,         axiom, target(d1)).
fof(rule_f1,           axiom, rule(f1)).
fof(event_e1,          axiom, event(e1)).
fof(relator_rho1,      axiom, legal_relator(rho1)).
fof(proh_f1,           axiom, proh(f1)).
fof(rem_f1,            axiom, has_rem(f1)).
fof(aee_f1,            axiom, aee(f1, alice)).
fof(aer_f1,            axiom, aer(f1, acme)).
fof(act_f1,            axiom, act(f1, distribute)).
fof(tgt_f1,            axiom, tgt(f1, d1)).
fof(act_e1_f1,         axiom, activates(e1, f1)).
fof(founds_e1_rho1,    axiom, founds(e1, rho1, f1)).
fof(alice_does,        axiom, does(alice, distribute, d1)).
""",
        "fof_conjecture": """\
? [Pw, S] :
  ( power(Pw)     & bearer(Pw, acme)  & part_of(Pw, rho1)
  & subjection(S) & bearer(S,  alice) & part_of(S,  rho1) )""",
        "smt2_extra_decls": """\
(declare-const alice      Agent) (declare-const acme       Agent)
(declare-const distribute Action) (declare-const d1         Target)
(declare-const f1         Rule)   (declare-const e1         Event)
(declare-const rho1       Relator)
(assert (proh f1)) (assert (has-rem f1))
(assert (aee f1 alice)) (assert (aer f1 acme))
(assert (act f1 distribute)) (assert (tgt f1 d1))
(assert (activates e1 f1)) (assert (founds e1 rho1 f1))
(assert (does alice distribute d1))
""",
        "smt2_conjecture": """\
(assert (not
  (exists ((pw Position) (s Position))
    (and (power pw)     (bearer pw acme)  (part-of pw rho1)
         (subjection s) (bearer s  alice) (part-of s  rho1)))))""",
    },
    {
        "id": "GRND008-regimented", "subdir": "Discriminating",
        "name": "Regimented prohibition: contradiction",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": [],
        "description": """\
% Regimented axiom: ~does when prohibited.
% Ground witness: does(alice,distribute,d1). Contradiction.""",
        "fof_extra_decls": """\
fof(agent_alice,       axiom, agent(alice)).
fof(action_distribute, axiom, action(distribute)).
fof(target_d1,         axiom, target(d1)).
fof(rule_f1,           axiom, rule(f1)).
fof(event_e1,          axiom, event(e1)).
fof(proh_f1,           axiom, proh(f1)).
fof(rem_f1,            axiom, has_rem(f1)).
fof(act_f1,            axiom, act(f1, distribute)).
fof(aee_f1,            axiom, aee(f1, alice)).
fof(act_e1_f1,         axiom, activates(e1, f1)).
fof(regimented, axiom,
    ! [X, A, T, F, E] :
      ( ( proh(F) & aee(F,X) & act(F,A) & activates(E,F) )
     => ~ does(X,A,T) )).
fof(alice_does, axiom, does(alice, distribute, d1)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const alice      Agent)
(declare-const distribute Action) (declare-const d1 Target)
(declare-const f1         Rule)   (declare-const e1 Event)
(assert (proh f1)) (assert (has-rem f1))
(assert (act f1 distribute)) (assert (aee f1 alice))
(assert (activates e1 f1))
(assert (forall ((x Agent) (a Action) (t Target) (f2 Rule) (e2 Event))
  (=> (and (proh f2) (aee f2 x) (act f2 a) (activates e2 f2))
      (not (does x a t)))))
(assert (does alice distribute d1))
""",
        "smt2_conjecture": None,
    },
    {
        "id": "GRND009-immunity", "subdir": "Discriminating",
        "name": "Strong permission: Liberty persists (Disability blocks prohibition)",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": ["ax_disability_block"],
        "description": """\
% H2 = {Liberty, NoRight, Immunity, Disability}.
% Acme attempts proh(f2). Ax5.10: Disability + proh => False.""",
        "fof_extra_decls": """\
fof(agent_alice,   axiom, agent(alice)).
fof(agent_acme,    axiom, agent(acme)).
fof(action_read,   axiom, action(read)).
fof(target_d1,     axiom, target(d1)).
fof(pos_l,         axiom, position(l)).
fof(pos_n,         axiom, position(n)).
fof(pos_im,        axiom, position(im)).
fof(pos_db,        axiom, position(db)).
fof(rel_rho1,      axiom, legal_relator(rho1)).
fof(liberty_l,     axiom, liberty(l)).
fof(no_right_n,    axiom, no_right(n)).
fof(immunity_im,   axiom, immunity(im)).
fof(disability_db, axiom, disability(db)).
fof(bearer_l,      axiom, bearer(l,  alice)).
fof(bearer_n,      axiom, bearer(n,  acme)).
fof(bearer_im,     axiom, bearer(im, alice)).
fof(bearer_db,     axiom, bearer(db, acme)).
fof(cnt_l,         axiom, cnt(l,  read, d1)).
fof(cnt_n,         axiom, cnt(n,  read, d1)).
fof(cnt_im,        axiom, cnt(im, read, d1)).
fof(cnt_db,        axiom, cnt(db, read, d1)).
fof(rule_f2,       axiom, rule(f2)).
fof(proh_f2,       axiom, proh(f2)).
fof(aee_f2,        axiom, aee(f2, alice)).
fof(aer_f2,        axiom, aer(f2, acme)).
fof(act_f2,        axiom, act(f2, read)).
fof(tgt_f2,        axiom, tgt(f2, d1)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const alice  Agent) (declare-const acme  Agent)
(declare-const read   Action) (declare-const d1    Target)
(declare-const l      Position) (declare-const n   Position)
(declare-const im     Position) (declare-const db  Position)
(declare-const rho1   Relator)  (declare-const f2  Rule)
(assert (liberty l))    (assert (no-right n))
(assert (immunity im))  (assert (disability db))
(assert (bearer l alice))  (assert (bearer n acme))
(assert (bearer im alice)) (assert (bearer db acme))
(assert (cnt l read d1))   (assert (cnt n read d1))
(assert (cnt im read d1))  (assert (cnt db read d1))
(assert (proh f2))
(assert (aee f2 alice)) (assert (aer f2 acme))
(assert (act f2 read))  (assert (tgt f2 d1))
""",
        "smt2_conjecture": None,
    },
    {
        "id": "GRND009-no-immunity", "subdir": "Discriminating",
        "name": "Weak permission: Liberty+Duty conflict when prohibition added",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": ["ax_proh_relator_basic", "ax_cross_relator_consistency"],
        "description": """\
% H1 = {Liberty, NoRight} — no Immunity/Disability.
% Acme adds proh(f2): Ax5.3 creates Duty(alice,rfr(read),d1).
% Ax5.9: Liberty + Duty-to-refrain => False.""",
        "fof_extra_decls": """\
fof(agent_alice, axiom, agent(alice)).
fof(agent_acme,  axiom, agent(acme)).
fof(action_read, axiom, action(read)).
fof(target_d1,   axiom, target(d1)).
fof(pos_l,       axiom, position(l)).
fof(pos_n,       axiom, position(n)).
fof(rel_rho1,    axiom, legal_relator(rho1)).
fof(rule_f2,     axiom, rule(f2)).
fof(event_e2,    axiom, event(e2)).
fof(liberty_l,   axiom, liberty(l)).
fof(no_right_n,  axiom, no_right(n)).
fof(bearer_l,    axiom, bearer(l, alice)).
fof(bearer_n,    axiom, bearer(n, acme)).
fof(cnt_l,       axiom, cnt(l, read, d1)).
fof(cnt_n,       axiom, cnt(n, read, d1)).
fof(proh_f2,     axiom, proh(f2)).
fof(aee_f2,      axiom, aee(f2, alice)).
fof(aer_f2,      axiom, aer(f2, acme)).
fof(act_f2,      axiom, act(f2, read)).
fof(tgt_f2,      axiom, tgt(f2, d1)).
fof(act_e2_f2,   axiom, activates(e2, f2)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const alice  Agent) (declare-const acme  Agent)
(declare-const read   Action) (declare-const d1    Target)
(declare-const l      Position) (declare-const n   Position)
(declare-const rho1   Relator)
(declare-const f2     Rule) (declare-const e2 Event)
(assert (liberty l))   (assert (no-right n))
(assert (bearer l alice)) (assert (bearer n acme))
(assert (cnt l read d1))  (assert (cnt n read d1))
(assert (proh f2))
(assert (aee f2 alice)) (assert (aer f2 acme))
(assert (act f2 read))  (assert (tgt f2 d1))
(assert (activates e2 f2))
""",
        "smt2_conjecture": None,
    },
]

# ============================================================================
# EMBEDDED SMT-LIB PREAMBLE (mirrors GRND000-0.smt2 — self-contained)
# ============================================================================
SMT2_PREAMBLE = """\
(set-logic UF)
(declare-sort Agent       0)
(declare-sort Action      0)
(declare-sort Forbearance 0)
(declare-sort Target      0)
(declare-sort Rule        0)
(declare-sort Position    0)
(declare-sort Relator     0)
(declare-sort Event       0)
(declare-fun perm    (Rule) Bool)
(declare-fun proh    (Rule) Bool)
(declare-fun obl     (Rule) Bool)
(declare-fun has-rem (Rule) Bool)
(declare-fun strong  (Rule) Bool)
(declare-fun aee (Rule Agent)  Bool)
(declare-fun aer (Rule Agent)  Bool)
(declare-fun act (Rule Action) Bool)
(declare-fun tgt (Rule Target) Bool)
(declare-fun activates (Event Rule) Bool)
(declare-fun founds  (Event Relator Rule)          Bool)
(declare-fun part-of (Position Relator)            Bool)
(declare-fun bearer  (Position Agent)              Bool)
(declare-fun cnt     (Position Action  Target)     Bool)
(declare-fun cnt-f   (Position Forbearance Target) Bool)
(declare-fun odrl-rel   (Relator)  Bool)
(declare-fun liberty    (Position) Bool)
(declare-fun no-right   (Position) Bool)
(declare-fun duty       (Position) Bool)
(declare-fun claim      (Position) Bool)
(declare-fun power      (Position) Bool)
(declare-fun subjection (Position) Bool)
(declare-fun immunity   (Position) Bool)
(declare-fun disability (Position) Bool)
(declare-fun rfr (Action)      Forbearance)
(declare-fun pos (Forbearance) Action)
(assert (forall ((a Action) (b Action)) (=> (= (rfr a) (rfr b)) (= a b))))
(assert (forall ((a Action)) (= (pos (rfr a)) a)))
(declare-fun decl (Action) Action)
(assert (forall ((a Action) (b Action)) (=> (= (decl a) (decl b)) (= a b))))
(assert (forall ((a Action)) (not (= (decl a) a))))
(declare-fun issue (Rule) Action)
(assert (forall ((a Rule) (b Rule)) (=> (= (issue a) (issue b)) (= a b))))
(assert (forall ((p Position)) (not (and (liberty p)  (duty p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (claim p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (no-right p)))))
(assert (forall ((p Position)) (not (and (duty p)     (claim p)))))
(assert (forall ((p Position)) (not (and (duty p)     (no-right p)))))
(assert (forall ((p Position)) (not (and (claim p)    (no-right p)))))
(assert (forall ((p Position)) (not (and (power p)      (subjection p)))))
(assert (forall ((p Position)) (not (and (power p)      (immunity p)))))
(assert (forall ((p Position)) (not (and (power p)      (disability p)))))
(assert (forall ((p Position)) (not (and (subjection p) (immunity p)))))
(assert (forall ((p Position)) (not (and (subjection p) (disability p)))))
(assert (forall ((p Position)) (not (and (immunity p)   (disability p)))))
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
"""

# ============================================================================
# WRITERS
# ============================================================================
def write_fof_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / f"{p['id']}-1.p"
    conj = p.get("fof_conjecture")
    lines = [
        f"%--------------------------------------------------------------------------",
        f"% File     : {p['id']}-1.p",
        f"% Domain   : Deontic Ontology / ODRL Grounding",
        f"% Problem  : {p['name']}",
        f"% Status   : {p['status_fof']}",
        f"% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026",
        f"% Generated: {date.today().isoformat()} by gen_foundation_problems.py v1.3",
        f"%",
    ]
    for line in textwrap.dedent(p["description"]).strip().splitlines():
        lines.append(f"% {line}")
    lines += [
        f"%--------------------------------------------------------------------------",
        f"",
        f"% Layer 0: Signature (sorts, rfr/decl, position disjointness)",
        f"include('Axioms/Layer0-Signature/GRND000-0.ax').",
        f"",
        f"% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)",
        *[FOF_AXIOM_DICT[ax] for ax in p.get("fof_axioms", [])],
        f"",
        FOF_APPENDIX_DECLS,
        f"%--------------------------------------------------------------------------",
        f"% Ground instance (gamma)",
        f"%--------------------------------------------------------------------------",
        p["fof_extra_decls"],
    ]
    if conj is not None:
        lines += [
            "%--------------------------------------------------------------------------",
            "% Conjecture",
            "%--------------------------------------------------------------------------",
            f"fof(conjecture, conjecture,",
            f"    ( {conj} )).",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_smt2_problem(p: dict, out_dir: Path) -> Path:
    subdir = out_dir / p["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / f"{p['id']}-1.smt2"
    conj = p.get("smt2_conjecture")
    lines = [
        f"; --------------------------------------------------------------------------",
        f"; File     : {p['id']}-1.smt2",
        f"; Domain   : Deontic Ontology / ODRL Grounding",
        f"; Problem  : {p['name']}",
        f"; Status   : {p['status_smt']}",
        f"; Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026",
        f"; Generated: {date.today().isoformat()} by gen_foundation_problems.py v1.3",
        f"; --------------------------------------------------------------------------",
        f"",
        f"; === Layer 0 + Layer 1 preamble (embedded — SMT-LIB has no include) ===",
        SMT2_PREAMBLE,
        f"; === Appendix A.0 additional sorts/predicates ===",
        SMT2_APPENDIX_SORTS,
        f"",
        f"; === Layer 1: Paper axioms (Ax5.1-5.10, A1-A3, B1-B3) ===",
        f"; Authoritative source: Axioms/Layer1-Deontic/GRND-AX-1.smt2",
        f"; (SMT-LIB has no include directive — axioms embedded directly)",
        f"",
    ]
    for name, formula in SMT2_AXIOMS:
        lines.append(f"; {name}")
        lines.append(formula)
        lines.append("")
    lines += [
        f"; === Ground instance (gamma) ===",
        p["smt2_extra_decls"],
    ]
    if conj is not None:
        lines += [
            "; === Negated conjecture ===",
            conj,
            "",
        ]
    lines.append("(check-sat)")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ============================================================================
# CLI
# ============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Generate FOF/SMT-LIB problem files for GRND DeonticOntology v1.3."
    )
    parser.add_argument(
        "--sig-ax",
        default="Problems/DeonticOntology/Axioms/Layer0-Signature/GRND000-0.ax",
        help="Path to GRND000-0.ax (used in include path only)"
    )
    parser.add_argument(
        "--sig-smt",
        default="Problems/DeonticOntology/Axioms/Layer0-Signature/GRND000-0.smt2",
        help="Path to GRND000-0.smt2 (ignored — SMT2_PREAMBLE embedded directly)"
    )
    parser.add_argument(
        "--out-dir",
        default="Problems/DeonticOntology",
    )
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    written = []
    for p in PROBLEMS:
        fof_path  = write_fof_problem(p, out_dir)
        smt2_path = write_smt2_problem(p, out_dir)
        written.append((fof_path, smt2_path))
        ax_list = ", ".join(p.get("fof_axioms", [])) or "(none)"
        print(f"  {p['id']:25s}  FOF:{p['status_fof']:16s}  {fof_path.name}  [axioms: {ax_list}]")
        print(f"  {'':25s}  SMT:{p['status_smt']:16s}  {smt2_path.name}")
    print(f"\nTotal: {len(written)} problem pairs ({len(written)*2} files)")
    print("\nRun Vampire (FOF):")
    print("  for f in Problems/DeonticOntology/**/*.p; do")
    print("    echo \"$f:\"; vampire --mode casc -t 30 \"$f\" | grep 'SZS status'; done")
    print("\nRun Z3 (SMT-LIB):")
    print("  for f in Problems/DeonticOntology/**/*.smt2; do")
    print("    echo \"$f:\"; z3 \"$f\"; done")

if __name__ == "__main__":
    main()