"""
gen_layer1_deontic.py
=====================
Generates the Layer 1 deontic grounding axiom files:
  Problems/DeonticOntology/Axioms/Layer1-Deontic/GRND-AX-1.ax    — FOF/TPTP
  Problems/DeonticOntology/Axioms/Layer1-Deontic/GRND-AX-1.smt2  — SMT-LIB reference

Contains: Ax5.1-5.10, A1-A3, B1-B3
Requires: Layer0-Signature/GRND000-0.ax (included by problem files, not here)

SMT-LIB note:
  GRND-AX-1.smt2 is a reference/documentation file only.
  SMT-LIB has no include directive — axioms are embedded directly in
  each .smt2 problem file by gen_foundation_problems.py.
  SMT2_AXIOMS is imported from gen_foundation_problems.py to guarantee
  the reference copy is always identical to what is embedded.

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
    "version": "1.4",
}


def header() -> str:
    return textwrap.dedent(f"""\
        %--------------------------------------------------------------------------
        % File     : GRND-AX-1.ax
        % Domain   : {META['domain']}
        % Axioms   : Deontic grounding axioms (Ax5.1-5.10, A1-A3, B1-B3)
        % Version  : {META['version']}
        % English  : Layer 1 axioms for ODRL deontic grounding.
        %            Requires Layer0-Signature/GRND000-0.ax (included by
        %            problem files via include() — not repeated here).
        %
        %            Ax5.1  Permission Relator — Basic
        %            Ax5.2  Permission Relator — Strong
        %            Ax5.3  Prohibition Relator — Basic
        %            Ax5.4  Prohibition Relator — Remedy
        %            Ax5.5a Unique Founding (event+rule -> relator)
        %            Ax5.5b Unique Event (relator+rule -> event)
        %            Ax5.6  Obligation Relator
        %            Ax5.7  Hohfeldian Correlativity (4 parts, content-binding)
        %            Ax5.8  Conflict Detection (single relator)
        %            Ax5.9  Cross-Relator Position Disjointness
        %            Ax5.10 Disability Precludes Prohibition Creation
        %            A1     Normative State Changes Require Institutional Event
        %            A2     Institutional Events Require Competent Agent
        %            A3     Competence Is a Power-Subjection Pair
        %            B1     Performing Prohibited Action = NormStateChange
        %            B2     Power Content Links to Founding Event
        %            B3     Subjection Content Links to Founding Event
        %
        % Source   : {META['source']}
        % Generated: {date.today().isoformat()} by gen_layer1_deontic.py
        %
        % Status   : Layer 1 — Theory-Specific Deontic Axioms
        %
        % Syntax   : Number of formulae : 20 (0 unt; 0 def)
        %
        % SPC      : FOF_THM_RFN
        %
        % Predicates (from Layer0):
        %   perm/1, proh/1, obl/1, has_rem/1, strong/1
        %   aee/2, aer/2, act/2, tgt/2, activates/2
        %   founds/3, part_of/2, bearer/2, cnt/3
        %   liberty/1, no_right/1, duty/1, claim/1
        %   power/1, subjection/1, immunity/1, disability/1
        %   odrl_rel/1, action/1, forbearance/1
        %
        % Functions (from Layer0):
        %   rfr/1 : Act -> Forbearance
        %   decl/1 : Act -> Act
        %
        % Appendix A.0 predicates (declared in problem files):
        %   norm_state_change/4, inst_event/1, triggers/5
        %   competent_for/2, about_event/2, does/3, duty_rem/0
        %
        % CHANGELOG v1.4:
        %   - version aligned with gen_foundation_problems.py v1.4
        %   - GRND-AX-1.smt2 now imported from gen_foundation_problems.SMT2_AXIOMS
        %     to guarantee reference copy is identical to embedded content
        %--------------------------------------------------------------------------
    """)


AXIOMS = """\
%--------------------------------------------------------------------------
% Ax5.1  Permission Relator — Basic
% A permission activation founds a relator with Liberty + NoRight.
%--------------------------------------------------------------------------
fof(ax_perm_relator_basic, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T) & activates(E,P) )
     => ? [Rho, L, N] :
          ( founds(E,Rho,P)
          & liberty(L)  & bearer(L,X) & cnt(L,A,T)  & part_of(L,Rho)
          & no_right(N) & bearer(N,Y) & cnt(N,A,T)  & part_of(N,Rho) ) )).
%--------------------------------------------------------------------------
% Ax5.2  Permission Relator — Strong
% Requires strong(P) asserted by profile extension (not ODRL 2.2).
% Adds Immunity + Disability to the permission relator.
%--------------------------------------------------------------------------
fof(ax_perm_relator_strong, axiom,
    ! [P, X, Y, A, T, E, Rho] :
      ( ( perm(P) & strong(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T)
        & activates(E,P) & founds(E,Rho,P) )
     => ? [Im, Db] :
          ( immunity(Im)   & bearer(Im,X) & cnt(Im,A,T)  & part_of(Im,Rho)
          & disability(Db) & bearer(Db,Y) & cnt(Db,A,T)  & part_of(Db,Rho) ) )).
