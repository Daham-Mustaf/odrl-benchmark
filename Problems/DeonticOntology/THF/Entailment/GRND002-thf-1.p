%--------------------------------------------------------------------------
% File     : GRND002-thf-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Permission soundness — permission activation entails
%           : Permission position for assignee and No-Right for assigner.
% Version  : 1.1
% English  : Activating a Permission rule at actual_w founds a relator
%           : containing permission_p for bibliothek and no_right_p for
%           : ensemble (Ax5.1; Prop.8 faithfulness clause 1).
%           : THF0 SSE: positions are world-lifted (position_t > world_t > $o).
%
% Refs     : [MMC+26] Mustafa et al. What Does ODRL Mean? FOIS 2026.
%           : [BS10]  Benzmueller & Sutcliffe. JFR 3(1), 2010.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : GRND002-thf-1.p
%
% Status   : Theorem
% SPC      : THF_THM_EQU
%
% Comments : THF0 SSE variant of GRND002-1.p.
%           : Axiom subset: ax_perm_relator_weak only.
%           : Key SSE difference from FOF: world parameter W on every
%           :   position/relator predicate; type system replaces sort guards.
%           : Solvers: Leo-III, Satallax.
%           : Policy: Policies/GRND002-policy.ttl
%--------------------------------------------------------------------------

%--- Sort types
thf(entity_t_decl,   type, entity_t   : $tType).
thf(action_t_decl,   type, action_t   : $tType).
thf(target_t_decl,   type, target_t   : $tType).
thf(rule_t_decl,     type, rule_t     : $tType).
thf(position_t_decl, type, position_t : $tType).
thf(relator_t_decl,  type, relator_t  : $tType).
thf(event_t_decl,    type, event_t    : $tType).
thf(world_t_decl,    type, world_t    : $tType).

%--- Structural predicates (rule graph, not world-lifted)
thf(perm_decl, type, perm : rule_t > $o).
thf(aee_decl,  type, aee  : rule_t > entity_t > $o).
thf(aer_decl,  type, aer  : rule_t > entity_t > $o).
thf(act_decl,  type, act  : rule_t > action_t > $o).
thf(tgt_decl,  type, tgt  : rule_t > target_t > $o).

%--- World-lifted predicates (SSE layer)
thf(activates_decl,    type, activates    : event_t > rule_t > world_t > $o).
thf(founds_decl,       type, founds       : event_t > relator_t > rule_t > world_t > $o).
thf(bearer_decl,       type, bearer       : position_t > entity_t > world_t > $o).
thf(part_of_decl,      type, part_of      : position_t > relator_t > world_t > $o).
thf(cnt_decl,          type, cnt          : position_t > action_t > target_t > world_t > $o).
thf(permission_p_decl, type, permission_p : position_t > world_t > $o).
thf(no_right_p_decl,   type, no_right_p   : position_t > world_t > $o).

%--- Ground constants
thf(bibliothek_decl, type, bibliothek : entity_t).
thf(ensemble_decl,   type, ensemble   : entity_t).
thf(read_decl,       type, read       : action_t).
thf(theater_ds_decl, type, theater_ds : target_t).
thf(p1_decl,         type, p1         : rule_t).
thf(e1_decl,         type, e1         : event_t).
thf(actual_w_decl,   type, actual_w   : world_t).

%--------------------------------------------------------------------------
% Ax5.1  Permission Relator -- Weak  (THF0 world-lifted)
%--------------------------------------------------------------------------
thf(ax_perm_relator_weak, axiom,
    ! [P : rule_t, X : entity_t, Y : entity_t,
       A : action_t, T : target_t, E : event_t, W : world_t] :
      ( ( ( perm @ P )
        & ( aee @ P @ X )
        & ( aer @ P @ Y )
        & ( act @ P @ A )
        & ( tgt @ P @ T )
        & ( activates @ E @ P @ W ) )
     => ( ? [Rho : relator_t, L : position_t, N : position_t] :
            ( ( founds @ E @ Rho @ P @ W )
            & ( permission_p @ L @ W )
            & ( bearer @ L @ X @ W )
            & ( cnt @ L @ A @ T @ W )
            & ( part_of @ L @ Rho @ W )
            & ( no_right_p @ N @ W )
            & ( bearer @ N @ Y @ W )
            & ( cnt @ N @ A @ T @ W )
            & ( part_of @ N @ Rho @ W ) ) ) )).

%--- Ground instance gamma
thf(perm_p1,   axiom, ( perm @ p1 )).
thf(aee_p1,    axiom, ( aee @ p1 @ bibliothek )).
thf(aer_p1,    axiom, ( aer @ p1 @ ensemble )).
thf(act_p1,    axiom, ( act @ p1 @ read )).
thf(tgt_p1,    axiom, ( tgt @ p1 @ theater_ds )).
thf(act_e1_p1, axiom, ( activates @ e1 @ p1 @ actual_w )).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
thf(grnd002_thf_conjecture, conjecture,
    ( ? [Rho : relator_t, L : position_t, N : position_t] :
        ( ( founds @ e1 @ Rho @ p1 @ actual_w )
        & ( permission_p @ L @ actual_w )
        & ( bearer @ L @ bibliothek @ actual_w )
        & ( cnt @ L @ read @ theater_ds @ actual_w )
        & ( part_of @ L @ Rho @ actual_w )
        & ( no_right_p @ N @ actual_w )
        & ( bearer @ N @ ensemble @ actual_w )
        & ( cnt @ N @ read @ theater_ds @ actual_w )
        & ( part_of @ N @ Rho @ actual_w ) ) )).
