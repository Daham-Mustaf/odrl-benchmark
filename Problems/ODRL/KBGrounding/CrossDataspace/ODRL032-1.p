%--------------------------------------------------------------------------
% File     : ODRL032-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-dataspace diagnosis: purpose is the blocking operand
% Version  : GEO000-0.ax, DPV000-0.ax, ODRL000-0.ax, GROUND000-1.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe,  2026
% Notes    : Same setup as ODRL031-1.
%            After conjunction fails, we diagnose which operand blocks.
%            Conjecture: purpose pair has empty intersection.
%            advertising ⊄ nonCommercialPurpose (disjointness axiom)
%            → conflict on purpose dimension → Theorem.
%            Models real dataspace diagnostic workflow:
%            (1) test overall compatibility → fails
%            (2) test per-operand conflict → identifies purpose.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% --- Policy A: purpose isA nonCommercialPurpose ---

fof(policy_a_constraint_purpose, axiom, has_constraint(policy_a, c3)).
fof(c3_operand,  axiom, has_operand(c3, purpose)).
fof(c3_operator, axiom, has_operator(c3, isA)).
fof(c3_value,    axiom, has_value(c3, nonCommercialPurpose)).

% --- Request B: purpose eq advertising ---

fof(request_b_constraint_purpose, axiom, has_constraint(request_b, c4)).
fof(c4_operand,  axiom, has_operand(c4, purpose)).
fof(c4_operator, axiom, has_operator(c4, eq)).
fof(c4_value,    axiom, has_value(c4, advertising)).

% --- Conjecture: purpose pair has empty intersection (conflict) ---

fof(odrl032_purpose_conflict, conjecture,
    ~?[Y]: (in_denotation(Y, c3) & in_denotation(Y, c4))).
%--------------------------------------------------------------------------
