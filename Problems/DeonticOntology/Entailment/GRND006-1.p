%--------------------------------------------------------------------------
% File     : GRND006-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Correlativity: Liberty implies unique NoRight in relator
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND006-policy.ttl
% Generated: 2026-03-18 by gen_foundation_problems.py v1.4
%
% % odrl_rel(rho1), Liberty(l) partOf rho1 => exists unique n. NoRight(n) partOf rho1.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% 
% <drk:policy-corr> a odrl:Agreement ;
%     odrl:permission [ a odrl:Permission ;
%         odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
%         odrl:assigner <drk:BerlinerEnsemble> ;
%         odrl:action   odrl:use ;
%         odrl:target   <drk:PlayProductionMetadataDataset> ] .
% 
% <drk:PlayProductionMetadataDataset>   a dcat:Dataset ;
%     schema:name "Berliner Ensemble Play Production Metadata" .
% <drk:BerlinerEnsemble>                a schema:Organization .
% <drk:UniversitaetsbibliothekMuenchen> a schema:Organization .
% # Liberty(Bibliothek) entails unique NoRight(Ensemble) in relator.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)
fof(ax_correlativity_liberty, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [L] : ( liberty(L)  & part_of(L,Rho) & cnt(L,A,T) ) )
        <=> ( ? [N] : ( no_right(N) & part_of(N,Rho) & cnt(N,A,T)
                      & ! [M] : ( ( no_right(M) & part_of(M,Rho) & cnt(M,A,T) )
                                 => M = N ) ) ) ) )).

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
fof(pos_l,     axiom, position(l)).
fof(rel_rho1,  axiom, legal_relator(rho1)).
fof(odrl_rho1, axiom, odrl_rel(rho1)).
fof(liberty_l, axiom, liberty(l)).
fof(partof_l,  axiom, part_of(l, rho1)).
fof(cnt_l,     axiom, cnt(l, some_action, some_target)).
fof(some_action_typed, axiom, action(some_action)).
fof(some_target_typed, axiom, target(some_target)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [N] : ( no_right(N) & part_of(N, rho1) & cnt(N, some_action, some_target)
        & ! [M] : ( ( no_right(M) & part_of(M, rho1)
                    & cnt(M, some_action, some_target) )
                  => M = N ) ) )).