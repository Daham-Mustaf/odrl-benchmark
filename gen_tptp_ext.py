#!/usr/bin/env python3
"""
Generate TPTP (.p) files for extension benchmarks (090–207).
92 problems across 10 categories.

Usage:
    python3 gen_tptp_ext.py                    # generate all .p files
    python3 gen_tptp_ext.py --run              # generate + run vampire
    python3 gen_tptp_ext.py --run --timeout 60 # custom timeout
"""
import os, subprocess, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
TPTP_DIR = os.path.join(BASE, "Problems/ODRL/KBGrounding")

# ============================================================
# Axiom file references (Layer 0)
# ============================================================
GEO   = "Layer0-DomainKB/GEO000-0.ax"
GEO1  = "Layer0-DomainKB/GEO001-0.ax"
GEO_D = "Layer0-DomainKB/GEO002-0.ax"
DPV   = "Layer0-DomainKB/DPV000-0.ax"
DPV_E = "Layer0-DomainKB/DPV001-0.ax"  # enriched (sciRes not comm)
DPV_D = "Layer0-DomainKB/DPV002-0.ax"  # same-level UNA
DPV_X = "Layer0-DomainKB/DPV003-0.ax"  # cross-level UNA
LNG   = "Layer0-DomainKB/LNG000-0.ax"
LNG1  = "Layer0-DomainKB/LNG001-0.ax"
LNG_D = "Layer0-DomainKB/LNG002-0.ax"
NOM   = "Layer0-DomainKB/NOM000-0.ax"
CHN   = "Layer0-DomainKB/CHN000-0.ax"
CHN_D = "Layer0-DomainKB/CHN001-0.ax"
DIA   = "Layer0-DomainKB/DIA000-0.ax"
SNG   = "Layer0-DomainKB/SNG000-0.ax"
NMS   = "Layer0-DomainKB/NMS000-0.ax"
CORE  = "Layer1-ODRLCore/ODRL000-0.ax"
GRND  = "Layer2-Grounding/GROUND000-1.ax"

# ============================================================
# Helpers
# ============================================================
def header(pid, desc, status, notes=""):
    n = "\n".join(f"% {line}" for line in notes.strip().split("\n")) if notes else ""
    return f"""%--------------------------------------------------------------------------
% File     : {pid}.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : {desc}
% Status   : {status}
% Authors  : Mustafa, D. & Sutcliffe, G.
{n}
%--------------------------------------------------------------------------"""

def includes(*axioms):
    lines = [f"include('Axioms/{ax}')." for ax in axioms]
    return "\n".join(lines)

def con(name, operand, operator, value):
    return f"fof({name}_def, axiom,\n    has_operand({name},{operand}) & has_operator({name},{operator}) & has_value({name},{value}))."

def con_multi(name, operand, operator, values):
    parts = [f"has_operand({name},{operand})", f"has_operator({name},{operator})"]
    parts += [f"has_value({name},{v})" for v in values]
    return f"fof({name}_def, axiom,\n    {' & '.join(parts)})."

def compat_conj(c1, c2, label="compatible"):
    return f"fof({label}, conjecture,\n    ?[X]: (in_denotation(X,{c1}) & in_denotation(X,{c2})))."

def conflict_conj(c1, c2, label="conflict"):
    return f"fof({label}, conjecture,\n    ~(?[X]: (in_denotation(X,{c1}) & in_denotation(X,{c2}))))."

def cross2_conj(c1, c2, c3, c4, label="cross_compatible"):
    return f"""fof({label}, conjecture,
    (?[X]: (in_denotation(X,{c1}) & in_denotation(X,{c2})))
  & (?[Y]: (in_denotation(Y,{c3}) & in_denotation(Y,{c4}))))."""

def cross3_conj(c1, c2, c3, c4, c5, c6, label="cross_compatible"):
    return f"""fof({label}, conjecture,
    (?[X]: (in_denotation(X,{c1}) & in_denotation(X,{c2})))
  & (?[Y]: (in_denotation(Y,{c3}) & in_denotation(Y,{c4})))
  & (?[Z]: (in_denotation(Z,{c5}) & in_denotation(Z,{c6}))))."""

def or_compat_conj(c1, c2, c3):
    return f"""fof(or_compatible, conjecture,
    (?[X]: (in_denotation(X,{c1}) & in_denotation(X,{c3})))
  | (?[Y]: (in_denotation(Y,{c2}) & in_denotation(Y,{c3}))))."""

def or_conflict_conj(c1, c2, c3):
    return f"""fof(or_conflict, conjecture,
    ~((?[X]: (in_denotation(X,{c1}) & in_denotation(X,{c3})))
    | (?[Y]: (in_denotation(Y,{c2}) & in_denotation(Y,{c3})))))."""

def xone_compat_conj(c1, c2, c3):
    return f"""fof(xone_compatible, conjecture,
    (?[X]: (in_denotation(X,{c1}) & ~in_denotation(X,{c2}) & in_denotation(X,{c3})))
  | (?[Y]: (in_denotation(Y,{c2}) & ~in_denotation(Y,{c1}) & in_denotation(Y,{c3}))))."""

def xone_conflict_conj(c1, c2, c3):
    return f"""fof(xone_conflict, conjecture,
    ~((?[X]: (in_denotation(X,{c1}) & ~in_denotation(X,{c2}) & in_denotation(X,{c3})))
    | (?[Y]: (in_denotation(Y,{c2}) & ~in_denotation(Y,{c1}) & in_denotation(Y,{c3})))))."""

def witness_conj(e, c1, c2):
    return f"fof(witness, conjecture,\n    in_denotation({e},{c1}) & in_denotation({e},{c2}))."

