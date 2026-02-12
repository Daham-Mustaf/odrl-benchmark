%--------------------------------------------------------------------------
% File     : ODRL054-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Language isAnyOf compatible: en_GB ⊑ en ∈ {de, en}↓
% Status   : Theorem
% Expected : Compatible — witness = en_GB via English branch
%
% Scenario : Hamburger Kunsthalle permits metadata in German or
%            English. British Museum requests in British English.
%            en_GB ⊑ en → compatible via English branch.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_operand,  axiom, has_operand(c1, language)).
fof(c1_operator, axiom, has_operator(c1, isAnyOf)).
fof(c1_val_de,   axiom, has_value(c1, de)).
fof(c1_val_en,   axiom, has_value(c1, en)).

fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, eq) & has_value(c2, en_GB)).

fof(compatible, conjecture, ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
