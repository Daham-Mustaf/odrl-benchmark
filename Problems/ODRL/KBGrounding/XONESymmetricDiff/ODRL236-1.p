%--------------------------------------------------------------------------
% File     : ODRL236-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE All-Pairs Matrix — 3 Concepts, All Pairs
% Expected : Theorem
% Verdict  : XONEMatrix
% Paper    : XONE All-Pairs Matrix — 3 Concepts, All Pairs
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:germany ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:france ] ] .
%   %
%   %   ex:policyC a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:poland ] ] .
%
% Formal test:
%   XONE all-pairs: prove symmetric difference non-empty for ALL C(3,2) = 3 pairs.
%   %   de△fr ≠ ∅ [witness: germany, de ⊥ fr sibling]
%   %   de△pl ≠ ∅ [witness: germany, de ⊥ pl derived]
%   %   fr△pl ≠ ∅ [witness: france, fr ⊥ pl derived]
%   %   3 witnesses, 6 negative proofs → massive proof obligation.
%
% One-liner : XONE matrix: all C(3,2)=3 pairwise symmetric diffs non-empty
% Difficulty: Extreme
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl236, conjecture,
    ( ?[X1]: ( ( in_denotation(X1, germany, isPartOf)
               & ~in_denotation(X1, france, isPartOf) )
             | ( ~in_denotation(X1, germany, isPartOf)
               & in_denotation(X1, france, isPartOf) ) )
    & ?[X2]: ( ( in_denotation(X2, germany, isPartOf)
               & ~in_denotation(X2, poland, isPartOf) )
             | ( ~in_denotation(X2, germany, isPartOf)
               & in_denotation(X2, poland, isPartOf) ) )
    & ?[X3]: ( ( in_denotation(X3, france, isPartOf)
               & ~in_denotation(X3, poland, isPartOf) )
             | ( ~in_denotation(X3, france, isPartOf)
               & in_denotation(X3, poland, isPartOf) ) ) )).

%--------------------------------------------------------------------------