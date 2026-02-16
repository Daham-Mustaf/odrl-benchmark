#!/usr/bin/env python3
"""
gen_layer0_geo.py — Generate TPTP Layer 0 axiom files for geographic KBs.

Supports multiple profiles for different use cases:

  curated    ~24 concepts, depth 4. Combines UN M49 regions (levels 0–2)
             with countries (level 3) and illustrative sub-national divisions
             modelled after Eurostat NUTS 2021 (levels 3–4).
             Designed for ODRL policy conflict test problems.

  iso3166    Flat 2-level KB: europe → EU27 countries (ISO 3166-1 alpha-2).
             Alignment target for cross-dataspace tests.

  m49-europe Full UN M49 Europe subset (~58 concepts, depth 3).
  m49-full   Full UN M49 world (~279 concepts).

Usage:
    # Primary test KB
    uv run python gen_layer0_geo.py -o Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax \
        -p curated --sibling-disjointness --use-distinct

    # Alignment target + bridge axioms (one command)
    uv run python gen_layer0_geo.py -o Problems/ODRL/Axioms/Layer0-DomainKB/ISO3166-0.ax \
        -p iso3166 --use-distinct \
        --emit-alignment Problems/ODRL/Axioms/Alignment/ALIGN-GEO-ISO.ax

Sources:
    [1] UN M49 — Standard Country or Area Codes for Statistical Use:
        https://unstats.un.org/unsd/methodology/m49/
    [2] ISO 3166-1:2020 — Country codes (alpha-2):
        https://www.iso.org/iso-3166-country-codes.html
    [3] Eurostat NUTS 2021 — Nomenclature of Territorial Units for Statistics:
        https://ec.europa.eu/eurostat/web/nuts/overview
"""
import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path

# =============================================================================
# Profile: curated
#
# Combines UN M49 regions (levels 0–2) with illustrative sub-national
# divisions modelled after Eurostat NUTS 2021.  Designed for manageable
# test problems that exercise depth-4 subsumption chains and cross-region
# conflict detection.
#
# Hierarchy:
#   europe (M49:150)
#   ├── westernEurope (M49:155)
#   │   ├── france (M49:250)
#   │   │   ├── ileDeFrance (NUTS:FR1)
#   │   │   │   └── paris (NUTS:FR101)
#   │   │   └── provence (NUTS:FRL)
#   │   │       └── marseille (NUTS:FRL04)
#   │   └── germany (M49:276)
#   │       ├── bavaria (NUTS:DE2)
#   │       │   └── munich (NUTS:DE212)
#   │       └── northRhineWestphalia (NUTS:DEA)
#   │           └── cologne (NUTS:DEA23)
#   ├── easternEurope (M49:151)
#   │   └── poland (M49:616)
#   │       └── masovia (NUTS:PL9)
#   │           └── warsaw (NUTS:PL911)
#   ├── southernEurope (M49:039)
#   │   ├── italy (M49:380)
#   │   │   └── lombardy (NUTS:ITC4)
#   │   │       └── milan (NUTS:ITC4C)
#   │   └── spain (M49:724)
#   │       └── catalonia (NUTS:ES51)
#   │           └── barcelona (NUTS:ES511)
#   └── northernEurope (M49:154)
#
# Format: (id, label, parent_id, source)
# =============================================================================
CURATED_HIERARCHY = [
    # Level 0: root
    ("europe",           "Europe",                       None,               "M49:150"),
    # Level 1: M49 sub-regions
    ("westernEurope",    "Western Europe",               "europe",           "M49:155"),
    ("easternEurope",    "Eastern Europe",               "europe",           "M49:151"),
    ("southernEurope",   "Southern Europe",              "europe",           "M49:039"),
    ("northernEurope",   "Northern Europe",              "europe",           "M49:154"),
    # Level 2: countries (M49 codes)
    ("france",           "France",                       "westernEurope",    "M49:250"),
    ("germany",          "Germany",                      "westernEurope",    "M49:276"),
    ("poland",           "Poland",                       "easternEurope",    "M49:616"),
    ("italy",            "Italy",                        "southernEurope",   "M49:380"),
    ("spain",            "Spain",                        "southernEurope",   "M49:724"),
    # Level 3: NUTS-1 regions (illustrative)
    ("ileDeFrance",      "Île-de-France",                "france",           "NUTS:FR1"),
    ("provence",         "Provence-Alpes-Côte d'Azur",   "france",           "NUTS:FRL"),
    ("bavaria",          "Bavaria",                      "germany",          "NUTS:DE2"),
    ("northRhineWestphalia", "North Rhine-Westphalia",   "germany",          "NUTS:DEA"),
    ("masovia",          "Masovia",                      "poland",           "NUTS:PL9"),
    ("lombardy",         "Lombardy",                     "italy",            "NUTS:ITC4"),
    ("catalonia",        "Catalonia",                    "spain",            "NUTS:ES51"),
    # Level 4: NUTS-2/3 cities (illustrative)
    ("paris",            "Paris",                        "ileDeFrance",      "NUTS:FR101"),
    ("marseille",        "Marseille",                    "provence",         "NUTS:FRL04"),
    ("munich",           "Munich",                       "bavaria",          "NUTS:DE212"),
    ("cologne",          "Cologne",                      "northRhineWestphalia", "NUTS:DEA23"),
    ("warsaw",           "Warsaw",                       "masovia",          "NUTS:PL911"),
    ("milan",            "Milan",                        "lombardy",         "NUTS:ITC4C"),
    ("barcelona",        "Barcelona",                    "catalonia",        "NUTS:ES511"),
]

