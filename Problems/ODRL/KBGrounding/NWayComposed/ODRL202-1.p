%--------------------------------------------------------------------------
% File     : ODRL202-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf — Large Exclusion, Nearly Empty Complement
% Expected : Theorem
% Verdict  : NearEmpty
% Paper    : isNoneOf — Large Exclusion, Nearly Empty Complement
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( geo:westernEurope geo:easternEurope ) ] ] .
%
% Formal test:
%   isNoneOf({wE, eE}) = C \ (↓wE ∪ ↓eE)
%   %   In GEO KB: wE and eE are children of europe, which covers all countries.
%   %   Only europe itself is NOT below wE or eE.
%   %   Prove: the complement is exactly {europe}.
%   %   Extreme: requires exhaustive checking of all 24 GEO concepts.
%
% One-liner : Near-empty complement: isNoneOf({wE,eE}) = {europe} only
% Difficulty: Extreme
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_202_1, axiom, in_value_list(westernEurope, noneList202)).
fof(list_202_2, axiom, in_value_list(easternEurope, noneList202)).
fof(list_noneList202_closed, axiom,
    ![G]: (in_value_list(G, noneList202) => (G = westernEurope | G = easternEurope))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl202, conjecture,
    ![X]: ( in_denotation_set(X, noneList202, isNoneOf)
        => X = europe )).

%--------------------------------------------------------------------------