%--------------------------------------------------------------------------
% File     : GRND012-corr-duty-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Correlativity: Duty implies unique Claim in relator
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND012-corr-duty-policy.ttl
% Generated: 2026-03-18 by gen_foundation_problems.py v1.4
%
% % odrl_rel(rho1), Duty(d) partOf rho1 => exists unique c. Claim(c) partOf rho1.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% 
% # Correlativity: every Duty in an ODRL relator has a unique correlative Claim.
% # Tested on drk:TheaterShowtimeDataset prohibition relator.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)
fof(ax_correlativity_duty, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [D] : ( duty(D)  & part_of(D,Rho) & cnt(D,A,T) ) )
        <=> ( ? [C] : ( claim(C) & part_of(C,Rho) & cnt(C,A,T)
                      & ! [K] : ( ( claim(K) & part_of(K,Rho) & cnt(K,A,T) )
                                 => K = C ) ) ) ) )).

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
fof(pos_d,     axiom, position(d)).
fof(rel_rho1,  axiom, legal_relator(rho1)).
fof(odrl_rho1, axiom, odrl_rel(rho1)).
fof(duty_d,    axiom, duty(d)).
fof(partof_d,  axiom, part_of(d, rho1)).
fof(cnt_d,     axiom, cnt(d, some_action, some_target)).
fof(some_action_typed, axiom, action(some_action)).
fof(some_target_typed, axiom, target(some_target)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [C] : ( claim(C) & part_of(C, rho1) & cnt(C, some_action, some_target)
        & ! [K] : ( ( claim(K) & part_of(K, rho1)
                    & cnt(K, some_action, some_target) )
                  => K = C ) ) )).