# =============================================================================
# Profile: iso3166  —  ISO 3166-1 alpha-2 codes for EU27
# =============================================================================
ISO3166_COUNTRIES = [
    ("AT", "Austria"),  ("BE", "Belgium"),  ("BG", "Bulgaria"),
    ("HR", "Croatia"),  ("CY", "Cyprus"),   ("CZ", "Czechia"),
    ("DK", "Denmark"),  ("EE", "Estonia"),  ("FI", "Finland"),
    ("FR", "France"),   ("DE", "Germany"),  ("GR", "Greece"),
    ("HU", "Hungary"),  ("IE", "Ireland"),  ("IT", "Italy"),
    ("LV", "Latvia"),   ("LT", "Lithuania"),("LU", "Luxembourg"),
    ("MT", "Malta"),    ("NL", "Netherlands"), ("PL", "Poland"),
    ("PT", "Portugal"), ("RO", "Romania"),  ("SK", "Slovakia"),
    ("SI", "Slovenia"), ("ES", "Spain"),    ("SE", "Sweden"),
]

# =============================================================================
# Profile: m49-europe / m49-full  —  UN M49 hierarchy (Dec 2021)
# Format: (code, name, type, parent_code)
#   type: 0=global, 1=region, 2=sub-region, 3=intermediate, 4=country
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
    ("012", "Algeria", 4, "015"), ("818", "Egypt", 4, "015"),
    ("434", "Libya", 4, "015"), ("504", "Morocco", 4, "015"),
    ("736", "Sudan", 4, "015"), ("788", "Tunisia", 4, "015"),
    ("732", "Western Sahara", 4, "015"),
    ("086", "British Indian Ocean Territory", 4, "014"),
    ("108", "Burundi", 4, "014"), ("174", "Comoros", 4, "014"),
    ("262", "Djibouti", 4, "014"), ("232", "Eritrea", 4, "014"),
    ("231", "Ethiopia", 4, "014"),
    ("260", "French Southern Territories", 4, "014"),
    ("404", "Kenya", 4, "014"), ("450", "Madagascar", 4, "014"),
    ("454", "Malawi", 4, "014"), ("480", "Mauritius", 4, "014"),
    ("175", "Mayotte", 4, "014"), ("508", "Mozambique", 4, "014"),
    ("638", "Reunion", 4, "014"), ("646", "Rwanda", 4, "014"),
    ("690", "Seychelles", 4, "014"), ("706", "Somalia", 4, "014"),
    ("728", "South Sudan", 4, "014"), ("800", "Uganda", 4, "014"),
    ("834", "United Republic of Tanzania", 4, "014"),
    ("894", "Zambia", 4, "014"), ("716", "Zimbabwe", 4, "014"),
    ("024", "Angola", 4, "017"), ("120", "Cameroon", 4, "017"),
    ("140", "Central African Republic", 4, "017"),
    ("148", "Chad", 4, "017"), ("178", "Congo", 4, "017"),
    ("180", "Democratic Republic of the Congo", 4, "017"),
    ("226", "Equatorial Guinea", 4, "017"), ("266", "Gabon", 4, "017"),
    ("678", "Sao Tome and Principe", 4, "017"),
    ("072", "Botswana", 4, "018"), ("748", "Eswatini", 4, "018"),
    ("426", "Lesotho", 4, "018"), ("516", "Namibia", 4, "018"),
    ("710", "South Africa", 4, "018"),
    ("204", "Benin", 4, "011"), ("854", "Burkina Faso", 4, "011"),
    ("132", "Cabo Verde", 4, "011"), ("384", "Cote d'Ivoire", 4, "011"),
    ("270", "Gambia", 4, "011"), ("288", "Ghana", 4, "011"),
    ("324", "Guinea", 4, "011"), ("624", "Guinea-Bissau", 4, "011"),
    ("430", "Liberia", 4, "011"), ("466", "Mali", 4, "011"),
    ("478", "Mauritania", 4, "011"), ("562", "Niger", 4, "011"),
    ("566", "Nigeria", 4, "011"), ("654", "Saint Helena", 4, "011"),
    ("686", "Senegal", 4, "011"), ("694", "Sierra Leone", 4, "011"),
    ("768", "Togo", 4, "011"),
    ("660", "Anguilla", 4, "029"),
    ("028", "Antigua and Barbuda", 4, "029"),
    ("533", "Aruba", 4, "029"), ("044", "Bahamas", 4, "029"),
    ("052", "Barbados", 4, "029"),
    ("535", "Bonaire Sint Eustatius and Saba", 4, "029"),
    ("092", "British Virgin Islands", 4, "029"),
    ("136", "Cayman Islands", 4, "029"), ("192", "Cuba", 4, "029"),
    ("531", "Curacao", 4, "029"), ("212", "Dominica", 4, "029"),
    ("214", "Dominican Republic", 4, "029"),
    ("308", "Grenada", 4, "029"), ("312", "Guadeloupe", 4, "029"),
    ("332", "Haiti", 4, "029"), ("388", "Jamaica", 4, "029"),
    ("474", "Martinique", 4, "029"), ("500", "Montserrat", 4, "029"),
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
    ("084", "Belize", 4, "013"), ("188", "Costa Rica", 4, "013"),
    ("222", "El Salvador", 4, "013"), ("320", "Guatemala", 4, "013"),
    ("340", "Honduras", 4, "013"), ("484", "Mexico", 4, "013"),
    ("558", "Nicaragua", 4, "013"), ("591", "Panama", 4, "013"),
    ("032", "Argentina", 4, "005"), ("068", "Bolivia", 4, "005"),
    ("074", "Bouvet Island", 4, "005"), ("076", "Brazil", 4, "005"),
    ("152", "Chile", 4, "005"), ("170", "Colombia", 4, "005"),
    ("218", "Ecuador", 4, "005"),
    ("238", "Falkland Islands (Malvinas)", 4, "005"),
    ("254", "French Guiana", 4, "005"), ("328", "Guyana", 4, "005"),
    ("600", "Paraguay", 4, "005"), ("604", "Peru", 4, "005"),
    ("239", "South Georgia and the South Sandwich Islands", 4, "005"),
    ("740", "Suriname", 4, "005"), ("858", "Uruguay", 4, "005"),
    ("862", "Venezuela", 4, "005"),
    ("060", "Bermuda", 4, "021"), ("124", "Canada", 4, "021"),
    ("304", "Greenland", 4, "021"),
    ("666", "Saint Pierre and Miquelon", 4, "021"),
    ("840", "United States of America", 4, "021"),
    ("398", "Kazakhstan", 4, "143"), ("417", "Kyrgyzstan", 4, "143"),
    ("762", "Tajikistan", 4, "143"), ("795", "Turkmenistan", 4, "143"),
    ("860", "Uzbekistan", 4, "143"),
    ("156", "China", 4, "030"),
    ("344", "China Hong Kong SAR", 4, "030"),
    ("446", "China Macao SAR", 4, "030"),
    ("408", "Dem. Peoples Republic of Korea", 4, "030"),
    ("392", "Japan", 4, "030"), ("496", "Mongolia", 4, "030"),
    ("410", "Republic of Korea", 4, "030"),
    ("096", "Brunei Darussalam", 4, "035"),
    ("116", "Cambodia", 4, "035"), ("360", "Indonesia", 4, "035"),
    ("418", "Lao Peoples Dem. Republic", 4, "035"),
    ("458", "Malaysia", 4, "035"), ("104", "Myanmar", 4, "035"),
    ("608", "Philippines", 4, "035"), ("702", "Singapore", 4, "035"),
    ("764", "Thailand", 4, "035"), ("626", "Timor-Leste", 4, "035"),
    ("704", "Viet Nam", 4, "035"),
    ("004", "Afghanistan", 4, "034"), ("050", "Bangladesh", 4, "034"),
    ("064", "Bhutan", 4, "034"), ("356", "India", 4, "034"),
    ("364", "Iran", 4, "034"), ("462", "Maldives", 4, "034"),
    ("524", "Nepal", 4, "034"), ("586", "Pakistan", 4, "034"),
    ("144", "Sri Lanka", 4, "034"),
    ("051", "Armenia", 4, "145"), ("031", "Azerbaijan", 4, "145"),
    ("048", "Bahrain", 4, "145"), ("196", "Cyprus", 4, "145"),
    ("268", "Georgia", 4, "145"), ("368", "Iraq", 4, "145"),
    ("376", "Israel", 4, "145"), ("400", "Jordan", 4, "145"),
    ("414", "Kuwait", 4, "145"), ("422", "Lebanon", 4, "145"),
    ("512", "Oman", 4, "145"), ("634", "Qatar", 4, "145"),
    ("682", "Saudi Arabia", 4, "145"),
    ("275", "State of Palestine", 4, "145"),
    ("760", "Syrian Arab Republic", 4, "145"),
    ("792", "Turkey", 4, "145"),
    ("784", "United Arab Emirates", 4, "145"),
    ("887", "Yemen", 4, "145"),
    ("112", "Belarus", 4, "151"), ("100", "Bulgaria", 4, "151"),
    ("203", "Czechia", 4, "151"), ("348", "Hungary", 4, "151"),
    ("616", "Poland", 4, "151"),
    ("498", "Republic of Moldova", 4, "151"),
    ("642", "Romania", 4, "151"),
    ("643", "Russian Federation", 4, "151"),
    ("703", "Slovakia", 4, "151"), ("804", "Ukraine", 4, "151"),
    ("248", "Aland Islands", 4, "154"), ("208", "Denmark", 4, "154"),
    ("233", "Estonia", 4, "154"), ("234", "Faroe Islands", 4, "154"),
    ("246", "Finland", 4, "154"), ("352", "Iceland", 4, "154"),
    ("372", "Ireland", 4, "154"), ("833", "Isle of Man", 4, "154"),
    ("428", "Latvia", 4, "154"), ("440", "Lithuania", 4, "154"),
    ("578", "Norway", 4, "154"),
    ("744", "Svalbard and Jan Mayen Islands", 4, "154"),
    ("752", "Sweden", 4, "154"), ("826", "United Kingdom", 4, "154"),
    ("831", "Guernsey", 4, "830"), ("832", "Jersey", 4, "830"),
    ("680", "Sark", 4, "830"),
    ("008", "Albania", 4, "039"), ("020", "Andorra", 4, "039"),
    ("070", "Bosnia and Herzegovina", 4, "039"),
    ("191", "Croatia", 4, "039"), ("292", "Gibraltar", 4, "039"),
    ("300", "Greece", 4, "039"), ("336", "Holy See", 4, "039"),
    ("380", "Italy", 4, "039"), ("470", "Malta", 4, "039"),
    ("499", "Montenegro", 4, "039"),
    ("807", "North Macedonia", 4, "039"),
    ("620", "Portugal", 4, "039"), ("674", "San Marino", 4, "039"),
    ("688", "Serbia", 4, "039"), ("705", "Slovenia", 4, "039"),
    ("724", "Spain", 4, "039"),
    ("040", "Austria", 4, "155"), ("056", "Belgium", 4, "155"),
    ("250", "France", 4, "155"), ("276", "Germany", 4, "155"),
    ("438", "Liechtenstein", 4, "155"),
    ("442", "Luxembourg", 4, "155"), ("492", "Monaco", 4, "155"),
    ("528", "Netherlands", 4, "155"),
    ("756", "Switzerland", 4, "155"),
    ("036", "Australia", 4, "053"), ("554", "New Zealand", 4, "053"),
    ("162", "Christmas Island", 4, "053"),
    ("166", "Cocos (Keeling) Islands", 4, "053"),
    ("334", "Heard Island and McDonald Islands", 4, "053"),
    ("574", "Norfolk Island", 4, "053"),
    ("242", "Fiji", 4, "054"), ("540", "New Caledonia", 4, "054"),
    ("598", "Papua New Guinea", 4, "054"),
    ("090", "Solomon Islands", 4, "054"), ("548", "Vanuatu", 4, "054"),
    ("316", "Guam", 4, "057"), ("296", "Kiribati", 4, "057"),
    ("584", "Marshall Islands", 4, "057"),
    ("583", "Micronesia (Federated States of)", 4, "057"),
    ("520", "Nauru", 4, "057"),
    ("580", "Northern Mariana Islands", 4, "057"),
    ("585", "Palau", 4, "057"),
    ("016", "American Samoa", 4, "061"),
    ("184", "Cook Islands", 4, "061"),
    ("258", "French Polynesia", 4, "061"), ("570", "Niue", 4, "061"),
    ("612", "Pitcairn", 4, "061"), ("882", "Samoa", 4, "061"),
    ("772", "Tokelau", 4, "061"), ("776", "Tonga", 4, "061"),
    ("798", "Tuvalu", 4, "061"),
    ("876", "Wallis and Futuna Islands", 4, "061"),
    ("010", "Antarctica", 4, "001"),
]

