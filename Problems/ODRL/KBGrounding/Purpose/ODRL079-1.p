%--------------------------------------------------------------------------
% File     : ODRL079-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: deep leaves across disjoint subtrees (depth 4 × depth 4)
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 2, Definition 5
% Category : basic
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   Deep leaves from different root-level subtrees.
%   targetedAdvertising (under marketing) vs maintainFraudDatabase (under enforceSecurity)
%
% Denotation analysis:
%   marketing ⊥⊥ enforceSecurity [d_0113] → disj_downward to leaves → ∅
%   Prover must chain: targetedAdv→…→marketing ⊥⊥ enforceSecurity←…←maintainFraud
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl079, conjecture,
    ![X]: ~( in_denotation(X, targetedAdvertising, isA)
           & in_denotation(X, maintainFraudDatabase, isA) )).
%--------------------------------------------------------------------------
