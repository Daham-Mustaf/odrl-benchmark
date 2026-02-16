%--------------------------------------------------------------------------
% File     : ODRL041-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : AND-Conflict: spatial compatible ∧ purpose conflict → Conflict
% Expected : CounterSatisfiable (AND-Conflict)
% Verdict  : Conflict (conjunction — one operand conflicts)
% Paper    : Definition 6 (Constraint Composition, conjunction)
%
% ODRL Scenario:
%   Permission:
%     { "constraint": [{
%         "leftOperand": "spatial",
%         "operator": "isPartOf",
%         "rightOperand": "europe"
%       }],
%       "refinement": [{
%         "leftOperand": "purpose",
%         "operator": "isA",
%         "rightOperand": "dpv:AcademicResearch"
%       }] }
%   Prohibition:
%     { "constraint": [{
%         "leftOperand": "spatial",
%         "operator": "eq",
%         "rightOperand": "germany"
%       }],
%       "refinement": [{
%         "leftOperand": "purpose",
%         "operator": "isA",
%         "rightOperand": "dpv:Marketing"
%       }] }
%
%   Composition mode: AND
%
% Per-operand verdicts:
%   V_spatial:  isPartOf(europe) ∩ eq(germany) ≠ ∅     [Compatible]
%   V_purpose:  isA(AcademicResearch) ∩ isA(Marketing)  [Conflict — disjoint subtrees]
%     AcademicResearch ≤ ResearchAndDevelopment ≤ Purpose
%     Marketing ≤ Purpose
%     disjoint(ResearchAndDevelopment, Marketing) [DPV KB siblings]
%     → disj_downward → no overlap → Conflict
%   AND: ∃k: V_k = Conflict → verdict_and = Conflict
%
% Encoding: Full AND conjunction — fails because purpose pair is empty.
% Difficulty: Hard — cross-KB composition, disjointness in DPV
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl041, conjecture,
    ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)
             & in_denotation(Xs, germany, eq) )
    & ?[Xp]: ( in_denotation(Xp, academicResearch, isA)
             & in_denotation(Xp, marketing, isA) ) )).
%--------------------------------------------------------------------------
