%--------------------------------------------------------------------------
% File     : ODRL042-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : OR-Compatible: spatial conflict ∨ purpose compatible → Compatible
% Expected : Theorem (OR-Compatible)
% Verdict  : Compatible (disjunction — one operand suffices)
% Paper    : Definition 6 (Constraint Composition, disjunction)
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
%   Composition mode: OR
%
% Per-operand verdicts:
%   V_spatial:  isPartOf(wE) ∩ isPartOf(eE) = ∅  [Conflict — disjoint regions]
%   V_purpose:  isA(R&D) ∩ isA(AcadRes) ≠ ∅      [Compatible — AcadRes ≤ R&D]
%   OR: ∃k: V_k = Compatible → verdict_or = Compatible
%   The purpose overlap saves the overall verdict despite spatial conflict.
%
% Encoding: Disjunctive witness — either spatial OR purpose pair overlaps.
% Difficulty: Hard — OR-composition with mixed verdicts across KBs
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl042, conjecture,
    ( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)
             & in_denotation(Xs, easternEurope, isPartOf) )
    | ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)
             & in_denotation(Xp, academicResearch, isA) ) )).
%--------------------------------------------------------------------------