# =============================================================================
# Alignment: curated GEO → ISO 3166
# Country-level concepts map; sub-regions + sub-national do NOT (partial).
# =============================================================================
CURATED_TO_ISO3166 = {
    "europe":   "europe",
    "france":   "fR",
    "germany":  "dE",
    "poland":   "pL",
    "italy":    "iT",
    "spain":    "eS",
}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def name_to_tptp(name):
    """Convert a human name to a valid TPTP constant (lowerCamelCase)."""
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


def iso_to_tptp(code):
    """Convert ISO 3166 alpha-2 to TPTP constant (e.g., DE → dE)."""
    return code[0].lower() + code[1].upper()


def compute_sibling_disjointness(concepts, edges):
    children_map = defaultdict(set)
    for c, p in edges:
        children_map[p].add(c)
    seen = set()
    pairs = []
    for parent, children in children_map.items():
        for c1, c2 in combinations(sorted(children), 2):
            if (c1, c2) not in seen:
                seen.add((c1, c2))
                pairs.append((c1, c2))
    return sorted(pairs)


def generate_distinct_predicates(concepts, edges, prefix="geo"):
    children_map = defaultdict(set)
    for c, p in edges:
        children_map[p].add(c)
    groups = []
    for parent in sorted(children_map.keys()):
        children = sorted(children_map[parent])
        if len(children) > 1:
            groups.append((f"{prefix}_distinct_{parent}", children))
    return groups


