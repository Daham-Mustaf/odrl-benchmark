%--------------------------------------------------------------------------
% File     : ODRL010-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Transitive spatial containment: bavaria ⪯ europe
% Version  : GEO000-0.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe, 
% Notes    : Tests mereological transitivity (paper Def. 2).
%            bavaria partOf germany, germany partOf europe,
%            therefore bavaria partOf europe.
%            This is the minimal non-trivial inference the
%            grounding framework requires.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').

fof(odrl010_transitive_containment, conjecture,
    partOf(bavaria, europe)).
%--------------------------------------------------------------------------
