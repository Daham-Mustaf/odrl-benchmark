"""
header.py
=========
Shared TPTP header generator for all ODRL benchmark use cases.

Usage:
    from header import Header, AXHeader

    # For .p problem files
    h = Header(
        file     = "GRND002-1.p",
        domain   = "foundational",
        title    = "Permission creates Permission and NoRight",
        version  = "1.0",
        english  = "A permission activation founds a relator with\\n"
                   "Permission(assignee) and NoRight(assigner).",
        status   = "Theorem",
        refs     = ["fois2026"],
        comments = "Requires Axioms/GRND000-0.ax and Axioms/GRND-AX-1.ax.\\n"
                   "Policy source: Policies/GRND002-policy.ttl",
        fof_text = body,   # full FOF body — stats computed automatically
    ).render()

    # For .ax axiom files
    h = AXHeader(
        file     = "GRND000-0.ax",
        domain   = "foundational",
        title    = "Signature — sorts, predicates, rfr/decl functions",
        version  = "1.5",
        english  = "FOF signature for all DeonticOntology problems.\\n"
                   "Include via: include('Axioms/GRND000-0.ax').",
        refs     = ["fois2026"],
        comments = "Sorts encoded as unary guard predicates.\\n"
                   "UFO-L terms: permission/right replace liberty/claim.",
        fof_text = content,
    ).render()

Static fields (you define once):
    REFS    — citation keys → full citation strings
    DOMAINS — domain keys  → TPTP Domain strings

Dynamic fields (computed from fof_text automatically):
    formulae  — count of fof(...) declarations
    atoms     — count of predicate/function applications
    variables — count of unique uppercase variable names
    axioms    — count of fof(..., axiom, ...) declarations
    conjectures — count of fof(..., conjecture, ...) declarations
"""

import re
from dataclasses import dataclass, field

# =============================================================================
# STATIC REGISTRY — edit here when adding new papers or domains
# =============================================================================

REFS = {
    "fois2026": (
        "[MMC+26] Mohammed, D., Mustafa, D., Collarana, D., Lange, C., Guizzardi, G. "
        "What Does ODRL Mean? Grounding Permissions, Prohibitions, and Duties "
        "in Deontic Logic and Foundational Ontology. FOIS 2026."
    ),
    "axis2026": (
        "[Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., "
        "Quix, C., Decker, S. "
        "Axis Decomposition for ODRL: Resolving Dimensional Ambiguity "
        "in Policy Constraints through Interval Semantics. "
        "arXiv:2602.19878. https://arxiv.org/abs/2602.19878"
    ),
    "vldb2027": (
        "[Mus27]  Mustafa, D. et al. "
        "Conflict Detection via Denotational Semantics for ODRL Policies. "
        "VLDB 2027."
    ),
}

DOMAINS = {
    "foundational": "Deontic Ontology / ODRL Grounding",
    "axis":         "ODRL Policy / Axis Decomposition",
    "kb":           "ODRL Policy / KB Grounding",
}

# SPC codes — add more as needed
SPC = {
    "theorem":       "FOF_THM_RFN",
    "unsat":         "FOF_UNS_RFN",
    "sat":           "FOF_SAT_RFN",
    "epr_theorem":   "FOF_EPR_RFN_SEQ",
    "epr_unsat":     "FOF_EPR_UNS_SEQ",
}

# =============================================================================
# DYNAMIC STATISTICS — computed from actual FOF content
# =============================================================================

def _count_formulae(text: str) -> int:
    """Count all fof(...) declarations."""
    return len(re.findall(r"^fof\s*\(", text, re.MULTILINE))

def _count_by_role(text: str, role: str) -> int:
    """Count fof declarations with a specific role (axiom, conjecture, etc.)."""
    pattern = rf"^fof\s*\([^,]+,\s*{role}\s*,"
    return len(re.findall(pattern, text, re.MULTILINE))

def _count_atoms(text: str) -> int:
    """
    Count predicate/function applications.
    Approximation: count lowercase_word( patterns,
    excluding fof( and comment lines.
    """
    # Strip comment lines
    stripped = re.sub(r"%.*$", "", text, flags=re.MULTILINE)
    # Count lowercase identifier followed by (
    calls = re.findall(r"\b[a-z][a-z0-9_]*\s*\(", stripped)
    # Exclude structural keywords
    exclude = {"fof", "cnf", "tff", "thf", "include"}
    return sum(1 for c in calls if c.split("(")[0].strip() not in exclude)