# ─── Profile loaders ─────────────────────────────────────────────────────────

def load_curated():
    concepts = set()
    edges = []
    code_map = {}
    for cid, label, parent, source in CURATED_HIERARCHY:
        concepts.add(cid)
        code_map[cid] = f"{source} — {label}"
        if parent:
            edges.append((cid, parent))
    return concepts, edges, code_map


def load_iso3166():
    concepts = {"europe"}
    edges = []
    code_map = {"europe": "ISO 3166: Root"}
    for code, name in ISO3166_COUNTRIES:
        t = iso_to_tptp(code)
        concepts.add(t)
        code_map[t] = f"ISO 3166:{code} — {name}"
        edges.append((t, "europe"))
    return concepts, edges, code_map


def filter_m49_scope(scope):
    if scope == "full":
        return M49_HIERARCHY
    scope_roots = {
        "europe": "150", "africa": "002", "americas": "019",
        "asia": "142", "oceania": "009",
    }
    root_code = scope_roots[scope]
    children_map = defaultdict(set)
    for c, n, t, p in M49_HIERARCHY:
        if p:
            children_map[p].add(c)
    reachable = {root_code}
    queue = [root_code]
    while queue:
        cur = queue.pop(0)
        for ch in children_map.get(cur, []):
            if ch not in reachable:
                reachable.add(ch)
                queue.append(ch)
    reachable.add("001")
    result = []
    for c, n, t, p in M49_HIERARCHY:
        if c in reachable:
            if c == root_code:
                result.append((c, n, t, "001"))
            elif p in reachable:
                result.append((c, n, t, p))
    return result


