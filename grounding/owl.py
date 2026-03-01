"""
grounding/owl.py — Extract Hierarchy from OWL/TTL/RDF ontologies.

Replaces the extraction logic in gen_layer0_kb.py.
Supports rdfs:subClassOf, skos:broader, owl:disjointWith, AllDisjointClasses.
"""
from __future__ import annotations
import re
import sys
from .hierarchy import Hierarchy

try:
    from rdflib import Graph, RDF, RDFS, OWL, URIRef
    from rdflib.namespace import SKOS
    from rdflib.collection import Collection
except ImportError:
    print("ERROR: rdflib not installed. Run: pip install rdflib", file=sys.stderr)
    sys.exit(1)


def _iri_to_tptp(iri: str, namespace: str) -> str:
    local = iri
    if local.startswith(namespace):
        local = local[len(namespace):]
    elif "#" in local:
        local = local.split("#")[-1]
    elif "/" in local:
        local = local.split("/")[-1]
    if local and local[0].isupper():
        local = local[0].lower() + local[1:]
    local = re.sub(r'[^a-zA-Z0-9_]', '_', local)
    if local and not local[0].isalpha():
        local = "c_" + local
    return local


def load_owl(
    path: str,
    namespace: str,
    root_class: str,
    name: str,
    source: str,
    domain: str = "taxonomic",
    fmt: str | None = None,
) -> Hierarchy:
    """
    Extract a Hierarchy from an OWL ontology file.

    Parameters
    ----------
    path       : file path (TTL, RDF/XML, OWL/XML — auto-detected)
    namespace  : e.g. 'https://w3id.org/dpv#'
    root_class : local name of the root class, e.g. 'Purpose'
    name       : human label for TPTP header
    source     : provenance URI
    domain     : 'taxonomic' | 'mereological' | 'nominal'
    fmt        : rdflib format string (None = auto-detect)
    """
    print(f"Loading {path}...", file=sys.stderr)
    g = Graph()
    try:
        g.parse(path, format=fmt)
    except Exception as e:
        print(f"ERROR: Failed to parse {path}: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"  Loaded {len(g)} triples", file=sys.stderr)

    root_iri = URIRef(namespace + root_class)
    concepts, edges, iri_map = _extract_hierarchy(g, namespace, root_iri)

    if not concepts:
        _warn_empty(g, namespace)

    disjoint = _extract_disjointness(g, namespace, concepts, iri_map)
    print(f"  {len(concepts)} concepts, {len(edges)} edges, "
          f"{len(disjoint)} OWL ⊥⊥ assertions", file=sys.stderr)

    h = Hierarchy(
        name      = name,
        source    = source,
        domain    = domain,
        profile   = f"owl:{root_class}",
        concepts  = concepts,
        edges     = edges,
        disjoint  = disjoint,
        grounding = {name: iri for name, iri in iri_map.items()},
    )
    return h


# ── Internal helpers ──────────────────────────────────────────────────────────

def _extract_hierarchy(g, namespace, root_iri):
    """BFS from root_iri; collect classes + direct subsumption edges."""
    all_edges: dict = {}
    all_classes: set = set()

    for s, _, o in g.triples((None, RDFS.subClassOf, None)):
        if isinstance(s, URIRef) and isinstance(o, URIRef):
            if str(s).startswith(namespace) and str(o).startswith(namespace):
                all_edges.setdefault(s, set()).add(o)
                all_classes |= {s, o}

    for s, _, o in g.triples((None, SKOS.broader, None)):
        if isinstance(s, URIRef) and isinstance(o, URIRef):
            if str(s).startswith(namespace) and str(o).startswith(namespace):
                all_edges.setdefault(s, set()).add(o)
                all_classes |= {s, o}

    for s, _, _ in g.triples((None, RDF.type, OWL.Class)):
        if isinstance(s, URIRef) and str(s).startswith(namespace):
            all_classes.add(s)

    children_of: dict = {}
    for child, parents in all_edges.items():
        for parent in parents:
            children_of.setdefault(parent, set()).add(child)

    reachable: set = {root_iri}
    queue = [root_iri]
    while queue:
        cur = queue.pop(0)
        for ch in children_of.get(cur, []):
            if ch not in reachable:
                reachable.add(ch)
                queue.append(ch)

    iri_map: dict[str,str] = {}
    for cls in reachable:
        name = _iri_to_tptp(str(cls), namespace)
        iri_map[name] = str(cls)

    concepts: set[str] = set(iri_map.keys())
    edges: list[tuple[str,str]] = []
    for child_iri, parent_iris in all_edges.items():
        if child_iri in reachable:
            child_name = _iri_to_tptp(str(child_iri), namespace)
            for parent_iri in parent_iris:
                if parent_iri in reachable:
                    parent_name = _iri_to_tptp(str(parent_iri), namespace)
                    edges.append((child_name, parent_name))

    return concepts, edges, iri_map


def _extract_disjointness(g, namespace, concepts, iri_map):
    reverse = {v: k for k, v in iri_map.items()}
    seen: set = set()
    pairs: list = []

    for s, _, o in g.triples((None, OWL.disjointWith, None)):
        if isinstance(s, URIRef) and isinstance(o, URIRef):
            sn, on = reverse.get(str(s)), reverse.get(str(o))
            if sn and on and sn in concepts and on in concepts:
                pair = (min(sn,on), max(sn,on))
                if pair not in seen:
                    seen.add(pair)
                    pairs.append(pair)

    for s, _, _ in g.triples((None, RDF.type, OWL.AllDisjointClasses)):
        for _, _, member_list in g.triples((s, OWL.members, None)):
            try:
                members = [reverse.get(str(m)) for m in Collection(g, member_list)
                           if isinstance(m, URIRef)]
                members = [m for m in members if m and m in concepts]
                from itertools import combinations
                for c1, c2 in combinations(members, 2):
                    pair = (min(c1,c2), max(c1,c2))
                    if pair not in seen:
                        seen.add(pair)
                        pairs.append(pair)
            except Exception:
                pass

    return sorted(pairs)


def _warn_empty(g, namespace):
    print("WARNING: No concepts found. Check --namespace and --root-class.",
          file=sys.stderr)
    print("  Namespaces in file:", file=sys.stderr)
    for prefix, ns in list(g.namespaces())[:10]:
        print(f"    {prefix}: {ns}", file=sys.stderr)
