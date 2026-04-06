"""
header.py — see file for full docstring
"""
import re
from dataclasses import dataclass

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
        "[Mus+27] Mustafa, D., Collarana, D., Haque, R., Peng, Y., "
        "Quix, C., Lange, C., Geisler, S., Decker, S. "
        "Conflict Detection via Denotational Semantics: "
        "Policy Reasoning over Incomplete Hierarchies. "
        "arXiv:2602.19883. https://arxiv.org/abs/2602.19883"
    ),
}

DOMAINS = {
    "foundational": "Deontic Ontology / ODRL Grounding",
    "axis":         "ODRL Policy / Axis Decomposition",
    "kb":           "ODRL Policy / KB Grounding Concept-valued",
}

SPC = {
    "theorem":    "FOF_THM_RFN",
    "unsat":      "FOF_UNS_RFN",
    "sat":        "FOF_SAT_RFN",
    "countersat": "FOF_CSA_RFN",
}

def _count_formulae(text):
    return len(re.findall(r"^fof\s*\(", text, re.MULTILINE))

def _count_by_role(text, role):
    return len(re.findall(rf"^fof\s*\([^,]+,\s*{role}\s*,", text, re.MULTILINE))

def _count_atoms(text):
    stripped = re.sub(r"%.*$", "", text, flags=re.MULTILINE)
    calls = re.findall(r"\b[a-z][a-z0-9_]*\s*\(", stripped)
    exclude = {"fof", "cnf", "tff", "thf", "include"}
    return sum(1 for c in calls if c.split("(")[0].strip() not in exclude)

def _count_variables(text):
    stripped = re.sub(r"%.*$", "", text, flags=re.MULTILINE)
    return len(set(re.findall(r"\b[A-Z][A-Za-z0-9_]*\b", stripped)))

def _max_formula_depth(text):
    stripped = re.sub(r"%.*$", "", text, flags=re.MULTILINE)
    max_depth = depth = 0
    for ch in stripped:
        if ch == "(":
            depth += 1
            max_depth = max(max_depth, depth)
        elif ch == ")":
            depth = max(0, depth - 1)
    return max_depth

def compute_stats(fof_text):
    return {
        "formulae":    _count_formulae(fof_text),
        "axioms":      _count_by_role(fof_text, "axiom"),
        "conjectures": _count_by_role(fof_text, "conjecture"),
        "corollaries": _count_by_role(fof_text, "corollary"),
        "atoms":       _count_atoms(fof_text),
        "variables":   _count_variables(fof_text),
        "max_depth":   _max_formula_depth(fof_text),
    }

def _wrap(label, text):
    """Wrap multi-line text under a TPTP field label (% prefix)."""
    lines = text.strip().split("\n")
    pad = " " * 11
    out = f"% {label:<9s}: {lines[0]}"
    for line in lines[1:]:
        out += f"\n%{pad}: {line.strip()}"
    return out

def _smt_wrap(label, text):
    """Wrap multi-line text under a SMT-LIB field label (; prefix).
    Every continuation line gets a ; prefix so Z3 never sees bare text."""
    lines = text.strip().split("\n")
    out = f"; {label:<9s}: {lines[0]}"
    for line in lines[1:]:
        out += f"\n;            {line.strip()}"
    return out

def _refs_block(keys):
    lines = []
    for i, k in enumerate(keys):
        if k not in REFS:
            raise KeyError(f"Unknown ref key '{k}'. Add it to header.REFS.")
        label = "Refs" if i == 0 else "     "
        lines.append(f"% {label}     : {REFS[k]}")
    return "\n".join(lines)

def _smt_refs_block(keys):
    lines = []
    for i, k in enumerate(keys):
        if k not in REFS:
            raise KeyError(f"Unknown ref key '{k}'. Add it to header.REFS.")
        label = "Refs" if i == 0 else "     "
        lines.append(f"; {label}     : {REFS[k]}")
    return "\n".join(lines)

def _stats_block(stats):
    f  = stats["formulae"]
    ax = stats["axioms"]
    co = stats["conjectures"]
    cr = stats["corollaries"]
    at = stats["atoms"]
    va = stats["variables"]
    md = stats["max_depth"]
    role_str = f"{ax} axm"
    if co: role_str += f"; {co} cnj"
    if cr: role_str += f"; {cr} cor"
    return (
        f"% Syntax   : Number of formulae    : {f:4d}  ({role_str})\n"
        f"%            Number of atoms       : {at:4d}\n"
        f"%            Number of variables   : {va:4d}\n"
        f"%            Maximal formula depth : {md:4d}\n"
    )

_SEP     = "%--------------------------------------------------------------------------\n"
_SMT_SEP = "; --------------------------------------------------------------------------\n"


@dataclass
class Header:
    """TPTP header for .p problem files. Stats computed from fof_text."""
    file:     str
    domain:   str
    title:    str
    version:  str
    english:  str
    status:   str
    refs:     list
    comments: str
    spc:      str = ""
    fof_text: str = ""

    def _infer_spc(self):
        if self.spc: return self.spc
        s = self.status.lower()
        if "theorem"       in s: return SPC["theorem"]
        if "counter"       in s: return SPC["countersat"]
        if "unsatisfiable" in s or "unsat" in s: return SPC["unsat"]
        if "satisfiable"   in s or "sat"   in s: return SPC["sat"]
        return "FOF_UNK_RFN"

    def render(self):
        stats = _stats_block(compute_stats(self.fof_text)) if self.fof_text else ""
        return (
            _SEP
            + f"% File     : {self.file}\n"
            + f"% Domain   : {DOMAINS[self.domain]}\n"
            + f"% Problem  : {self.title}\n"
            + f"% Version  : {self.version}\n"
            + _wrap("English", self.english) + "\n"
            + "%\n"
            + _refs_block(self.refs) + "\n"
            + "% Source   : Mustafa, D. (2026)\n"
            + "% Authors  : Mustafa, D. & Sutcliffe, G.\n"
            + f"% Names    : {self.file}\n"
            + "%\n"
            + f"% Status   : {self.status}\n"
            + stats
            + f"% SPC      : {self._infer_spc()}\n"
            + "%\n"
            + _wrap("Comments", self.comments) + "\n"
            + _SEP
        )


