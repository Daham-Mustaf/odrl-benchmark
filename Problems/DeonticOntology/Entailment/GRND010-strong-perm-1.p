%--------------------------------------------------------------------------
% File     : GRND010-strong-perm-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Strong permission creates Immunity and Disability
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND010-strong-perm-policy.ttl
% Generated: 2026-03-18 by gen_foundation_problems.py v1.4
%
% % perm(p1) + strong(p1) + founds(e1,rho1,p1).
% % Entails Immunity(alice,read,d1) and Disability(acme,read,d1).
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% 
% # strong(p1) asserted by profile extension (not ODRL 2.2 alone).
% <drk:policy-strong-read> a odrl:Agreement ;
%     odrl:permission [ a odrl:Permission ;
%         odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
%         odrl:assigner <drk:StaatlicheMuseenBerlin> ;
%         odrl:action   odrl:read ;
%         odrl:target   <drk:MuseumCollectionAPI> ] .
% 
% <drk:MuseumCollectionAPI>             a dcat:DataService .
% <drk:StaatlicheMuseenBerlin>          a schema:Organization .
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
fof(ax_perm_relator_strong, axiom,
    ! [P, X, Y, A, T, E, Rho] :
      ( ( perm(P) & strong(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T)
        & activates(E,P) & founds(E,Rho,P) )
     => ? [Im, Db] :
          ( immunity(Im)   & bearer(Im,X) & cnt(Im,A,T)  & part_of(Im,Rho)
          & disability(Db) & bearer(Db,Y) & cnt(Db,A,T)  & part_of(Db,Rho) ) )).

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
fof(agent_alice,   axiom, agent(alice)).
fof(agent_acme,    axiom, agent(acme)).
fof(action_read,   axiom, action(read)).
fof(target_d1,     axiom, target(d1)).
fof(rule_p1,       axiom, rule(p1)).
fof(event_e1,      axiom, event(e1)).
fof(relator_rho1,  axiom, legal_relator(rho1)).
fof(perm_p1,       axiom, perm(p1)).
fof(strong_p1,     axiom, strong(p1)).
fof(aee_p1,        axiom, aee(p1, alice)).
fof(aer_p1,        axiom, aer(p1, acme)).
fof(act_p1,        axiom, act(p1, read)).
fof(tgt_p1,        axiom, tgt(p1, d1)).
fof(act_e1_p1,     axiom, activates(e1, p1)).
fof(founds_e1,     axiom, founds(e1, rho1, p1)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [Im, Db] :
  ( immunity(Im)   & bearer(Im, alice) & cnt(Im, read, d1) & part_of(Im, rho1)
  & disability(Db) & bearer(Db, acme)  & cnt(Db, read, d1) & part_of(Db, rho1) ) )).