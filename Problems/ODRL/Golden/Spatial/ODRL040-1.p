%--------------------------------------------------------------------------
% File     : ODRL040-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : AND-Compatible: spatial compatible ∧ purpose compatible → Compatible
% Expected : Theorem (AND-Compatible)
% Verdict  : Compatible (conjunction)
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
%         "rightOperand": "dpv:ResearchAndDevelopment"
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
%         "rightOperand": "dpv:AcademicResearch"
%       }] }
%
%   Composition mode: AND (both operands must overlap)
%
% Per-operand verdicts:
%   V_spatial:  isPartOf(europe) ∩ eq(germany) ≠ ∅    [Compatible, cf ODRL011]
%   V_purpose:  isA(R&D) ∩ isA(AcademicResearch) ≠ ∅  [Compatible, AcadRes ≤ R&D]
%   AND: ∀k: V_k = Compatible → verdict_and = Compatible
%
% Encoding: ∃Xs, Xp: (spatial_pair(Xs)) ∧ (purpose_pair(Xp))
%           Uses operand independence (Assumption 2): separate witnesses.
% Difficulty: Medium — multi-KB, multi-operand
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl040, conjecture,
    ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)
             & in_denotation(Xs, germany, eq) )
    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)
             & in_denotation(Xp, academicResearch, isA) ) )).
%--------------------------------------------------------------------------
