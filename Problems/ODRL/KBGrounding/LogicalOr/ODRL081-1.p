%--------------------------------------------------------------------------
% File     : ODRL081-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : OR conflict: neither branch covers fr
% Status   : Theorem
%
% or(isA de, isA en) vs eq fr
%   Branch 1: ⟦isA de⟧ ∩ ⟦eq fr⟧ = ∅ (fr ⊄ de)
%   Branch 2: ⟦isA en⟧ ∩ ⟦eq fr⟧ = ∅ (fr ⊄ en)
%   or: both branches empty → Conflict
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, de)).
fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, isA) & has_value(c2, en)).
fof(c3_def, axiom, has_operand(c3, language) & has_operator(c3, eq) & has_value(c3, fr)).

fof(or_conflict, conjecture,
    ~((?[X]: (in_denotation(X, c1) & in_denotation(X, c3)))
    | (?[Y]: (in_denotation(Y, c2) & in_denotation(Y, c3))))).
%--------------------------------------------------------------------------
