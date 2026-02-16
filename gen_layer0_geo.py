#!/usr/bin/env python3
"""
gen_layer0_geo.py — Generate TPTP Layer 0 axiom file from UN M49 hierarchy.

The UN Standard Country or Area Codes for Statistical Use (M49) provides a
4-level geographic containment hierarchy:
    World → Continent → Sub-region → [Intermediate region →] Country/Area

Usage:
    uv run python gen_layer0_geo.py \
        --output Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax \
        --scope europe \
        --sibling-disjointness \
        --no-una

Source: https://unstats.un.org/unsd/methodology/m49/
"""
import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path

# =============================================================================
# UN M49 Hierarchy Data (December 2021 revision)
# Format: (code, name, type, parent_code)
#   type: 0=global, 1=region, 2=sub-region, 3=intermediate region, 4=country
# =============================================================================
M49_HIERARCHY = [
    ("001", "World", 0, None),
    ("002", "Africa", 1, "001"),
    ("019", "Americas", 1, "001"),
    ("142", "Asia", 1, "001"),
    ("150", "Europe", 1, "001"),
    ("009", "Oceania", 1, "001"),
    ("015", "Northern Africa", 2, "002"),
    ("202", "Sub-Saharan Africa", 2, "002"),
    ("419", "Latin America and the Caribbean", 2, "019"),
    ("021", "Northern America", 2, "019"),
    ("143", "Central Asia", 2, "142"),
    ("030", "Eastern Asia", 2, "142"),
    ("035", "South-eastern Asia", 2, "142"),
    ("034", "Southern Asia", 2, "142"),
    ("145", "Western Asia", 2, "142"),
    ("151", "Eastern Europe", 2, "150"),
    ("154", "Northern Europe", 2, "150"),
    ("039", "Southern Europe", 2, "150"),
    ("155", "Western Europe", 2, "150"),
    ("053", "Australia and New Zealand", 2, "009"),
    ("054", "Melanesia", 2, "009"),
    ("057", "Micronesia", 2, "009"),
    ("061", "Polynesia", 2, "009"),
    ("014", "Eastern Africa", 3, "202"),
    ("017", "Middle Africa", 3, "202"),
    ("018", "Southern Africa", 3, "202"),
    ("011", "Western Africa", 3, "202"),
    ("029", "Caribbean", 3, "419"),
    ("013", "Central America", 3, "419"),
    ("005", "South America", 3, "419"),
    ("830", "Channel Islands", 3, "154"),
    ("012", "Algeria", 4, "015"),
    ("818", "Egypt", 4, "015"),
    ("434", "Libya", 4, "015"),
    ("504", "Morocco", 4, "015"),
    ("736", "Sudan", 4, "015"),
    ("788", "Tunisia", 4, "015"),
    ("732", "Western Sahara", 4, "015"),
    ("086", "British Indian Ocean Territory", 4, "014"),
    ("108", "Burundi", 4, "014"),
    ("174", "Comoros", 4, "014"),
    ("262", "Djibouti", 4, "014"),
    ("232", "Eritrea", 4, "014"),
    ("231", "Ethiopia", 4, "014"),
    ("260", "French Southern Territories", 4, "014"),
    ("404", "Kenya", 4, "014"),
    ("450", "Madagascar", 4, "014"),
    ("454", "Malawi", 4, "014"),
    ("480", "Mauritius", 4, "014"),
    ("175", "Mayotte", 4, "014"),
    ("508", "Mozambique", 4, "014"),
    ("638", "Reunion", 4, "014"),
    ("646", "Rwanda", 4, "014"),
    ("690", "Seychelles", 4, "014"),
    ("706", "Somalia", 4, "014"),
    ("728", "South Sudan", 4, "014"),
    ("800", "Uganda", 4, "014"),
    ("834", "United Republic of Tanzania", 4, "014"),
    ("894", "Zambia", 4, "014"),
    ("716", "Zimbabwe", 4, "014"),
    ("024", "Angola", 4, "017"),
    ("120", "Cameroon", 4, "017"),
    ("140", "Central African Republic", 4, "017"),
    ("148", "Chad", 4, "017"),
    ("178", "Congo", 4, "017"),
    ("180", "Democratic Republic of the Congo", 4, "017"),
    ("226", "Equatorial Guinea", 4, "017"),
    ("266", "Gabon", 4, "017"),
    ("678", "Sao Tome and Principe", 4, "017"),
    ("072", "Botswana", 4, "018"),
    ("748", "Eswatini", 4, "018"),
    ("426", "Lesotho", 4, "018"),
    ("516", "Namibia", 4, "018"),
    ("710", "South Africa", 4, "018"),
    ("204", "Benin", 4, "011"),
    ("854", "Burkina Faso", 4, "011"),
    ("132", "Cabo Verde", 4, "011"),
    ("384", "Cote d'Ivoire", 4, "011"),
    ("270", "Gambia", 4, "011"),
    ("288", "Ghana", 4, "011"),
    ("324", "Guinea", 4, "011"),
    ("624", "Guinea-Bissau", 4, "011"),
    ("430", "Liberia", 4, "011"),
    ("466", "Mali", 4, "011"),
    ("478", "Mauritania", 4, "011"),
    ("562", "Niger", 4, "011"),
    ("566", "Nigeria", 4, "011"),
    ("654", "Saint Helena", 4, "011"),
    ("686", "Senegal", 4, "011"),
    ("694", "Sierra Leone", 4, "011"),
    ("768", "Togo", 4, "011"),
    ("660", "Anguilla", 4, "029"),
    ("028", "Antigua and Barbuda", 4, "029"),
    ("533", "Aruba", 4, "029"),
    ("044", "Bahamas", 4, "029"),
    ("052", "Barbados", 4, "029"),
    ("535", "Bonaire Sint Eustatius and Saba", 4, "029"),
    ("092", "British Virgin Islands", 4, "029"),
    ("136", "Cayman Islands", 4, "029"),
    ("192", "Cuba", 4, "029"),
    ("531", "Curacao", 4, "029"),
    ("212", "Dominica", 4, "029"),
    ("214", "Dominican Republic", 4, "029"),
    ("308", "Grenada", 4, "029"),
    ("312", "Guadeloupe", 4, "029"),
    ("332", "Haiti", 4, "029"),
    ("388", "Jamaica", 4, "029"),
    ("474", "Martinique", 4, "029"),
    ("500", "Montserrat", 4, "029"),
    ("630", "Puerto Rico", 4, "029"),
    ("652", "Saint Barthelemy", 4, "029"),
    ("659", "Saint Kitts and Nevis", 4, "029"),
    ("662", "Saint Lucia", 4, "029"),
    ("663", "Saint Martin (French part)", 4, "029"),
    ("670", "Saint Vincent and the Grenadines", 4, "029"),
    ("534", "Sint Maarten (Dutch part)", 4, "029"),
    ("780", "Trinidad and Tobago", 4, "029"),
    ("796", "Turks and Caicos Islands", 4, "029"),
    ("850", "United States Virgin Islands", 4, "029"),
    ("084", "Belize", 4, "013"),
    ("188", "Costa Rica", 4, "013"),
    ("222", "El Salvador", 4, "013"),
    ("320", "Guatemala", 4, "013"),
    ("340", "Honduras", 4, "013"),
    ("484", "Mexico", 4, "013"),
    ("558", "Nicaragua", 4, "013"),
    ("591", "Panama", 4, "013"),
    ("032", "Argentina", 4, "005"),
    ("068", "Bolivia", 4, "005"),
    ("074", "Bouvet Island", 4, "005"),
    ("076", "Brazil", 4, "005"),
    ("152", "Chile", 4, "005"),
    ("170", "Colombia", 4, "005"),
    ("218", "Ecuador", 4, "005"),
    ("238", "Falkland Islands (Malvinas)", 4, "005"),
    ("254", "French Guiana", 4, "005"),
    ("328", "Guyana", 4, "005"),
    ("600", "Paraguay", 4, "005"),
    ("604", "Peru", 4, "005"),
    ("239", "South Georgia and the South Sandwich Islands", 4, "005"),
    ("740", "Suriname", 4, "005"),
    ("858", "Uruguay", 4, "005"),
    ("862", "Venezuela", 4, "005"),
    ("060", "Bermuda", 4, "021"),
    ("124", "Canada", 4, "021"),
    ("304", "Greenland", 4, "021"),
    ("666", "Saint Pierre and Miquelon", 4, "021"),
    ("840", "United States of America", 4, "021"),
    ("398", "Kazakhstan", 4, "143"),
    ("417", "Kyrgyzstan", 4, "143"),
    ("762", "Tajikistan", 4, "143"),
    ("795", "Turkmenistan", 4, "143"),
    ("860", "Uzbekistan", 4, "143"),
    ("156", "China", 4, "030"),
    ("344", "China Hong Kong SAR", 4, "030"),
    ("446", "China Macao SAR", 4, "030"),
    ("408", "Dem. Peoples Republic of Korea", 4, "030"),
    ("392", "Japan", 4, "030"),
    ("496", "Mongolia", 4, "030"),
    ("410", "Republic of Korea", 4, "030"),
    ("096", "Brunei Darussalam", 4, "035"),
    ("116", "Cambodia", 4, "035"),
    ("360", "Indonesia", 4, "035"),
    ("418", "Lao Peoples Dem. Republic", 4, "035"),
    ("458", "Malaysia", 4, "035"),
    ("104", "Myanmar", 4, "035"),
    ("608", "Philippines", 4, "035"),
    ("702", "Singapore", 4, "035"),
    ("764", "Thailand", 4, "035"),
    ("626", "Timor-Leste", 4, "035"),
    ("704", "Viet Nam", 4, "035"),
    ("004", "Afghanistan", 4, "034"),
    ("050", "Bangladesh", 4, "034"),
    ("064", "Bhutan", 4, "034"),
    ("356", "India", 4, "034"),
    ("364", "Iran", 4, "034"),
    ("462", "Maldives", 4, "034"),
    ("524", "Nepal", 4, "034"),
    ("586", "Pakistan", 4, "034"),
    ("144", "Sri Lanka", 4, "034"),
    ("051", "Armenia", 4, "145"),
    ("031", "Azerbaijan", 4, "145"),
    ("048", "Bahrain", 4, "145"),
    ("196", "Cyprus", 4, "145"),
    ("268", "Georgia", 4, "145"),
    ("368", "Iraq", 4, "145"),
    ("376", "Israel", 4, "145"),
    ("400", "Jordan", 4, "145"),
    ("414", "Kuwait", 4, "145"),
    ("422", "Lebanon", 4, "145"),
    ("512", "Oman", 4, "145"),
    ("634", "Qatar", 4, "145"),
    ("682", "Saudi Arabia", 4, "145"),
    ("275", "State of Palestine", 4, "145"),
    ("760", "Syrian Arab Republic", 4, "145"),
    ("792", "Turkey", 4, "145"),
    ("784", "United Arab Emirates", 4, "145"),
    ("887", "Yemen", 4, "145"),
    ("112", "Belarus", 4, "151"),
    ("100", "Bulgaria", 4, "151"),
    ("203", "Czechia", 4, "151"),
    ("348", "Hungary", 4, "151"),
    ("616", "Poland", 4, "151"),
    ("498", "Republic of Moldova", 4, "151"),
    ("642", "Romania", 4, "151"),
    ("643", "Russian Federation", 4, "151"),
    ("703", "Slovakia", 4, "151"),
    ("804", "Ukraine", 4, "151"),
    ("248", "Aland Islands", 4, "154"),
    ("208", "Denmark", 4, "154"),
    ("233", "Estonia", 4, "154"),
    ("234", "Faroe Islands", 4, "154"),
    ("246", "Finland", 4, "154"),
    ("352", "Iceland", 4, "154"),
    ("372", "Ireland", 4, "154"),
    ("833", "Isle of Man", 4, "154"),
    ("428", "Latvia", 4, "154"),
    ("440", "Lithuania", 4, "154"),
    ("578", "Norway", 4, "154"),
    ("744", "Svalbard and Jan Mayen Islands", 4, "154"),
    ("752", "Sweden", 4, "154"),
    ("826", "United Kingdom", 4, "154"),
    ("831", "Guernsey", 4, "830"),
    ("832", "Jersey", 4, "830"),
    ("680", "Sark", 4, "830"),
    ("008", "Albania", 4, "039"),
    ("020", "Andorra", 4, "039"),
    ("070", "Bosnia and Herzegovina", 4, "039"),
    ("191", "Croatia", 4, "039"),
    ("292", "Gibraltar", 4, "039"),
    ("300", "Greece", 4, "039"),
    ("336", "Holy See", 4, "039"),
    ("380", "Italy", 4, "039"),
    ("470", "Malta", 4, "039"),
    ("499", "Montenegro", 4, "039"),
    ("807", "North Macedonia", 4, "039"),
    ("620", "Portugal", 4, "039"),
    ("674", "San Marino", 4, "039"),
    ("688", "Serbia", 4, "039"),
    ("705", "Slovenia", 4, "039"),
    ("724", "Spain", 4, "039"),
    ("040", "Austria", 4, "155"),
    ("056", "Belgium", 4, "155"),
    ("250", "France", 4, "155"),
    ("276", "Germany", 4, "155"),
    ("438", "Liechtenstein", 4, "155"),
    ("442", "Luxembourg", 4, "155"),
    ("492", "Monaco", 4, "155"),
    ("528", "Netherlands", 4, "155"),
    ("756", "Switzerland", 4, "155"),
    ("036", "Australia", 4, "053"),
    ("554", "New Zealand", 4, "053"),
    ("162", "Christmas Island", 4, "053"),
    ("166", "Cocos (Keeling) Islands", 4, "053"),
    ("334", "Heard Island and McDonald Islands", 4, "053"),
    ("574", "Norfolk Island", 4, "053"),
    ("242", "Fiji", 4, "054"),
    ("540", "New Caledonia", 4, "054"),
    ("598", "Papua New Guinea", 4, "054"),
    ("090", "Solomon Islands", 4, "054"),
    ("548", "Vanuatu", 4, "054"),
    ("316", "Guam", 4, "057"),
    ("296", "Kiribati", 4, "057"),
    ("584", "Marshall Islands", 4, "057"),
    ("583", "Micronesia (Federated States of)", 4, "057"),
    ("520", "Nauru", 4, "057"),
    ("580", "Northern Mariana Islands", 4, "057"),
    ("585", "Palau", 4, "057"),
    ("016", "American Samoa", 4, "061"),
    ("184", "Cook Islands", 4, "061"),
    ("258", "French Polynesia", 4, "061"),
    ("570", "Niue", 4, "061"),
    ("612", "Pitcairn", 4, "061"),
    ("882", "Samoa", 4, "061"),
    ("772", "Tokelau", 4, "061"),
    ("776", "Tonga", 4, "061"),
    ("798", "Tuvalu", 4, "061"),
    ("876", "Wallis and Futuna Islands", 4, "061"),
    ("010", "Antarctica", 4, "001"),
]

