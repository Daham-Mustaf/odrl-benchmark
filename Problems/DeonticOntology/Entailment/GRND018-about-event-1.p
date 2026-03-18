%--------------------------------------------------------------------------
% File     : GRND018-about-event-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : B2+B3: Power and Subjection in relator concern founding event
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND018-about-event-policy.ttl
% Generated: 2026-03-18 by gen_foundation_problems.py v1.4
%
% % proh(f1) + has_rem(f1) + founds(e1,rho1,f1).
% % Ax5.4 creates Power(pw,decl(distribute),d1) partOf rho1.
% % B2: about_event(pw, e1).
% % B3: about_event(s, e1).
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% 
% <drk:policy-about-event> a odrl:Agreement ;
%     odrl:prohibition [ a odrl:Prohibition ;
%         odrl:assignee <drk:MusicMarketplaceAG> ;
%         odrl:assigner <drk:PhilharmonieBerlin> ;
%         odrl:action   odrl:distribute ;
%         odrl:target   <drk:ConcertRecordingDataset> ;
%         odrl:remedy   [ a odrl:Duty ;
%             odrl:action odrl:compensate ] ] .
% 
% <drk:ConcertRecordingDataset> a dcat:Dataset .
% <drk:PhilharmonieBerlin>      a schema:Organization .
% <drk:MusicMarketplaceAG>      a schema:Organization .
% # The Power and Subjection constituted at activation concern the founding event.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)
fof(ax_proh_relator_remedy, axiom,
    ! [F, X, Y, A, T, E, Rho] :
      ( ( proh(F) & has_rem(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T)
        & activates(E,F) & founds(E,Rho,F) )
     => ? [Pw, S] :
          ( power(Pw)     & bearer(Pw,Y) & cnt(Pw,decl(A),T) & part_of(Pw,Rho)
          & subjection(S) & bearer(S,X)  & cnt(S,decl(A),T)  & part_of(S,Rho) ) )).
fof(ax_B2, axiom,
    ! [Pw, A, T, Rho, E, R] :
      ( ( power(Pw) & cnt(Pw,decl(A),T) & part_of(Pw,Rho) & founds(E,Rho,R) )
     => about_event(Pw,E) )).
fof(ax_B3, axiom,
    ! [S, A, T, Rho, E, R] :
      ( ( subjection(S) & cnt(S,decl(A),T) & part_of(S,Rho) & founds(E,Rho,R) )
     => about_event(S,E) )).

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
fof(relator_rho1,      axiom, legal_relator(rho1)).
fof(proh_f1,           axiom, proh(f1)).
fof(rem_f1,            axiom, has_rem(f1)).
fof(aee_f1,            axiom, aee(f1, alice)).
fof(aer_f1,            axiom, aer(f1, acme)).
fof(act_f1,            axiom, act(f1, distribute)).
fof(tgt_f1,            axiom, tgt(f1, d1)).
fof(act_e1_f1,         axiom, activates(e1, f1)).
fof(founds_e1_rho1,    axiom, founds(e1, rho1, f1)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [Pw, S] :
  ( power(Pw)     & bearer(Pw, acme)  & part_of(Pw, rho1)
  & about_event(Pw, e1)
  & subjection(S) & bearer(S,  alice) & part_of(S,  rho1)
  & about_event(S, e1) ) )).