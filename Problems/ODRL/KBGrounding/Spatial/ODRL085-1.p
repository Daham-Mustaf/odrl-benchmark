%--------------------------------------------------------------------------
% File     : ODRL085-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Graceful degradation: unmapped concept → Unknown
% Expected : CounterSatisfiable
% Verdict  : Unknown
% Paper    : Proposition 2(2) — Graceful Degradation
%
% ODRL Policy (Turtle):
%   Dataspace A (GEO): permission spatial isPartOf westernEurope
%   Dataspace B (ISO): prohibition spatial eq dE
%
% Denotation analysis:
%   westernEurope has NO ISO 3166 counterpart (unmapped).
%   leq(dE, westernEurope) NOT derivable — align_order_backward needs
%   align(???, westernEurope) which doesn't exist.
%   Verdict degrades to Unknown (Prop 2.2): cannot prove or refute overlap.
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').

fof(odrl085, conjecture,
    ?[X]: ( in_denotation(X, westernEurope, isPartOf)
          & in_denotation(X, dE, eq) )).
%--------------------------------------------------------------------------
