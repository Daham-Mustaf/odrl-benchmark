"""
gen_layer1_deontic.py
=====================
Generates the Layer 1 deontic grounding axiom files:
  Problems/DeonticOntology/Axioms/Layer1-Deontic/GRND-AX-1.ax    — FOF/TPTP
  Problems/DeonticOntology/Axioms/Layer1-Deontic/GRND-AX-1.smt2  — SMT-LIB reference

Contains: Ax5.1-5.11, A1-A3, B1-B3
Requires: Layer0-Signature/GRND000-0.ax (included by problem files, not here)

SMT-LIB note:
  GRND-AX-1.smt2 is a reference/documentation file only.
  SMT-LIB has no include directive — axioms are embedded directly in
  each .smt2 problem file by gen_foundation_problems.py.
  SMT2_AXIOMS is imported from axiom_data.py to guarantee the reference
  copy is always identical to what is embedded.

Usage:
    uv run Generators/DeonticOntology/gen_layer1_deontic.py \
      --out-dir Problems/DeonticOntology/Axioms/Layer1-Deontic
"""
import argparse
import textwrap
from pathlib import Path
from datetime import date
import sys
sys.path.insert(0, str(Path(__file__).parent))
from axiom_data import SMT2_AXIOMS

META = {
    "domain":  "Deontic Ontology / ODRL Grounding",
    "source":  "Mohammed et al., What Does ODRL Mean? FOIS 2026",
    "version": "1.5",
}


def header() -> str:
    return textwrap.dedent(f"""\
        %--------------------------------------------------------------------------
        % File     : GRND-AX-1.ax
        % Domain   : {META['domain']}
        % Axioms   : Deontic grounding axioms (Ax5.1-5.11, A1-A3, B1-B3)
        % Version  : {META['version']}
        % English  : Layer 1 axioms for ODRL deontic grounding.
        %            Requires Layer0-Signature/GRND000-0.ax (included by
        %            problem files via include() — not repeated here).
        %
        %            Ax5.1   Permission Relator — Basic
        %            Ax5.2   Permission Relator — Strong (founds_imm; rho_P != rho_I)
        %            Ax5.3   Prohibition Relator — Basic
        %            Ax5.4   Prohibition Relator — Remedy (founds_rem; rho_F != rho_R)
        %            Ax5.5a  Unique Founding — founds
        %            Ax5.5b  Unique Event    — founds
        %            Ax5.5c  Unique Founding — founds_rem
        %            Ax5.5d  Unique Founding — founds_imm
        %            Ax5.6   Obligation Relator
        %            Ax5.7   ODRL Relator Typing (3 rules: founds / founds_rem / founds_imm)
        %            Ax5.8   Correlativity (4 biconditionals)
        %            Ax5.9   Conflict Detection (within relator)
        %            Ax5.10  Cross-Relator Position Incompatibility
        %            Ax5.11  Disability Precludes Prohibition Creation
        %            A1      Normative State Changes Require Institutional Event
        %            A2      Institutional Events Require Competent Agent
        %            A3      Competence Is a Power-Subjection Pair
        %            B1      Performing Prohibited Action = NormStateChange
        %            B2      Power Content Links to Founding Event (founds_rem)
        %            B3      Subjection Content Links to Founding Event (founds_rem)
        %
        % Source   : {META['source']}
        % Generated: {date.today().isoformat()} by gen_layer1_deontic.py
        %
        % Status   : Layer 1 — Theory-Specific Deontic Axioms
        %
        % Syntax   : Number of formulae : 25 (0 unt; 0 def)
        %
        % SPC      : FOF_THM_RFN
        %
        % Predicates (from Layer0 — UFO-L terms):
        %   perm/1, proh/1, obl/1, has_rem/1, strong/1
        %   aee/2, aer/2, act/2, tgt/2, activates/2
        %   founds/3, founds_rem/3, founds_imm/3
        %   part_of/2, bearer/2, cnt/3
        %   permission/1, no_right/1, duty/1, right/1
        %   power/1, subjection/1, immunity/1, disability/1
        %   odrl_rel/1, action/1, forbearance/1
        %
        % Functions (from Layer0):
        %   rfr/1  : Act -> Forbearance
        %   decl/1 : Act -> Act
        %
        % Appendix A.0 predicates (declared in problem files):
        %   norm_state_change/4, inst_event/1, triggers/5
        %   competent_for/2, about_event/2, does/3, rem_act/2, duty_rem/0
        %
        % CHANGELOG v1.5:
        %   - Bug 1 : liberty -> permission, claim -> right (UFO-L terms)
        %   - Bug 2 : B1 existential B with rem_act guard (was unsound)
        %   - Bug 4 : Ax5.2 uses founds_imm for rho_I (rho_P != rho_I)
        %   - Bug 5 : Ax5.4 uses founds_rem for rho_R (rho_F != rho_R)
        %   - Added : ax_unique_founding_rem, ax_unique_founding_imm
        %   - Added : ax_odrl_rel_typing + _rem + _imm
        %   - B2/B3 : updated to founds_rem
        %   - Count : 20 -> 25 axioms
        % CHANGELOG v1.4:
        %   - version aligned with gen_foundation_problems.py v1.4
        %   - GRND-AX-1.smt2 imported from axiom_data.SMT2_AXIOMS
        %--------------------------------------------------------------------------
    """)


