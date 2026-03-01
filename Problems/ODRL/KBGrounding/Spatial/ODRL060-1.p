%--------------------------------------------------------------------------
% File     : ODRL060-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Tautology: isPartOf(europe) = C (root covers all concepts)
% Expected : Theorem
% Verdict  : Tautological
% Paper    : Tautology Detection
%
% ODRL Policy (Turtle):
%   c: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .
%
% Formal:
%   ⟦isPartOf(europe)⟧ = {X ∈ C | leq(X, europe)} = C
%   europe is the root of GEO KB (26 concepts, no world above)
%   Ground encoding: prove leq(c, europe) for each of the 26 named concepts
%   Chain: country → sub-region → europe by transitivity
%
% Notes    : Ground conjunction over all 26 GEO concepts. No concept/1 predicate: open-world quantification is unsound for tautology.
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl060, conjecture,
    ( in_denotation(europe, europe, isPartOf) & in_denotation(westernEurope, europe, isPartOf) & in_denotation(easternEurope, europe, isPartOf) & in_denotation(northernEurope, europe, isPartOf)
    & in_denotation(southernEurope, europe, isPartOf) & in_denotation(germany, europe, isPartOf) & in_denotation(france, europe, isPartOf) & in_denotation(austria, europe, isPartOf)
    & in_denotation(belgium, europe, isPartOf) & in_denotation(liechtenstein, europe, isPartOf) & in_denotation(luxembourg, europe, isPartOf) & in_denotation(monaco, europe, isPartOf)
    & in_denotation(netherlands, europe, isPartOf) & in_denotation(switzerland, europe, isPartOf) & in_denotation(poland, europe, isPartOf) & in_denotation(czechia, europe, isPartOf)
    & in_denotation(slovakia, europe, isPartOf) & in_denotation(hungary, europe, isPartOf) & in_denotation(sweden, europe, isPartOf) & in_denotation(norway, europe, isPartOf)
    & in_denotation(finland, europe, isPartOf) & in_denotation(denmark, europe, isPartOf) & in_denotation(italy, europe, isPartOf) & in_denotation(spain, europe, isPartOf)
    & in_denotation(bavaria, europe, isPartOf) & in_denotation(ileDeFrance, europe, isPartOf) )).
%--------------------------------------------------------------------------