def name_to_tptp(name):
    name = re.sub(r'\(.*?\)', '', name).strip()
    parts = re.split(r"[\s\-']+", name)
    parts = [p for p in parts if p]
    if not parts:
        return "unknown"
    result = parts[0].lower()
    for p in parts[1:]:
        result += p[0].upper() + p[1:].lower() if len(p) > 1 else p.upper()
    result = re.sub(r'[^a-zA-Z0-9_]', '', result)
    if result and not result[0].isalpha():
        result = "r_" + result
    if result and result[0].isupper():
        result = result[0].lower() + result[1:]
    return result

def filter_scope(hierarchy, scope):
    if scope == "full":
        return hierarchy
    code_to_entry = {c: (c,n,t,p) for c,n,t,p in hierarchy}
    scope_roots = {"europe":"150","africa":"002","americas":"019","asia":"142","oceania":"009"}
    if scope not in scope_roots:
        print(f"ERROR: Unknown scope '{scope}'.", file=sys.stderr); sys.exit(1)
    root_code = scope_roots[scope]
    children_map = defaultdict(set)
    for c,n,t,p in hierarchy:
        if p: children_map[p].add(c)
    reachable = set()
    queue = [root_code]
    reachable.add(root_code)
    while queue:
        cur = queue.pop(0)
        for ch in children_map.get(cur, []):
            if ch not in reachable:
                reachable.add(ch); queue.append(ch)
    reachable.add("001")
    result = []
    for c,n,t,p in hierarchy:
        if c in reachable:
            if c == root_code: result.append((c,n,t,"001"))
            elif p in reachable: result.append((c,n,t,p))
    return result