AXIOMS = """\
%--------------------------------------------------------------------------
% Ax5.1  Permission Relator — Basic
% A permission activation founds a relator with Permission + NoRight.
%--------------------------------------------------------------------------
fof(ax_perm_relator_basic, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T) & activates(E,P) )
     => ? [Rho, L, N] :
          ( founds(E,Rho,P)
          & permission(L) & bearer(L,X) & cnt(L,A,T) & part_of(L,Rho)
          & no_right(N)   & bearer(N,Y) & cnt(N,A,T) & part_of(N,Rho) ) )).

%--------------------------------------------------------------------------
% Ax5.2  Permission Relator — Strong
% Requires strong(P) asserted by profile extension (not ODRL 2.2).
% rho_I is a DISTINCT simple relator founded by founds_imm, not founds,
% so ax_unique_founding cannot collapse rho_P = rho_I.
%--------------------------------------------------------------------------
fof(ax_perm_relator_strong, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & strong(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T)
        & activates(E,P) )
     => ? [RhoI, Im, Db] :
          ( founds_imm(E,RhoI,P)
          & immunity(Im)   & bearer(Im,X) & cnt(Im,A,T) & part_of(Im,RhoI)
          & disability(Db) & bearer(Db,Y) & cnt(Db,A,T) & part_of(Db,RhoI) ) )).

%--------------------------------------------------------------------------
% Ax5.3  Prohibition Relator — Basic
% A prohibition activation founds a relator with Duty + Right.
% Content is rfr(A) — the forbearance of performing A.
%--------------------------------------------------------------------------
fof(ax_proh_relator_basic, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) & activates(E,F) )
     => ? [Rho, D, C] :
          ( founds(E,Rho,F)
          & duty(D)  & bearer(D,X) & cnt(D,rfr(A),T) & part_of(D,Rho)
          & right(C) & bearer(C,Y) & cnt(C,rfr(A),T) & part_of(C,Rho) ) )).

%--------------------------------------------------------------------------
% Ax5.4  Prohibition Relator — Remedy
% rho_R is a DISTINCT simple relator founded by founds_rem, not founds,
% so ax_unique_founding cannot collapse rho_F = rho_R.
% Power is constituted at activation time, not at violation time.
%--------------------------------------------------------------------------
fof(ax_proh_relator_remedy, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & has_rem(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T)
        & activates(E,F) )
     => ? [RhoR, Pw, S] :
          ( founds_rem(E,RhoR,F)
          & power(Pw)     & bearer(Pw,Y) & cnt(Pw,decl(A),T) & part_of(Pw,RhoR)
          & subjection(S) & bearer(S,X)  & cnt(S,decl(A),T)  & part_of(S,RhoR) ) )).

%--------------------------------------------------------------------------
% Ax5.5a  Unique Founding — founds
% Same event+rule founds at most one relator (UFO axiom a77).
%--------------------------------------------------------------------------
fof(ax_unique_founding, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds(E,Rho1,R) & founds(E,Rho2,R) ) => Rho1 = Rho2 )).

%--------------------------------------------------------------------------
% Ax5.5b  Unique Event — founds
% Same relator+rule founded by at most one event.
%--------------------------------------------------------------------------
fof(ax_unique_relator_per_event, axiom,
    ! [R, E1, E2, Rho] :
      ( ( founds(E1,Rho,R) & founds(E2,Rho,R) ) => E1 = E2 )).

%--------------------------------------------------------------------------
% Ax5.5c  Unique Founding — founds_rem
% Same event+rule founds at most one remedy-competence relator.
%--------------------------------------------------------------------------
fof(ax_unique_founding_rem, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds_rem(E,Rho1,R) & founds_rem(E,Rho2,R) ) => Rho1 = Rho2 )).

%--------------------------------------------------------------------------
% Ax5.5d  Unique Founding — founds_imm
% Same event+rule founds at most one immunity-competence relator.
%--------------------------------------------------------------------------
fof(ax_unique_founding_imm, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds_imm(E,Rho1,R) & founds_imm(E,Rho2,R) ) => Rho1 = Rho2 )).

%--------------------------------------------------------------------------
% Ax5.6  Obligation Relator
% An obligation activation founds a relator with Duty + Right.
%--------------------------------------------------------------------------
fof(ax_obl_relator, axiom,
    ! [D, X, Y, A, T, E] :
      ( ( obl(D) & aee(D,X) & aer(D,Y) & act(D,A) & tgt(D,T) & activates(E,D) )
     => ? [Rho, Du, C] :
          ( founds(E,Rho,D)
          & duty(Du) & bearer(Du,X) & cnt(Du,A,T) & part_of(Du,Rho)
          & right(C) & bearer(C,Y)  & cnt(C,A,T)  & part_of(C,Rho) ) )).

%--------------------------------------------------------------------------
% Ax5.7  ODRL Relator Typing
% All three founding predicates produce odrl_rel-typed relators.
%--------------------------------------------------------------------------
fof(ax_odrl_rel_typing, axiom,
    ! [E, Rho, R] :
      ( ( founds(E,Rho,R) & ( perm(R) | proh(R) | obl(R) ) )
     => odrl_rel(Rho) )).

fof(ax_odrl_rel_typing_rem, axiom,
    ! [E, Rho, R] :
      ( ( founds_rem(E,Rho,R) & proh(R) )
     => odrl_rel(Rho) )).

fof(ax_odrl_rel_typing_imm, axiom,
    ! [E, Rho, R] :
      ( ( founds_imm(E,Rho,R) & perm(R) )
     => odrl_rel(Rho) )).

%--------------------------------------------------------------------------
% Ax5.8  Correlativity (4 biconditionals, content-binding)
% Each ODRL relator pairs each position with exactly one correlative
% over the same action-target content. odrl_rel(Rho) guards each.
%--------------------------------------------------------------------------
fof(ax_correlativity_permission, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [L] : ( permission(L) & part_of(L,Rho) & cnt(L,A,T) ) )
        <=> ( ? [N] : ( no_right(N) & part_of(N,Rho) & cnt(N,A,T)
                      & ! [M] : ( ( no_right(M) & part_of(M,Rho) & cnt(M,A,T) )
                                 => M = N ) ) ) ) )).

fof(ax_correlativity_duty, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [D] : ( duty(D)  & part_of(D,Rho) & cnt(D,A,T) ) )
        <=> ( ? [C] : ( right(C) & part_of(C,Rho) & cnt(C,A,T)
                      & ! [K] : ( ( right(K) & part_of(K,Rho) & cnt(K,A,T) )
                                 => K = C ) ) ) ) )).

fof(ax_correlativity_power, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [Pw] : ( power(Pw)     & part_of(Pw,Rho) & cnt(Pw,A,T) ) )
        <=> ( ? [S] : ( subjection(S) & part_of(S,Rho)  & cnt(S,A,T)
                      & ! [S2] : ( ( subjection(S2) & part_of(S2,Rho) & cnt(S2,A,T) )
                                  => S2 = S ) ) ) ) )).

fof(ax_correlativity_immunity, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [Im] : ( immunity(Im)    & part_of(Im,Rho)  & cnt(Im,A,T) ) )
        <=> ( ? [Db] : ( disability(Db) & part_of(Db,Rho) & cnt(Db,A,T)
                       & ! [Db2] : ( ( disability(Db2) & part_of(Db2,Rho) & cnt(Db2,A,T) )
                                    => Db2 = Db ) ) ) ) )).

%--------------------------------------------------------------------------
% Ax5.9  Conflict Detection (within relator)
% No ODRL relator contains Permission and Duty-to-refrain for same bearer.
%--------------------------------------------------------------------------
fof(ax_conflict_detection, axiom,
    ! [Rho, L, D, X, A, T] :
      ( ( part_of(L,Rho) & part_of(D,Rho)
        & permission(L) & duty(D)
        & bearer(L,X) & bearer(D,X)
        & cnt(L,A,T)  & cnt(D,rfr(A),T) )
     => $false )).

%--------------------------------------------------------------------------
% Ax5.10  Cross-Relator Position Incompatibility
% Permission and Duty-to-refrain cannot be co-borne regardless of relator.
% Normative axiom — independent of UFO type disjointness (paper Ax5.9).
%--------------------------------------------------------------------------
fof(ax_cross_relator_consistency, axiom,
    ! [L, D, X, A, T] :
      ( ( permission(L) & bearer(L,X) & cnt(L,A,T)
        & duty(D)       & bearer(D,X) & cnt(D,rfr(A),T) )
     => $false )).

%--------------------------------------------------------------------------
% Ax5.11  Disability Precludes Prohibition Creation
% No prohibition by Y over (A,T) can exist while Y holds Disability
% over (A,T). Disability renders the institutional act void.
%--------------------------------------------------------------------------
fof(ax_disability_block, axiom,
    ! [F, X, Y, A, T] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) )
     => ~ ? [Db] : ( disability(Db) & bearer(Db,Y) & cnt(Db,A,T) ) )).

%--------------------------------------------------------------------------
% A1  Normative State Changes Require an Institutional Event
%--------------------------------------------------------------------------
fof(ax_A1, axiom,
    ! [X, A, T, Q] :
      ( norm_state_change(X,A,T,Q)
     => ? [E] : ( inst_event(E) & triggers(E,X,A,T,Q) ) )).

%--------------------------------------------------------------------------
% A2  Institutional Events Require a Competent Agent
%--------------------------------------------------------------------------
fof(ax_A2, axiom,
    ! [E] :
      ( inst_event(E)
     => ? [Y] : competent_for(Y,E) )).

%--------------------------------------------------------------------------
% A3  Competence Is a Power-Subjection Pair
%--------------------------------------------------------------------------
fof(ax_A3, axiom,
    ! [Y, E] :
      ( competent_for(Y,E)
     => ? [Pw, S, X] :
          ( power(Pw)     & bearer(Pw,Y) & about_event(Pw,E)
          & subjection(S) & bearer(S,X)  & about_event(S,E) ) )).

%--------------------------------------------------------------------------
% B1  Performing a Prohibited Action Constitutes a NormStateChange
% B is existentially quantified and guarded by rem_act so the state
% change is scoped to the remedy action of F (not every action).
%--------------------------------------------------------------------------
fof(ax_B1, axiom,
    ! [F, X, A, T] :
      ( ( proh(F) & has_rem(F) & act(F,A) & tgt(F,T) & aee(F,X) & does(X,A,T) )
     => ? [B] : ( rem_act(F,B) & norm_state_change(X,B,T,duty_rem) ) )).

%--------------------------------------------------------------------------
% B2  Power Content Links to Founding Event (via founds_rem)
% Power lives in rho_R, not rho_F, so founds_rem is the correct predicate.
%--------------------------------------------------------------------------
fof(ax_B2, axiom,
    ! [Pw, A, T, Rho, E, R] :
      ( ( power(Pw) & cnt(Pw,decl(A),T) & part_of(Pw,Rho) & founds_rem(E,Rho,R) )
     => about_event(Pw,E) )).

%--------------------------------------------------------------------------
% B3  Subjection Content Links to Founding Event (via founds_rem)
% Subjection lives in rho_R, not rho_F, so founds_rem is correct.
%--------------------------------------------------------------------------
fof(ax_B3, axiom,
    ! [S, A, T, Rho, E, R] :
      ( ( subjection(S) & cnt(S,decl(A),T) & part_of(S,Rho) & founds_rem(E,Rho,R) )
     => about_event(S,E) )).
"""


