%--------------------------------------------------------------------------
% File     : KGC422-1.p
% Domain   : ODRL Policy / KB Grounding Concept-valued
% Problem  : isPartOf / Unknown: isPartOf gn:Germany x eq gn:Strasbourg
% Version  : 1.0
% English  : isPartOf operator, Unknown verdict.  GeoNames asserts neither
%           : Strasbourg <= Germany nor disjointness; OWA gives Unknown.
%           : (In closed-world geography, Strasbourg is in France, but
%           : GeoNames doesn't assert sibling-country disjointness.)
%
% Refs     : [Mus+26b] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Denotational Semantics for ODRL: Knowledge-Based Constraint Conflict Detection. 2026. arXiv:2602.19883. https://arxiv.org/abs/2602.19883
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : KGC422-1.p
%
% Status   : CounterSatisfiable
% Verdict  : Unknown
% SPC      : FOF_CSA_RFN
%
% Comments : KB-grounding tier. arXiv:2602.19883.
%           : Requires Axioms/KGE000-0.ax + Axioms/DENOT000-0.ax + resource axioms.
%           : Policy source: Policies/KGC422-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/KGE000-0.ax').
include('Axioms/DENOT000-0.ax').
include('Axioms/GN000-0.ax').

% ─── Constraint tokens, groundings, and resource hooks ───────────────────
% Constraint tokens: defined denotations.
fof(c_offer_defined,   axiom, ~denotation_undef(c_offer)).
fof(c_request_defined, axiom, ~denotation_undef(c_request)).

% Denotations
fof(c_offer_den,   axiom,
    ![X]: (in_denotation(X, c_offer)   <=> den_ispartof(X, gn_germany))).
fof(c_request_den, axiom,
    ![X]: (in_denotation(X, c_request) <=> den_eq(X, gn_strasbourg))).
% ─── Conjecture ────────────────────────────────────────────────────
fof(kgc422, conjecture,
    verdict_unknown(c_offer, c_request)).
%--------------------------------------------------------------------------