def compute_sibling_disjointness(concepts, hierarchy_edges):
    children_map = defaultdict(set)
    for child, parent in hierarchy_edges:
        children_map[parent].add(child)
    seen = set(); pairs = []
    for parent, children in children_map.items():
        cl = sorted(children)
        for c1,c2 in combinations(cl,2):
            if (c1,c2) not in seen:
                seen.add((c1,c2)); pairs.append((c1,c2))
    return sorted(pairs)

def generate_tptp(concepts, hierarchy_edges, disjointness, code_map,
                  scope, filename, sibling_disj=False, skip_una=False):
    cs = sorted(concepts)
    hs = sorted(hierarchy_edges)
    n_una = 0 if skip_una else len(cs)*(len(cs)-1)//2
    n_formulae = len(cs)+len(hs)+len(disjointness)+n_una

    children_map = defaultdict(set); parents_map = defaultdict(set)
    for c,p in hs: children_map[p].add(c); parents_map[c].add(p)
    leaves = sorted([c for c in cs if not children_map[c]])
    roots = sorted([c for c in cs if not parents_map[c]])
    internal = len(cs)-len(leaves)-len(roots)
    br = [len(children_map[c]) for c in cs if children_map[c]]
    avg_b = sum(br)/len(br) if br else 0; max_b = max(br) if br else 0

    memo={}
    def md(n):
        if n in memo: return memo[n]
        if not parents_map[n]: memo[n]=0; return 0
        memo[n]=1+max(md(p) for p in parents_map[n]); return memo[n]
    for c in cs: md(c)
    max_d = max(memo.values()) if memo else 0

    n_pred = 2 if not disjointness else 3
    pred_str = "concept/1; leq/2" + ("; disjoint/2" if disjointness else "")
    scope_desc = "Full UN M49" if scope=="full" else f"UN M49 — {scope.title()} subset"

    L = []
    L.append("%--------------------------------------------------------------------------")
    L.append(f"% File     : {filename} : TPTP v0.1.0. Released v0.1.0.")
    L.append(f"% Domain   : UN M49 Geographic Regions — {scope_desc}")
    L.append(f"% Axioms   : Containment hierarchy (mereological)")
    L.append(f"% Version  : Generated from UN M49 standard.")
    L.append(f"% English  : UN M49 encoded as TPTP Layer 0 mereological KB.")
    if skip_una:
        L.append(f"%            UNA is implicit from tree + sibling disjointness.")
    else:
        L.append(f"%            Includes UNA for all concept pairs.")
    L.append(f"% Refs     : [MuS25] Mustafa, D. & Sutcliffe, G. (2025),")
    L.append(f"%            Automated Reasoning for ODRL Policy Conflict Detection")
    L.append(f"% Source   : https://unstats.un.org/unsd/methodology/m49/")
    L.append(f"% Names    : {filename}")
    L.append(f"% Status   : Layer 0 — Domain Knowledge Base")
    L.append(f"% Syntax   : Number of formulae    : {n_formulae:>5} ({n_formulae:>5} unt;   0 def)")
    L.append(f"%            Number of atoms       : {n_formulae:>5} ({n_una:>5} equ)")
    L.append(f"%            Maximal formula atoms  :     1 (   1 avg)")
    L.append(f"%            Number of connectives  :     0 (   0   ~;   0   |;   0   &)")
    L.append(f"%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)")
    L.append(f"%            Maximal formula depth  :     1 (   1 avg)")
    L.append(f"%            Maximal term depth     :     1 (   1 avg)")
    L.append(f"%            Number of predicates   : {n_pred:>5} ({n_pred:>5} usr;   0 prp; 1-2 aty)")
    L.append(f"%            Number of functors     : {len(cs):>5} ({len(cs):>5} usr; {len(cs):>3} con; 0-0 aty)")
    L.append(f"%            Number of variables    :     0 (   0   !;   0   ?)")
    L.append(f"% SPC      : FOF_EPR_RFN_NEQ")
    L.append(f"% Comments : All formulae are ground unit clauses.")
    L.append(f"%          : Layer 1 provides reflexivity + transitivity of leq/2.")
    if skip_una:
        L.append(f"%          : UNA: IMPLICIT — tree + sibling disjointness (Implicit UNA Lemma).")
    L.append(f"%          : Root: {', '.join(roots)}")
    L.append(f"% Ontology : Predicates: {pred_str}")
    L.append(f"%          : Relation: leq/2 — geographic containment (paper Def. 2, ≤ = ⪯)")
    L.append(f"% Stats    : Concepts {len(cs)} | Edges {len(hs)} | Disjoint {len(disjointness)} | UNA {n_una} | Total {n_formulae}")
    L.append(f"%          : Depth {max_d} | Leaves {len(leaves)} | Internal {internal} | Branch avg {avg_b:.1f} max {max_b}")
    L.append(f"% Date     : {date.today().isoformat()}")
    L.append(f"% Authors  : Mustafa, D. & Sutcliffe, G.")
    L.append(f"% Gen      : gen_layer0_geo.py from UN M49 (Dec 2021)")
    L.append("%--------------------------------------------------------------------------")

    L.append("")
    L.append("% ─── Concept membership (Definition 2: C) ─────────────────────────────")
    for c in cs:
        L.append(f"fof(c_{c}, axiom, concept({c})).  % {code_map.get(c,'')}")

    L.append("")
    L.append("% ─── Hierarchy (Definition 2: ≤ = ⪯ containment) ──────────────────────")
    L.append("% Only direct edges. Layer 1 provides reflexivity + transitivity.")
    for i,(ch,pa) in enumerate(hs):
        L.append(f"fof(h_{i:04d}, axiom, leq({ch}, {pa})).")

    L.append("")
    L.append("% ─── Disjointness (Definition 2: ⊥⊥) ─────────────────────────────────")
    if sibling_disj:
        L.append("% Sibling disjointness: children of the same parent are disjoint.")
        L.append("% Derived disjointness follows from disj_downward (Layer 1).")
    if disjointness:
        for i,(c1,c2) in enumerate(disjointness):
            L.append(f"fof(d_{i:04d}, axiom, disjoint({c1}, {c2})).")
    else:
        L.append("% (none)")

    L.append("")
    una_count = 0
    if skip_una:
        L.append("% ─── Unique Name Assumption ───────────────────────────────────────────")
        L.append("% SKIPPED (--no-una): UNA is implicit from tree structure + sibling")
        L.append("% disjointness. All constants are provably distinct via:")
        L.append("%   - leq antisymmetry + disj_downward + disj_irrefl")
    else:
        L.append("% ─── Unique Name Assumption ───────────────────────────────────────────")
        L.append(f"% C({len(cs)},2) = {n_una} pairwise distinctness axioms.")
        for c1,c2 in combinations(cs,2):
            L.append(f"fof(una_{una_count:04d}, axiom, {c1} != {c2}).")
            una_count += 1

    L.append("")
    L.append("%--------------------------------------------------------------------------")
    total = len(cs)+len(hs)+len(disjointness)+una_count
    L.append(f"% Summary: {len(cs)} concept + {len(hs)} leq + {len(disjointness)} disjoint + {una_count} UNA = {total} axioms")
    L.append("%--------------------------------------------------------------------------")
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser(description="Generate TPTP Layer 0 from UN M49.")
    ap.add_argument("-o","--output", required=True)
    ap.add_argument("-s","--scope", default="full",
        choices=["full","europe","africa","americas","asia","oceania"])
    ap.add_argument("--sibling-disjointness", action="store_true")
    ap.add_argument("--no-una", action="store_true",
        help="Skip UNA axioms (implicit from tree + disjointness)")
    args = ap.parse_args()

    hierarchy = filter_scope(M49_HIERARCHY, args.scope)
    print(f"Scope: {args.scope} → {len(hierarchy)} entries", file=sys.stderr)

    concepts = set(); hierarchy_edges = []; code_map = {}; code_to_tptp = {}
    type_labels = {0:"global",1:"region",2:"sub-region",3:"intermediate",4:"country"}
    for code,name,typ,parent in hierarchy:
        t = name_to_tptp(name); concepts.add(t); code_to_tptp[code] = t
        code_map[t] = f"M49:{code} {name} [{type_labels.get(typ,'?')}]"
    for code,name,typ,parent in hierarchy:
        if parent and parent in code_to_tptp:
            hierarchy_edges.append((code_to_tptp[code], code_to_tptp[parent]))

    # Check collisions
    nc = defaultdict(list)
    for code,name,typ,parent in hierarchy: nc[name_to_tptp(name)].append((code,name))
    collisions = {k:v for k,v in nc.items() if len(v)>1}
    if collisions:
        print(f"WARNING: name collisions: {collisions}", file=sys.stderr)
        for code,name,typ,parent in hierarchy:
            t = name_to_tptp(name)
            if t in collisions: code_to_tptp[code] = f"{t}M{code}"
        concepts = set(code_to_tptp.values())
        hierarchy_edges = []; code_map = {}
        for code,name,typ,parent in hierarchy:
            t = code_to_tptp[code]
            code_map[t] = f"M49:{code} {name} [{type_labels.get(typ,'?')}]"
            if parent and parent in code_to_tptp:
                hierarchy_edges.append((t, code_to_tptp[parent]))

    disjointness = []
    if args.sibling_disjointness:
        disjointness = compute_sibling_disjointness(concepts, hierarchy_edges)
        print(f"  {len(disjointness)} sibling disjointness pairs", file=sys.stderr)

    filename = Path(args.output).name
    tptp = generate_tptp(concepts, hierarchy_edges, disjointness, code_map,
                         args.scope, filename, sibling_disj=args.sibling_disjointness,
                         skip_una=args.no_una)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f: f.write(tptp + "\n")

    una_count = 0 if args.no_una else len(concepts)*(len(concepts)-1)//2
    total = len(concepts)+len(hierarchy_edges)+len(disjointness)+una_count
    saved = len(concepts)*(len(concepts)-1)//2 if args.no_una else 0
    print(f"\nWritten: {args.output}", file=sys.stderr)
    print(f"  {len(concepts)} concepts, {len(hierarchy_edges)} leq, "
          f"{len(disjointness)} disjoint, {una_count} UNA = {total} axioms", file=sys.stderr)
    if saved: print(f"  (--no-una saved {saved} axioms)", file=sys.stderr)

if __name__ == "__main__":
    main()
