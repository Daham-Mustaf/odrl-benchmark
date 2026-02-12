%--------------------------------------------------------------------------
% File     : ODRL058-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : Compatible preservation: BCP 47 compatible → ISO 639-3 compatible
% Status   : Theorem
% Expected : Compatible — witness = arz (arz ⊑ ara in both KBs)
%
% Validates: Proposition 1(1) — Verdict Preservation (total alignment)
%
% Parallel : ODRL053-1.p (same scenario in BCP 47 KB: ar vs arz → Compatible)
%
% Scenario : Dataspace A (BCP 47) found Arabic collection compatible with
%            Egyptian Arabic request. Dataspace B (ISO 639-3) uses
%            three-letter codes. Alignment α: ar→ara, arz→arz preserves
%            compatibility.
%
% Alignment: α(ar) = ara, α(arz) = arz (total for relevant concepts)
% Note    : arz is identical in both standards (ISO 639-3 code)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, ara)).
fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, eq) & has_value(c2, arz)).

fof(compatible, conjecture, ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
