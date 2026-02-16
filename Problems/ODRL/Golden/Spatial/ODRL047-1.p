%--------------------------------------------------------------------------
% File     : ODRL047-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE-Conflict: all branches conflict → Conflict
% Expected : CounterSatisfiable (XONE-Conflict)
% Verdict  : Conflict (xone — no branch overlaps at all)
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
%         "rightOperand": "dpv:AcademicResearch"
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
%         "rightOperand": "dpv:Marketing"
%       }] }
%
%   Composition mode: XONE
%
% Per-operand verdicts:
%   V_spatial:  isPartOf(wE) ∩ isPartOf(eE)              [Conflict]
%   V_purpose:  isA(AcademicResearch) ∩ isA(Marketing)    [Conflict]
%   XONE: ∀k: V_k = Conflict → verdict_xone = Conflict
%   No branch overlaps → neither can be the "exactly one".
%
% Encoding: Same as OR-Conflict (ODRL043) — no disjunct succeeds.
%   Under XONE semantics, this maps to Conflict.
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% XONE: at least one branch must overlap (prerequisite for XONE-Compatible)
fof(odrl047, conjecture,
    ( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)
             & in_denotation(Xs, easternEurope, isPartOf) )
    | ?[Xp]: ( in_denotation(Xp, academicResearch, isA)
             & in_denotation(Xp, marketing, isA) ) )).
%--------------------------------------------------------------------------
