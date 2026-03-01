"""
grounding/geo.py — Geographic Hierarchy loaders → Hierarchy.

All TPTP generation is in encoding/tptp.py.
All data stays here as plain Python constants.
"""
from __future__ import annotations
import re
import sys
from collections import defaultdict
from .hierarchy import Hierarchy

# ── Raw data ──────────────────────────────────────────────────────────────────
# Format: (tptp_id, label, parent_id | None, source_citation)
_CURATED = [
    ("europe",               "Europe",                     None,             "M49:150"),
    ("westernEurope",        "Western Europe",             "europe",         "M49:155"),
    ("easternEurope",        "Eastern Europe",             "europe",         "M49:151"),
    ("southernEurope",       "Southern Europe",            "europe",         "M49:039"),
    ("northernEurope",       "Northern Europe",            "europe",         "M49:154"),
    ("france",               "France",                     "westernEurope",  "M49:250"),
    ("germany",              "Germany",                    "westernEurope",  "M49:276"),
    ("poland",               "Poland",                     "easternEurope",  "M49:616"),
    ("italy",                "Italy",                      "southernEurope", "M49:380"),
    ("spain",                "Spain",                      "southernEurope", "M49:724"),
    ("ileDeFrance",          "Île-de-France",              "france",         "NUTS:FR1"),
    ("provence",             "Provence-Alpes-Côte d'Azur", "france",         "NUTS:FRL"),
    ("bavaria",              "Bavaria",                    "germany",        "NUTS:DE2"),
    ("northRhineWestphalia", "North Rhine-Westphalia",     "germany",        "NUTS:DEA"),
    ("masovia",              "Masovia",                    "poland",         "NUTS:PL9"),
    ("lombardy",             "Lombardy",                   "italy",          "NUTS:ITC4"),
    ("catalonia",            "Catalonia",                  "spain",          "NUTS:ES51"),
    ("paris",                "Paris",                      "ileDeFrance",    "NUTS:FR101"),
    ("marseille",            "Marseille",                  "provence",       "NUTS:FRL04"),
    ("munich",               "Munich",                     "bavaria",        "NUTS:DE212"),
    ("cologne",              "Cologne",                    "northRhineWestphalia", "NUTS:DEA23"),
    ("warsaw",               "Warsaw",                     "masovia",        "NUTS:PL911"),
    ("milan",                "Milan",                      "lombardy",       "NUTS:ITC4C"),
    ("barcelona",            "Barcelona",                  "catalonia",      "NUTS:ES511"),
]

# ISO 3166-1 alpha-2, EU27
_ISO3166_EU27 = [
    ("AT","Austria"),  ("BE","Belgium"),   ("BG","Bulgaria"), ("HR","Croatia"),
    ("CY","Cyprus"),   ("CZ","Czechia"),   ("DK","Denmark"),  ("EE","Estonia"),
    ("FI","Finland"),  ("FR","France"),    ("DE","Germany"),  ("GR","Greece"),
    ("HU","Hungary"),  ("IE","Ireland"),   ("IT","Italy"),    ("LV","Latvia"),
    ("LT","Lithuania"),("LU","Luxembourg"),("MT","Malta"),    ("NL","Netherlands"),
    ("PL","Poland"),   ("PT","Portugal"),  ("RO","Romania"),  ("SK","Slovakia"),
    ("SI","Slovenia"), ("ES","Spain"),     ("SE","Sweden"),
]

# UN M49 — abridged to Europe for default use; extend as needed
# Format: (code, name, type_int, parent_code | None)
_M49_EUROPE_ROOT = "150"
_M49 = [
    ("001","World",0,None),
    ("002","Africa",1,"001"), ("019","Americas",1,"001"), ("142","Asia",1,"001"),
    ("150","Europe",1,"001"), ("009","Oceania",1,"001"),
    ("151","Eastern Europe",2,"150"), ("154","Northern Europe",2,"150"),
    ("039","Southern Europe",2,"150"), ("155","Western Europe",2,"150"),
    ("830","Channel Islands",3,"154"),
    ("112","Belarus",4,"151"),    ("100","Bulgaria",4,"151"),
    ("203","Czechia",4,"151"),    ("348","Hungary",4,"151"),
    ("616","Poland",4,"151"),     ("498","Republic of Moldova",4,"151"),
    ("642","Romania",4,"151"),    ("643","Russian Federation",4,"151"),
    ("703","Slovakia",4,"151"),   ("804","Ukraine",4,"151"),
    ("248","Aland Islands",4,"154"),("208","Denmark",4,"154"),
    ("233","Estonia",4,"154"),    ("246","Finland",4,"154"),
    ("352","Iceland",4,"154"),    ("372","Ireland",4,"154"),
    ("428","Latvia",4,"154"),     ("440","Lithuania",4,"154"),
    ("578","Norway",4,"154"),     ("752","Sweden",4,"154"),
    ("826","United Kingdom",4,"154"),
    ("831","Guernsey",4,"830"),   ("832","Jersey",4,"830"),
    ("008","Albania",4,"039"),    ("070","Bosnia and Herzegovina",4,"039"),
    ("191","Croatia",4,"039"),    ("300","Greece",4,"039"),
    ("380","Italy",4,"039"),      ("470","Malta",4,"039"),
    ("499","Montenegro",4,"039"), ("807","North Macedonia",4,"039"),
    ("620","Portugal",4,"039"),   ("688","Serbia",4,"039"),
    ("705","Slovenia",4,"039"),   ("724","Spain",4,"039"),
    ("040","Austria",4,"155"),    ("056","Belgium",4,"155"),
    ("250","France",4,"155"),     ("276","Germany",4,"155"),
    ("438","Liechtenstein",4,"155"),("442","Luxembourg",4,"155"),
    ("492","Monaco",4,"155"),     ("528","Netherlands",4,"155"),
    ("756","Switzerland",4,"155"),
]