def generate() -> str:
    return header() + "\n" + AXIOMS


def main():
    parser = argparse.ArgumentParser(
        description="Generate GRND-AX-1.ax and GRND-AX-1.smt2 — Layer 1 deontic axioms."
    )
    parser.add_argument(
        "--out-dir",
        default="Problems/DeonticOntology/Axioms/Layer1-Deontic",
    )
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    content = generate()

    if args.stdout:
        print(content)
        return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Write FOF axiom file
    ax_path = out_dir / "GRND-AX-1.ax"
    ax_path.write_text(content, encoding="utf-8")
    axiom_count = content.count("fof(")
    print(f"Written: {ax_path}")
    print(f"  Lines : {content.count(chr(10))}")
    print(f"  Axioms: {axiom_count}")
    print(f"\nInclude in problem files with:")
    print(f"  include('Axioms/Layer1-Deontic/GRND-AX-1.ax').")

    # Write SMT-LIB reference copy
    # SMT2_AXIOMS imported from axiom_data.py — guaranteed identical to
    # what is embedded in every .smt2 problem file by gen_foundation_problems.py.
    smt2_lines = [
        "; --------------------------------------------------------------------------",
        "; File     : GRND-AX-1.smt2",
        "; Domain   : Deontic Ontology / ODRL Grounding",
        f"; Version  : {META['version']}",
        "; Axioms   : Layer 1 deontic grounding axioms (Ax5.1-5.11, A1-A3, B1-B3)",
        f"; Refs     : {META['source']}",
        f"; Generated: {date.today().isoformat()} by gen_layer1_deontic.py",
        ";",
        "; NOTE: SMT-LIB 2 has no include directive.",
        "; These axioms are embedded directly in each .smt2 problem file.",
        "; This file is the authoritative reference — generated from",
        "; axiom_data.SMT2_AXIOMS to guarantee identity with embedded content.",
        "; --------------------------------------------------------------------------",
        "",
    ]
    for name, formula in SMT2_AXIOMS:
        smt2_lines.append(f"; {name}")
        smt2_lines.append(formula)
        smt2_lines.append("")

    smt2_path = out_dir / "GRND-AX-1.smt2"
    smt2_path.write_text("\n".join(smt2_lines), encoding="utf-8")

    smt2_count = len(SMT2_AXIOMS)
    print(f"Written: {smt2_path}")
    print(f"  SMT-LIB axiom blocks: {smt2_count}")


if __name__ == "__main__":
    main()