%--------------------------------------------------------------------------
% File     : GRND010-strong-perm-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Strong permission creates Immunity and Disability
% Version  : 1.6
% English  : perm(p1) + strong(p1) + activates(e1,p1).
%           : Ax5.2 existentially founds rho_I via founds_imm.
%           : Entails Immunity(bibliothek,read,museum_api) and Disability(museen,read,museum_api)
%           : in the fresh immunity relator rho_I.
%           : Abstract constants: bibliothek=drk:UniversitaetsbibliothekMuenchen,
%           : museen=drk:StaatlicheMuseenBerlin, read=odrl:read,
%           : museum_api=drk:MuseumCollectionAPI
%
% Refs     : [MMC+26] Mohammed, D., Mustafa, D., Collarana, D., Lange, C., Guizzardi, G. What Does ODRL Mean? Grounding Permissions, Prohibitions, and Duties in Deontic Logic and Foundational Ontology. FOIS 2026.
% Source   : Mohammed, D. (2026)
% Names    : GRND010-strong-perm-1.p
%
% Status   : Theorem
% Syntax   : Number of formulae    :   16  (15 axm; 1 cnj)
%            Number of atoms       :   53
%            Number of variables   :   12
%            Maximal formula depth :    4
% SPC      : FOF_THM_RFN
%
% Comments : Foundational ontology tier. FOIS 2026 benchmark.
%           : Requires Axioms/GRND000-0.ax (Layer 0) and
%           : inline Layer 1 axiom subset (fof_axioms key).
%           : FOF inlines per-problem subsets only to avoid Vampire timeouts.
%           : SMT-LIB embeds the full axiom set (Z3 handles it). Asymmetry intentional.
%           : Policy source: Policies/GRND010-strong-perm-policy.ttl
%           : @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
%           : @prefix drk:    <http://w3id.org/drk/ontology/> .
%           : @prefix dcat:   <http://www.w3.org/ns/dcat#> .
%           : @prefix schema: <https://schema.org/> .
%           : # strong(p1) asserted by profile extension (not ODRL 2.2 alone).
%           : ... (11 more lines — see Policies/ file)
%--------------------------------------------------------------------------


% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
fof(ax_perm_relator_weak, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T) & activates(E,P) )
     => ? [Rho, L, N] :
          ( founds(E,Rho,P)
          & permission(L) & bearer(L,X) & cnt(L,A,T) & part_of(L,Rho)
          & no_right(N)   & bearer(N,Y) & cnt(N,A,T) & part_of(N,Rho) ) )).
fof(ax_perm_relator_strong, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & strong(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T)
        & activates(E,P) )
     => ? [RhoI, Im, Db] :
          ( founds_imm(E,RhoI,P)
          & immunity(Im)   & bearer(Im,X) & cnt(Im,A,T) & part_of(Im,RhoI)
          & disability(Db) & bearer(Db,Y) & cnt(Db,A,T) & part_of(Db,RhoI) ) )).

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
%   legal_relator(Rho)          -- Rho is a UFO legal relator (subsumes odrl_rel)
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Ground instance (gamma)
%--------------------------------------------------------------------------
fof(agent_bibliothek, axiom, agent(bibliothek)).
fof(agent_museen,     axiom, agent(museen)).
fof(action_read,      axiom, action(read)).
fof(target_museum,    axiom, target(museum_api)).
fof(rule_p1,          axiom, rule(p1)).
fof(event_e1,         axiom, event(e1)).
fof(perm_p1,          axiom, perm(p1)).
fof(strong_p1,        axiom, strong(p1)).
fof(aee_p1,           axiom, aee(p1, bibliothek)).
fof(aer_p1,           axiom, aer(p1, museen)).
fof(act_p1,           axiom, act(p1, read)).
fof(tgt_p1,           axiom, tgt(p1, museum_api)).
fof(act_e1_p1,        axiom, activates(e1, p1)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [RhoI, Im, Db] :
  ( founds_imm(e1, RhoI, p1)
  & immunity(Im)   & bearer(Im, bibliothek) & cnt(Im, read, museum_api) & part_of(Im, RhoI)
  & disability(Db) & bearer(Db, museen)     & cnt(Db, read, museum_api) & part_of(Db, RhoI) ) )).