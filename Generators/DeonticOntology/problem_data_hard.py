"""
problem_data_hard.py
====================
Hard/medium problems for the PAAR 2026 automated reasoning track.
These test deeper inference chains, multi-relator reasoning,
and untested functions (issue/1).
  GRND019  Two policies conflict via assigner Right          Hard
  GRND020  Strong perm + prohibition attempt = Unsat (H2)   Medium
  GRND021  Full A1-B1-B2-B3 violation-to-remedy chain       Hard
  GRND022  Correlativity blocks non-unique NoRight           Medium
  GRND023  Policy issuance Power (P3-P4, issue/1)           Hard
  GRND024  obl + proh on same target = conflict             Medium

Fix history:
  Bug 1 — GRND019: liberty -> permission (UFO-L terms)
  Bug 2 — GRND022: ax_correlativity_liberty -> ax_correlativity_permission;
           liberty -> permission
  Bug 3 — GRND023: SMT2 conjecture was (not (= (issue pi) (issue pi))) —
           trivially (assert false). Replaced with injectivity negation
           using two distinct rule constants.
  Note  — GRND020/GRND021: founds(e1,rho1,...) assertions are redundant
           (Ax5.2 and Ax5.4 fire from activates alone after Bug 4/5 fixes)
           but harmless — retained for explicitness.
"""

