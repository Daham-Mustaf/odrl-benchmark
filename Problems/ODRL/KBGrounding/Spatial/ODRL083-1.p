%--------------------------------------------------------------------------
% File     : ODRL083-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Aligned compatible: isPartOf(europe) ∩ eq(dE) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Proposition 2(1) — Compatible Verdict Preservation
%
% ODRL Policy (Turtle):
%   Dataspace A (GEO): permission spatial isPartOf europe
%   Dataspace B (ISO): prohibition spatial eq dE
%
% Denotation analysis:
%   GEO: isPartOf(europe) ∩ eq(germany) → Compatible (witness: germany)
%   ISO: isPartOf(europe) ∩ eq(dE) → Compatible (witness: dE)
%   Alignment preserves compatible verdict.
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').

fof(odrl083, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & in_denotation(X, dE, eq) )).
%--------------------------------------------------------------------------