def load_m49(scope):
    hierarchy = filter_m49_scope(scope)
    type_labels = {0: "global", 1: "region", 2: "sub-region",
                   3: "intermediate", 4: "country"}
    code_to_tptp_map = {}
    for code, name, typ, parent in hierarchy:
        code_to_tptp_map[code] = name_to_tptp(name)

    # Handle collisions
    nc = defaultdict(list)
    for code, name, typ, parent in hierarchy:
        nc[name_to_tptp(name)].append((code, name))
    collisions = {k: v for k, v in nc.items() if len(v) > 1}
    if collisions:
        print(f"WARNING: name collisions: {collisions}", file=sys.stderr)
        for code, name, typ, parent in hierarchy:
            t = name_to_tptp(name)
            if t in collisions:
                code_to_tptp_map[code] = f"{t}M{code}"

    concepts = set()
    edges = []
    code_map = {}
    for code, name, typ, parent in hierarchy:
        t = code_to_tptp_map[code]
        concepts.add(t)
        code_map[t] = f"M49:{code} {name} [{type_labels.get(typ, '?')}]"
        if parent and parent in code_to_tptp_map:
            edges.append((t, code_to_tptp_map[parent]))
    return concepts, edges, code_map


# ─── TPTP generation ─────────────────────────────────────────────────────────

