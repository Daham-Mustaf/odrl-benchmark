"""
header.py
=========
TPTP / SMT-LIB header rendering for the ODRL benchmark.
Statistics (% Syntax block) are intentionally omitted from generated files.
tptp4X computes and inserts them automatically during TPTP library processing.
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
        "[Mus+26] Mustafa, D., Collarana, D., Haque, R., Peng, Y., "
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

# ---------------------------------------------------------------------------
# Formula counting (used by _ax_comment)
# ---------------------------------------------------------------------------
def _count_formulae(text):
    return len(re.findall(r"^fof\s*\(", text, re.MULTILINE))

# ---------------------------------------------------------------------------
# _ax_comment — builds comments= string with auto-computed formula count
# ---------------------------------------------------------------------------
def _ax_comment(body: str, breakdown: str, include_note: str) -> str:
    n = _count_formulae(body)
    return f"{include_note}\n{n} axioms: {breakdown}."

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------
def _wrap(label, text):
    lines = text.strip().split("\n")
    pad = " " * 11
    out = f"% {label:<9s}: {lines[0]}"
    for line in lines[1:]:
        out += f"\n%{pad}: {line.strip()}"
    return out

def _smt_wrap(label, text):
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

_SEP     = "%--------------------------------------------------------------------------\n"
_SMT_SEP = "; --------------------------------------------------------------------------\n"

# ---------------------------------------------------------------------------
# Header dataclasses
# ---------------------------------------------------------------------------
@dataclass
class Header:
    """TPTP header for .p problem files."""
    file:     str
    domain:   str
    title:    str
    version:  str
    english:  str
    status:   str
    refs:     list
    comments: str
    spc:      str = ""
    fof_text: str = ""   # retained for API compatibility, not used in render

    def _infer_spc(self):
        if self.spc: return self.spc
        s = self.status.lower()
        if "theorem"       in s: return SPC["theorem"]
        if "counter"       in s: return SPC["countersat"]
        if "unsatisfiable" in s or "unsat" in s: return SPC["unsat"]
        if "satisfiable"   in s or "sat"   in s: return SPC["sat"]
        return "FOF_UNK_RFN"

    def render(self):
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
            + f"% SPC      : {self._infer_spc()}\n"
            + "%\n"
            + _wrap("Comments", self.comments) + "\n"
            + _SEP
        )


@dataclass
class AXHeader:
    """TPTP header for .ax axiom files."""
    file:     str
    domain:   str
    title:    str
    version:  str
    english:  str
    refs:     list
    comments: str
    spc:      str = "FOF_SAT_RFN"
    fof_text: str = ""   # used only by _ax_comment, not in render

    def render(self):
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
            + f"% SPC      : {self.spc}\n"
            + "%\n"
            + _wrap("Comments", self.comments) + "\n"
            + _SEP
        )


@dataclass
class SMTHeader:
    """SMT-LIB 2 header for .smt2 files."""
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


# ---------------------------------------------------------------------------
# Convenience factory used by problem generators
# ---------------------------------------------------------------------------
def problem_header(p, domain, fof_body=""):
    ref_map = {
        "foundational": ["fois2026"],
        "axis":         ["axis2026"],
        "kb":           ["vldb2027"],
    }
    comment_map = {
        "foundational": (
            "Foundational ontology tier. FOIS 2026 benchmark.\n"
            f"Policy source: Policies/{p['id']}-policy.ttl"
        ),
        "axis": (
            "Axis decomposition tier. arXiv:2602.19878.\n"
            + ("Requires Axioms/ORD000-0.ax + Axioms/ORD001-0.ax + Axioms/AXIS000-0.ax.\n"
               if p.get("needs_density") else
               "Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.\n")
            + f"Policy source: Policies/{p['id']}-policy.ttl"
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


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    note = (
        "Depends on ORD000-0.ax (loaded by problem file).\n"
        "Include for open/half-open boundaries:\n"
        "  include('Axioms/ORD000-0.ax').\n"
        "  include('Axioms/PREC000-0.ax').\n"
        "  include('Axioms/AXIS000-0.ax')."
    )
    sample_fof = """\
fof(ax1, axiom, ![X]: (perm(X) => rule(X))).
fof(ax2, axiom, ![X,Y]: (aee(X,Y) => agent(Y))).
fof(conj, conjecture, ?[R,L,N]: (founds(e1,R,p1) & permission(L) & no_right(N))).
"""
    c = _ax_comment(sample_fof, "2 axm + 1 cnj", note)
    assert "3 axioms:" in c
    print("_ax_comment OK:", c.splitlines()[-1])

    print("\n=== Header (.p) ===")
    print(Header(
        file="ODRL300-1.p", domain="axis",
        title="SingleAxis conflict — eq vs eq same value", version="1.0",
        english="Two eq constraints on the same value conflict.",
        status="Theorem", refs=["axis2026"],
        comments="Axis decomposition tier. arXiv:2602.19878.\nRequires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.",
    ).render())

    print("=== AXHeader (.ax) ===")
    print(AXHeader(
        file="AXIS000-0.ax", domain="axis",
        title="Interval denotation and verdict algebra",
        version="1.1",
        english="Layer 1 axioms for the ODRL Axis Decomposition benchmark.",
        refs=["axis2026"],
        comments=_ax_comment(sample_fof, "2 axm + 1 cnj", note),
        fof_text=sample_fof,
    ).render())

    print("=== SMTHeader (.smt2) ===")
    smt = SMTHeader(
        file="ODRL300-1.smt2", domain="axis",
        title="SingleAxis conflict", version="1.0",
        refs=["axis2026"],
        comments="Verdict: Conflict. Category: SingleAxis.",
        status="unsat",
    ).render()
    print(smt)
    bad = [l for l in smt.splitlines() if l and not l.startswith(";")]
    assert not bad, f"BARE LINES: {bad}"
    print("All SMTHeader lines start with ';' ")