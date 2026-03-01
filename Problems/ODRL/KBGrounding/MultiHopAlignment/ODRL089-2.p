%--------------------------------------------------------------------------
% File     : ODRL089-2.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Positive control: rich multi-KB structure enables conflict detection
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Multi-KB Positive Control — Rich Structure Enables Detection
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   GEO: disj(westernEurope, easternEurope)         [sibling M49]
%   DPV: disj(commercialPurpose, nonCommercialPurpose) [sibling DPV]
%   LANG: disj(de, en)                              [base languages]
%   AND-composition: at least one dimension conflicts → Conflict
%
% Notes    : Contrast with ODRL088 (flat ISO alone cannot detect spatial conflict). Spatial conflict alone is sufficient for the disjunctive conjecture.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/LANG000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(spatial_conflict, axiom,
    ![X]: ~( in_denotation(X, westernEurope, isPartOf)
           & in_denotation(X, easternEurope, isPartOf) )).
fof(purpose_conflict, axiom,
    ![X]: ~( in_denotation(X, commercialPurpose, isA)
           & in_denotation(X, nonCommercialPurpose, isA) )).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl089b, conjecture,
    ( ![Xs]: ~( in_denotation(Xs, westernEurope, isPartOf)
              & in_denotation(Xs, easternEurope, isPartOf) )
    | ![Xp]: ~( in_denotation(Xp, commercialPurpose, isA)
              & in_denotation(Xp, nonCommercialPurpose, isA) ) )).
%--------------------------------------------------------------------------
