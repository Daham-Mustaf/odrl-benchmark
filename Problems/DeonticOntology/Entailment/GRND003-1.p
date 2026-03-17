%--------------------------------------------------------------------------
% File     : GRND003-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Prohibition creates Duty and Claim over rfr(a)
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND003-policy.ttl
% Generated: 2026-03-17 by gen_foundation_problems.py v1.4
%
% % proh(f1) activated by e1 entails Duty(alice,rfr(distribute),d1)
% % and Claim(acme,rfr(distribute),d1).
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% 
% <drk:policy-no-distribute> a odrl:Agreement ;
%     odrl:prohibition [ a odrl:Prohibition ;
%         odrl:assignee <drk:StreamingPortalGmbH> ;
%         odrl:assigner <drk:StaatlicheMuseenBerlin> ;
%         odrl:action   odrl:distribute ;
%         odrl:target   <drk:MuseumCollectionAPI> ] .
% 
% <drk:MuseumCollectionAPI>    a dcat:DataService ;
%     schema:name "Staatliche Museen Berlin Collection API" .
% <drk:StaatlicheMuseenBerlin> a schema:Organization .
% <drk:StreamingPortalGmbH>    a schema:Organization .
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)
fof(ax_proh_relator_basic, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) & activates(E,F) )
     => ? [Rho, D, C] :
          ( founds(E,Rho,F)
          & duty(D)  & bearer(D,X) & cnt(D,rfr(A),T) & part_of(D,Rho)
          & claim(C) & bearer(C,Y) & cnt(C,rfr(A),T) & part_of(C,Rho) ) )).

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

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [Rho, D, C] :
  ( founds(e1, Rho, f1)
  & duty(D)  & bearer(D, alice) & cnt(D, rfr(distribute), d1) & part_of(D, Rho)
  & claim(C) & bearer(C, acme)  & cnt(C, rfr(distribute), d1) & part_of(C, Rho) ) )).