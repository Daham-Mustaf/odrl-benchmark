%--------------------------------------------------------------------------
% File     : KGC402-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : eq / Unknown: dpv:ScientificResearch x dpv:CommercialResearch
% Version  : 1.0
% English  : eq operator, Unknown verdict.  DPV asserts neither equality
%           : nor disjointness between ScientificResearch and
%           : CommercialResearch directly; OWA leaves the verdict open.
%           : 
%           : FOF side: Vampire returns CounterSatisfiable - verdict_unknown
%           : is not derivable as a theorem under OWA.
%           : SMT side: Z3 returns sat - the axioms have a model where
%           : neither Compatible nor Conflict is forced.
%
% Refs     : [Mus+26b] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Denotational Semantics for ODRL: Knowledge-Based Constraint Conflict Detection. 2026. arXiv:2602.19883. https://arxiv.org/abs/2602.19883
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : KGC402-1.p
%
% Status   : CounterSatisfiable
% Verdict  : Unknown
% SPC      : FOF_CSA_RFN
%
% Comments : KB-grounding tier. arXiv:2602.19883.
%           : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC402-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/DPV000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_eq(X, dpv_scientific_research))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, dpv_commercial_research))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc402, conjecture,
    verdict_unknown(c_offer, c_request)).
%--------------------------------------------------------------------------