# Per-problem grounding helpers
def isNoneOf_if_tax(cname, values, operand="purpose"):
    """If-direction for isNoneOf: ¬subClassOf to all values → in denotation"""
    neg = " & ".join(f"~subClassOf(X,{v})" for v in values)
    return f"fof({cname}_isNoneOf_if, axiom,\n    ![X]: (({neg} & taxonomic({operand})) => in_denotation(X,{cname})))."

def isNoneOf_if_mereo(cname, values):
    """If-direction for isNoneOf mereological"""
    neg = " & ".join(f"~partOf(X,{v})" for v in values)
    return f"fof({cname}_isNoneOf_if, axiom,\n    ![X]: (({neg} & mereological(spatial)) => in_denotation(X,{cname})))."

def isAllOf_if_tax(cname, values, operand="purpose"):
    """If-direction for isAllOf: subClassOf to all values → in denotation"""
    pos = " & ".join(f"subClassOf(X,{v})" for v in values)
    return f"fof({cname}_isAllOf_if, axiom,\n    ![X]: (({pos} & taxonomic({operand})) => in_denotation(X,{cname})))."

def isAnyOf_onlyif_tax(cname, values):
    """Only-if for isAnyOf: in denotation → subClassOf to some value"""
    dj = " | ".join(f"subClassOf(X,{v})" for v in values)
    return f"fof({cname}_isAnyOf_onlyif, axiom,\n    ![X]: (in_denotation(X,{cname}) => ({dj})))."

def isAnyOf_onlyif_mereo(cname, values):
    dj = " | ".join(f"partOf(X,{v})" for v in values)
    return f"fof({cname}_isAnyOf_onlyif, axiom,\n    ![X]: (in_denotation(X,{cname}) => ({dj})))."

def isNoneOf_bidir_nom(cname, values):
    """Bidirectional isNoneOf for nominal: x ≠ all values ↔ in denotation"""
    neg = " & ".join(f"X != {v}" for v in values)
    lines = f"fof({cname}_isNoneOf_if, axiom,\n    ![X]: (({neg}) => in_denotation(X,{cname}))).\n"
    lines += f"fof({cname}_isNoneOf_onlyif, axiom,\n    ![X]: (in_denotation(X,{cname}) => ({neg})))."
    return lines

def isAnyOf_onlyif_nom(cname, values):
    dj = " | ".join(f"X = {v}" for v in values)
    return f"fof({cname}_isAnyOf_onlyif, axiom,\n    ![X]: (in_denotation(X,{cname}) => ({dj})))."

# ============================================================
# Problem catalog
# ============================================================
P = []
def add(pid, sub, desc, status, axfiles, constraints, extra_axioms, conjecture, notes=""):
    P.append(dict(id=pid, sub=sub, desc=desc, status=status,
                  axfiles=axfiles, constraints=constraints,
                  extra=extra_axioms, conjecture=conjecture, notes=notes))

# ============================================================
# NEQ (090–096)
# ============================================================
add("ODRL090-1","Neq","neq acadRes vs eq sciRes: Compatible","Theorem",
    [DPV, DPV_D, CORE, GRND],
    [con("c1","purpose","neq","academicResearch"), con("c2","purpose","eq","scientificResearch")],
    [], compat_conj("c1","c2"))

add("ODRL091-1","Neq","neq acadRes vs eq acadRes: Conflict","Theorem",
    [DPV, CORE, GRND],
    [con("c1","purpose","neq","academicResearch"), con("c2","purpose","eq","academicResearch")],
    [], conflict_conj("c1","c2"))

add("ODRL092-1","Neq","neq france vs eq germany: Compatible","Theorem",
    [GEO, CORE, GRND],
    [con("c1","spatial","neq","france"), con("c2","spatial","eq","germany")],
    [], compat_conj("c1","c2"))

add("ODRL093-1","Neq","neq fr vs isA de: Compatible","Theorem",
    [LNG, CORE, GRND],
    [con("c1","language","neq","fr"), con("c2","language","isA","de")],
    [], compat_conj("c1","c2"))

add("ODRL094-1","Neq","neq de vs isA de: overlap on de_AT, de_CH","Theorem",
    [LNG, LNG_D, CORE, GRND],
    [con("c1","language","neq","de"), con("c2","language","isA","de")],
    [], compat_conj("c1","c2"))

add("ODRL095-1","Neq","neq singleton: C\\{g}=empty on |C|=1","Theorem",
    [SNG, CORE, GRND],
    [con("c1","purpose","neq","singleton"), con("c2","purpose","eq","singleton")],
    [], conflict_conj("c1","c2"))

add("ODRL096-1","Neq","neq de vs neq fr: double complement, Compatible","Theorem",
    [LNG, CORE, GRND],
    [con("c1","language","neq","de"), con("c2","language","neq","fr")],
    [], compat_conj("c1","c2"))

# ============================================================
# HASPART (100–106)
# ============================================================
add("ODRL100-1","HasPart","hasPart bavaria vs eq europe: Compatible","Theorem",
    [GEO, CORE, GRND],
    [con("c1","spatial","hasPart","bavaria"), con("c2","spatial","eq","europe")],
    [], compat_conj("c1","c2"))

add("ODRL101-1","HasPart","hasPart europe vs eq france: Conflict","Theorem",
    [GEO, CORE, GRND],
    [con("c1","spatial","hasPart","europe"), con("c2","spatial","eq","france")],
    [], conflict_conj("c1","c2"))

