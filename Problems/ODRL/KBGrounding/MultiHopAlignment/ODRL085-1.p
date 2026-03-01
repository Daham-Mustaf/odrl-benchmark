%--------------------------------------------------------------------------
% File     : ODRL085-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Graceful degradation: unmapped concept westernEurope → Unknown
% Expected : CounterSatisfiable
% Verdict  : Unknown
% Paper    : Proposition 2(2) — Graceful Degradation
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   westernEurope has NO ISO 3166 counterpart.
%   align_order_backward needs align(???, westernEurope) — doesn't exist.
%   leq(dE, westernEurope) cannot be derived from ISO alone.
%   Prover cannot prove OR refute overlap → Unknown (Prop 2.2)
%
% Notes    : TPTP: loads full alignment (Vampire searches and fails → CounterSat). SMT2: data-only preamble (no align theory foralls — Z3 loops otherwise). Paired with ODRL083 (mapped concept dE → immediate sat).
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl085, conjecture,
    ?[X]: ( in_denotation(X, westernEurope, isPartOf)
          & in_denotation(X, dE, eq) )).
%--------------------------------------------------------------------------
