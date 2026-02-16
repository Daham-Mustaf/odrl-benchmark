%--------------------------------------------------------------------------
% File     : ODRL035-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict propagation: c1⊑c2 ∧ conflict(c2,c3) → conflict(c1,c3)
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Lemma 2 (Conflict Propagation)
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   c1: isPartOf(germany), c2: isPartOf(westernEurope), c3: isPartOf(easternEurope)
%
% Denotation analysis:
%   c1⊑c2 (ODRL030) ∧ conflict(c2,c3) (ODRL013) ⟹ conflict(c1,c3)
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl035, conjecture,
    ![X]: ~( in_denotation(X, germany, isPartOf)
           & in_denotation(X, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