add("ODRL102-1","HasPart","hasPart france vs isPartOf europe: overlap","Theorem",
    [GEO, CORE, GRND],
    [con("c1","spatial","hasPart","france"), con("c2","spatial","isPartOf","europe")],
    [], compat_conj("c1","c2"))

add("ODRL103-1","HasPart","hasPart bavaria vs hasPart france: meet at europe","Theorem",
    [GEO, CORE, GRND],
    [con("c1","spatial","hasPart","bavaria"), con("c2","spatial","hasPart","france")],
    [], compat_conj("c1","c2"))

add("ODRL104-1","HasPart","hasPart germany vs eq bavaria: upward excludes downward","Theorem",
    [GEO, GEO_D, CORE, GRND],
    [con("c1","spatial","hasPart","germany"), con("c2","spatial","eq","bavaria")],
    [], conflict_conj("c1","c2"))

add("ODRL105-1","HasPart","hasPart bavaria vs isPartOf germany: Compatible","Theorem",
    [GEO, CORE, GRND],
    [con("c1","spatial","hasPart","bavaria"), con("c2","spatial","isPartOf","germany")],
    [], compat_conj("c1","c2"))

add("ODRL106-1","HasPart","hasPart europe vs isPartOf france: disjoint","Theorem",
    [GEO, CORE, GRND],
    [con("c1","spatial","hasPart","europe"), con("c2","spatial","isPartOf","france")],
    [], conflict_conj("c1","c2"))

# ============================================================
# ISANYOF (110–118)
# ============================================================
add("ODRL110-1","IsAnyOf","isAnyOf {de,en} vs eq de_AT: branch 1 hit","Theorem",
    [LNG, CORE, GRND],
    [con_multi("c1","language","isAnyOf",["de","en"]), con("c2","language","eq","de_AT")],
    [], compat_conj("c1","c2"))

add("ODRL111-1","IsAnyOf","isAnyOf {de,en} vs eq fr: both branches fail","Theorem",
    [LNG, CORE, GRND],
    [con_multi("c1","language","isAnyOf",["de","en"]), con("c2","language","eq","fr")],
    [isAnyOf_onlyif_tax("c1",["de","en"])], conflict_conj("c1","c2"))

add("ODRL112-1","IsAnyOf","isAnyOf {comm,nonComm} vs eq sciRes: Unknown","CounterSatisfiable",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAnyOf",["commercialPurpose","nonCommercialPurpose"]),
     con("c2","purpose","eq","scientificResearch")],
    [], compat_conj("c1","c2"))

add("ODRL113-1","IsAnyOf","isAnyOf {comm,mkt} vs eq commRes: Compatible","Theorem",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAnyOf",["commercialPurpose","marketing"]),
     con("c2","purpose","eq","commercialResearch")],
    [], compat_conj("c1","c2"))

add("ODRL114-1","IsAnyOf","isAnyOf {france,germany} spatial vs eq bavaria","Theorem",
    [GEO, CORE, GRND],
    [con_multi("c1","spatial","isAnyOf",["france","germany"]), con("c2","spatial","eq","bavaria")],
    [], compat_conj("c1","c2"))

add("ODRL115-1","IsAnyOf","isAnyOf {france,germany} vs eq europe: Unknown","CounterSatisfiable",
    [GEO, CORE, GRND],
    [con_multi("c1","spatial","isAnyOf",["france","germany"]), con("c2","spatial","eq","europe")],
    [], compat_conj("c1","c2"))

add("ODRL116-1","IsAnyOf","isAnyOf {comm,mkt} vs isA R&D: cross-op overlap","Theorem",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAnyOf",["commercialPurpose","marketing"]),
     con("c2","purpose","isA","researchAndDevelopment")],
    [], compat_conj("c1","c2"))

add("ODRL117-1","IsAnyOf","isAnyOf {de,en} vs isAnyOf {fr,ar}: Unknown","CounterSatisfiable",
    [LNG, CORE, GRND],
    [con_multi("c1","language","isAnyOf",["de","en"]),
     con_multi("c2","language","isAnyOf",["fr","ar"])],
    [isAnyOf_onlyif_tax("c1",["de","en"]), isAnyOf_onlyif_tax("c2",["fr","ar"])],
    conflict_conj("c1","c2"))

add("ODRL118-1","IsAnyOf","isAnyOf {de,ar} vs isAnyOf {en,ar}: overlap on ar","Theorem",
    [LNG, CORE, GRND],
    [con_multi("c1","language","isAnyOf",["de","ar"]),
     con_multi("c2","language","isAnyOf",["en","ar"])],
    [], compat_conj("c1","c2"))

# ============================================================
# ISALLOF (120–128)
# ============================================================
add("ODRL120-1","IsAllOf","isAllOf {R&D,comm} vs eq commRes: Compatible","Theorem",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["researchAndDevelopment","commercialPurpose"]),
     con("c2","purpose","eq","commercialResearch")],
    [isAllOf_if_tax("c1",["researchAndDevelopment","commercialPurpose"])],
    compat_conj("c1","c2"))

add("ODRL121-1","IsAllOf","isAllOf {comm,nonComm}: impossible intersection","CounterSatisfiable",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["commercialPurpose","nonCommercialPurpose"]),
     con("c2","purpose","eq","commercialResearch")],
    [isAllOf_if_tax("c1",["commercialPurpose","nonCommercialPurpose"])],
    compat_conj("c1","c2"))

add("ODRL122-1","IsAllOf","isAllOf {R&D,nonComm} vs eq nonCommRes: Compatible","Theorem",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["researchAndDevelopment","nonCommercialPurpose"]),
     con("c2","purpose","eq","nonCommercialResearch")],
    [isAllOf_if_tax("c1",["researchAndDevelopment","nonCommercialPurpose"])],
    compat_conj("c1","c2"))

