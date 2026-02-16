%--------------------------------------------------------------------------
% File     : ODRL046-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE-Unknown: two branches both compatible → Unknown
% Expected : CounterSatisfiable (Unknown — exclusivity not provable)
% Verdict  : Unknown (xone requires exactly one, but both overlap)
% Paper    : Definition 6 (Constraint Composition, xone — Unknown case)
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
%   Composition mode: XONE
%
% Per-operand verdicts:
%   V_spatial:  isPartOf(europe) ∩ eq(germany) ≠ ∅          [Compatible]
%   V_purpose:  isA(R&D) ∩ isA(AcademicResearch) ≠ ∅        [Compatible]
%   XONE: Both operands are Compatible.
%   XONE requires exactly one Compatible + rest Conflict.
%   Since BOTH are Compatible, exclusivity cannot be established.
%   → verdict_xone = Unknown
%
% Encoding: We encode the XONE-Compatible conjecture (which should FAIL
%   because we can't prove exactly one branch):
%   "exactly one overlaps and the other is provably empty"
%   This fails → CounterSatisfiable → maps to Unknown.
%   Note: This is the critical XONE test case referenced in the paper
%   as demonstrating why open-world semantics forces Unknown.
% Difficulty: Very Hard — most nuanced composition case
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% XONE encoding attempt 1: spatial overlaps, purpose provably empty
% (Should FAIL: purpose IS compatible, so ¬purpose_overlap is false)
fof(odrl046, conjecture,
    ( ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)
              & in_denotation(Xs, germany, eq) )
      & ~( ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)
                   & in_denotation(Xp, academicResearch, isA) ) ) )
    | ( ?[Xp2]: ( in_denotation(Xp2, researchAndDevelopment, isA)
                & in_denotation(Xp2, academicResearch, isA) )
      & ~( ?[Xs2]: ( in_denotation(Xs2, europe, isPartOf)
                   & in_denotation(Xs2, germany, eq) ) ) ) )).
%--------------------------------------------------------------------------
