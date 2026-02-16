%--------------------------------------------------------------------------
% File     : ODRL109-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict propagation: isA(adv)⊑isA(mkt) ∧ conflict(mkt,sec) → conflict(adv,sec)
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Lemma 2 (Conflict Propagation)
% Category : subsumption
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   c1=isA(advertising), c2=isA(marketing), c3=isA(enforceSecurity)
%   c1⊑c2 (ODRL104) ∧ conflict(c2,c3) (ODRL068) → conflict(c1,c3)
%
% Denotation analysis:
%   advertising ≤ marketing, marketing ⊥⊥ enforceSecurity → advertising ⊥⊥ enforceSecurity
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl109, conjecture,
    ![X]: ~( in_denotation(X, advertising, isA)
           & in_denotation(X, enforceSecurity, isA) )).
%--------------------------------------------------------------------------
