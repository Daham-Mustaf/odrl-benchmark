%--------------------------------------------------------------------------
% File     : GRND023-policy-issuance-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Policy issuance: Power to issue policy creates Subjection
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND023-policy-issuance-policy.ttl
% Generated: 2026-03-18 by gen_foundation_problems.py v1.4
%
% % Ground facts: Power(pw, issue(pi), d1) and Subjection(s, issue(pi), d1).
% % issue/1 is injective and issue(R) is an action (from Layer0).
% % Conjecture: action(issue(pi)) holds — issue function types correctly.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% 
% # Policy issuance authority:
% # PhilharmonieBerlin holds Power to issue policies over concert recordings.
% # UniversitaetsbibliothekMuenchen holds Subjection to those issuances.
% <drk:policy-issuance> a odrl:Agreement ;
%     odrl:obligation [ a odrl:Duty ;
%         odrl:assignee <drk:PhilharmonieBerlin> ;
%         odrl:assigner <drk:FraunhoferFIT> ;
%         odrl:action   odrl:distribute ;
%         odrl:target   <drk:ConcertRecordingDataset> ] .
% 
% <drk:ConcertRecordingDataset> a dcat:Dataset .
% <drk:PhilharmonieBerlin>      a schema:Organization .
% <drk:FraunhoferFIT>           a schema:Organization .
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)
fof(ax_obl_relator, axiom,
    ! [D, X, Y, A, T, E] :
      ( ( obl(D) & aee(D,X) & aer(D,Y) & act(D,A) & tgt(D,T) & activates(E,D) )
     => ? [Rho, Du, C] :
          ( founds(E,Rho,D)
          & duty(Du) & bearer(Du,X) & cnt(Du,A,T) & part_of(Du,Rho)
          & claim(C) & bearer(C,Y)  & cnt(C,A,T)  & part_of(C,Rho) ) )).

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
fof(rule_pi,      axiom, rule(pi)).
fof(target_d1,    axiom, target(d1)).
fof(pos_pw,       axiom, position(pw)).
fof(pos_s,        axiom, position(s)).
fof(rel_rho1,     axiom, legal_relator(rho1)).
fof(power_pw,     axiom, power(pw)).
fof(subjection_s, axiom, subjection(s)).
fof(agent_alice,  axiom, agent(alice)).
fof(agent_acme,   axiom, agent(acme)).
fof(bearer_pw,    axiom, bearer(pw, acme)).
fof(bearer_s,     axiom, bearer(s,  alice)).
fof(cnt_pw,       axiom, cnt(pw, issue(pi), d1)).
fof(cnt_s,        axiom, cnt(s,  issue(pi), d1)).
fof(partof_pw,    axiom, part_of(pw, rho1)).
fof(partof_s,     axiom, part_of(s,  rho1)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( action(issue(pi)) )).