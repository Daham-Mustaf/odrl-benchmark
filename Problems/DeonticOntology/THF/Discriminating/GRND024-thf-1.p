%--------------------------------------------------------------------------
% File     : GRND024-thf-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Obl-proh coexist — both a Duty to Act and a Duty to Omit
%           : are entailed for the same assignee when an obligation and a
%           : prohibition over the same action/target are both activated.
% Version  : 1.2
% English  : Activating odrl:Duty d1 and odrl:Prohibition f1 for the same
%           : assignee (consumer) over the same action (distribute) and
%           : target (showtimes_ds) entails two distinct duty positions:
%           :   Du: duty_p with content distribute (Duty to Act, from d1)
%           :   D:  duty_p with content rfr(distribute) (Duty to Omit, from f1)
%           : The ODRL evaluator reports both rules active but cannot
%           : represent the normative incompatibility; the grounding makes
%           : both duties explicit at actual_w (Ax5.3 + Ax5.5).
%           : THF0 SSE: world-lifted typed predicates.
%
% Refs     : [MMC+26] Mustafa et al. What Does ODRL Mean? FOIS 2026.
%           : [BS10]  Benzmueller & Sutcliffe. JFR 3(1), 2010.
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : GRND024-thf-1.p
%
% Status   : Theorem
% SPC      : THF_THM_EQU
%
% Comments : THF0 SSE variant of GRND024-1.p.
%           : Axiom subset: ax_proh_relator_conduct + ax_obl_relator + rfr.
%           : Conjecture witnesses only the two duty positions (not their
%           :   relators): the relator/part_of witnesses are entailed but
%           :   omitted to reduce the search space for Leo-III.
%           : Adding ax_cross_relator flips to CounterSatisfiable (Ax5.9
%           :   blocks permission_p + duty to omit for the same bearer;
%           :   the dual duty case is the full discriminating problem).
%           : Solvers: Leo-III, Satallax.
%           : Policy: Policies/GRND024-obl-proh-coexist-policy.ttl
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

%--- rfr function
thf(rfr_decl, type, rfr : action_t > action_t).

%--- Structural predicates
thf(proh_decl,     type, proh     : rule_t > $o).
thf(obl_rule_decl, type, obl_rule : rule_t > $o).
thf(aee_decl,      type, aee      : rule_t > entity_t > $o).
thf(aer_decl,      type, aer      : rule_t > entity_t > $o).
thf(act_decl,      type, act      : rule_t > action_t > $o).
thf(tgt_decl,      type, tgt      : rule_t > target_t > $o).

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
thf(d1_decl,           type, d1           : rule_t).
thf(f1_decl,           type, f1           : rule_t).
thf(e1_decl,           type, e1           : event_t).
thf(actual_w_decl,     type, actual_w     : world_t).

%--- rfr distinctness
thf(rfr_distinct, axiom,
    ! [A : action_t] : ( rfr @ A ) != A).

%--------------------------------------------------------------------------
% Ax5.3  Prohibition Relator -- Conduct
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

%--------------------------------------------------------------------------
% Ax5.5  Obligation Relator
%--------------------------------------------------------------------------
thf(ax_obl_relator, axiom,
    ! [D : rule_t, X : entity_t, Y : entity_t,
       A : action_t, T : target_t, E : event_t, W : world_t] :
      ( ( ( obl_rule @ D )
        & ( aee @ D @ X )
        & ( aer @ D @ Y )
        & ( act @ D @ A )
        & ( tgt @ D @ T )
        & ( activates @ E @ D @ W ) )
     => ( ? [Rho : relator_t, Du : position_t, C : position_t] :
            ( ( founds @ E @ Rho @ D @ W )
            & ( duty_p @ Du @ W )
            & ( bearer @ Du @ X @ W )
            & ( cnt @ Du @ A @ T @ W )
            & ( part_of @ Du @ Rho @ W )
            & ( right_p @ C @ W )
            & ( bearer @ C @ Y @ W )
            & ( cnt @ C @ A @ T @ W )
            & ( part_of @ C @ Rho @ W ) ) ) )).

%--- Ground instance gamma
thf(obl_rule_d1, axiom, ( obl_rule @ d1 )).
thf(aee_d1,      axiom, ( aee @ d1 @ consumer )).
thf(aer_d1,      axiom, ( aer @ d1 @ provider )).
thf(act_d1,      axiom, ( act @ d1 @ distribute )).
thf(tgt_d1,      axiom, ( tgt @ d1 @ showtimes_ds )).
thf(act_e1_d1,   axiom, ( activates @ e1 @ d1 @ actual_w )).

thf(proh_f1,   axiom, ( proh @ f1 )).
thf(aee_f1,    axiom, ( aee @ f1 @ consumer )).
thf(aer_f1,    axiom, ( aer @ f1 @ provider )).
thf(act_f1,    axiom, ( act @ f1 @ distribute )).
thf(tgt_f1,    axiom, ( tgt @ f1 @ showtimes_ds )).
thf(act_e1_f1, axiom, ( activates @ e1 @ f1 @ actual_w )).

%--------------------------------------------------------------------------
% Conjecture: both duty positions exist at actual_w.
% Witnesses: Du (Duty to Act) and D (Duty to Omit rfr(distribute)).
% Relator/part_of witnesses are omitted to reduce the search space;
% they are entailed by the axioms but not needed for the main claim.
%--------------------------------------------------------------------------
thf(grnd024_thf_conjecture, conjecture,
    ( ( ? [Du : position_t] :
          ( ( duty_p @ Du @ actual_w )
          & ( bearer @ Du @ consumer @ actual_w )
          & ( cnt @ Du @ distribute @ showtimes_ds @ actual_w ) ) )
    & ( ? [D : position_t] :
          ( ( duty_p @ D @ actual_w )
          & ( bearer @ D @ consumer @ actual_w )
          & ( cnt @ D @ ( rfr @ distribute ) @ showtimes_ds @ actual_w ) ) ) )).