add("ODRL123-1","IsAllOf","isAllOf {R&D,nonComm} vs eq sciRes: Unknown","CounterSatisfiable",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["researchAndDevelopment","nonCommercialPurpose"]),
     con("c2","purpose","eq","scientificResearch")],
    [isAllOf_if_tax("c1",["researchAndDevelopment","nonCommercialPurpose"])],
    compat_conj("c1","c2"))

add("ODRL124-1","IsAllOf","Diamond: isAllOf {A,B} finds X","Theorem",
    [DIA, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["diaA","diaB"]),
     con("c2","purpose","eq","diaX")],
    [isAllOf_if_tax("c1",["diaA","diaB"])],
    compat_conj("c1","c2"))

add("ODRL125-1","IsAllOf","Diamond: isAllOf {A,B} vs eq C: C not below both","CounterSatisfiable",
    [DIA, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["diaA","diaB"]),
     con("c2","purpose","eq","diaC")],
    [isAllOf_if_tax("c1",["diaA","diaB"])],
    compat_conj("c1","c2"))

add("ODRL126-1","IsAllOf","Chain: isAllOf {C,D} vs eq A: transitive hit","Theorem",
    [CHN, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["chainC","chainD"]),
     con("c2","purpose","eq","chainA")],
    [isAllOf_if_tax("c1",["chainC","chainD"])],
    compat_conj("c1","c2"))

add("ODRL127-1","IsAllOf","isAllOf {R&D,comm} vs isA comm: overlap","Theorem",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["researchAndDevelopment","commercialPurpose"]),
     con("c2","purpose","isA","commercialPurpose")],
    [isAllOf_if_tax("c1",["researchAndDevelopment","commercialPurpose"])],
    compat_conj("c1","c2"))

add("ODRL128-1","IsAllOf","isAllOf vs isAnyOf: cross-operator Unknown","CounterSatisfiable",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["researchAndDevelopment","commercialPurpose"]),
     con_multi("c2","purpose","isAnyOf",["nonCommercialPurpose","marketing"])],
    [isAllOf_if_tax("c1",["researchAndDevelopment","commercialPurpose"]),
     isAnyOf_onlyif_tax("c2",["nonCommercialPurpose","marketing"])],
    conflict_conj("c1","c2"))

# ============================================================
# ISNONEOF (130–139)
# ============================================================
add("ODRL130-1","IsNoneOf","isNoneOf {comm} vs eq nonCommRes: Compatible","Theorem",
    [DPV, CORE, GRND],
    [con("c1","purpose","isNoneOf","commercialPurpose"),
     con("c2","purpose","eq","nonCommercialResearch")],
    [isNoneOf_if_tax("c1",["commercialPurpose"])],
    compat_conj("c1","c2"))

add("ODRL131-1","IsNoneOf","isNoneOf {comm} vs eq commRes: Conflict","Theorem",
    [DPV, CORE, GRND],
    [con("c1","purpose","isNoneOf","commercialPurpose"),
     con("c2","purpose","eq","commercialResearch")],
    [], conflict_conj("c1","c2"))

add("ODRL132-1","IsNoneOf","isNoneOf {comm} vs eq sciRes: Unknown","CounterSatisfiable",
    [DPV, CORE, GRND],
    [con("c1","purpose","isNoneOf","commercialPurpose"),
     con("c2","purpose","eq","scientificResearch")],
    [isNoneOf_if_tax("c1",["commercialPurpose"])],
    compat_conj("c1","c2"))

add("ODRL133-1","IsNoneOf","isNoneOf {comm,nonComm} vs eq R&D: Unknown","CounterSatisfiable",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isNoneOf",["commercialPurpose","nonCommercialPurpose"]),
     con("c2","purpose","eq","researchAndDevelopment")],
    [isNoneOf_if_tax("c1",["commercialPurpose","nonCommercialPurpose"])],
    compat_conj("c1","c2"))

add("ODRL134-1","IsNoneOf","isNoneOf {R&D} vs isA R&D: contradiction","Theorem",
    [DPV, CORE, GRND],
    [con("c1","purpose","isNoneOf","researchAndDevelopment"),
     con("c2","purpose","isA","researchAndDevelopment")],
    [], conflict_conj("c1","c2"))

add("ODRL135-1","IsNoneOf","isNoneOf {de} vs isA de: lang contradiction","Theorem",
    [LNG, CORE, GRND],
    [con("c1","language","isNoneOf","de"), con("c2","language","isA","de")],
    [], conflict_conj("c1","c2"))

add("ODRL136-1","IsNoneOf","isNoneOf {france} spatial vs isPartOf europe","Theorem",
    [GEO, CORE, GRND],
    [con("c1","spatial","isNoneOf","france"), con("c2","spatial","isPartOf","europe")],
    [isNoneOf_if_mereo("c1",["france"])],
    compat_conj("c1","c2"))

add("ODRL137-1","IsNoneOf","isNoneOf {de,en} vs isAnyOf {de,en}: contradiction","Theorem",
    [LNG, CORE, GRND],
    [con_multi("c1","language","isNoneOf",["de","en"]),
     con_multi("c2","language","isAnyOf",["de","en"])],
    [isAnyOf_onlyif_tax("c2",["de","en"])],
    conflict_conj("c1","c2"))

