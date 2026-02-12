%--------------------------------------------------------------------------
% File     : ODRL064-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : Purpose compatible preservation: W3C DPV → GDPR taxonomy
% Status   : Theorem
% Expected : Compatible — witness = nichtKommerzielleForschung
%
% Validates: Proposition 1(1) — Verdict Preservation (total alignment)
%
% Parallel : ODRL020-1.p (DPV: nonCommercialPurpose vs nonCommercialResearch → Compatible)
%
% Scenario : Dataspace A (W3C DPV) found non-commercial policy compatible
%            with non-commercial research request. Dataspace B (GDPR)
%            uses German terminology.
%            Alignment α: nonCommercialPurpose→nichtKommerziellerZweck,
%            nonCommercialResearch→nichtKommerzielleForschung.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, purpose) & has_operator(c1, isA) & has_value(c1, nichtKommerziellerZweck)).
fof(c2_def, axiom, has_operand(c2, purpose) & has_operator(c2, eq) & has_value(c2, nichtKommerzielleForschung)).

fof(compatible, conjecture, ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
