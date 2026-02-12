%--------------------------------------------------------------------------
% File     : ODRL059-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : Graceful degradation: BCP 47 compatible → ISO 639-3 unknown
% Status   : CounterSatisfiable
% Expected : Unknown — de_AT has no grounding in ISO 639-3 KB
%
% Validates: Proposition 1(2) — Graceful Degradation (partial alignment)
%
% Parallel : ODRL050-1.p (same scenario in BCP 47 KB: de vs de_AT → Compatible)
%
% Scenario : Dataspace A (BCP 47) found German policy compatible with
%            Austrian German request (de_AT ⊑ de). Dataspace B
%            (ISO 639-3) has no regional variants — de_AT is unmappable.
%            The Compatible verdict degrades to Unknown, not false Conflict.
%
% Alignment: α(de) = deu, α(de_AT) = ⊥ (partial — regional variant lost)
%
% Key test : de_AT appears in constraint but has no relationships in
%            LNG001-0.ax. Framework must NOT produce false Conflict.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, deu)).
fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, eq) & has_value(c2, de_AT)).

fof(compatible, conjecture, ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