def _count_variables(text: str) -> int:
    """Count unique uppercase variable names (TPTP convention)."""
    stripped = re.sub(r"%.*$", "", text, flags=re.MULTILINE)
    return len(set(re.findall(r"\b[A-Z][A-Za-z0-9_]*\b", stripped)))

def _max_formula_depth(text: str) -> int:
    """
    Estimate maximum nesting depth of a formula by counting
    max bracket depth across all fof bodies. Fast approximation.
    """
    stripped = re.sub(r"%.*$", "", text, flags=re.MULTILINE)
    max_depth = 0
    depth = 0
    for ch in stripped:
        if ch == "(":
            depth += 1
            max_depth = max(max_depth, depth)
        elif ch == ")":
            depth = max(0, depth - 1)
    return max_depth

def compute_stats(fof_text: str) -> dict:
    """
    Compute all dynamic statistics from raw FOF text.
    Returns a dict with keys:
        formulae, axioms, conjectures, corollaries,
        atoms, variables, max_depth
    """
    return {
        "formulae":    _count_formulae(fof_text),
        "axioms":      _count_by_role(fof_text, "axiom"),
        "conjectures": _count_by_role(fof_text, "conjecture"),
        "corollaries": _count_by_role(fof_text, "corollary"),
        "atoms":       _count_atoms(fof_text),
        "variables":   _count_variables(fof_text),
        "max_depth":   _max_formula_depth(fof_text),
    }

# =============================================================================
# HEADER RENDERING UTILITIES
# =============================================================================

def _wrap(label: str, text: str, width: int = 65) -> str:
    lines = text.strip().split("\n")
    pad   = " " * 11          # "% Comments : " minus "% " = 11 chars
    out   = f"% {label:<9s}: {lines[0]}"   # 9-char label field
    for line in lines[1:]:
        out += f"\n%{pad}: {line.strip()}"
    return out

def _refs_block(keys: list) -> str:
    lines = []
    for i, k in enumerate(keys):
        if k not in REFS:
            raise KeyError(f"Unknown ref key '{k}'. Add it to header.REFS.")
        label = "Refs" if i == 0 else "     "
        lines.append(f"% {label}     : {REFS[k]}")
    return "\n".join(lines)

def _stats_block(stats: dict) -> str:
    """Render the Syntax statistics block."""
    f  = stats["formulae"]
    ax = stats["axioms"]
    co = stats["conjectures"]
    cr = stats["corollaries"]
    at = stats["atoms"]
    va = stats["variables"]
    md = stats["max_depth"]

    role_str = f"{ax} axm"
    if co:
        role_str += f"; {co} cnj"
    if cr:
        role_str += f"; {cr} cor"

    return (
        f"% Syntax   : Number of formulae    : {f:4d}  ({role_str})\n"
        f"%            Number of atoms       : {at:4d}\n"
        f"%            Number of variables   : {va:4d}\n"
        f"%            Maximal formula depth : {md:4d}\n"
    )

# =============================================================================
# PROBLEM FILE HEADER  (.p files)
# =============================================================================

@dataclass
class Header:
    """
    TPTP header for .p problem files.

    Static fields (set by generator):
        file, domain, title, version, english,
        status, refs, comments, spc

    Dynamic field (pass full FOF body):
        fof_text — statistics computed automatically

    If fof_text is empty, the Syntax block is omitted.
    """
    file:     str
    domain:   str           # key from DOMAINS
    title:    str
    version:  str
    english:  str
    status:   str           # "Theorem" / "Unsatisfiable" / "Satisfiable"
    refs:     list          # list of keys from REFS
    comments: str
    spc:      str = ""      # if empty, inferred from status
    fof_text: str = ""      # full FOF body for dynamic stats

    def _infer_spc(self) -> str:
        if self.spc:
            return self.spc
        s = self.status.lower()
        if "theorem" in s:
            return SPC["theorem"]
        if "unsat" in s:
            return SPC["unsat"]
        if "sat" in s:
            return SPC["sat"]
        return "FOF_UNK_RFN"

    def render(self) -> str:
        stats = _stats_block(compute_stats(self.fof_text)) if self.fof_text else ""
        return (
            f"%--------------------------------------------------------------------------\n"
            f"% File     : {self.file}\n"
            f"% Domain   : {DOMAINS[self.domain]}\n"
            f"% Problem  : {self.title}\n"
            f"% Version  : {self.version}\n"
            f"{_wrap('English', self.english)}\n"
            f"%\n"
            f"{_refs_block(self.refs)}\n"
            f"% Source   : Mohammed, D. (2026)\n"
            f"% Names    : {self.file}\n"
            f"%\n"
            f"% Status   : {self.status}\n"
            f"{stats}"
            f"% SPC      : {self._infer_spc()}\n"
            f"%\n"
            f"{_wrap('Comments', self.comments)}\n"
            f"%--------------------------------------------------------------------------\n"
        )

