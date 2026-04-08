%--------------------------------------------------------------------------
% File     : GRND030-b3-subjection-about-event-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : B3 alone: Subjection in remedy relator concerns founding event
% Version  : 1.6
% English  : Subjection(s) with cnt(s,decl(some_action),some_target) partOf rho_R,
%           : and founds_rem(e1,rho_R,f1) => about_event(s, e1).
%           : B3 tested in isolation (not combined with B2 or A-axioms).
%
% Refs     : [MMC+26] Mohammed, D., Mustafa, D., Collarana, D., Lange, C., Guizzardi, G. What Does ODRL Mean? Grounding Permissions, Prohibitions, and Duties in Deontic Logic and Foundational Ontology. FOIS 2026.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : GRND030-b3-subjection-about-event-1.p
%
% Status   : Theorem
% Syntax   : Number of formulae    :   12  (11 axm; 1 cnj)
%            Number of atoms       :   18
%            Number of variables   :    6
%            Maximal formula depth :    5
% SPC      : FOF_THM_RFN
%
% Comments : Foundational ontology tier. FOIS 2026 benchmark.
%           : inline Layer 1 axiom subset (fof_axioms key).
%           : FOF inlines per-problem subsets only to avoid Vampire timeouts.
%           : SMT-LIB embeds the full axiom set (Z3 handles it). Asymmetry intentional.
%           : Policy source: Policies/GRND030-b3-subjection-about-event-policy.ttl
%           : @prefix odrl: <http://www.w3.org/ns/odrl/2/> .
%           : @prefix drk:  <http://w3id.org/drk/ontology/> .
%           : # B3 standalone: Subjection in a remedy relator concerns the founding event.
%--------------------------------------------------------------------------


% Layer 0: Signature (sorts, rfr/decl, position disjointness)

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.11, A1-A3, B1-B3)
fof(ax_B3, axiom,
    ! [S, A, T, Rho, E, R] :
      ( ( subjection(S) & cnt(S,decl(A),T) & part_of(S,Rho) & founds_rem(E,Rho,R) )
     => about_event(S,E) )).

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
fof(pos_s,       axiom, position(s)).
fof(rel_rho_r,   axiom, legal_relator(rho_r)).
fof(rule_f1,     axiom, rule(f1)).
fof(event_e1,    axiom, event(e1)).
fof(action_a,    axiom, action(some_action)).
fof(target_t,    axiom, target(some_target)).
fof(subj_s,      axiom, subjection(s)).
fof(cnt_s,       axiom, cnt(s, decl(some_action), some_target)).
fof(partof_s,    axiom, part_of(s, rho_r)).
fof(founds_rem1, axiom, founds_rem(e1, rho_r, f1)).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( about_event(s, e1) )).