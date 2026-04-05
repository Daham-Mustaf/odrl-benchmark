"""
header.py
=========
Shared TPTP header generator for all ODRL benchmark domains.

Paper -> ref key mapping:
    fois2026   — Mohammed et al. What Does ODRL Mean? FOIS 2026.
    axis2026   — Mustafa et al. Axis Decomposition for ODRL. arXiv:2602.19878.
    vldb2027   — Mustafa et al. Conflict Detection. VLDB 2027.
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
    lines = text.strip().split("\n")
    pad = " " * 11
    out = f"% {label:<9s}: {lines[0]}"
    for line in lines[1:]:
        out += f"\n%{pad}: {line.strip()}"
    return out

def _refs_block(keys):
    lines = []
    for i, k in enumerate(keys):
        if k not in REFS:
            raise KeyError(f"Unknown ref key '{k}'. Add it to header.REFS.")
        label = "Refs" if i == 0 else "     "
        lines.append(f"% {label}     : {REFS[k]}")
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

@dataclass
class Header:
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
        if "theorem" in s:    return SPC["theorem"]
        if "counter" in s:    return SPC["countersat"]
        if "unsat" in s:      return SPC["unsat"]
        if "sat" in s:        return SPC["sat"]
        return "FOF_UNK_RFN"

    def render(self):
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
            f"% Source   : Mustafa, D. (2026)\n"
            f"% Names    : {self.file}\n"
            f"%\n"
            f"% Status   : {self.status}\n"
            f"{stats}"
            f"% SPC      : {self._infer_spc()}\n"
            f"%\n"
            f"{_wrap('Comments', self.comments)}\n"
            f"%--------------------------------------------------------------------------\n"
        )

@dataclass
class AXHeader:
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
            f"%--------------------------------------------------------------------------\n"
            f"% File     : {self.file}\n"
            f"% Domain   : {DOMAINS[self.domain]}\n"
            f"% Axioms   : {self.title}\n"
            f"% Version  : {self.version}\n"
            f"{_wrap('English', self.english)}\n"
            f"%\n"
            f"{_refs_block(self.refs)}\n"
            f"% Source   : Mustafa, D. (2026)\n"
            f"% Names    : {self.file}\n"
            f"%\n"
            f"% Status   : Satisfiable\n"
            f"% SPC      : {self.spc}\n"
            f"%\n"
            f"{_wrap('Comments', self.comments)}\n"
            f"%--------------------------------------------------------------------------\n"
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
            "Axis decomposition tier. PAAR 2026 benchmark.\n"
            "Requires Axioms/AXIS000-0.ax (+ ORD001-0.ax if dense).\n"
            f"Policy source: Policies/{p['id']}-policy.ttl"
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