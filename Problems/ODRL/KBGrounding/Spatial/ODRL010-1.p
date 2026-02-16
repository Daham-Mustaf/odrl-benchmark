%--------------------------------------------------------------------------
% File     : ODRL010-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Transitive spatial containment: germany ⪯ europe
% Expected : Theorem
% Verdict  : Valid
% Paper    : Definition 2 (KB: leq transitivity)
%
% ODRL Policy (Turtle):
%   (No ODRL policy — pure KB property test)
%
% Denotation analysis:
%   leq(germany, westernEurope) ∧ leq(westernEurope, europe) ⟹ leq(germany, europe)
%
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl010, conjecture, leq(germany, europe)).
%--------------------------------------------------------------------------
