%--------------------------------------------------------------------------
% File     : ODRL081-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Aligned conflict: disjoint(dE, pL) via alignment transfer
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Def. 8(ii), Proposition 2(1) — Disjointness Transfer
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   Dataspace A (GEO): permission spatial isPartOf germany
%   Dataspace B (ISO): prohibition spatial isPartOf pL
%
% Denotation analysis:
%   disj_downward(wE⊥eE, de≤wE, pl≤eE) → disjoint(de, pl)
%   align_disj_forward(de→dE, pl→pL, disj(de,pl)) → disjoint(dE, pL)
%   → ⟦isPartOf(dE)⟧ ∩ ⟦isPartOf(pL)⟧ = ∅ → Conflict
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').

fof(odrl081, conjecture,
    ![X]: ~( in_denotation(X, dE, isPartOf)
           & in_denotation(X, pL, isPartOf) )).
%--------------------------------------------------------------------------