%--------------------------------------------------------------------------
% Ax5.3  Prohibition Relator — Basic
% A prohibition activation founds a relator with Duty + Claim.
% Content is rfr(A) — the forbearance of performing A.
%--------------------------------------------------------------------------
fof(ax_proh_relator_basic, axiom,
    ! [F, X, Y, A, T, E] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) & activates(E,F) )
     => ? [Rho, D, C] :
          ( founds(E,Rho,F)
          & duty(D)  & bearer(D,X) & cnt(D,rfr(A),T) & part_of(D,Rho)
          & claim(C) & bearer(C,Y) & cnt(C,rfr(A),T) & part_of(C,Rho) ) )).
%--------------------------------------------------------------------------
% Ax5.4  Prohibition Relator — Remedy
% A prohibition with remedy adds Power + Subjection to the relator.
% Power is constituted at activation time, not at violation time.
%--------------------------------------------------------------------------
fof(ax_proh_relator_remedy, axiom,
    ! [F, X, Y, A, T, E, Rho] :
      ( ( proh(F) & has_rem(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T)
        & activates(E,F) & founds(E,Rho,F) )
     => ? [Pw, S] :
          ( power(Pw)     & bearer(Pw,Y) & cnt(Pw,decl(A),T) & part_of(Pw,Rho)
          & subjection(S) & bearer(S,X)  & cnt(S,decl(A),T)  & part_of(S,Rho) ) )).
%--------------------------------------------------------------------------
% Ax5.5a  Unique Founding: same event+rule founds at most one relator.
% UFO axiom a77 — particular individuation by rule-event pair.
%--------------------------------------------------------------------------
fof(ax_unique_founding, axiom,
    ! [R, E, Rho1, Rho2] :
      ( ( founds(E,Rho1,R) & founds(E,Rho2,R) ) => Rho1 = Rho2 )).
%--------------------------------------------------------------------------
% Ax5.5b  Unique Event: same relator+rule founded by at most one event.
%--------------------------------------------------------------------------
fof(ax_unique_relator_per_event, axiom,
    ! [R, E1, E2, Rho] :
      ( ( founds(E1,Rho,R) & founds(E2,Rho,R) ) => E1 = E2 )).
%--------------------------------------------------------------------------
% Ax5.6  Obligation Relator
% An obligation activation founds a relator with Duty + Claim.
%--------------------------------------------------------------------------
fof(ax_obl_relator, axiom,
    ! [D, X, Y, A, T, E] :
      ( ( obl(D) & aee(D,X) & aer(D,Y) & act(D,A) & tgt(D,T) & activates(E,D) )
     => ? [Rho, Du, C] :
          ( founds(E,Rho,D)
          & duty(Du) & bearer(Du,X) & cnt(Du,A,T) & part_of(Du,Rho)
          & claim(C) & bearer(C,Y)  & cnt(C,A,T)  & part_of(C,Rho) ) )).
%--------------------------------------------------------------------------
% Ax5.7  Hohfeldian Correlativity (4 biconditionals, content-binding)
% Each ODRL relator pairs each position with exactly one correlative
% over the same action-target content.
% odrl_rel(Rho) guards each biconditional.
%--------------------------------------------------------------------------
fof(ax_correlativity_liberty, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [L] : ( liberty(L)  & part_of(L,Rho) & cnt(L,A,T) ) )
        <=> ( ? [N] : ( no_right(N) & part_of(N,Rho) & cnt(N,A,T)
                      & ! [M] : ( ( no_right(M) & part_of(M,Rho) & cnt(M,A,T) )
                                 => M = N ) ) ) ) )).
