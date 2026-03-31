%--------------------------------------------------------------------------
% File     : GRND015-unique-founding-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Unique founding: same event+rule founds at most one relator
% Version  : 1.6
% English  : founds(e1,rho1,p1) and founds(e1,rho2,p1) => rho1 = rho2.
%           : UFO axiom a77 — relator individuated by rule-event pair.
%
% Refs     : [MMC+26] Mohammed, D., Mustafa, D., Collarana, D., Lange, C., Guizzardi, G. What Does ODRL Mean? Grounding Permissions, Prohibitions, and Duties in Deontic Logic and Foundational Ontology. FOIS 2026.
% Source   : Mohammed, D. (2026)
% Names    : GRND015-unique-founding-1.p
%
% Status   : Theorem
% Syntax   : Number of formulae    :    8  (7 axm; 1 cnj)
%            Number of atoms       :    8
%            Number of variables   :    4
%            Maximal formula depth :    4
% SPC      : FOF_THM_RFN
%
% Comments : Foundational ontology tier. FOIS 2026 benchmark.
%           : Requires Axioms/GRND000-0.ax (Layer 0) and
%           : inline Layer 1 axiom subset (fof_axioms key).
%           : FOF inlines per-problem subsets only to avoid Vampire timeouts.
%           : SMT-LIB embeds the full axiom set (Z3 handles it). Asymmetry intentional.
%           : Policy source: Policies/GRND015-unique-founding-policy.ttl
%           : @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
%           : @prefix drk:    <http://w3id.org/drk/ontology/> .
%           : # Uniqueness: activating the same permission twice at the same event
%           : # cannot produce two distinct relators.
%--------------------------------------------------------------------------


% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
fof(ax_unique_founding, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds(E,Rho1,R) & founds(E,Rho2,R) ) => Rho1 = Rho2 )).

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
fof(rule_p1,      axiom, rule(p1)).
fof(event_e1,     axiom, event(e1)).
fof(relator_rho1, axiom, legal_relator(rho1)).
fof(relator_rho2, axiom, legal_relator(rho2)).
fof(founds1,      axiom, founds(e1, rho1, p1)).
fof(founds2,      axiom, founds(e1, rho2, p1)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( rho1 = rho2 )).