# Alignment: curated GEO → ISO 3166 (partial — countries + root only)
CURATED_TO_ISO3166 = {
    "europe":  "europe",
    "france":  "fR",
    "germany": "dE",
    "poland":  "pL",
    "italy":   "iT",
    "spain":   "eS",
}

# ── Name helpers ──────────────────────────────────────────────────────────────

def _iso_to_tptp(code: str) -> str:
    """DE → dE, FR → fR, etc."""
    return code[0].lower() + code[1].upper()

def _m49_name_to_tptp(name: str) -> str:
    name = re.sub(r'\(.*?\)', '', name).strip()
    parts = re.split(r"[\s\-']+", name)
    parts = [p for p in parts if p]
    if not parts:
        return "unknown"
    result = parts[0].lower()
    for p in parts[1:]:
        result += (p[0].upper() + p[1:].lower()) if len(p) > 1 else p.upper()
    result = re.sub(r'[^a-zA-Z0-9_]', '', result)
    if result and not result[0].isalpha():
        result = "r_" + result
    if result and result[0].isupper():
        result = result[0].lower() + result[1:]
    return result

# ── Public loaders ────────────────────────────────────────────────────────────

def load_curated() -> Hierarchy:
    h = Hierarchy(
        name    = "Geographic Regions — Curated European Hierarchy",
        source  = "[1] https://unstats.un.org/unsd/methodology/m49/ (levels 0-2)\n"
                  "%            [3] https://ec.europa.eu/eurostat/web/nuts/overview (levels 3-4)",
        domain  = "mereological",
        profile = "curated",
    )
    for cid, label, parent, source in _CURATED:
        h.concepts.add(cid)
        h.grounding[cid] = f"{source} — {label}"
        if parent:
            h.edges.append((cid, parent))
    return h


def load_iso3166() -> Hierarchy:
    h = Hierarchy(
        name    = "ISO 3166-1 Country Codes — European Union",
        source  = "[2] https://www.iso.org/iso-3166-country-codes.html",
        domain  = "mereological",
        profile = "iso3166",
    )
    h.concepts.add("europe")
    h.grounding["europe"] = "ISO 3166: Root"
    for code, label in _ISO3166_EU27:
        t = _iso_to_tptp(code)
        h.concepts.add(t)
        h.grounding[t] = f"ISO 3166:{code} — {label}"
        h.edges.append((t, "europe"))
    return h


def load_m49(scope: str = "europe") -> Hierarchy:
    """scope: 'europe' (default) | 'full'"""
    if scope == "full":
        rows = _M49
    else:
        # BFS from Europe root
        children_map: dict = defaultdict(set)
        for code, _, _, parent in _M49:
            if parent:
                children_map[parent].add(code)
        reachable = {_M49_EUROPE_ROOT, "001"}
        queue = [_M49_EUROPE_ROOT]
        while queue:
            cur = queue.pop(0)
            for ch in children_map.get(cur, []):
                if ch not in reachable:
                    reachable.add(ch)
                    queue.append(ch)
        rows = [(c,n,t,p) for c,n,t,p in _M49 if c in reachable]

    # Detect name collisions
    from collections import Counter
    name_counts = Counter(_m49_name_to_tptp(n) for _,n,_,_ in rows)
    collisions  = {k for k,v in name_counts.items() if v > 1}

    code_to_tptp: dict[str,str] = {}
    for code, name, _, _ in rows:
        t = _m49_name_to_tptp(name)
        code_to_tptp[code] = f"{t}M{code}" if t in collisions else t

    if collisions:
        print(f"WARNING: M49 name collisions resolved: {collisions}", file=__import__('sys').stderr)

    type_labels = {0:"global", 1:"region", 2:"sub-region", 3:"intermediate", 4:"country"}
    h = Hierarchy(
        name    = f"UN M49 Geographic Regions — {scope.capitalize()}",
        source  = "[1] https://unstats.un.org/unsd/methodology/m49/",
        domain  = "mereological",
        profile = f"m49-{scope}",
    )
    for code, name, typ, parent in rows:
        t = code_to_tptp[code]
        h.concepts.add(t)
        h.grounding[t] = f"M49:{code} {name} [{type_labels.get(typ,'?')}]"
        if parent and parent in code_to_tptp:
            h.edges.append((t, code_to_tptp[parent]))

    return h
