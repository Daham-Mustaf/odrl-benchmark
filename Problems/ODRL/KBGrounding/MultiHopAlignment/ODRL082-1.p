%--------------------------------------------------------------------------
% File     : ODRL082-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Lemma 3: denotation transfer derivable from Part A + ODRL000-0.ax
% Expected : Theorem
% Verdict  : Derivable
% Paper    : Lemma 3 — Denotation Transfer Derivability
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   Prove: in_den(X,G,isPartOf) ∧ align(X,Xp) ∧ align(G,Gp)
%          ⟹ in_den(Xp, Gp, isPartOf)
%   Proof: den_isPartOf_onlyif → leq(X,G)
%          align_order_forward → leq(Xp,Gp)
%          den_isPartOf_if → in_denotation(Xp,Gp,isPartOf)
%
% Notes    : Part A inlined; ALIGN000-0.ax NOT loaded. Meta-theorem verification.
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
% --- Inline Part A of ALIGN000-0.ax (Definition 8) ---
fof(align_order_forward, axiom,
    ![X,Y,Xp,Yp]: ((align(X, Xp) & align(Y, Yp) & leq(X, Y))
        => leq(Xp, Yp))).
fof(align_order_backward, axiom,
    ![X,Y,Xp,Yp]: ((align(X, Xp) & align(Y, Yp) & leq(Xp, Yp))
        => leq(X, Y))).
fof(align_disj_forward, axiom,
    ![X,Y,Xp,Yp]: ((align(X, Xp) & align(Y, Yp) & disjoint(X, Y))
        => disjoint(Xp, Yp))).
fof(align_injective, axiom,
    ![X,Y,Z]: ((align(X, Z) & align(Y, Z)) => (X = Y))).
fof(align_functional, axiom,
    ![X,Y,Z]: ((align(X, Y) & align(X, Z)) => (Y = Z))).
fof(align_typed, axiom,
    ![X,Y]: (align(X, Y) => (concept(X) & concept(Y)))).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl082, conjecture,
    ![X,G,Xp,Gp]: ((in_denotation(X, G, isPartOf)
                    & align(X, Xp)
                    & align(G, Gp))
        => in_denotation(Xp, Gp, isPartOf))).
%--------------------------------------------------------------------------