PROBLEMS_HARD = [
    # =========================================================================
    # GRND019 — Two policies conflict via assigner Right
    # Difficulty: Hard
    # Bug 1 fix: liberty -> permission throughout
    # =========================================================================
    {
        "id": "GRND019-two-policy-conflict", "subdir": "Discriminating",
        "name": "Two policies conflict: competing Rights from distinct assigners",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": [
            "ax_proh_relator_basic",
            "ax_cross_relator_consistency",
        ],
        "description": """\
% Two prohibitions over the same (alice, read, d1):
%   f1: assigner acme1, activates at e1 => Duty(alice,rfr(read),d1) + Right(acme1,...)
%   f2: assigner acme2, activates at e2 => Duty(alice,rfr(read),d1) + Right(acme2,...)
% alice also holds Permission(alice,read,d1).
% ax_cross_relator_consistency: Permission + Duty(rfr) => False.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Two competing prohibitions from different assigners over the same asset.
# Combined with an existing Permission => conflict.
<drk:policy-conflict-two> a odrl:Agreement ;
    odrl:permission  [ a odrl:Permission ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:BerlinerEnsemble> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:TheaterShowtimeDataset> ] ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:StaatlicheMuseenBerlin> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:TheaterShowtimeDataset> ] ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:PhilharmonieBerlin> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:TheaterShowtimeDataset> ] .
<drk:TheaterShowtimeDataset>          a dcat:Dataset .
<drk:BerlinerEnsemble>                a schema:Organization .
<drk:StaatlicheMuseenBerlin>          a schema:Organization .
<drk:PhilharmonieBerlin>              a schema:Organization .
<drk:UniversitaetsbibliothekMuenchen> a schema:Organization .""",
        "fof_extra_decls": """\
fof(agent_alice,  axiom, agent(alice)).
fof(agent_acme1,  axiom, agent(acme1)).
fof(agent_acme2,  axiom, agent(acme2)).
fof(action_read,  axiom, action(read)).
fof(target_d1,    axiom, target(d1)).
% Existing permission (Bug 1 fix: was liberty)
fof(pos_l,        axiom, position(l)).
fof(permission_l, axiom, permission(l)).
fof(bearer_l,     axiom, bearer(l, alice)).
fof(cnt_l,        axiom, cnt(l, read, d1)).
% Prohibition 1: acme1 prohibits alice from reading d1
fof(rule_f1,      axiom, rule(f1)).
fof(event_e1,     axiom, event(e1)).
fof(proh_f1,      axiom, proh(f1)).
fof(aee_f1,       axiom, aee(f1, alice)).
fof(aer_f1,       axiom, aer(f1, acme1)).
fof(act_f1,       axiom, act(f1, read)).
fof(tgt_f1,       axiom, tgt(f1, d1)).
fof(act_e1_f1,    axiom, activates(e1, f1)).
% Prohibition 2: acme2 also prohibits alice from reading d1
fof(rule_f2,      axiom, rule(f2)).
fof(event_e2,     axiom, event(e2)).
fof(proh_f2,      axiom, proh(f2)).
fof(aee_f2,       axiom, aee(f2, alice)).
fof(aer_f2,       axiom, aer(f2, acme2)).
fof(act_f2,       axiom, act(f2, read)).
fof(tgt_f2,       axiom, tgt(f2, d1)).
fof(act_e2_f2,    axiom, activates(e2, f2)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const alice  Agent)
(declare-const acme1  Agent) (declare-const acme2  Agent)
(declare-const read   Action) (declare-const d1    Target)
(declare-const l      Position)
(declare-const f1     Rule) (declare-const e1 Event)
(declare-const f2     Rule) (declare-const e2 Event)
; Existing permission for alice (Bug 1 fix: was liberty)
(assert (permission l)) (assert (bearer l alice)) (assert (cnt l read d1))
; Prohibition 1
(assert (proh f1))
(assert (aee f1 alice)) (assert (aer f1 acme1))
(assert (act f1 read))  (assert (tgt f1 d1))
(assert (activates e1 f1))
; Prohibition 2
(assert (proh f2))
(assert (aee f2 alice)) (assert (aer f2 acme2))
(assert (act f2 read))  (assert (tgt f2 d1))
(assert (activates e2 f2))
""",
        "smt2_conjecture": None,
    },
    # =========================================================================
    # GRND020 — Strong perm + prohibition attempt = Unsatisfiable (full H2)
    # Difficulty: Medium
    # Note: founds(e1,rho1,p1) is redundant (Ax5.2 fires from activates alone)
    # but retained for explicitness. Ax5.2 produces rho_I via founds_imm;
    # Disability(acme,read,d1) ends up in rho_I. ax_disability_block then
    # fires: proh(f2) & aer(f2,acme) & Disability(acme,read,d1) => False.
    # =========================================================================
    {
        "id": "GRND020-strong-perm-full-h2", "subdir": "Discriminating",
        "name": "Strong permission full H2: Disability blocks same assigner prohibition",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": [
            "ax_perm_relator_basic",
            "ax_perm_relator_strong",
            "ax_disability_block",
        ],
        "description": """\
% perm(p1) + strong(p1) + activates(e1,p1).
% Ax5.2 (founds_imm): creates rho_I with Immunity(alice,read,d1)
%                     and Disability(acme,read,d1).
% proh(f2) with aer(f2,acme) also asserted.
% ax_disability_block: Disability(acme,read,d1) + proh(f2,aer=acme) => False.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Strong permission: assigner holds Disability over the asset.
# Assigner then attempts to issue a prohibition => blocked.
<drk:policy-strong-h2> a odrl:Agreement ;
    odrl:permission [ a odrl:Permission ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:StaatlicheMuseenBerlin> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:MuseumCollectionAPI> ] .
# strong(p) asserted by profile extension.
# StaatlicheMuseenBerlin then attempts prohibition => contradiction.
<drk:MuseumCollectionAPI>             a dcat:DataService .
<drk:StaatlicheMuseenBerlin>          a schema:Organization .
<drk:UniversitaetsbibliothekMuenchen> a schema:Organization .""",
        "fof_extra_decls": """\
fof(agent_alice,  axiom, agent(alice)).
fof(agent_acme,   axiom, agent(acme)).
fof(action_read,  axiom, action(read)).
fof(target_d1,    axiom, target(d1)).
fof(rule_p1,      axiom, rule(p1)).
fof(event_e1,     axiom, event(e1)).
fof(relator_rho1, axiom, legal_relator(rho1)).
fof(perm_p1,      axiom, perm(p1)).
fof(strong_p1,    axiom, strong(p1)).
fof(aee_p1,       axiom, aee(p1, alice)).
fof(aer_p1,       axiom, aer(p1, acme)).
fof(act_p1,       axiom, act(p1, read)).
fof(tgt_p1,       axiom, tgt(p1, d1)).
fof(act_e1_p1,    axiom, activates(e1, p1)).
fof(founds_e1,    axiom, founds(e1, rho1, p1)).
% acme now attempts a prohibition — blocked by Disability from Ax5.2
fof(rule_f2,      axiom, rule(f2)).
fof(proh_f2,      axiom, proh(f2)).
fof(aee_f2,       axiom, aee(f2, alice)).
fof(aer_f2,       axiom, aer(f2, acme)).
fof(act_f2,       axiom, act(f2, read)).
fof(tgt_f2,       axiom, tgt(f2, d1)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const alice  Agent) (declare-const acme  Agent)
(declare-const read   Action) (declare-const d1   Target)
(declare-const p1     Rule)   (declare-const e1   Event)
(declare-const rho1   Relator)
(declare-const f2     Rule)
(assert (perm p1)) (assert (strong p1))
(assert (aee p1 alice)) (assert (aer p1 acme))
(assert (act p1 read))  (assert (tgt p1 d1))
(assert (activates e1 p1)) (assert (founds e1 rho1 p1))
; acme attempts prohibition — Disability created by Ax5.2 blocks it
(assert (proh f2))
(assert (aee f2 alice)) (assert (aer f2 acme))
(assert (act f2 read))  (assert (tgt f2 d1))
""",
        "smt2_conjecture": None,
    },
    # =========================================================================
    # GRND021 — Full A1-B1-B2-B3 violation-to-remedy chain
    # Difficulty: Hard
    # Note: founds(e1,rho1,f1) is redundant after Bug 5 fix (Ax5.4 fires from
    # activates alone). Retained for explicitness. B2/B3 fire on rho_R
    # (founded by founds_rem), not rho1.
    # =========================================================================
    {
        "id": "GRND021-remedy-chain", "subdir": "Discriminating",
        "name": "Full remedy chain: violation triggers Power-licensed institutional act",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": [
            "ax_proh_relator_basic",
            "ax_proh_relator_remedy",
            "ax_B1", "ax_B2", "ax_B3",
            "ax_A1", "ax_A2", "ax_A3",
        ],
        "description": """\
% proh(f1) + has_rem(f1) + activates(e1,f1) + does(alice,distribute,d1).
% Ax5.4 (founds_rem): creates rho_R with Power(acme,decl(distribute),d1)
%                     and Subjection(alice,decl(distribute),d1).
% B1: does(alice,...) => NormStateChange.
% A1: NormStateChange => exists InstEvent(ev) triggers it.
% B2: Power(pw) partOf rho_R & founds_rem(e1,rho_R,f1) => about_event(pw,e1).
% B3: Subjection(s,...) => about_event(s,e1).
% A2: InstEvent => competent agent.
% A3: competence => Power+Subjection pair about ev.
% Conjecture: exists pw, s, ev such that about_event(pw,ev) and about_event(s,ev).""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Full violation-to-remedy chain.
# MusicMarketplaceAG violates the prohibition.
# PhilharmonieBerlin holds Power to declare violation.
# The chain A1->A2->A3 grounds the institutional authority.
<drk:policy-remedy-chain> a odrl:Agreement ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:MusicMarketplaceAG> ;
        odrl:assigner <drk:PhilharmonieBerlin> ;
        odrl:action   odrl:distribute ;
        odrl:target   <drk:ConcertRecordingDataset> ;
        odrl:remedy   [ a odrl:Duty ;
            odrl:action odrl:compensate ] ] .
<drk:ConcertRecordingDataset> a dcat:Dataset .
<drk:PhilharmonieBerlin>      a schema:Organization .
<drk:MusicMarketplaceAG>      a schema:Organization .""",
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
? [Pw, S, Y, X, Ev] :
  ( power(Pw) & bearer(Pw, Y) & about_event(Pw, Ev)
  & subjection(S) & bearer(S, X) & about_event(S, Ev) )""",
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
  (exists ((pw Position) (s Position) (y Agent) (x Agent) (ev Event))
    (and (power pw) (bearer pw y) (about-event pw ev)
         (subjection s) (bearer s x) (about-event s ev)))))""",
    },
    # =========================================================================
    # GRND022 — Correlativity blocks non-unique NoRight
    # Difficulty: Medium
    # Bug 2 fix: ax_correlativity_liberty -> ax_correlativity_permission;
    #            liberty -> permission throughout
    # =========================================================================
    {
        "id": "GRND022-corr-nonunique", "subdir": "Discriminating",
        "name": "Correlativity violated: two NoRight positions in same relator",
        "status_fof": "Unsatisfiable",
        "status_smt": "unsat",
        "fof_axioms": ["ax_correlativity_permission"],
        "description": """\
% odrl_rel(rho1) + Permission(l) partOf rho1.
% Two distinct no_right positions n1 != n2 both partOf rho1 with same content.
% ax_correlativity_permission requires unique NoRight => contradiction.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
# Correlativity uniqueness test:
# A relator cannot contain two distinct NoRight positions
# with the same content — correlativity requires exactly one.""",
        "fof_extra_decls": """\
fof(pos_l,         axiom, position(l)).
fof(pos_n1,        axiom, position(n1)).
fof(pos_n2,        axiom, position(n2)).
fof(rel_rho1,      axiom, legal_relator(rho1)).
fof(odrl_rho1,     axiom, odrl_rel(rho1)).
fof(permission_l,  axiom, permission(l)).
fof(no_right_n1,   axiom, no_right(n1)).
fof(no_right_n2,   axiom, no_right(n2)).
fof(partof_l,      axiom, part_of(l,  rho1)).
fof(partof_n1,     axiom, part_of(n1, rho1)).
fof(partof_n2,     axiom, part_of(n2, rho1)).
fof(cnt_l,         axiom, cnt(l,  some_action, some_target)).
fof(cnt_n1,        axiom, cnt(n1, some_action, some_target)).
fof(cnt_n2,        axiom, cnt(n2, some_action, some_target)).
fof(action_typed,  axiom, action(some_action)).
fof(target_typed,  axiom, target(some_target)).
fof(n1_neq_n2,     axiom, n1 != n2).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const l           Position)
(declare-const n1          Position)
(declare-const n2          Position)
(declare-const rho1        Relator)
(declare-const some-action NormContent)
(declare-const some-target Target)
; Bug 2 fix: permission replaces liberty
(assert (permission l))
(assert (no-right n1)) (assert (no-right n2))
(assert (part-of l  rho1)) (assert (part-of n1 rho1)) (assert (part-of n2 rho1))
(assert (cnt l  some-action some-target))
(assert (cnt n1 some-action some-target))
(assert (cnt n2 some-action some-target))
(assert (odrl-rel rho1))
(assert (not (= n1 n2)))
""",
        "smt2_conjecture": None,
    },
    # =========================================================================
    # GRND023 — Policy issuance Power (P3-P4, issue/1 function)
    # Difficulty: Hard
    # Bug 3 fix: SMT2 conjecture was (not (= (issue pi) (issue pi))) —
    # trivially (assert false). Replaced: two rule constants pi1, pi2 with
    # pi1 != pi2 asserted; conjecture negates injectivity: issue(pi1) = issue(pi2).
    # This correctly tests ISSUE2 (injectivity of issue/1) and will be unsat
    # because the Layer0 injectivity axiom for issue forces pi1=pi2, contradicting
    # the assertion pi1 != pi2.
    # =========================================================================
    {
        "id": "GRND023-policy-issuance", "subdir": "Discriminating",
        "name": "Policy issuance: issue/1 injectivity (distinct rules => distinct acts)",
        "status_fof": "Theorem",
        "status_smt": "unsat",
        "fof_axioms": ["ax_obl_relator"],
        "description": """\
% Two distinct rules pi1 != pi2.
% Layer0 ISSUE2: issue(A)=issue(B) => A=B (injectivity).
% Conjecture (FOF): issue(pi1) != issue(pi2).
% SMT2 negated: (assert (= (issue pi1) (issue pi2))) with (assert (not (= pi1 pi2))).
% Injectivity forces pi1=pi2 => contradiction with distinctness.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Policy issuance authority test.
# Two distinct policies — their issue() acts must be distinct.
<drk:policy-issuance-1> a odrl:Agreement ;
    odrl:obligation [ a odrl:Duty ;
        odrl:assignee <drk:PhilharmonieBerlin> ;
        odrl:assigner <drk:FraunhoferFIT> ;
        odrl:action   odrl:distribute ;
        odrl:target   <drk:ConcertRecordingDataset> ] .
<drk:policy-issuance-2> a odrl:Agreement ;
    odrl:obligation [ a odrl:Duty ;
        odrl:assignee <drk:StaatlicheMuseenBerlin> ;
        odrl:assigner <drk:FraunhoferFIT> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:MuseumCollectionAPI> ] .
<drk:ConcertRecordingDataset> a dcat:Dataset .
<drk:MuseumCollectionAPI>     a dcat:DataService .
<drk:PhilharmonieBerlin>      a schema:Organization .
<drk:StaatlicheMuseenBerlin>  a schema:Organization .
<drk:FraunhoferFIT>           a schema:Organization .""",
        "fof_extra_decls": """\
fof(rule_pi1,     axiom, rule(pi1)).
fof(rule_pi2,     axiom, rule(pi2)).
fof(pi1_neq_pi2,  axiom, pi1 != pi2).
""",
        "fof_conjecture": "issue(pi1) != issue(pi2)",
        "smt2_extra_decls": """\
(declare-const pi1  Rule)
(declare-const pi2  Rule)
; Distinctness of the two rules
(assert (not (= pi1 pi2)))
; Negated conjecture: assume issue(pi1) = issue(pi2) — should be unsat
; via Layer0 injectivity: issue(A)=issue(B) => A=B, contradicting pi1!=pi2
""",
        "smt2_conjecture": """\
(assert (= (issue pi1) (issue pi2)))""",
    },
    # =========================================================================
    # GRND024 — obl + proh on same target = Satisfiable (no direct conflict)
    # Difficulty: Medium
    # obl creates Duty(alice, read, d1); proh creates Duty(alice, rfr(read), d1).
    # Different content => ax_cross_relator_consistency does NOT fire.
    # Status: Satisfiable — demonstrates obl+proh coexist in the grounding.
    # =========================================================================
    {
        "id": "GRND024-obl-proh-conflict", "subdir": "Discriminating",
        "name": "Obligation + Prohibition coexist: Duty(a) vs Duty(rfr(a)) distinct",
        "status_fof": "Satisfiable",
        "status_smt": "sat",
        "fof_axioms": [
            "ax_obl_relator",
            "ax_proh_relator_basic",
            "ax_cross_relator_consistency",
        ],
        "description": """\
% obl(obl1) activated at e1: creates Duty(alice, read, d1).
% proh(f1)  activated at e2: creates Duty(alice, rfr(read), d1).
% ax_cross_relator_consistency fires on Permission+Duty(rfr), NOT Duty(a)+Duty(rfr(a)).
% Status: Satisfiable — the two duties coexist (different content).
% Discriminating: shows obl and proh do NOT directly conflict in the grounding.""",
        "ttl": """\
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix drk:    <http://w3id.org/drk/ontology/> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix schema: <https://schema.org/> .
# Obligation to read AND prohibition on reading coexist
# because their duties have different content: read vs rfr(read).
# This demonstrates obl+proh do NOT directly conflict in the grounding.
<drk:policy-obl-proh> a odrl:Agreement ;
    odrl:obligation  [ a odrl:Duty ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:BerlinerEnsemble> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:TheaterShowtimeDataset> ] ;
    odrl:prohibition [ a odrl:Prohibition ;
        odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
        odrl:assigner <drk:StaatlicheMuseenBerlin> ;
        odrl:action   odrl:read ;
        odrl:target   <drk:TheaterShowtimeDataset> ] .
<drk:TheaterShowtimeDataset>          a dcat:Dataset .
<drk:BerlinerEnsemble>                a schema:Organization .
<drk:StaatlicheMuseenBerlin>          a schema:Organization .
<drk:UniversitaetsbibliothekMuenchen> a schema:Organization .""",
        "fof_extra_decls": """\
fof(agent_alice,  axiom, agent(alice)).
fof(agent_acme1,  axiom, agent(acme1)).
fof(agent_acme2,  axiom, agent(acme2)).
fof(action_read,  axiom, action(read)).
fof(target_d1,    axiom, target(d1)).
% Obligation: alice must read d1
fof(rule_obl1,    axiom, rule(obl1)).
fof(event_e1,     axiom, event(e1)).
fof(obl_obl1,     axiom, obl(obl1)).
fof(aee_obl1,     axiom, aee(obl1, alice)).
fof(aer_obl1,     axiom, aer(obl1, acme1)).
fof(act_obl1,     axiom, act(obl1, read)).
fof(tgt_obl1,     axiom, tgt(obl1, d1)).
fof(act_e1_obl1,  axiom, activates(e1, obl1)).
% Prohibition: alice must not read d1
fof(rule_f1,      axiom, rule(f1)).
fof(event_e2,     axiom, event(e2)).
fof(proh_f1,      axiom, proh(f1)).
fof(aee_f1,       axiom, aee(f1, alice)).
fof(aer_f1,       axiom, aer(f1, acme2)).
fof(act_f1,       axiom, act(f1, read)).
fof(tgt_f1,       axiom, tgt(f1, d1)).
fof(act_e2_f1,    axiom, activates(e2, f1)).
""",
        "fof_conjecture": None,
        "smt2_extra_decls": """\
(declare-const alice  Agent)
(declare-const acme1  Agent) (declare-const acme2  Agent)
(declare-const read   Action) (declare-const d1    Target)
(declare-const obl1   Rule)  (declare-const e1    Event)
(declare-const f1     Rule)  (declare-const e2    Event)
; Obligation
(assert (obl obl1))
(assert (aee obl1 alice)) (assert (aer obl1 acme1))
(assert (act obl1 read))  (assert (tgt obl1 d1))
(assert (activates e1 obl1))
; Prohibition
(assert (proh f1))
(assert (aee f1 alice)) (assert (aer f1 acme2))
(assert (act f1 read))  (assert (tgt f1 d1))
(assert (activates e2 f1))
""",
        "smt2_conjecture": None,
    },
]