add("ODRL138-1","IsNoneOf","Double negation: isNoneOf {comm} vs isNoneOf {nonComm}","Theorem",
    [DPV, CORE, GRND],
    [con("c1","purpose","isNoneOf","commercialPurpose"),
     con("c2","purpose","isNoneOf","nonCommercialPurpose")],
    [isNoneOf_if_tax("c1",["commercialPurpose"]),
     isNoneOf_if_tax("c2",["nonCommercialPurpose"])],
    compat_conj("c1","c2"))

add("ODRL139-1","IsNoneOf","isNoneOf singleton on |C|=1: empty set","Theorem",
    [SNG, CORE, GRND],
    [con("c1","purpose","isNoneOf","singleton"), con("c2","purpose","eq","singleton")],
    [], conflict_conj("c1","c2"))

# ============================================================
# NOMINAL (140–147)
# ============================================================
add("ODRL140-1","Nominal","Nominal eq email vs eq email: Compatible","Theorem",
    [NOM, CORE, GRND],
    [con("c1","channel","eq","email"), con("c2","channel","eq","email")],
    [], compat_conj("c1","c2"))

add("ODRL141-1","Nominal","Nominal eq email vs eq api: Conflict","Theorem",
    [NOM, CORE, GRND],
    [con("c1","channel","eq","email"), con("c2","channel","eq","api")],
    [], conflict_conj("c1","c2"))

add("ODRL142-1","Nominal","Nominal isA email = eq email: Compatible","Theorem",
    [NOM, CORE, GRND],
    [con("c1","channel","isA","email"), con("c2","channel","eq","email")],
    [], compat_conj("c1","c2"))

add("ODRL143-1","Nominal","Nominal isA email vs eq api: Conflict","Theorem",
    [NOM, CORE, GRND],
    [con("c1","channel","isA","email"), con("c2","channel","eq","api")],
    [], conflict_conj("c1","c2"))

add("ODRL144-1","Nominal","Nominal isAnyOf {email,api} vs eq ftp: Conflict","Theorem",
    [NOM, CORE, GRND],
    [con_multi("c1","channel","isAnyOf",["email","api"]), con("c2","channel","eq","ftp")],
    [isAnyOf_onlyif_nom("c1",["email","api"])],
    conflict_conj("c1","c2"))

add("ODRL145-1","Nominal","Nominal isAnyOf {email,api} vs eq email: Compatible","Theorem",
    [NOM, CORE, GRND],
    [con_multi("c1","channel","isAnyOf",["email","api"]), con("c2","channel","eq","email")],
    [], compat_conj("c1","c2"))

add("ODRL146-1","Nominal","Nominal isNoneOf {email,api} vs eq ftp: Compatible","Theorem",
    [NOM, CORE, GRND],
    [con_multi("c1","channel","isNoneOf",["email","api"]), con("c2","channel","eq","ftp")],
    [isNoneOf_bidir_nom("c1",["email","api"])],
    compat_conj("c1","c2"))

add("ODRL147-1","Nominal","Nominal neq email vs eq email: Conflict","Theorem",
    [NOM, CORE, GRND],
    [con("c1","channel","neq","email"), con("c2","channel","eq","email")],
    [], conflict_conj("c1","c2"))

# ============================================================
# OPERATOR PAIRS (150–161)
# ============================================================
add("ODRL150-1","OperatorPairs","isA nonComm vs isNoneOf nonComm: contradiction","Theorem",
    [DPV, CORE, GRND],
    [con("c1","purpose","isA","nonCommercialPurpose"),
     con("c2","purpose","isNoneOf","nonCommercialPurpose")],
    [], conflict_conj("c1","c2"))

add("ODRL151-1","OperatorPairs","neq comm vs isA comm: overlap on children","Theorem",
    [DPV, DPV_D, DPV_X, CORE, GRND],
    [con("c1","purpose","neq","commercialPurpose"),
     con("c2","purpose","isA","commercialPurpose")],
    [], compat_conj("c1","c2"))

add("ODRL152-1","OperatorPairs","hasPart france vs isPartOf france: reflexive overlap","Theorem",
    [GEO, CORE, GRND],
    [con("c1","spatial","hasPart","france"), con("c2","spatial","isPartOf","france")],
    [], compat_conj("c1","c2"))

add("ODRL153-1","OperatorPairs","isAllOf {R&D,nonComm} vs isAnyOf {comm,mkt}: Unknown","CounterSatisfiable",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["researchAndDevelopment","nonCommercialPurpose"]),
     con_multi("c2","purpose","isAnyOf",["commercialPurpose","marketing"])],
    [isAllOf_if_tax("c1",["researchAndDevelopment","nonCommercialPurpose"]),
     isAnyOf_onlyif_tax("c2",["commercialPurpose","marketing"])],
    conflict_conj("c1","c2"))

add("ODRL154-1","OperatorPairs","isNoneOf {de} vs isNoneOf {en}: shared exclusion","Theorem",
    [LNG, CORE, GRND],
    [con("c1","language","isNoneOf","de"), con("c2","language","isNoneOf","en")],
    [isNoneOf_if_tax("c1",["de"],"language"),
     isNoneOf_if_tax("c2",["en"],"language")],
    compat_conj("c1","c2"))

add("ODRL155-1","OperatorPairs","isPartOf germany vs hasPart france: Unknown","CounterSatisfiable",
    [GEO, CORE, GRND],
    [con("c1","spatial","isPartOf","germany"), con("c2","spatial","hasPart","france")],
    [], compat_conj("c1","c2"))

add("ODRL156-1","OperatorPairs","eq acadRes vs isNoneOf {R&D}: Conflict","Theorem",
    [DPV, CORE, GRND],
    [con("c1","purpose","eq","academicResearch"),
     con("c2","purpose","isNoneOf","researchAndDevelopment")],
    [], conflict_conj("c1","c2"))

