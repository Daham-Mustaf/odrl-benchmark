"""
problem_data.py
===============
Problem definitions for the FOIS 2026 deontic grounding benchmark.
Each problem dict contains:
  id, subdir, name, status_fof, status_smt
  fof_axioms        — axiom keys from axiom_data.FOF_AXIOM_DICT
  description       — comment lines for .p / .smt2 header
  ttl               — real Turtle policy (written to Policies/ directory)
  fof_extra_decls   — FOF ground instance
  fof_conjecture    — FOF conjecture string or None
  smt2_extra_decls  — SMT-LIB ground instance
  smt2_conjecture   — SMT-LIB negated conjecture or None

DRK ontology entities used:
  Prefix  drk:    <http://w3id.org/drk/ontology/>
  Classes dcat:Dataset, dcat:DataService, schema:Organization
  Only classes/properties defined in the DRK ontology or imported vocabs.

Imported by: writers.py, gen_foundation_problems.py
"""
from pathlib import Path
from datetime import date

# ============================================================================
# TTL WRITER — saves real Turtle policy files
# ============================================================================
def write_ttl_policy(p: dict, out_dir: Path) -> Path | None:
    """Write a real .ttl policy file for problem p into out_dir/Policies/."""
    ttl = p.get("ttl")
    if not ttl:
        return None
    subdir = out_dir / "Policies"
    subdir.mkdir(parents=True, exist_ok=True)
    path = subdir / f"{p['id']}-policy.ttl"
    header = (
        f"# ------------------------------------------------------------------------------\n"
        f"# File     : {p['id']}-policy.ttl\n"
        f"# Domain   : Deontic Ontology / ODRL Grounding\n"
        f"# Problem  : {p['name']}\n"
        f"# Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026\n"
        f"# Generated: {date.today().isoformat()} by gen_foundation_problems.py\n"
        f"# Links    : {p['subdir']}/{p['id']}-1.p\n"
        f"#            {p['subdir']}/{p['id']}-1.smt2\n"
        f"# ------------------------------------------------------------------------------\n\n"
    )
    path.write_text(header + ttl.strip() + "\n", encoding="utf-8")
    return path


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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .

<drk:policy-theater-read> a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:BerlinerEnsemble> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:TheaterShowtimeDataset> ] .

<drk:TheaterShowtimeDataset>          a dcat:Dataset ;
    schema:name "Berliner Ensemble Showtime Dataset" .
<drk:BerlinerEnsemble>                a schema:Organization .
<drk:UniversitaetsbibliothekMuenchen> a schema:Organization .""",
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
(declare-const alice  Agent) (declare-const acme  Agent)
(declare-const read   Action) (declare-const d1   Target)
(declare-const p1     Rule)   (declare-const e1   Event)
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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .

# Same policy as GRND001 — different question asked (entailment)
<drk:policy-theater-read> a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:BerlinerEnsemble> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:TheaterShowtimeDataset> ] .

<drk:TheaterShowtimeDataset>          a dcat:Dataset ;
    schema:name "Berliner Ensemble Showtime Dataset" .
<drk:BerlinerEnsemble>                a schema:Organization .
<drk:UniversitaetsbibliothekMuenchen> a schema:Organization .""",
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
(declare-const alice Agent) (declare-const acme  Agent)
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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .

<drk:policy-no-distribute> a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:StreamingPortalGmbH> ;
        odrl:assigner <drk:StaatlicheMuseenBerlin> ;
        odrl:action   odrl:distribute ;
        odrl:target   <drk:MuseumCollectionAPI> ] .

<drk:MuseumCollectionAPI>    a dcat:DataService ;
    schema:name "Staatliche Museen Berlin Collection API" .
<drk:StaatlicheMuseenBerlin> a schema:Organization .
<drk:StreamingPortalGmbH>    a schema:Organization .""",
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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .

<drk:policy-concert-remedy> a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:MusicMarketplaceAG> ;
        odrl:assigner <drk:PhilharmonieBerlin> ;
        odrl:action   odrl:distribute ;
        odrl:target   <drk:ConcertRecordingDataset> ;
        odrl:remedy   [ a odrl:Duty ;
            odrl:action odrl:compensate ] ] .

<drk:ConcertRecordingDataset> a dcat:Dataset ;
    schema:name "Philharmonie Berlin Concert Recordings" .
<drk:PhilharmonieBerlin>  a schema:Organization .
<drk:MusicMarketplaceAG>  a schema:Organization .""",
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
% Ax5.9 derives False.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .

# Conflict witness — not a valid standalone policy.
# Ground instance asserts:
#   Liberty(drk:UniversitaetsbibliothekMuenchen,
#           read, drk:TheaterShowtimeDataset)
# AND
#   Duty(drk:UniversitaetsbibliothekMuenchen,
#        rfr(read), drk:TheaterShowtimeDataset)
# in the same relator. Ax5.9 derives False.""",
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
(declare-const read   Action) (declare-const d1   Target)
(declare-const l      Position) (declare-const d   Position)
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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .

<drk:policy-corr> a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:BerlinerEnsemble> ;
        odrl:action   odrl:use ;
        odrl:target   <drk:PlayProductionMetadataDataset> ] .

<drk:PlayProductionMetadataDataset>   a dcat:Dataset ;
    schema:name "Berliner Ensemble Play Production Metadata" .
<drk:BerlinerEnsemble>                a schema:Organization .
<drk:UniversitaetsbibliothekMuenchen> a schema:Organization .
# Liberty(Bibliothek) entails unique NoRight(Ensemble) in relator.""",
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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .

# behaviour=open policy over drk:TheaterShowtimeDataset.
# No prohibition on odrl:modify declared.
# => Liberty(drk:StreamingPortalGmbH, modify,
#            drk:TheaterShowtimeDataset) derivable by default.""",
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
(declare-const modify Action) (declare-const d1    Target)
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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .

# behaviour=closed policy over drk:TheaterShowtimeDataset.
# No permission for odrl:modify declared.
# => Liberty(drk:StreamingPortalGmbH, modify,
#            drk:TheaterShowtimeDataset) NOT derivable.""",
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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .

<drk:policy-sanctioned> a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:MusicMarketplaceAG> ;
        odrl:assigner <drk:PhilharmonieBerlin> ;
        odrl:action   odrl:distribute ;
        odrl:target   <drk:ConcertRecordingDataset> ;
        odrl:remedy   [ a odrl:Duty ;
            odrl:action odrl:compensate ] ] .

<drk:ConcertRecordingDataset> a dcat:Dataset ;
    schema:name "Philharmonie Berlin Concert Recordings" .
<drk:PhilharmonieBerlin> a schema:Organization .
<drk:MusicMarketplaceAG> a schema:Organization .
# drk:MusicMarketplaceAG performs distribute => violation reachable.
# Power(drk:PhilharmonieBerlin, decl(distribute)) constituted at activation.""",
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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .

<drk:policy-regimented> a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:MusicMarketplaceAG> ;
        odrl:action   odrl:distribute ;
        odrl:target   <drk:ConcertRecordingDataset> ] .

<drk:ConcertRecordingDataset> a dcat:Dataset .
<drk:MusicMarketplaceAG>      a schema:Organization .
# Regimented reading: does(MusicMarketplaceAG, distribute) impossible.
# Ground witness asserts it => contradiction.""",
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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .

<drk:policy-strong> a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:StaatlicheMuseenBerlin> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:MuseumCollectionAPI> ] .

<drk:MuseumCollectionAPI>             a dcat:DataService ;
    schema:name "Staatliche Museen Berlin Collection API" .
<drk:StaatlicheMuseenBerlin>          a schema:Organization .
<drk:UniversitaetsbibliothekMuenchen> a schema:Organization .
# strong(p) asserted (profile extension, not ODRL 2.2).
# Immunity(Bibliothek) + Disability(Museen).
# StaatlicheMuseenBerlin attempts prohibition => blocked by Disability.""",
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
(declare-const read   Action) (declare-const d1   Target)
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
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .

<drk:policy-conflict> a odrl:Agreement ;
    odrl:permission  [ a odrl:Permission ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:StaatlicheMuseenBerlin> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:MuseumCollectionAPI> ] ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:StaatlicheMuseenBerlin> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:MuseumCollectionAPI> ] .

<drk:MuseumCollectionAPI>             a dcat:DataService .
<drk:StaatlicheMuseenBerlin>          a schema:Organization .
<drk:UniversitaetsbibliothekMuenchen> a schema:Organization .
# Weak permission (no Immunity/Disability).
# Prohibition creates Duty(rfr(read)) => Liberty + Duty conflict => False.""",
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
(declare-const read   Action) (declare-const d1   Target)
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
