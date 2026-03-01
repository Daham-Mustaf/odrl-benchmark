%--------------------------------------------------------------------------
% File     : ODRL156-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : 3-Hop Ablation — COMP Alone Cannot Detect Conflict
% Expected : CounterSatisfiable
% Verdict  : Unknown
% Paper    : 3-Hop Ablation — COMP Alone Cannot Detect Conflict
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand comp:gdprFull ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand comp:gdprPartial ] ] .
%
% Formal test:
%   Same query as ODRL154 but WITHOUT GEO/ISO/SYNTH/alignment.
%   %   COMP has no disjoint axioms → prover cannot derive disj(gdprFull, gdprPartial).
%   %   → Unknown (expected timeout).
%
% One-liner : Ablation: COMP alone → Unknown (no disjointness)
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
% --- Compliance KB (COMP) — NO native disjointness ---
% 4th dataspace: GDPR compliance tier classification.
% Concepts align to SYNTH (regulatory zones) but have no sibling disjointness.
% Disjointness must be derived through 3-hop alignment: GEO → ISO → SYNTH → COMP.
fof(comp_root, axiom, concept(complianceScope)).
fof(comp_c1, axiom, concept(gdprFull)).
fof(comp_c2, axiom, concept(gdprPartial)).

fof(comp_leq1, axiom, leq(gdprFull, complianceScope)).
fof(comp_leq2, axiom, leq(gdprPartial, complianceScope)).
fof(comp_refl1, axiom, leq(complianceScope, complianceScope)).
fof(comp_refl2, axiom, leq(gdprFull, gdprFull)).
fof(comp_refl3, axiom, leq(gdprPartial, gdprPartial)).

% NO disjoint axiom — must come from 3-hop alignment
fof(comp_una, axiom, $distinct(complianceScope, gdprFull, gdprPartial)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl156, conjecture,
    ?[X]: ( in_denotation(X, gdprFull, isPartOf)
          & in_denotation(X, gdprPartial, isPartOf) )).

%--------------------------------------------------------------------------