def generate_tptp(concepts, edges, disjointness, code_map,
                  profile, filename,
                  sibling_disj=False, skip_una=False, use_distinct=False):
    cs = sorted(concepts)
    hs = sorted(edges)

    # UNA counts
    if use_distinct:
        prefix = "iso" if profile == "iso3166" else "geo"
        distinct_groups = generate_distinct_predicates(concepts, edges, prefix)
        n_una = len(distinct_groups)
        n_una_equ = 0
    elif skip_una:
        distinct_groups = []
        n_una = 0
        n_una_equ = 0
    else:
        distinct_groups = []
        n_una = len(cs) * (len(cs) - 1) // 2
        n_una_equ = n_una

    n_formulae = len(cs) + len(hs) + len(disjointness) + n_una

    # Stats
    children_map = defaultdict(set)
    parents_map = defaultdict(set)
    for c, p in hs:
        children_map[p].add(c)
        parents_map[c].add(p)
    leaves = sorted([c for c in cs if not children_map[c]])
    roots = sorted([c for c in cs if not parents_map[c]])
    internal = len(cs) - len(leaves) - len(roots)
    br = [len(children_map[c]) for c in cs if children_map[c]]
    avg_b = sum(br) / len(br) if br else 0
    max_b = max(br) if br else 0
    memo = {}
    def md(n):
        if n in memo:
            return memo[n]
        if not parents_map[n]:
            memo[n] = 0
            return 0
        memo[n] = 1 + max(md(p) for p in parents_map[n])
        return memo[n]
    for c in cs:
        md(c)
    max_d = max(memo.values()) if memo else 0

    n_pred = 2 if not disjointness else 3
    pred_str = "concept/1; leq/2" + ("; disjoint/2" if disjointness else "")

    domain_desc = {
        "curated": "Geographic Regions — Curated European Hierarchy",
        "iso3166": "ISO 3166-1 Country Codes — European Union",
        "m49-europe": "UN M49 Geographic Regions — Europe subset",
        "m49-full": "UN M49 Geographic Regions — Full",
    }
    source_desc = {
        "curated": "[1] https://unstats.un.org/unsd/methodology/m49/ (levels 0-2)\n"
                   "%            [3] https://ec.europa.eu/eurostat/web/nuts/overview (levels 3-4)",
        "iso3166": "[2] https://www.iso.org/iso-3166-country-codes.html",
        "m49-europe": "[1] https://unstats.un.org/unsd/methodology/m49/",
        "m49-full": "[1] https://unstats.un.org/unsd/methodology/m49/",
    }
    english_desc = {
        "curated": "Curated European geographic KB combining UN M49 regions\n"
                   "%            (levels 0-2) with illustrative sub-national divisions modelled\n"
                   "%            after Eurostat NUTS 2021 (levels 3-4). Designed for ODRL\n"
                   "%            policy conflict test problems requiring depth-4 subsumption.",
        "iso3166": "Flat 2-level KB: europe → country (no sub-regions).\n"
                   "%            For cross-dataspace alignment with GEO000-0.ax.",
        "m49-europe": "UN M49 Europe subset encoded as TPTP Layer 0 KB.",
        "m49-full": "Full UN M49 encoded as TPTP Layer 0 KB.",
    }

    L = []
    L.append("%--------------------------------------------------------------------------")
    L.append(f"% File     : {filename} : TPTP v0.1.0. Released v0.1.0.")
    L.append(f"% Domain   : {domain_desc.get(profile, profile)}")
    L.append(f"% Axioms   : Containment hierarchy (mereological)")
    L.append(f"% Version  : Profile: {profile}")
    L.append(f"% English  : {english_desc.get(profile, '')}")
    if use_distinct:
        L.append(f"%            UNA via $distinct — avoids clause explosion (Sutcliffe).")
    elif skip_una:
        L.append(f"%            UNA is implicit from tree + sibling disjointness.")
    L.append(f"% Refs     : [MuS25] Mustafa, D. & Sutcliffe, G. (2025),")
    L.append(f"%            Automated Reasoning for ODRL Policy Conflict Detection")
    L.append(f"% Source   : {source_desc.get(profile, '')}")
    L.append(f"% Names    : {filename}")
    L.append(f"% Status   : Layer 0 — Domain Knowledge Base")
    L.append(f"% Syntax   : Number of formulae    : {n_formulae:>5} ({n_formulae:>5} unt;   0 def)")
    L.append(f"%            Number of atoms       : {n_formulae:>5} ({n_una_equ:>5} equ)")
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
    if use_distinct:
        L.append(f"%          : UNA: $distinct groups by parent (Sutcliffe).")
    elif skip_una:
        L.append(f"%          : UNA: IMPLICIT — tree + disjointness.")
    L.append(f"%          : Root: {', '.join(roots)}")
    L.append(f"% Ontology : Predicates: {pred_str}")
    L.append(f"%          : Relation: leq/2 — geographic containment (paper Def. 2)")
    L.append(f"% Stats    : Concepts {len(cs)} | Edges {len(hs)} | Disjoint {len(disjointness)} | UNA {n_una} | Total {n_formulae}")
    L.append(f"%          : Depth {max_d} | Leaves {len(leaves)} | Internal {internal} | Branch avg {avg_b:.1f} max {max_b}")
    L.append(f"% Date     : {date.today().isoformat()}")
    L.append(f"% Authors  : Mustafa, D. & Sutcliffe, G.")
    L.append(f"% Gen      : gen_layer0_geo.py --profile {profile}")
    L.append("%--------------------------------------------------------------------------")
    L.append("")

    L.append("% ─── Concept membership (Definition 2: C) ─────────────────────────────")
    for c in cs:
        L.append(f"fof(c_{c}, axiom, concept({c})).  % {code_map.get(c, '')}")
    L.append("")

    L.append("% ─── Hierarchy (Definition 2: ≤ = containment) ────────────────────────")
    L.append("% Only direct edges. Layer 1 provides reflexivity + transitivity.")
    for i, (ch, pa) in enumerate(hs):
        L.append(f"fof(h_{i:04d}, axiom, leq({ch}, {pa})).")
    L.append("")

    L.append("% ─── Disjointness (Definition 2: ⊥⊥) ─────────────────────────────────")
    if sibling_disj:
        L.append("% Sibling disjointness: children of the same parent are disjoint.")
        L.append("% Derived disjointness follows from disj_downward (Layer 1).")
    if disjointness:
        for i, (c1, c2) in enumerate(disjointness):
            L.append(f"fof(d_{i:04d}, axiom, disjoint({c1}, {c2})).")
    else:
        L.append("% (none)")
    L.append("")

    una_count = 0
    if use_distinct:
        L.append("% ─── Unique Name Assumption (via $distinct) ──────────────────────────")
        L.append("% Geoff Sutcliffe recommendation: $distinct avoids clause explosion.")
        L.append("")
        for group_name, members in distinct_groups:
            member_str = ", ".join(members)
            if len(member_str) > 70:
                L.append(f"fof({group_name}, axiom,")
                L.append(f"    $distinct(")
                chunks = [members[i:i+8] for i in range(0, len(members), 8)]
                for j, chunk in enumerate(chunks):
                    chunk_str = ", ".join(chunk)
                    suffix = "," if j < len(chunks) - 1 else ""
                    L.append(f"        {chunk_str}{suffix}")
                L.append("    )).")
            else:
                L.append(f"fof({group_name}, axiom,")
                L.append(f"    $distinct({member_str})).")
            L.append("")
        una_count = len(distinct_groups)
    elif skip_una:
        L.append("% ─── Unique Name Assumption ───────────────────────────────────────────")
        L.append("% SKIPPED (--no-una): implicit from tree + disjointness.")
    else:
        L.append("% ─── Unique Name Assumption (pairwise !=) ────────────────────────────")
        L.append(f"% C({len(cs)},2) = {len(cs) * (len(cs) - 1) // 2} pairwise distinctness axioms.")
        for c1, c2 in combinations(cs, 2):
            L.append(f"fof(una_{una_count:04d}, axiom, {c1} != {c2}).")
            una_count += 1

    L.append("")
    L.append("%--------------------------------------------------------------------------")
    total = len(cs) + len(hs) + len(disjointness) + una_count
    L.append(f"% Summary: {len(cs)} concept + {len(hs)} leq + {len(disjointness)} disjoint + {una_count} UNA = {total} axioms")
    L.append("%--------------------------------------------------------------------------")
    return "\n".join(L)


