%--------------------------------------------------------------------------
% File     : GRND009-immunity-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Strong permission: Liberty persists (Disability blocks prohibition)
% Status   : Unsatisfiable
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Policy   : Policies/GRND009-immunity-policy.ttl
% Generated: 2026-03-17 by gen_foundation_problems.py v1.4
%
% % H2 = {Liberty, NoRight, Immunity, Disability}.
% % Acme attempts proh(f2). Ax5.10: Disability + proh => False.
%
% ODRL Policy (Turtle) — see Policies/ for full file:
% @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
% @prefix drk:    <http://w3id.org/drk/ontology/> .
% @prefix dcat:   <http://www.w3.org/ns/dcat#> .
% @prefix schema: <https://schema.org/> .
% 
% <drk:policy-strong> a odrl:Agreement ;
%     odrl:permission [ a odrl:Permission ;
%         odrl:assignee <drk:UniversitaetsbibliothekMuenchen> ;
%         odrl:assigner <drk:StaatlicheMuseenBerlin> ;
%         odrl:action   odrl:read ;
%         odrl:target   <drk:MuseumCollectionAPI> ] .
% 
% <drk:MuseumCollectionAPI>             a dcat:DataService ;
%     schema:name "Staatliche Museen Berlin Collection API" .
% <drk:StaatlicheMuseenBerlin>          a schema:Organization .
% <drk:UniversitaetsbibliothekMuenchen> a schema:Organization .
% # strong(p) asserted (profile extension, not ODRL 2.2).
% # Immunity(Bibliothek) + Disability(Museen).
% # StaatlicheMuseenBerlin attempts prohibition => blocked by Disability.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)
fof(ax_disability_block, axiom,
    ! [F, X, Y, A, T] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) )
     => ~ ? [Db] : ( disability(Db) & bearer(Db,Y) & cnt(Db,A,T) ) )).

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
fof(pos_l,         axiom, position(l)).
fof(pos_n,         axiom, position(n)).
fof(pos_im,        axiom, position(im)).
fof(pos_db,        axiom, position(db)).
fof(rel_rho1,      axiom, legal_relator(rho1)).
fof(liberty_l,     axiom, liberty(l)).
fof(no_right_n,    axiom, no_right(n)).
fof(immunity_im,   axiom, immunity(im)).
fof(disability_db, axiom, disability(db)).
fof(bearer_l,      axiom, bearer(l,  alice)).
fof(bearer_n,      axiom, bearer(n,  acme)).
fof(bearer_im,     axiom, bearer(im, alice)).
fof(bearer_db,     axiom, bearer(db, acme)).
fof(cnt_l,         axiom, cnt(l,  read, d1)).
fof(cnt_n,         axiom, cnt(n,  read, d1)).
fof(cnt_im,        axiom, cnt(im, read, d1)).
fof(cnt_db,        axiom, cnt(db, read, d1)).
fof(rule_f2,       axiom, rule(f2)).
fof(proh_f2,       axiom, proh(f2)).
fof(aee_f2,        axiom, aee(f2, alice)).
fof(aer_f2,        axiom, aer(f2, acme)).
fof(act_f2,        axiom, act(f2, read)).
fof(tgt_f2,        axiom, tgt(f2, d1)).
