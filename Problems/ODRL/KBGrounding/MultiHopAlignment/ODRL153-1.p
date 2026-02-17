%--------------------------------------------------------------------------
% File     : ODRL153-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : 2-Hop Intermediate — 1-Hop Result as Prerequisite
% Expected : Theorem
% Verdict  : Conflict
% Paper    : 2-Hop Intermediate — 1-Hop Result as Prerequisite
%
% ODRL Policy (Conceptual):
%   (Proves intermediate result needed for ODRL150 hop 2)
%
% Formal test:
%   1-hop alignment: GEO → ISO
%   %   disj(wE,eE) → disj_downward → disj(de,pl)
%   %   align(de,dE) + align(pl,pL) + align_disj_forward → disj(dE,pL)
%   %   Tests: hop 1 result that feeds into ODRL150.
%
% One-liner : Intermediate: hop 1 derives disjoint(dE, pL)
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl153, conjecture, disjoint(dE, pL)).

%--------------------------------------------------------------------------