# ─── Alignment generation ────────────────────────────────────────────────────

def generate_alignment(mapping, filename):
    n_axioms = len(mapping)
    unmapped = [c for c, _, _, _ in CURATED_HIERARCHY
                if c not in mapping]

    L = []
    L.append("%--------------------------------------------------------------------------")
    L.append(f"% File     : {filename} : TPTP v0.1.0.")
    L.append("% Domain   : KB Alignment — Curated GEO to ISO 3166-1")
    L.append("% Axioms   : Order-preserving alignment (Definition 8)")
    L.append("% Version  : Partial alignment (countries + root only)")
    L.append("% English  : Maps curated GEO (GEO000-0.ax) to ISO 3166 (ISO3166-0.ax).")
    L.append(f"%            {len(unmapped)} concepts unmapped (partial — granularity mismatch).")
    L.append("%            Tests Proposition 2: verdict preservation under alignment.")
    L.append("% Refs     : [MuS25] Mustafa, D. & Sutcliffe, G. (2025), §3.3")
    L.append(f"% Names    : {filename}")
    L.append("% Status   : Layer 0+ — Alignment Bridge")
    L.append(f"% Syntax   : Number of formulae    : {n_axioms:>5} ({n_axioms:>5} unt;   0 def)")
    L.append(f"%            Number of predicates   :     1 (   1 usr;   0 prp; 2-2 aty)")
    L.append("% Ontology : Predicate: align/2 — alignment function α: C_A → C_B")
    L.append(f"% Stats    : {n_axioms} alignment pairs (partial — {n_axioms} of {len(CURATED_HIERARCHY)} concepts)")
    L.append(f"% Date     : {date.today().isoformat()}")
    L.append("% Authors  : Mustafa, D. & Sutcliffe, G.")
    L.append("%--------------------------------------------------------------------------")
    L.append("")
    L.append("% ─── Alignment Axioms (Definition 8: α: C_A → C_B) ────────────────────")
    L.append("% align(X_geo, Y_iso3166): curated GEO concept X maps to ISO 3166 concept Y.")
    L.append("% Partial: countries + root map; sub-regions and sub-national do NOT.")
    L.append("")

    for i, (src, tgt) in enumerate(sorted(mapping.items())):
        L.append(f"fof(align_{i:04d}, axiom, align({src}, {tgt})).")

    L.append("")
    L.append("%--------------------------------------------------------------------------")
    L.append(f"% Summary: {n_axioms} alignment axioms (partial mapping)")
    L.append(f"% Unmapped ({len(unmapped)}): {', '.join(unmapped)}")
    L.append("%--------------------------------------------------------------------------")
    return "\n".join(L)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Generate TPTP Layer 0 geographic KBs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
