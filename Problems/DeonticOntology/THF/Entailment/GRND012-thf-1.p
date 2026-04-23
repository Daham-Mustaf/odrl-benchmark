%--------------------------------------------------------------------------
% File     : GRND012-thf-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Corr-duty — prohibition activation entails Right to Omission
%           : for the assigner (Ax5.3; correlative surfacing).
% Version  : 1.1
% English  : Activating a Prohibition rule founds a conduct relator with
%           : a Duty to Omit for the assignee and a Right to Omission for
%           : the assigner (rfr(distribute)). The assigner's Right is absent
%           : from the ODRL Evaluation Report but entailed by Ax5.3.
%           : THF0 SSE: rfr is typed action_t > action_t — no forbearance
%           :   guard predicates needed (key advantage over FOF encoding).
%
% Refs     : [MMC+26] Mustafa et al. What Does ODRL Mean? FOIS 2026.
%           : [BS10]  Benzmueller & Sutcliffe. JFR 3(1), 2010.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : GRND012-thf-1.p
%
% Status   : Theorem
% SPC      : THF_THM_EQU
%
% Comments : THF0 SSE variant of GRND012-1.p.
%           : Axiom subset: ax_proh_relator_conduct + rfr_distinct.
%           : Solvers: Leo-III, Satallax.
%           : Policy: Policies/GRND012-policy.ttl
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

%--- rfr function (typed: no guard predicates needed)
thf(rfr_decl, type, rfr : action_t > action_t).

%--- Structural predicates
thf(proh_decl, type, proh : rule_t > $o).
thf(aee_decl,  type, aee  : rule_t > entity_t > $o).
thf(aer_decl,  type, aer  : rule_t > entity_t > $o).
thf(act_decl,  type, act  : rule_t > action_t > $o).
thf(tgt_decl,  type, tgt  : rule_t > target_t > $o).

%--- World-lifted predicates (SSE layer)
thf(activates_decl, type, activates : event_t > rule_t > world_t > $o).
thf(founds_decl,    type, founds    : event_t > relator_t > rule_t > world_t > $o).
thf(bearer_decl,    type, bearer    : position_t > entity_t > world_t > $o).
thf(part_of_decl,   type, part_of   : position_t > relator_t > world_t > $o).
thf(cnt_decl,       type, cnt       : position_t > action_t > target_t > world_t > $o).
thf(duty_p_decl,    type, duty_p    : position_t > world_t > $o).
thf(right_p_decl,   type, right_p   : position_t > world_t > $o).

%--- Ground constants
thf(consumer_decl,     type, consumer     : entity_t).
thf(provider_decl,     type, provider     : entity_t).
thf(distribute_decl,   type, distribute   : action_t).
thf(showtimes_ds_decl, type, showtimes_ds : target_t).
thf(f1_decl,           type, f1           : rule_t).
thf(e1_decl,           type, e1           : event_t).
thf(actual_w_decl,     type, actual_w     : world_t).

%--- rfr injectivity (used by prover to distinguish rfr(A) from A)
thf(rfr_distinct, axiom,
    ! [A : action_t] : ( rfr @ A ) != A).

%--------------------------------------------------------------------------
% Ax5.3  Prohibition Relator -- Conduct  (THF0 world-lifted)
% rfr : action_t > action_t is typed; forbearance sort guards not needed.
%--------------------------------------------------------------------------
thf(ax_proh_relator_conduct, axiom,
    ! [F : rule_t, X : entity_t, Y : entity_t,
       A : action_t, T : target_t, E : event_t, W : world_t] :
      ( ( ( proh @ F )
        & ( aee @ F @ X )
        & ( aer @ F @ Y )
        & ( act @ F @ A )
        & ( tgt @ F @ T )
        & ( activates @ E @ F @ W ) )
     => ( ? [Rho : relator_t, D : position_t, C : position_t] :
            ( ( founds @ E @ Rho @ F @ W )
            & ( duty_p @ D @ W )
            & ( bearer @ D @ X @ W )
            & ( cnt @ D @ ( rfr @ A ) @ T @ W )
            & ( part_of @ D @ Rho @ W )
            & ( right_p @ C @ W )
            & ( bearer @ C @ Y @ W )
            & ( cnt @ C @ ( rfr @ A ) @ T @ W )
            & ( part_of @ C @ Rho @ W ) ) ) )).

%--- Ground instance gamma
thf(proh_f1,   axiom, ( proh @ f1 )).
thf(aee_f1,    axiom, ( aee @ f1 @ consumer )).
thf(aer_f1,    axiom, ( aer @ f1 @ provider )).
thf(act_f1,    axiom, ( act @ f1 @ distribute )).
thf(tgt_f1,    axiom, ( tgt @ f1 @ showtimes_ds )).
thf(act_e1_f1, axiom, ( activates @ e1 @ f1 @ actual_w )).

%--------------------------------------------------------------------------
% Conjecture: Right to Omission rfr(distribute) for provider at actual_w.
% Absent from ODRL Evaluation Report; entailed by grounding.
%--------------------------------------------------------------------------
thf(grnd012_thf_conjecture, conjecture,
    ( ? [Rho : relator_t, D : position_t, C : position_t] :
        ( ( founds @ e1 @ Rho @ f1 @ actual_w )
        & ( duty_p @ D @ actual_w )
        & ( bearer @ D @ consumer @ actual_w )
        & ( cnt @ D @ ( rfr @ distribute ) @ showtimes_ds @ actual_w )
        & ( part_of @ D @ Rho @ actual_w )
        & ( right_p @ C @ actual_w )
        & ( bearer @ C @ provider @ actual_w )
        & ( cnt @ C @ ( rfr @ distribute ) @ showtimes_ds @ actual_w )
        & ( part_of @ C @ Rho @ actual_w ) ) )).
