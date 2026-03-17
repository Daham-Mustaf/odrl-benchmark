%--------------------------------------------------------------------------
% File     : GRND002-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Permission creates Liberty and NoRight
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND002-policy.ttl
% Generated: 2026-03-17 by gen_foundation_problems.py v1.4
%
% % perm(p1) activated by e1 entails Liberty(alice,read,d1) and NoRight(acme,read,d1).
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% 
% # Same policy as GRND001 — different question asked (entailment)
% <drk:policy-theater-read> a odrl:Agreement ;
%     odrl:permission [ a odrl:Permission ;
%         odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
%         odrl:assigner <drk:BerlinerEnsemble> ;
%         odrl:action   odrl:read ;
%         odrl:target   <drk:TheaterShowtimeDataset> ] .
% 
% <drk:TheaterShowtimeDataset>          a dcat:Dataset ;
%     schema:name "Berliner Ensemble Showtime Dataset" .
% <drk:BerlinerEnsemble>                a schema:Organization .
% <drk:UniversitaetsbibliothekMuenchen> a schema:Organization .
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)
fof(ax_perm_relator_basic, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T) & activates(E,P) )
     => ? [Rho, L, N] :
          ( founds(E,Rho,P)
          & liberty(L)  & bearer(L,X) & cnt(L,A,T)  & part_of(L,Rho)
          & no_right(N) & bearer(N,Y) & cnt(N,A,T)  & part_of(N,Rho) ) )).

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

%--------------------------------------------------------------------------
% Ground instance (gamma)
%--------------------------------------------------------------------------
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

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [Rho, L, N] :
  ( founds(e1, Rho, p1)
  & liberty(L)  & bearer(L, alice) & cnt(L, read, d1)  & part_of(L, Rho)
  & no_right(N) & bearer(N, acme)  & cnt(N, read, d1)  & part_of(N, Rho) ) )).