profiles:
  curated      ~24 concepts, depth 4 (M49 + NUTS, for test problems)
  iso3166      flat EU27 (ISO 3166-1 alpha-2, alignment target)
  m49-europe   full M49 Europe (~58 concepts)
  m49-full     full M49 world (~279 concepts)
""")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("-p", "--profile", required=True,
        choices=["curated", "iso3166", "m49-europe", "m49-full"])
    ap.add_argument("--sibling-disjointness", action="store_true")

    una_group = ap.add_mutually_exclusive_group()
    una_group.add_argument("--no-una", action="store_true",
        help="Skip UNA axioms (implicit from tree + disjointness)")
    una_group.add_argument("--use-distinct", action="store_true",
        help="Use $distinct predicates (recommended by Geoff Sutcliffe)")

    ap.add_argument("--emit-alignment",
        help="Also emit alignment axioms to this path (curated → ISO 3166)")

    args = ap.parse_args()

    # Load profile
    if args.profile == "curated":
        concepts, edges, code_map = load_curated()
    elif args.profile == "iso3166":
        concepts, edges, code_map = load_iso3166()
    elif args.profile == "m49-europe":
        concepts, edges, code_map = load_m49("europe")
    elif args.profile == "m49-full":
        concepts, edges, code_map = load_m49("full")

    print(f"Profile: {args.profile} → {len(concepts)} concepts, "
          f"{len(edges)} edges", file=sys.stderr)

    # Disjointness
    disjointness = []
    if args.sibling_disjointness:
        disjointness = compute_sibling_disjointness(concepts, edges)
        print(f"  {len(disjointness)} sibling disjointness pairs",
              file=sys.stderr)

    # Generate main KB
    filename = Path(args.output).name
    tptp = generate_tptp(
        concepts, edges, disjointness, code_map,
        args.profile, filename,
        sibling_disj=args.sibling_disjointness,
        skip_una=args.no_una, use_distinct=args.use_distinct)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        f.write(tptp + "\n")

    # Stats
    if args.use_distinct:
        prefix = "iso" if args.profile == "iso3166" else "geo"
        distinct_groups = generate_distinct_predicates(concepts, edges, prefix)
        una_count = len(distinct_groups)
        pairwise_equiv = sum(len(m) * (len(m) - 1) // 2
                             for _, m in distinct_groups)
    elif args.no_una:
        una_count = 0
        pairwise_equiv = 0
    else:
        una_count = len(concepts) * (len(concepts) - 1) // 2
        pairwise_equiv = una_count

    total = len(concepts) + len(edges) + len(disjointness) + una_count
    print(f"\nWritten: {args.output}", file=sys.stderr)
    print(f"  {len(concepts)} concepts, {len(edges)} leq, "
          f"{len(disjointness)} disjoint, {una_count} UNA = {total} axioms",
          file=sys.stderr)
    if args.use_distinct:
        saved = len(concepts) * (len(concepts) - 1) // 2 - una_count
        print(f"  ($distinct: {una_count} groups ≡ {pairwise_equiv} "
              f"pairwise; saved {saved} axioms)", file=sys.stderr)

    # Emit alignment if requested
    if args.emit_alignment:
        align_filename = Path(args.emit_alignment).name
        align_tptp = generate_alignment(CURATED_TO_ISO3166, align_filename)
        Path(args.emit_alignment).parent.mkdir(parents=True, exist_ok=True)
        with open(args.emit_alignment, "w") as f:
            f.write(align_tptp + "\n")
        print(f"\nAlignment: {args.emit_alignment}", file=sys.stderr)
        print(f"  {len(CURATED_TO_ISO3166)} alignment pairs "
              f"({len(CURATED_HIERARCHY) - len(CURATED_TO_ISO3166)} unmapped)",
              file=sys.stderr)


if __name__ == "__main__":
    main()