%--------------------------------------------------------------------------
% File     : GRND019-two-policy-conflict-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Two policies conflict: competing Rights from distinct assigners
% Status   : Unsatisfiable
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND019-two-policy-conflict-policy.ttl
% Generated: 2026-03-22 by gen_foundation_problems.py v1.5
%
% % Two prohibitions over the same (alice, read, d1):
% %   f1: assigner acme1, activates at e1 => Duty(alice,rfr(read),d1) + Right(acme1,...)
% %   f2: assigner acme2, activates at e2 => Duty(alice,rfr(read),d1) + Right(acme2,...)
% % alice also holds Permission(alice,read,d1).
% % ax_cross_relator_consistency: Permission + Duty(rfr) => False.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% # Two competing prohibitions from different assigners over the same asset.
% # Combined with an existing Permission => conflict.
% <drk:policy-conflict-two> a odrl:Agreement ;
%     odrl:permission  [ a odrl:Permission ;
%         odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
%         odrl:assigner <drk:BerlinerEnsemble> ;
%         odrl:action   odrl:read ;
%         odrl:target   <drk:TheaterShowtimeDataset> ] ;
%     odrl:prohibition [ a odrl:Prohibition ;
%         odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
%         odrl:assigner <drk:StaatlicheMuseenBerlin> ;
%         odrl:action   odrl:read ;
%         odrl:target   <drk:TheaterShowtimeDataset> ] ;
%     odrl:prohibition [ a odrl:Prohibition ;
%         odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
%         odrl:assigner <drk:PhilharmonieBerlin> ;
%         odrl:action   odrl:read ;
%         odrl:target   <drk:TheaterShowtimeDataset> ] .
% <drk:TheaterShowtimeDataset>          a dcat:Dataset .
% <drk:BerlinerEnsemble>                a schema:Organization .
% <drk:StaatlicheMuseenBerlin>          a schema:Organization .
% <drk:PhilharmonieBerlin>              a schema:Organization .
% <drk:UniversitaetsbibliothekMuenchen> a schema:Organization .
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
fof(ax_cross_relator_consistency, axiom,
    ! [L, D, X, A, T] :
      ( ( permission(L) & bearer(L,X) & cnt(L,A,T)
        & duty(D)       & bearer(D,X) & cnt(D,rfr(A),T) )
     => $false )).

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
