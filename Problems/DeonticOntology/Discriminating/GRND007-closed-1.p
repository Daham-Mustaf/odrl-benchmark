%--------------------------------------------------------------------------
% File     : GRND007-closed-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Closed-world: no Liberty for uncovered action
% Status   : Satisfiable
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND007-closed-policy.ttl
% Generated: 2026-03-18 by gen_foundation_problems.py v1.4
%
% % No perm rule for 'modify'. No open-world closure.
% % Liberty(alice,modify,d1) is NOT derivable — consistent with its negation.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% 
% # behaviour=closed policy over drk:TheaterShowtimeDataset.
% # No permission for odrl:modify declared.
% # => Liberty(drk:StreamingPortalGmbH, modify,
% #            drk:TheaterShowtimeDataset) NOT derivable.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)

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
fof(action_modify, axiom, action(modify)).
fof(target_d1,     axiom, target(d1)).
fof(no_liberty_modify, axiom,
    ~ ? [L] : ( liberty(L) & bearer(L, alice) & cnt(L, modify, d1) )).