@dataclass
class AXHeader:
    """TPTP header for .ax axiom files. Stats computed from fof_text."""
    file:     str
    domain:   str
    title:    str
    version:  str
    english:  str
    refs:     list
    comments: str
    spc:      str = "FOF_SAT_RFN"
    fof_text: str = ""

    def render(self):
        stats = _stats_block(compute_stats(self.fof_text)) if self.fof_text else ""
        return (
            _SEP
            + f"% File     : {self.file}\n"
            + f"% Domain   : {DOMAINS[self.domain]}\n"
            + f"% Axioms   : {self.title}\n"
            + f"% Version  : {self.version}\n"
            + _wrap("English", self.english) + "\n"
            + "%\n"
            + _refs_block(self.refs) + "\n"
            + "% Source   : Mustafa, D. (2026)\n"
            + "% Authors  : Mustafa, D. & Sutcliffe, G.\n"
            + f"% Names    : {self.file}\n"
            + "%\n"
            + "% Status   : Satisfiable\n"
            + stats
            + f"% SPC      : {self.spc}\n"
            + "%\n"
            + _wrap("Comments", self.comments) + "\n"
            + _SEP
        )


@dataclass
class SMTHeader:
    """SMT-LIB 2 header for .smt2 files.
    All lines use ; comment prefix.
    Multi-line comments wrapped with _smt_wrap — Z3 never sees bare text.
    """
    file:     str
    domain:   str
    title:    str
    version:  str
    refs:     list
    comments: str
    status:   str = "unknown"

    def render(self):
        return (
            _SMT_SEP
            + f"; File     : {self.file}\n"
            + f"; Domain   : {DOMAINS[self.domain]}\n"
            + f"; Axioms   : {self.title}\n"
            + f"; Version  : {self.version}\n"
            + f"; Authors  : Mustafa, D. & Sutcliffe, G.\n"
            + _smt_refs_block(self.refs) + "\n"
            + "; Source   : Mustafa, D. (2026)\n"
            + f"; Names    : {self.file}\n"
            + f"; Status   : {self.status}\n"
            + _smt_wrap("Comments", self.comments) + "\n"
            + _SMT_SEP
        )


def problem_header(p, domain, fof_body=""):
    ref_map = {
        "foundational": ["fois2026"],
        "axis":         ["axis2026"],
        "kb":           ["vldb2027"],
    }
    comment_map = {
        "foundational": (
            "Foundational ontology tier. FOIS 2026 benchmark.\n"
            "Requires Axioms/GRND000-0.ax and Axioms/GRND-AX-1.ax.\n"
            f"Policy source: Policies/{p['id']}-policy.ttl"
        ),
        "axis": (
            "Axis decomposition tier. arXiv:2602.19878.\n"
            "Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).\n"
            f"Policy source: Policies/{p['id']}-policy.ttl"
        ),
        "kb": (
            "KB-grounding tier. VLDB 2027. arXiv:2602.19883.\n"
            "Requires Axioms/ODRL000-0.ax and domain KB axioms.\n"
            f"Policy source: Policies/{p['id']}-policy.ttl"
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
    sample_fof = """\
fof(ax1, axiom, ![X]: (perm(X) => rule(X))).
fof(ax2, axiom, ![X,Y]: (aee(X,Y) => agent(Y))).
fof(conj, conjecture, ?[R,L,N]: (founds(e1,R,p1) & permission(L) & no_right(N))).
"""
    print("=== Header (.p) ===")
    print(Header(
        file="GRND002-1.p", domain="foundational",
        title="Permission creates Permission and NoRight", version="1.0",
        english="A permission activation founds a relator containing\nPermission(assignee) and NoRight(assigner).",
        status="Theorem", refs=["fois2026"],
        comments="Requires Axioms/GRND000-0.ax and Axioms/GRND-AX-1.ax.\nPolicy source: Policies/GRND002-policy.ttl",
        fof_text=sample_fof,
    ).render())

    print("=== AXHeader (.ax) ===")
    print(AXHeader(
        file="GRND000-0.ax", domain="foundational",
        title="Signature — sorts, predicates, rfr/decl functions", version="1.5",
        english="FOF signature for all DeonticOntology problems.\nInclude via: include('Axioms/GRND000-0.ax').",
        refs=["fois2026"],
        comments="Sorts encoded as unary guard predicates.\nrfr/1: Act -> Forbearance. decl/1: violation declaration.",
        fof_text=sample_fof,
    ).render())

    print("=== SMTHeader (.smt2) — multi-line comments test ===")
    smt_out = SMTHeader(
        file="GRND000-0.smt2", domain="foundational",
        title="Signature — sorts, predicates, rfr/decl functions", version="1.5",
        refs=["fois2026"],
        comments="SMT-LIB preamble embedded verbatim in every .smt2 problem file.\nLine two — must start with semicolon.\nLine three — Z3 must never see bare text.",
        status="unknown",
    ).render()
    print(smt_out)

    # Safety check: no bare lines
    bad = [l for l in smt_out.splitlines() if l and not l.startswith(";")]
    assert not bad, f"BARE LINES: {bad}"
    print("All SMTHeader lines start with ';'")