add("ODRL157-1","OperatorPairs","isAnyOf {de,en} vs isNoneOf {de,en}: contradiction","Theorem",
    [LNG, CORE, GRND],
    [con_multi("c1","language","isAnyOf",["de","en"]),
     con_multi("c2","language","isNoneOf",["de","en"])],
    [isAnyOf_onlyif_tax("c1",["de","en"]),
     isNoneOf_if_tax("c2",["de","en"],"language")],
    conflict_conj("c1","c2"))

add("ODRL158-1","OperatorPairs","neq de vs neq en: large overlap","Theorem",
    [LNG, CORE, GRND],
    [con("c1","language","neq","de"), con("c2","language","neq","en")],
    [], compat_conj("c1","c2"))

add("ODRL159-1","OperatorPairs","isA R&D vs isAnyOf {comm,nonComm}: overlap","Theorem",
    [DPV, CORE, GRND],
    [con("c1","purpose","isA","researchAndDevelopment"),
     con_multi("c2","purpose","isAnyOf",["commercialPurpose","nonCommercialPurpose"])],
    [], compat_conj("c1","c2"))

add("ODRL160-1","OperatorPairs","hasPart germany vs hasPart france: meet at europe","Theorem",
    [GEO, CORE, GRND],
    [con("c1","spatial","hasPart","germany"), con("c2","spatial","hasPart","france")],
    [], compat_conj("c1","c2"))

add("ODRL161-1","OperatorPairs","isAllOf {R&D,comm} vs isNoneOf {comm}: Conflict","Theorem",
    [DPV, CORE, GRND],
    [con_multi("c1","purpose","isAllOf",["researchAndDevelopment","commercialPurpose"]),
     con("c2","purpose","isNoneOf","commercialPurpose")],
    [isAllOf_if_tax("c1",["researchAndDevelopment","commercialPurpose"])],
    conflict_conj("c1","c2"))

# ============================================================
# ADVERSARIAL DEEP (170–181)
# ============================================================
add("ODRL170-1","AdvDeep","Chain-5: isA E vs eq A: transitive Compatible","Theorem",
    [CHN, CORE, GRND],
    [con("c1","purpose","isA","chainE"), con("c2","purpose","eq","chainA")],
    [], compat_conj("c1","c2"))

add("ODRL171-1","AdvDeep","Chain-5: isA C vs eq D: D not below C","Theorem",
    [CHN, CORE, GRND],
    [con("c1","purpose","isA","chainC"), con("c2","purpose","eq","chainD")],
    [], conflict_conj("c1","c2"))

add("ODRL172-1","AdvDeep","Diamond: isA C vs eq X: X below C via A","Theorem",
    [DIA, CORE, GRND],
    [con("c1","purpose","isA","diaC"), con("c2","purpose","eq","diaX")],
    [], compat_conj("c1","c2"))

add("ODRL173-1","AdvDeep","Diamond: isA A vs isA B: overlap on X","Theorem",
    [DIA, CORE, GRND],
    [con("c1","purpose","isA","diaA"), con("c2","purpose","isA","diaB")],
    [], compat_conj("c1","c2"))

add("ODRL174-1","AdvDeep","Diamond: isA A vs eq B: incomparable","Theorem",
    [DIA, CORE, GRND],
    [con("c1","purpose","isA","diaA"), con("c2","purpose","eq","diaB")],
    [], conflict_conj("c1","c2"))

add("ODRL175-1","AdvDeep","Single |C|=1: eq vs eq: Compatible","Theorem",
    [SNG, CORE, GRND],
    [con("c1","purpose","eq","singleton"), con("c2","purpose","eq","singleton")],
    [], compat_conj("c1","c2"))

add("ODRL176-1","AdvDeep","Single |C|=1: isA vs neq: Conflict","Theorem",
    [SNG, CORE, GRND],
    [con("c1","purpose","isA","singleton"), con("c2","purpose","neq","singleton")],
    [], conflict_conj("c1","c2"))

add("ODRL177-1","AdvDeep","Near-miss: isA Left vs isA Right: overlap on Shared","Theorem",
    [NMS, CORE, GRND],
    [con("c1","purpose","isA","nmLeft"), con("c2","purpose","isA","nmRight")],
    [], compat_conj("c1","c2"))

add("ODRL178-1","AdvDeep","Near-miss: eq OnlyLeft vs isA Right: Conflict","Theorem",
    [NMS, CORE, GRND],
    [con("c1","purpose","eq","nmOnlyLeft"), con("c2","purpose","isA","nmRight")],
    [], conflict_conj("c1","c2"))

add("ODRL179-1","AdvDeep","All-Unknown conjunction: both operands Unknown","CounterSatisfiable",
    [GEO, DPV, CORE, GRND],
    [con("c1","spatial","isPartOf","france"), con("c2","spatial","eq","bavaria"),
     con("c3","purpose","isA","nonCommercialPurpose"), con("c4","purpose","eq","scientificResearch")],
    [], cross2_conj("c1","c2","c3","c4"))

add("ODRL180-1","AdvDeep","Chain: isAnyOf {A,E} vs eq C: A below C","Theorem",
    [CHN, CORE, GRND],
    [con_multi("c1","purpose","isAnyOf",["chainA","chainE"]),
     con("c2","purpose","eq","chainC")],
    [], compat_conj("c1","c2"))

add("ODRL181-1","AdvDeep","Chain: isNoneOf {E} vs eq D: D below E","Theorem",
    [CHN, CHN_D, CORE, GRND],
    [con("c1","purpose","isNoneOf","chainE"), con("c2","purpose","eq","chainD")],
    [isNoneOf_if_tax("c1",["chainE"])],
    conflict_conj("c1","c2"))

