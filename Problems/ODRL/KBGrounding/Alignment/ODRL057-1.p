%--------------------------------------------------------------------------
% File     : ODRL057-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : Conflict preservation: BCP 47 conflict → ISO 639-3 conflict
% Status   : Theorem
% Expected : Conflict — fra ⊄ deu (same structure, different identifiers)
%
% Validates: Proposition 1(1) — Verdict Preservation (total alignment)
%
% Parallel : ODRL051-1.p (same scenario in BCP 47 KB: de vs fr → Conflict)
%
% Scenario : Dataspace A (Germany, BCP 47) detected conflict between
%            German-language policy and French request. Dataspace B
%            (international, ISO 639-3) uses three-letter codes.
%            Alignment α: de→deu, fr→fra preserves the conflict.
%
% Alignment: α(de) = deu, α(fr) = fra (total for relevant concepts)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, deu)).
fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, eq) & has_value(c2, fra)).

fof(conflict, conjecture, ~?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
