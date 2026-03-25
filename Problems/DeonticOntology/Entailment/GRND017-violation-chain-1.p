%--------------------------------------------------------------------------
% File     : GRND017-violation-chain-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : A1-A3+B1: violation triggers norm state change requiring Power
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND017-violation-chain-policy.ttl
% Generated: 2026-03-22 by gen_foundation_problems.py v1.5
%
% % proh(f1) + has_rem(f1) + does(alice,distribute,d1).
% % B1: violation => NormStateChange.
% % A1: NormStateChange => InstEvent.
% % A2: InstEvent => competent agent.
% % A3: competence => Power+Subjection pair.
% % Conjecture: exists Power pw and Subjection s about some event.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% <drk:policy-violation-chain> a odrl:Agreement ;
%     odrl:prohibition [ a odrl:Prohibition ;
%         odrl:assignee <drk:MusicMarketplaceAG> ;
%         odrl:assigner <drk:PhilharmonieBerlin> ;
%         odrl:action   odrl:distribute ;
%         odrl:target   <drk:ConcertRecordingDataset> ;
%         odrl:remedy   [ a odrl:Duty ;
%             odrl:action odrl:compensate ] ] .
% <drk:ConcertRecordingDataset> a dcat:Dataset .
% <drk:PhilharmonieBerlin>      a schema:Organization .
% <drk:MusicMarketplaceAG>      a schema:Organization .
% # drk:MusicMarketplaceAG violates the prohibition.
% # The violation triggers a normative state change (B1),
% # which requires an institutional event (A1),
% # which requires a competent agent (A2),
% # whose competence is a Power-Subjection pair (A3).
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
fof(ax_proh_relator_basic, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) & activates(E,F) )
     => ? [Rho, D, C] :
          ( founds(E,Rho,F)
          & duty(D)  & bearer(D,X) & cnt(D,rfr(A),T) & part_of(D,Rho)
          & right(C) & bearer(C,Y) & cnt(C,rfr(A),T) & part_of(C,Rho) ) )).
fof(ax_proh_relator_remedy, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & has_rem(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T)
        & activates(E,F) )
     => ? [RhoR, Pw, S] :
          ( founds_rem(E,RhoR,F)
          & power(Pw)     & bearer(Pw,Y) & cnt(Pw,decl(A),T) & part_of(Pw,RhoR)
          & subjection(S) & bearer(S,X)  & cnt(S,decl(A),T)  & part_of(S,RhoR) ) )).
fof(ax_A1, axiom,
    ! [X, A, T, Q] :
      ( norm_state_change(X,A,T,Q)
     => ? [E] : ( inst_event(E) & triggers(E,X,A,T,Q) ) )).
fof(ax_A2, axiom,
    ! [E] :
      ( inst_event(E)
     => ? [Y] : competent_for(Y,E) )).
fof(ax_A3, axiom,
    ! [Y, E] :
      ( competent_for(Y,E)
     => ? [Pw, S, X] :
          ( power(Pw)     & bearer(Pw,Y) & about_event(Pw,E)
          & subjection(S) & bearer(S,X)  & about_event(S,E) ) )).
fof(ax_B1, axiom,
    ! [F, X, A, T] :
      ( ( proh(F) & has_rem(F) & act(F,A) & tgt(F,T) & aee(F,X) & does(X,A,T) )
     => ? [B] : ( rem_act(F,B) & norm_state_change(X,B,T,duty_rem) ) )).

%--------------------------------------------------------------------------
% Appendix A.0 extra predicates (declared via axiom context in Layer1)
%   norm_state_change(X,A,T,Q)  -- position Q changes for X over (A,T)
%   inst_event(E)               -- E is an institutional event
%   triggers(E,X,A,T,Q)         -- E triggers the change of Q
%   competent_for(Y,E)          -- Y is competent to perform E
%   about_event(Pos,E)          -- position Pos concerns event E
%   does(X,A,T)                 -- X performs A on T
%   rem_act(F,B)                -- B is the action of the remedy attached to F
%   founds_rem(E,Rho,F)         -- E founds the competence relator rho_R for
%                                  prohibition F with remedy; distinct from
%                                  founds/3 so rho_F != rho_R.
%                                  B2/B3 use founds_rem because Power and
%                                  Subjection live in rho_R, not rho_F.
%   founds_imm(E,Rho,P)         -- E founds the competence relator rho_I for
%                                  strongly-permitted rule P; distinct from
%                                  founds/3 so rho_P != rho_I
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
fof(rem_f1,            axiom, has_rem(f1)).
fof(aee_f1,            axiom, aee(f1, alice)).
fof(aer_f1,            axiom, aer(f1, acme)).
fof(act_f1,            axiom, act(f1, distribute)).
fof(tgt_f1,            axiom, tgt(f1, d1)).
fof(act_e1_f1,         axiom, activates(e1, f1)).
fof(alice_does,        axiom, does(alice, distribute, d1)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [Pw, S, Y, X, Ev] :
  ( power(Pw) & bearer(Pw, Y) & about_event(Pw, Ev)
  & subjection(S) & bearer(S, X) & about_event(S, Ev) ) )).