# ============================================================
# ALIGNMENT ADVERSARIAL (190–199)
# ============================================================
add("ODRL190-1","AlignAdv","Unmapped witness: de_AT in KB_A, unmapped in KB_B","CounterSatisfiable",
    [LNG1, CORE, GRND],
    [con("c1","language","isA","deu"), con("c2","language","eq","de_AT")],
    [], compat_conj("c1","c2"))

add("ODRL191-1","AlignAdv","Unmapped witness: no false conflict either","CounterSatisfiable",
    [LNG1, CORE, GRND],
    [con("c1","language","isA","deu"), con("c2","language","eq","de_AT")],
    [], conflict_conj("c1","c2"))

add("ODRL192-1","AlignAdv","Spatial: bavaria unmapped in ISO3166","CounterSatisfiable",
    [GEO1, CORE, GRND],
    [con("c1","spatial","isPartOf","deu"), con("c2","spatial","eq","bavaria")],
    [], compat_conj("c1","c2"))

add("ODRL193-1","AlignAdv","Aligned isAnyOf conflict: {deu,eng} vs fra","Theorem",
    [LNG1, CORE, GRND],
    [con_multi("c1","language","isAnyOf",["deu","eng"]), con("c2","language","eq","fra")],
    [isAnyOf_onlyif_tax("c1",["deu","eng"])],
    conflict_conj("c1","c2"))

add("ODRL194-1","AlignAdv","Aligned isNoneOf: {deu} vs eq fra: Compatible","Theorem",
    [LNG1, CORE, GRND],
    [con("c1","language","isNoneOf","deu"), con("c2","language","eq","fra")],
    [isNoneOf_if_tax("c1",["deu"],"language")],
    compat_conj("c1","c2"))

add("ODRL195-1","AlignAdv","Aligned hasPart: fra hasPart vs eq eur","Theorem",
    [GEO1, CORE, GRND],
    [con("c1","spatial","hasPart","fra"), con("c2","spatial","eq","eur")],
    [], compat_conj("c1","c2"))

add("ODRL196-1","AlignAdv","Aligned neq: neq deu vs eq fra: Compatible","Theorem",
    [LNG1, CORE, GRND],
    [con("c1","language","neq","deu"), con("c2","language","eq","fra")],
    [], compat_conj("c1","c2"))

add("ODRL197-1","AlignAdv","Aligned neq: neq deu vs eq deu: Conflict","Theorem",
    [LNG1, CORE, GRND],
    [con("c1","language","neq","deu"), con("c2","language","eq","deu")],
    [], conflict_conj("c1","c2"))

add("ODRL198-1","AlignAdv","3-KB aligned: hasPart + isA purpose + isA lang","CounterSatisfiable",
    [GEO1, DPV, LNG1, CORE, GRND],
    [con("c1","spatial","hasPart","fra"), con("c2","spatial","eq","eur"),
     con("c3","purpose","isA","researchAndDevelopment"), con("c4","purpose","eq","academicResearch"),
     con("c5","language","isA","deu"), con("c6","language","eq","fra")],
    [], cross3_conj("c1","c2","c3","c4","c5","c6"))

add("ODRL199-1","AlignAdv","Triple degradation: all 3 operands unmapped","CounterSatisfiable",
    [GEO1, DPV, LNG1, CORE, GRND],
    [con("c1","spatial","isPartOf","deu"), con("c2","spatial","eq","bavaria"),
     con("c3","purpose","isA","researchAndDevelopment"), con("c4","purpose","eq","scientificResearch"),
     con("c5","language","isA","deu"), con("c6","language","eq","de_AT")],
    [], cross3_conj("c1","c2","c3","c4","c5","c6"))

# ============================================================
# COMPOSITION DEEP (200–207)
# ============================================================
add("ODRL200-1","CompDeep","3-op AND all Compatible","Theorem",
    [GEO, DPV, LNG, CORE, GRND],
    [con("c1","spatial","isPartOf","europe"), con("c2","spatial","eq","france"),
     con("c3","purpose","isA","researchAndDevelopment"), con("c4","purpose","eq","academicResearch"),
     con("c5","language","isA","de"), con("c6","language","eq","de_AT")],
    [], cross3_conj("c1","c2","c3","c4","c5","c6"))

add("ODRL201-1","CompDeep","3-op AND: language conflicts blocks","CounterSatisfiable",
    [GEO, DPV, LNG, CORE, GRND],
    [con("c1","spatial","isPartOf","europe"), con("c2","spatial","eq","france"),
     con("c3","purpose","isA","researchAndDevelopment"), con("c4","purpose","eq","academicResearch"),
     con("c5","language","isA","de"), con("c6","language","eq","fr")],
    [], cross3_conj("c1","c2","c3","c4","c5","c6"))

add("ODRL202-1","CompDeep","OR: one Compatible branch resolves","Theorem",
    [DPV, LNG, CORE, GRND],
    [con("c1","purpose","isA","nonCommercialPurpose"),
     con("c2","language","isA","de"), con("c3","language","eq","de_AT")],
    [], or_compat_conj("c1","c2","c3"))

add("ODRL203-1","CompDeep","OR: all branches Conflict","Theorem",
    [LNG, CORE, GRND],
    [con("c1","language","isA","de"), con("c2","language","isA","en"),
     con("c3","language","eq","fr")],
    [], or_conflict_conj("c1","c2","c3"))

