%--------------------------------------------------------------------------
% File     : GRND004-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Prohibition with remedy creates Power and Subjection
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND004-policy.ttl
% Generated: 2026-03-17 by gen_foundation_problems.py v1.4
%
% % proh(f1) + has_rem(f1) + founds(e1,rho1,f1).
% % Entails Power(acme,decl(distribute),d1) and Subjection(alice,decl(distribute),d1).
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% 
% <drk:policy-concert-remedy> a odrl:Agreement ;
%     odrl:prohibition [ a odrl:Prohibition ;
%         odrl:assignee <drk:MusicMarketplaceAG> ;
%         odrl:assigner <drk:PhilharmonieBerlin> ;
%         odrl:action   odrl:distribute ;
%         odrl:target   <drk:ConcertRecordingDataset> ;
%         odrl:remedy   [ a odrl:Duty ;
%             odrl:action odrl:compensate ] ] .
% 
% <drk:ConcertRecordingDataset> a dcat:Dataset ;
%     schema:name "Philharmonie Berlin Concert Recordings" .
% <drk:PhilharmonieBerlin>  a schema:Organization .
% <drk:MusicMarketplaceAG>  a schema:Organization .
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
fof(ax_proh_relator_remedy, axiom,
    ! [F, X, Y, A, T, E, Rho] :
      ( ( proh(F) & has_rem(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T)
        & activates(E,F) & founds(E,Rho,F) )
     => ? [Pw, S] :
          ( power(Pw)     & bearer(Pw,Y) & cnt(Pw,decl(A),T) & part_of(Pw,Rho)
          & subjection(S) & bearer(S,X)  & cnt(S,decl(A),T)  & part_of(S,Rho) ) )).

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
  ( power(Pw)     & bearer(Pw, acme)  & cnt(Pw, decl(distribute), d1) & part_of(Pw, rho1)
  & subjection(S) & bearer(S,  alice) & cnt(S,  decl(distribute), d1) & part_of(S,  rho1) ) )).