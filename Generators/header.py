"""
header.py
=========
TPTP / SMT-LIB header rendering for the ODRL benchmark.
"""
import re
from dataclasses import dataclass

REFS = {
    "fois2026": (
        "[Mus+26a] Mustafa, D., et al. "
        "What Does ODRL Mean? Grounding Permissions, Prohibitions, and Duties "
        "in Deontic Logic and Foundational Ontology. FOIS 2026."
    ),
    "axis2026": (
        "[Mus+26b] Mustafa, D., et al. "
        "Axis Decomposition for ODRL: Resolving Dimensional Ambiguity "
        "in Policy Constraints through Interval Semantics. ISWC 2026 (submitted)."
    ),
    "kgc2026": (
        "[Mus+26c] Mustafa, D., et al. "
        "Conflict Detection via Denotational Semantics: "
        "Policy Reasoning over Incomplete Hierarchies. (under submission)."
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


def _ax_comment(body, breakdown, include_note):
    n = _count_formulae(body)
    return f"{include_note}\n{n} axioms: {breakdown}."


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
    verdict:  str = ""    # Conflict | Compatible | Unknown | CounterSatisfiable
    relation: str = ""    # conflict | subsumption | verdict_algebra
    fof_text: str = ""

    def _infer_spc(self):
        if self.spc:
            return self.spc
        s = self.status.lower()
        if "theorem"       in s: return SPC["theorem"]
        if "counter"       in s: return SPC["countersat"]
        if "unsatisfiable" in s or "unsat" in s: return SPC["unsat"]
        if "satisfiable"   in s or "sat"   in s: return SPC["sat"]
        return "FOF_UNK_RFN"

    def render(self):
        verdict_line  = f"% Verdict  : {self.verdict}\n"  if self.verdict  else ""
        relation_line = f"% Relation : {self.relation}\n" if self.relation else ""
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
            + verdict_line
            + relation_line
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
    fof_text: str = ""

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


def problem_header(p, domain, fof_body=""):
    ref_map = {
        "foundational": ["fois2026"],
        "axis":         ["axis2026"],
        "kb":           ["kgc2026"],
    }
    comment_map = {
        "foundational": (
            "Foundational ontology tier. FOIS 2026 benchmark.\n"
            f"Policy source: Policies/{p['id']}-policy.ttl"
        ),
        "axis": (
            "Axis decomposition tier. ISWC 2026.\n"
            "Requires Axioms/ORD000-0.ax + Axioms/AXIS000-0.ax.\n"
            f"Policy source: Policies/{p['id']}-policy.ttl"
        ),
        "kb": (
            "KB-grounding tier.\n"
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
        verdict  = p.get("verdict", ""),
        relation = p.get("relation", ""),
        fof_text = fof_body,
    ).render()


if __name__ == "__main__":
    test_p = {
        "id": "ODRLTEST",
        "name": "smoke test",
        "description": "smoke test",
        "status_fof": "Theorem",
        "verdict": "Compatible",
        "relation": "verdict_algebra",
    }
    print(problem_header(test_p, "axis", ""))