add("ODRL204-1","CompDeep","XONE: two branches Compatible: Unknown","CounterSatisfiable",
    [DPV, CORE, GRND],
    [con("c1","purpose","isA","researchAndDevelopment"),
     con("c2","purpose","isA","nonCommercialPurpose"),
     con("c3","purpose","eq","nonCommercialResearch")],
    [], xone_compat_conj("c1","c2","c3"))

add("ODRL205-1","CompDeep","XONE: one Unknown branch: Unknown","CounterSatisfiable",
    [DPV, CORE, GRND],
    [con("c1","purpose","isA","commercialPurpose"),
     con("c2","purpose","isA","nonCommercialPurpose"),
     con("c3","purpose","eq","scientificResearch")],
    [], xone_compat_conj("c1","c2","c3"))

add("ODRL206-1","CompDeep","AND-of-OR: spatial AND or(purpose)","Theorem",
    [GEO, DPV, CORE, GRND],
    [con("cs","spatial","isPartOf","europe"), con("co","spatial","eq","france"),
     con("c1","purpose","isA","commercialPurpose"),
     con("c2","purpose","isA","nonCommercialPurpose"),
     con("c3","purpose","eq","nonCommercialResearch")],
    [],
    f"""fof(and_or_compatible, conjecture,
    (?[X]: (in_denotation(X,cs) & in_denotation(X,co)))
  & ((?[Y]: (in_denotation(Y,c1) & in_denotation(Y,c3)))
   | (?[Z]: (in_denotation(Z,c2) & in_denotation(Z,c3))))).""")

add("ODRL207-1","CompDeep","AND-of-XONE: spatial compat AND xone purpose: Unknown","CounterSatisfiable",
    [GEO, DPV, CORE, GRND],
    [con("cs","spatial","isPartOf","europe"), con("co","spatial","eq","france"),
     con("c1","purpose","isA","commercialPurpose"),
     con("c2","purpose","isA","nonCommercialPurpose"),
     con("c3","purpose","eq","scientificResearch")],
    [],
    f"""fof(and_xone_compatible, conjecture,
    (?[X]: (in_denotation(X,cs) & in_denotation(X,co)))
  & ((?[Y]: (in_denotation(Y,c1) & ~in_denotation(Y,c2) & in_denotation(Y,c3)))
   | (?[Z]: (in_denotation(Z,c2) & ~in_denotation(Z,c1) & in_denotation(Z,c3))))).""")

# ============================================================
# Generator + Runner
# ============================================================
def gen(p):
    parts = [header(p["id"], p["desc"], p["status"], p.get("notes",""))]
    parts.append("")
    parts.append(includes(*p["axfiles"]))
    parts.append("")
    for c in p["constraints"]:
        parts.append(c)
    if p["extra"]:
        parts.append("")
        parts.append("% --- Per-problem grounding (if/only-if direction) ---")
        for e in p["extra"]:
            parts.append(e)
    parts.append("")
    parts.append("% --- Conjecture ---")
    parts.append(p["conjecture"])
    parts.append("")
    parts.append("%--------------------------------------------------------------------------")
    return "\n".join(parts)

def run_vampire(fp, timeout=30):
    try:
        t0 = time.time()
        r = subprocess.run(["vampire","--time_limit",str(timeout),fp],
                           capture_output=True, text=True, timeout=timeout+5)
        out = r.stdout
        for status in ["Theorem","CounterSatisfiable","Timeout","Unknown","GaveUp"]:
            if status in out:
                return status, time.time()-t0
        return "???", time.time()-t0
    except subprocess.TimeoutExpired:
        return "timeout", timeout
    except FileNotFoundError:
        return "not_found", 0

def main():
    do_run = "--run" in sys.argv
    timeout = 30
    for i, a in enumerate(sys.argv):
        if a == "--timeout" and i+1 < len(sys.argv):
            timeout = int(sys.argv[i+1])

    cats = {}
    for p in P:
        cats[p["sub"]] = cats.get(p["sub"], 0) + 1

    for p in P:
        sd = os.path.join(TPTP_DIR, p["sub"])
        os.makedirs(sd, exist_ok=True)
        fp = os.path.join(sd, f"{p['id']}.p")
        with open(fp, "w") as f:
            f.write(gen(p))

    print(f"Generated {len(P)} TPTP files in {TPTP_DIR}/")
    print("\nBreakdown:")
    for c, n in sorted(cats.items()):
        print(f"  {c:<16} {n}")

    if not do_run:
        print("\nUse --run to execute Vampire.")
        return

    hdr = f"{'Problem':<14} {'Expected':>18} {'Vampire':>18} {'Time':>8}  {'OK':>3}"
    print(); print(hdr); print("-"*len(hdr))
    ok = True; rcats = {}
    for p in P:
        fp = os.path.join(TPTP_DIR, p["sub"], f"{p['id']}.p")
        vr, vt = run_vampire(fp, timeout)
        m = "✓" if vr == p["status"] else "✗"
        if vr != p["status"]: ok = False
        print(f"{p['id']:<14} {p['status']:>18} {vr:>18} {vt:>7.3f}s  {m:>3}")
        c = p["sub"]
        if c not in rcats: rcats[c] = [0,0]
        rcats[c][0] += 1
        rcats[c][1] += 1 if vr == p["status"] else 0

    print()
    for c, (t, p_) in sorted(rcats.items()):
        print(f"  {c:<16} {p_}/{t} {'✓' if p_==t else '✗'}")
    total_ok = sum(v[1] for v in rcats.values())
    total = sum(v[0] for v in rcats.values())
    print(f"  {'TOTAL':<16} {total_ok}/{total}")
    print("\nAll match ✓" if ok else "\nWARNING: mismatches ✗")

if __name__ == "__main__":
    main()