fof(ax_correlativity_duty, axiom,
    ! [Rho, A, T] :
      ( odrl_rel(Rho)
     => ( ( ? [D] : ( duty(D)  & part_of(D,Rho) & cnt(D,A,T) ) )
        <=> ( ? [C] : ( claim(C) & part_of(C,Rho) & cnt(C,A,T)
                      & ! [K] : ( ( claim(K) & part_of(K,Rho) & cnt(K,A,T) )
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
% Ax5.8  Liberty-Duty Conflict Detection (single relator)
% No ODRL relator contains Liberty and Duty-to-refrain for same bearer.
% Corollary of Ax5.9 (within-relator instance).
%--------------------------------------------------------------------------
fof(ax_conflict_detection, axiom,
    ! [Rho, L, D, X, A, T] :
      ( ( part_of(L,Rho) & part_of(D,Rho)
        & liberty(L) & duty(D)
        & bearer(L,X) & bearer(D,X)
        & cnt(L,A,T)  & cnt(D,rfr(A),T) )
     => $false )).
%--------------------------------------------------------------------------
% Ax5.9  Cross-Relator Position Disjointness
% Liberty and Duty-to-refrain cannot be co-borne regardless of relator.
% Grounded in UFO disjointness of moment types.
%--------------------------------------------------------------------------
fof(ax_cross_relator_consistency, axiom,
    ! [L, D, X, A, T] :
      ( ( liberty(L) & bearer(L,X) & cnt(L,A,T)
        & duty(D)    & bearer(D,X) & cnt(D,rfr(A),T) )
     => $false )).
%--------------------------------------------------------------------------
% Ax5.10  Disability Precludes Prohibition Creation
% No prohibition by Y over (A,T) can exist while Y holds Disability
% over (A,T). Disability renders the institutional act void.
%--------------------------------------------------------------------------
fof(ax_disability_block, axiom,
    ! [F, X, Y, A, T] :
      ( ( proh(F) & aee(F,X) & aer(F,Y) & act(F,A) & tgt(F,T) )
     => ~ ? [Db] : ( disability(Db) & bearer(Db,Y) & cnt(Db,A,T) ) )).
%--------------------------------------------------------------------------
% A1  Normative State Changes Require an Institutional Event
% UFO-L regulative reading: no norm changes without triggering event.
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
          ( power(Pw) & bearer(Pw,Y) & about_event(Pw,E)
          & subjection(S) & bearer(S,X) & about_event(S,E) ) )).
%--------------------------------------------------------------------------
% B1  Performing a Prohibited Action Constitutes a NormStateChange
% Bridge axiom connecting does/3 to A1-A3 chain.
%--------------------------------------------------------------------------
fof(ax_B1, axiom,
    ! [F, X, A, T, B] :
      ( ( proh(F) & has_rem(F) & act(F,A) & tgt(F,T) & aee(F,X) & does(X,A,T) )
     => norm_state_change(X,B,T,duty_rem) )).
%--------------------------------------------------------------------------
% B2  Power Content Links to Founding Event
%--------------------------------------------------------------------------
fof(ax_B2, axiom,
    ! [Pw, A, T, Rho, E, R] :
      ( ( power(Pw) & cnt(Pw,decl(A),T) & part_of(Pw,Rho) & founds(E,Rho,R) )
     => about_event(Pw,E) )).
%--------------------------------------------------------------------------
% B3  Subjection Content Links to Founding Event
%--------------------------------------------------------------------------
fof(ax_B3, axiom,
    ! [S, A, T, Rho, E, R] :
      ( ( subjection(S) & cnt(S,decl(A),T) & part_of(S,Rho) & founds(E,Rho,R) )
     => about_event(S,E) )).
%--------------------------------------------------------------------------
% Summary:
%   Ax5.1-5.4  : 4 relator generation axioms
%   Ax5.5a-5.5b: 2 uniqueness axioms
%   Ax5.6      : 1 obligation relator axiom
%   Ax5.7      : 4 correlativity biconditionals
%   Ax5.8-5.10 : 3 constraint axioms
%   A1-A3      : 3 UFO-L regulative axioms
%   B1-B3      : 3 bridge axioms
%   Total      : 20 axioms
%--------------------------------------------------------------------------
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
    # SMT2_AXIOMS imported from gen_foundation_problems.py — guaranteed identical
    # to what is embedded in every .smt2 problem file.
    smt2_lines = [
        "; --------------------------------------------------------------------------",
        "; File     : GRND-AX-1.smt2",
        "; Domain   : Deontic Ontology / ODRL Grounding",
        f"; Version  : {META['version']}",
        "; Axioms   : Layer 1 deontic grounding axioms (Ax5.1-5.10, A1-A3, B1-B3)",
        f"; Refs     : {META['source']}",
        f"; Generated: {date.today().isoformat()} by gen_layer1_deontic.py",
        ";",
        "; NOTE: SMT-LIB 2 has no include directive.",
        "; These axioms are embedded directly in each .smt2 problem file.",
        "; This file is the authoritative source for the embedded content.",
        "; SMT2_AXIOMS is imported from gen_foundation_problems.py to guarantee",
        "; this reference copy is always identical to what is embedded.",
        "; --------------------------------------------------------------------------",
        "",
    ]
    for name, formula in SMT2_AXIOMS:
        smt2_lines.append(f"; {name}")
        smt2_lines.append(formula)
        smt2_lines.append("")

    smt2_path = out_dir / "GRND-AX-1.smt2"
    smt2_path.write_text("\n".join(smt2_lines), encoding="utf-8")
    print(f"Written: {smt2_path}")


if __name__ == "__main__":
    main()