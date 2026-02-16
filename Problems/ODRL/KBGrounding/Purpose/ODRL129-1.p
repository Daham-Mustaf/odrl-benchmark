%--------------------------------------------------------------------------
% File     : ODRL129-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : KB transitivity: targetedAdvertising ≤ purpose (depth 4)
% Expected : Theorem
% Verdict  : Confirmed
% Paper    : Definition 2 (KB transitivity)
% Category : edge
%
% ODRL Policy (Turtle):
%   (No ODRL policy — pure KB property test)
%   targetedAdvertising ≤ personalisedAdvertising ≤ advertising ≤ marketing ≤ purpose
%
% Denotation analysis:
%   leq(targetedAdvertising, purpose) via 4 transitivity steps
%
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl129, conjecture, leq(targetedAdvertising, purpose)).
%--------------------------------------------------------------------------
