"""
axiom_data.py
=============
Shared axiom content for the FOIS 2026 deontic grounding benchmark.
Imported by:
  - gen_foundation_problems.py  (problem generation)
  - gen_layer1_deontic.py       (GRND-AX-1.smt2 reference copy)

Contents:
  FOF_AXIOM_DICT      — named FOF axioms for per-problem selective inclusion
  SMT2_AXIOMS         — SMT-LIB axiom blocks (embedded in every .smt2 file)
  SMT2_APPENDIX_SORTS — Appendix A.0 sort/predicate declarations
  FOF_APPENDIX_DECLS  — Appendix A.0 comment block for .p files
"""

# ============================================================================
# FOF: individual axioms by name — subset included per problem
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
# SMT-LIB: axiom blocks — embedded in every .smt2 problem file
# founds is 3-ary: (founds Event Relator Rule) throughout.
# Authoritative source: Axioms/Layer1-Deontic/GRND-AX-1.smt2
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
# SMT-LIB: Appendix A.0 sort/predicate declarations
# odrl-rel and strong are declared in the preamble — not repeated here.
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
# FOF: Appendix A.0 comment block for .p files
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
