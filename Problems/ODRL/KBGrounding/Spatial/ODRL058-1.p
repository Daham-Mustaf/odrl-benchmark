%--------------------------------------------------------------------------
% File     : ODRL058-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : All 6 multi-parent concepts verified in DAG-safe mode
% Expected : Theorem
% Verdict  : Verified
% Paper    : Note 1 — All 6 Multi-Parent Concepts (Table 1)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:commercialResearch ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:nonCommercialResearch ] ] .
%
%   ex:policy3 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:personalisedAdvertising ] ] .
%
%   ex:policy4 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:servicePersonalisation ] ] .
%
%   ex:policy5 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:communicationForCustomerCare ] ] .
%
%   ex:policy6 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:hasPurpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:improveInternalCRMProcesses ] ] .
%
% Denotation analysis:
%   Validates all 6 multi-parent concepts from paper Table 1:
%   1. commercialResearch (commercialPurpose ∧ researchAndDevelopment)
%   2. nonCommercialResearch (nonCommercialPurpose ∧ researchAndDevelopment)
%   3. personalisedAdvertising (advertising ∧ personalisation)
%   4. servicePersonalisation (personalisation ∧ serviceProvision)
%   5. communicationForCustomerCare (communicationManagement ∧ customerCare)
%   6. improveInternalCRMProcesses (customerRelationshipManagement ∧ optimisationForController)
% Each can witness both parents in DAG-SAFE mode
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(multi1, conjecture,
    ?[X1]: ( in_denotation(X1, commercialPurpose, isA)
           & in_denotation(X1, researchAndDevelopment, isA) )).
fof(multi2, conjecture,
    ?[X2]: ( in_denotation(X2, nonCommercialPurpose, isA)
           & in_denotation(X2, researchAndDevelopment, isA) )).
fof(multi3, conjecture,
    ?[X3]: ( in_denotation(X3, advertising, isA)
           & in_denotation(X3, personalisation, isA) )).
fof(multi4, conjecture,
    ?[X4]: ( in_denotation(X4, personalisation, isA)
           & in_denotation(X4, serviceProvision, isA) )).
fof(multi5, conjecture,
    ?[X5]: ( in_denotation(X5, communicationManagement, isA)
           & in_denotation(X5, customerCare, isA) )).
fof(multi6, conjecture,
    ?[X6]: ( in_denotation(X6, customerRelationshipManagement, isA)
           & in_denotation(X6, optimisationForController, isA) )).
%--------------------------------------------------------------------------