# =============================================================================
# AXIOM FILE HEADER  (.ax files)
# =============================================================================

@dataclass
class AXHeader:
    """
    TPTP header for .ax axiom files.
    Same structure as Header but uses 'Axioms' instead of 'Problem'.
    """
    file:     str
    domain:   str
    title:    str
    version:  str
    english:  str
    refs:     list
    comments: str
    spc:      str = "FOF_SAT_RFN"
    fof_text: str = ""

    def render(self) -> str:
        stats = _stats_block(compute_stats(self.fof_text)) if self.fof_text else ""
        return (
            f"%--------------------------------------------------------------------------\n"
            f"% File     : {self.file}\n"
            f"% Domain   : {DOMAINS[self.domain]}\n"
            f"% Axioms   : {self.title}\n"
            f"% Version  : {self.version}\n"
            f"{_wrap('English', self.english)}\n"
            f"%\n"
            f"{_refs_block(self.refs)}\n"
            f"% Source   : Mohammed, D. (2026)\n"
            f"% Names    : {self.file}\n"
            f"%\n"
            f"% Status   : Satisfiable\n"
            f"{stats}"
            f"% SPC      : {self.spc}\n"
            f"%\n"
            f"{_wrap('Comments', self.comments)}\n"
            f"%--------------------------------------------------------------------------\n"
        )

# =============================================================================
# CONVENIENCE FUNCTION — domain-specific defaults
# =============================================================================

def problem_header(p: dict, domain: str, fof_body: str = "") -> str:
    """
    Build a Header from a problem dict and render it.
    p must have: id, name, status_fof, description
    """
    ref_map = {
        "foundational": ["fois2026"],
        "axis":         ["vldb2027"],
        "kb":           ["vldb2027"],
    }
    comment_map = {
        "foundational": (
            "Foundational ontology tier. FOIS 2026 benchmark.\n"
            "Requires Axioms/GRND000-0.ax and Axioms/GRND-AX-1.ax.\n"
            f"Policy source: Policies/{p['id']}-policy.ttl"
        ),
        "axis": (
            "Axis decomposition tier. VLDB 2027 benchmark.\n"
            "Requires Axioms/ODRL000-0.ax and domain KB axioms."
        ),
        "kb": (
            "KB-grounding tier. VLDB 2027 benchmark.\n"
            "Requires Axioms/ODRL000-0.ax and domain KB axioms."
        ),
    }
    return Header(
        file     = f"{p['id']}-1.p",
        domain   = domain,
        title    = p["name"],
        version  = "1.0",
        english  = p.get("description", p["name"]),
        status   = p["status_fof"],
        refs     = ref_map[domain],
        comments = comment_map[domain],
        fof_text = fof_body,
    ).render()


if __name__ == "__main__":
    # Quick self-test
    sample_fof = """
fof(ax1, axiom, ![X]: (perm(X) => rule(X))).
fof(ax2, axiom, ![X,Y]: (aee(X,Y) => agent(Y))).
fof(conj, conjecture, ?[R,L,N]: (founds(e1,R,p1) & permission(L) & no_right(N))).
"""
    h = Header(
        file     = "GRND002-1.p",
        domain   = "foundational",
        title    = "Permission creates Permission and NoRight",
        version  = "1.0",
        english  = "A permission activation founds a relator containing\n"
                   "Permission(assignee) and NoRight(assigner).",
        status   = "Theorem",
        refs     = ["fois2026"],
        comments = "Requires Axioms/GRND000-0.ax and Axioms/GRND-AX-1.ax.\n"
                   "Policy source: Policies/GRND002-policy.ttl",
        fof_text = sample_fof,
    ).render()
    print(h)

    ax = AXHeader(
        file     = "GRND000-0.ax",
        domain   = "foundational",
        title    = "Signature — sorts, predicates, rfr/decl functions",
        version  = "1.5",
        english  = "FOF signature for all DeonticOntology problems.\n"
                   "Include via: include('Axioms/GRND000-0.ax').",
        refs     = ["fois2026"],
        comments = "Sorts encoded as unary guard predicates (FOF has no\n"
                   "native sorts). Guards asserted per problem, not here.\n"
                   "UFO-L terms: permission/right replace liberty/claim.\n"
                   "Three founding predicates: founds, founds_rem, founds_imm.",
        fof_text = sample_fof,
    ).render()
    print(ax)
