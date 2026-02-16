%--------------------------------------------------------------------------
% File     : ODRL045-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE-Compatible: exactly one branch overlaps, other provably empty
% Expected : Theorem (XONE-Compatible)
% Verdict  : Compatible (exclusive disjunction)
% Paper    : Definition 6 (Constraint Composition, xone)
%
% ODRL Scenario:
%   Permission:
%     { "constraint": [{
%         "leftOperand": "spatial",
%         "operator": "isPartOf",
%         "rightOperand": "westernEurope"
%       }],
%       "refinement": [{
%         "leftOperand": "purpose",
%         "operator": "isA",
%         "rightOperand": "dpv:ResearchAndDevelopment"
%       }] }
%   Prohibition:
%     { "constraint": [{
%         "leftOperand": "spatial",
%         "operator": "isPartOf",
%         "rightOperand": "easternEurope"
%       }],
%       "refinement": [{
%         "leftOperand": "purpose",
%         "operator": "isA",
%         "rightOperand": "dpv:AcademicResearch"
%       }] }
%
%   Composition mode: XONE (exactly one branch must overlap)
%
% Per-operand verdicts:
%   V_spatial:  isPartOf(wE) ∩ isPartOf(eE) = ∅           [Conflict — provable]
%   V_purpose:  isA(R&D) ∩ isA(AcademicResearch) ≠ ∅      [Compatible]
%   XONE: ∃!k: V_k=Compatible ∧ ∀j≠k: V_j=Conflict → Compatible
%   Exactly purpose overlaps; spatial is provably empty. ✓
%
% Encoding: XONE = exactly_one_overlaps ∧ rest_provably_empty
%   Positive: purpose pair has witness.
%   Negative: spatial pair has NO witness (provable via disjointness).
%   Combined: purpose_overlap ∧ ¬spatial_overlap
% Difficulty: Very Hard — requires both positive witness AND negative proof
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% XONE encoding: exactly one branch overlaps
fof(odrl045, conjecture,
    ( ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)
             & in_denotation(Xp, academicResearch, isA) )
    & ~( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)
                & in_denotation(Xs, easternEurope, isPartOf) ) ) )).
%--------------------------------------------------------------------------
