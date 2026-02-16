#!/usr/bin/env python3
"""
gen_layer0_kb.py — Generate TPTP Layer 0 axiom files from OWL ontologies.
Generates axiom files conforming to the TPTP library header standard.
See: https://www.tptp.org/TPTP/TR/TPTPTR.shtml

Usage:
    uv run python gen_layer0_kb.py \
            --input data/dpv/dpv-owl.ttl \
            --output Problems/ODRL/Axioms/Layer0-DomainKB/DPV000-0.ax \
            --namespace "https://w3id.org/dpv#" \
            --root-class "Purpose" \
            --domain taxonomic \
            --sibling-disjointness \
            --no-una \
            --name "W3C Data Privacy Vocabulary — Purpose taxonomy" \
            --source "https://w3id.org/dpv"
    uv run python gen_layer0_kb.py \
            --input data/dpv/dpv-owl.ttl \
            --output Problems/ODRL/Axioms/Layer0-DomainKB/DPV-NAIVE.ax \
            --namespace "https://w3id.org/dpv#" \
            --root-class "Purpose" \
            --domain taxonomic \
            --sibling-disjointness \
            --naive-sibling-disjointness \
            --no-una \
            --name "W3C Data Privacy Vocabulary — Purpose taxonomy" \
            --source "https://w3id.org/dpv"

Extracts:
    - rdfs:subClassOf  → leq/2
    - owl:disjointWith → disjoint/2
    - All classes under root → concept/1
    - UNA for all concept pairs (unless --no-una)

The --no-una flag is recommended when the KB forms a tree with sibling
disjointness at every level. In that case, UNA is implicit:
    Lemma (Implicit UNA). Let K = (C, ≤, ⊥) satisfy Definition 2 where
    (C, ≤) forms a tree with sibling disjointness at every level. Then
    for all distinct constants a, b ∈ C: a ≠ b is derivable from the KB
    axioms alone (via leq antisymmetry + disj_downward + disj_irrefl).

DAG-SAFE MODE (default):
    When --sibling-disjointness is enabled, the generator uses a DAG-safe
    approach: siblings a, b are asserted disjoint only when their downward
    closures are disjoint (↓a ∩ ↓b = ∅). This prevents contradictions in
    DAG-structured vocabularies with multi-parent concepts.
    
    Use --naive-sibling-disjointness to revert to tree-assumed generation
    (generates all sibling pairs without checking for multi-parent overlap).

Supports: OWL/TTL, OWL/XML, RDF/XML (auto-detected by rdflib).
"""
import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path

try:
    from rdflib import Graph, RDF, RDFS, OWL, Namespace, URIRef
    from rdflib.namespace import SKOS
except ImportError:
    print("ERROR: rdflib not installed. Run: pip install rdflib", file=sys.stderr)
    sys.exit(1)

# =============================================================================
# IRI → TPTP name conversion
# =============================================================================
def iri_to_tptp_name(iri: str, namespace: str) -> str:
    """Convert IRI to valid TPTP constant name.
    
    Strips namespace prefix, converts to lowerCamelCase TPTP constant.
    E.g., "https://w3id.org/dpv#CommercialPurpose" → "commercialPurpose"
    """
    local = str(iri)
    if local.startswith(namespace):
        local = local[len(namespace):]
    elif "#" in local:
        local = local.split("#")[-1]
    elif "/" in local:
        local = local.split("/")[-1]
    
    # lowerCamelCase: first char lowercase
    if local and local[0].isupper():
        local = local[0].lower() + local[1:]
    
    # Replace invalid TPTP chars
    local = re.sub(r'[^a-zA-Z0-9_]', '_', local)
    
    # TPTP constants must start with lowercase letter
    if local and not local[0].isalpha():
        local = "c_" + local
    
    return local

# =============================================================================
# Extract hierarchy from OWL graph
# =============================================================================
def extract_hierarchy(g: Graph, namespace: str, root_iri: URIRef):
    """Extract all classes under root and their subClassOf edges.
    
    Returns:
        concepts: set of TPTP names
        hierarchy: list of (child_tptp, parent_tptp) tuples
        iri_map: dict mapping TPTP name → original IRI (for traceability)
    """
    concepts = set()
    hierarchy = []
    iri_map = {}
    
    all_edges = {}  # child_iri → set of parent_iris
    all_classes = set()
    
    # rdfs:subClassOf
    for s, p, o in g.triples((None, RDFS.subClassOf, None)):
        if isinstance(s, URIRef) and isinstance(o, URIRef):
            if str(s).startswith(namespace) and str(o).startswith(namespace):
                all_edges.setdefault(s, set()).add(o)
                all_classes.add(s)
                all_classes.add(o)
    
    # skos:broader (DPV and many SKOS-based vocabs use this)
    for s, p, o in g.triples((None, SKOS.broader, None)):
        if isinstance(s, URIRef) and isinstance(o, URIRef):
            if str(s).startswith(namespace) and str(o).startswith(namespace):
                all_edges.setdefault(s, set()).add(o)
                all_classes.add(s)
                all_classes.add(o)
    
    # Collect classes declared via rdf:type owl:Class / rdfs:Class
    for s, p, o in g.triples((None, RDF.type, OWL.Class)):
        if isinstance(s, URIRef) and str(s).startswith(namespace):
            all_classes.add(s)
    for s, p, o in g.triples((None, RDF.type, RDFS.Class)):
        if isinstance(s, URIRef) and str(s).startswith(namespace):
            all_classes.add(s)
    
    # Collect instances typed as the root class
    for s, p, o in g.triples((None, RDF.type, root_iri)):
        if isinstance(s, URIRef) and str(s).startswith(namespace):
            all_classes.add(s)
    
    # BFS from root to find reachable classes
    reachable = set()
    queue = [root_iri]
    reachable.add(root_iri)
    children_of = {}
    for child, parents in all_edges.items():
        for parent in parents:
            children_of.setdefault(parent, set()).add(child)
    
    while queue:
        current = queue.pop(0)
        for child in children_of.get(current, []):
            if child not in reachable:
                reachable.add(child)
                queue.append(child)
    
    # Convert to TPTP
    for cls in reachable:
        name = iri_to_tptp_name(str(cls), namespace)
        concepts.add(name)
        iri_map[name] = str(cls)
    
    for child_iri, parent_iris in all_edges.items():
        if child_iri in reachable:
            for parent_iri in parent_iris:
                if parent_iri in reachable:
                    child_name = iri_to_tptp_name(str(child_iri), namespace)
                    parent_name = iri_to_tptp_name(str(parent_iri), namespace)
                    hierarchy.append((child_name, parent_name))
    
    return concepts, hierarchy, iri_map

# =============================================================================
# Extract disjointness from OWL graph
# =============================================================================
def extract_disjointness(g: Graph, namespace: str, concepts: set, iri_map: dict):
    """Extract owl:disjointWith assertions between known concepts."""
    reverse_iri = {v: k for k, v in iri_map.items()}
    disjointness = []
    seen = set()
    
    for s, p, o in g.triples((None, OWL.disjointWith, None)):
        if isinstance(s, URIRef) and isinstance(o, URIRef):
            s_name = reverse_iri.get(str(s))
            o_name = reverse_iri.get(str(o))
            if s_name and o_name and s_name in concepts and o_name in concepts:
                pair = tuple(sorted([s_name, o_name]))
                if pair not in seen:
                    seen.add(pair)
                    disjointness.append(pair)
    
    for s, p, o in g.triples((None, RDF.type, OWL.AllDisjointClasses)):
        members = []
        for _, _, member_list in g.triples((s, OWL.members, None)):
            from rdflib.collection import Collection
            try:
                coll = Collection(g, member_list)
                for member in coll:
                    if isinstance(member, URIRef):
                        name = reverse_iri.get(str(member))
                        if name and name in concepts:
                            members.append(name)
            except Exception:
                pass
        
        for c1, c2 in combinations(members, 2):
            pair = tuple(sorted([c1, c2]))
            if pair not in seen:
                seen.add(pair)
                disjointness.append(pair)
    
    return sorted(disjointness)

# =============================================================================
# Compute downward closure
# =============================================================================
def compute_downward_closure(concepts, hierarchy):
    """Compute ↓x = {y ∈ C | y ≤ x} for all concepts.
    
    Returns: dict mapping concept → set of descendants (including self)
    """
    # Initialize: each concept includes itself
    descendants = {c: {c} for c in concepts}
    
    # Fixed-point iteration: propagate descendants upward
    changed = True
    iterations = 0
    while changed:
        changed = False
        iterations += 1
        for child, parent in hierarchy:
            before = len(descendants[parent])
            descendants[parent] |= descendants[child]
            if len(descendants[parent]) > before:
                changed = True
    
    print(f"  Downward closure computed in {iterations} iterations", file=sys.stderr)
    return descendants

# =============================================================================
# Compute sibling disjointness (NAIVE - tree-assumed)
# =============================================================================
def compute_sibling_disjointness_naive(concepts, hierarchy):
    """NAIVE approach: all siblings are disjoint (tree assumption).
    
    This is UNSOUND for DAG-structured vocabularies with multi-parent concepts.
    Siblings = concepts sharing a direct parent. Under the closed-world
    assumption on the taxonomy, siblings are disjoint. The disj_downward
    axiom in Layer 1 propagates this to all descendants.
    
    Returns sorted list of (c1, c2) pairs with c1 < c2.
    """
    children_map = defaultdict(set)
    for child, parent in hierarchy:
        children_map[parent].add(child)
    
    seen = set()
    pairs = []
    for parent, children in children_map.items():
        children_list = sorted(children)
        for c1, c2 in combinations(children_list, 2):
            pair = (c1, c2)  # already sorted since children_list is sorted
            if pair not in seen:
                seen.add(pair)
                pairs.append(pair)
    
    return sorted(pairs)

# =============================================================================
# Compute sibling disjointness (DAG-SAFE)
# =============================================================================
def compute_sibling_disjointness_dag_safe(concepts, hierarchy):
    """DAG-SAFE approach: assert a ⊥⊥ b only when ↓a ∩ ↓b = ∅.
    
    This prevents contradictions in DAG-structured vocabularies where
    multi-parent concepts m with m ≤ a and m ≤ b would violate
    irreflexivity if a ⊥⊥ b were asserted.
    
    Returns:
        pairs: sorted list of (c1, c2) tuples
        skipped: list of (c1, c2, shared_descendants) for suppressed pairs
    """
    # Compute downward closure
    descendants = compute_downward_closure(concepts, hierarchy)
    
    # Group siblings
    children_map = defaultdict(set)
    for child, parent in hierarchy:
        children_map[parent].add(child)
    
    # DAG-safe filtering
    pairs = []
    skipped = []
    seen = set()
    
    for parent, children in children_map.items():
        children_list = sorted(children)
        for c1, c2 in combinations(children_list, 2):
            pair = (c1, c2)
            if pair in seen:
                continue
            seen.add(pair)
            
            # CHECK: ↓c1 ∩ ↓c2 = ∅
            overlap = descendants[c1] & descendants[c2]
            if not overlap:
                pairs.append(pair)
            else:
                skipped.append((c1, c2, sorted(overlap)))
                print(f"  SKIP: {c1} ⊥⊥ {c2} (overlap: {', '.join(sorted(overlap))})", 
                      file=sys.stderr)
    
    return sorted(pairs), skipped

# =============================================================================
# Compute hierarchy metadata
# =============================================================================
def compute_hierarchy_stats(concepts, hierarchy):
    """Compute structural statistics about the concept hierarchy."""
    parents_map = defaultdict(set)
    children_map = defaultdict(set)
    
    for child, parent in hierarchy:
        parents_map[child].add(parent)
        children_map[parent].add(child)
    
    # Multi-parent concepts
    multi_parent = sorted([c for c in concepts if len(parents_map[c]) > 1])
    
    # Leaves (no children)
    leaves = sorted([c for c in concepts if not children_map[c]])
    
    # Root (no parents)
    roots = sorted([c for c in concepts if not parents_map[c]])
    
    # Max depth (longest path from leaf to root)
    def max_depth(node, memo={}):
        if node in memo:
            return memo[node]
        if not parents_map[node]:
            memo[node] = 0
            return 0
        d = 1 + max(max_depth(p, memo) for p in parents_map[node])
        memo[node] = d
        return d
    
    memo = {}
    depths = {c: max_depth(c, memo) for c in concepts}
    max_d = max(depths.values()) if depths else 0
    
    # Branching factor
    branching = [len(children_map[c]) for c in concepts if children_map[c]]
    avg_branch = sum(branching) / len(branching) if branching else 0
    max_branch = max(branching) if branching else 0
    
    return {
        "multi_parent": multi_parent,
        "leaves": leaves,
        "roots": roots,
        "max_depth": max_d,
        "n_internal": len(concepts) - len(leaves) - len(roots),
        "avg_branching": avg_branch,
        "max_branching": max_branch,
    }

# =============================================================================
# Generate TPTP output
# =============================================================================
def generate_tptp(concepts, hierarchy, disjointness, iri_map,
                  name, source, domain, filename, version="0.1.0",
                  sibling_disjointness=False, skip_una=False,
                  dag_safe_mode=True, skipped_pairs=None):
    """Generate complete TPTP Layer 0 axiom file with standard header."""
    concepts_sorted = sorted(concepts)
    hierarchy_sorted = sorted(hierarchy)
    
    n_una = 0 if skip_una else len(concepts_sorted) * (len(concepts_sorted) - 1) // 2
    h_stats = compute_hierarchy_stats(concepts, hierarchy)
    
    n_formulae = len(concepts_sorted) + len(hierarchy_sorted) + len(disjointness) + n_una
    n_equality = n_una
    
    # Domain string for the Relation field
    domain_desc = {
        "taxonomic": "class subsumption (paper Def. 2, ≤ = ⊑)",
        "mereological": "part-whole containment (paper Def. 2, ≤ = ⪯)",
        "nominal": "identity (paper Def. 2, ≤ = =)",
    }
    
    # Predicate summary
    predicates = []
    if concepts_sorted:
        predicates.append(("concept", 1, len(concepts_sorted)))
    if hierarchy_sorted:
        predicates.append(("leq", 2, len(hierarchy_sorted)))
    if disjointness:
        predicates.append(("disjoint", 2, len(disjointness)))
    
    n_usr_pred = len(predicates)
    pred_summary = "; ".join(f"{n}/{a}" for n, a, _ in predicates)
    
    lines = []
    
    # ─── TPTP Standard Header ─────────────────────────────────────────────
    lines.append("%--------------------------------------------------------------------------")
    lines.append(f"% File     : {filename} : TPTP v{version}. Released v{version}.")
    lines.append(f"% Domain   : {name}")
    lines.append(f"% Axioms   : Full hierarchy ({domain})")
    lines.append(f"% Version  : Generated from OWL source.")
    lines.append(f"% English  : {name} encoded as a TPTP Layer 0 domain")
    if skip_una:
        lines.append(f"%            knowledge base. Contains concept membership, direct")
        lines.append(f"%            subsumption edges, and disjointness. UNA is implicit")
        lines.append(f"%            from tree structure + sibling disjointness (Implicit UNA Lemma).")
    else:
        lines.append(f"%            knowledge base. Contains concept membership, direct")
        lines.append(f"%            subsumption edges, disjointness, and the unique name")
        lines.append(f"%            assumption (UNA).")
    
    lines.append(f"% Refs     : [MuS25] Mustafa, D. & Sutcliffe, G. (2025),")
    lines.append(f"%            Automated Reasoning for ODRL Policy Conflict Detection")
    lines.append(f"% Source   : {source}")
    lines.append(f"% Names    : {filename}")
    lines.append(f"% Status   : Layer 0 — Domain Knowledge Base")
    lines.append(f"% Syntax   : Number of formulae    : {n_formulae:>5}"
                 f" ({n_formulae:>5} unt;   0 def)")
    lines.append(f"%            Number of atoms       : {n_formulae:>5}"
                 f" ({n_equality:>5} equ)")
    lines.append(f"%            Maximal formula atoms  :     1 (   1 avg)")
    lines.append(f"%            Number of connectives  :     0"
                 f" (   0   ~;   0   |;   0   &)")
    lines.append(f"%                                         "
                 f"(   0 <=>;   0  =>;   0  <=;   0 <~>)")
    lines.append(f"%            Maximal formula depth  :     1 (   1 avg)")
    lines.append(f"%            Maximal term depth     :     1 (   1 avg)")
    lines.append(f"%            Number of predicates   : {n_usr_pred:>5}"
                 f" ({n_usr_pred:>5} usr;   0 prp; 1-2 aty)")
    lines.append(f"%            Number of functors     : {len(concepts_sorted):>5}"
                 f" ({len(concepts_sorted):>5} usr; {len(concepts_sorted):>3} con; 0-0 aty)")
    lines.append(f"%            Number of variables    :     0 (   0   !;   0   ?)")
    lines.append(f"% SPC      : FOF_EPR_RFN_NEQ")
    
    lines.append(f"% Comments : All formulae are ground unit clauses (no variables).")
    lines.append(f"%          : Reflexivity and transitivity of leq/2 are provided by")
    lines.append(f"%          : Layer 1 (ODRL000-0.ax), not asserted here.")
    
    if skip_una:
        lines.append(f"%          : UNA: IMPLICIT — tree + sibling disjointness makes all")
        lines.append(f"%          :   constants provably distinct via antisymmetry +")
        lines.append(f"%          :   disj_downward + disj_irrefl (Implicit UNA Lemma).")
    
    if sibling_disjointness and dag_safe_mode and skipped_pairs:
        lines.append(f"%          : DAG-SAFE MODE — {len(skipped_pairs)} sibling pairs suppressed")
        lines.append(f"%          :   to avoid contradictions from multi-parent concepts.")
    elif sibling_disjointness and not dag_safe_mode:
        lines.append(f"%          : NAIVE MODE — tree-assumed sibling disjointness (may be")
        lines.append(f"%          :   unsound for DAG-structured vocabularies).")
    
    lines.append(f"%          : Multi-parent: {', '.join(h_stats['multi_parent']) or 'none'}")
    lines.append(f"%          : Root: {', '.join(h_stats['roots'])}")
    
    lines.append(f"% Ontology : Predicates: {pred_summary}")
    lines.append(f"%          : Relation: leq/2 — {domain_desc.get(domain, domain)}")
    lines.append(f"% Stats    : Concepts {len(concepts_sorted)}"
                 f" | Edges {len(hierarchy_sorted)}"
                 f" | Disjoint {len(disjointness)}"
                 f" | UNA {n_una}"
                 f" | Total {n_formulae}")
    lines.append(f"%          : Depth {h_stats['max_depth']}"
                 f" | Leaves {len(h_stats['leaves'])}"
                 f" | Internal {h_stats['n_internal']}"
                 f" | Branch avg {h_stats['avg_branching']:.1f}"
                 f" max {h_stats['max_branching']}")
    
    lines.append(f"% Date     : {date.today().isoformat()}")
    lines.append(f"% Authors  : Mustafa, D. & Sutcliffe, G.")
    lines.append(f"% Gen      : gen_layer0_kb.py from {source}")
    lines.append("%--------------------------------------------------------------------------")
    
    # ─── Section 1: Concept membership ─────────────────────────────────────
    lines.append("")
    lines.append("% ─── Concept membership (Definition 2: C) ─────────────────────────────")
    for c in concepts_sorted:
        iri_comment = iri_map.get(c, "")
        lines.append(f"fof(c_{c}, axiom, concept({c})).  % {iri_comment}")
    
    # ─── Section 2: Hierarchy ──────────────────────────────────────────────
    lines.append("")
    lines.append("% ─── Hierarchy (Definition 2: ≤) ──────────────────────────────────────")
    lines.append("% Only direct edges. Layer 1 provides reflexivity + transitivity.")
    for i, (child, parent) in enumerate(hierarchy_sorted):
        lines.append(f"fof(h_{i:04d}, axiom, leq({child}, {parent})).")
    
    # ─── Section 3: Disjointness ───────────────────────────────────────────
    lines.append("")
    lines.append("% ─── Disjointness (Definition 2: ⊥⊥) ─────────────────────────────────")
    if sibling_disjointness:
        if dag_safe_mode:
            lines.append("% DAG-SAFE sibling disjointness: children of the same parent are")
            lines.append("% disjoint ONLY WHEN their downward closures do not overlap.")
            if skipped_pairs:
                lines.append(f"% Suppressed {len(skipped_pairs)} pairs due to multi-parent overlap.")
        else:
            lines.append("% NAIVE sibling disjointness: children of the same parent are disjoint.")
            lines.append("% WARNING: May be unsound for DAG-structured vocabularies.")
        lines.append("% Derived disjointness follows from disj_downward (Layer 1).")
    else:
        lines.append("% Only assertions from the source ontology.")
        lines.append("% Derived disjointness follows from disj_downward (Layer 1).")
    
    if disjointness:
        for i, (c1, c2) in enumerate(disjointness):
            lines.append(f"fof(d_{i:04d}, axiom, disjoint({c1}, {c2})).")
    else:
        lines.append("% (none found in source ontology)")
    
    # ─── Section 4: UNA ────────────────────────────────────────────────────
    lines.append("")
    if skip_una:
        lines.append("% ─── Unique Name Assumption ───────────────────────────────────────────")
        lines.append("% SKIPPED (--no-una): UNA is implicit from tree structure + sibling")
        lines.append("% disjointness. All constants are provably distinct via:")
        lines.append("%   - leq antisymmetry: a ≤ b ∧ b ≤ a → a = b")
        lines.append("%   - disj_downward:    ⊥(a,b) ∧ c ≤ a → ⊥(c,b)")
        lines.append("%   - disj_irrefl:      ⊥(a,b) ∧ c ≤ a ∧ c ≤ b → ⊥")
        lines.append("% Collapsing any two constants leads to contradiction.")
        una_count = 0
    else:
        lines.append("% ─── Unique Name Assumption ───────────────────────────────────────────")
        lines.append(f"% C({len(concepts_sorted)},2) = {n_una} pairwise distinctness axioms.")
        una_count = 0
        for c1, c2 in combinations(concepts_sorted, 2):
            lines.append(f"fof(una_{una_count:04d}, axiom, {c1} != {c2}).")
            una_count += 1
    
    # ─── Footer ────────────────────────────────────────────────────────────
    lines.append("")
    lines.append("%--------------------------------------------------------------------------")
    total = len(concepts_sorted) + len(hierarchy_sorted) + len(disjointness) + una_count
    lines.append(f"% Summary: {len(concepts_sorted)} concept"
                f" + {len(hierarchy_sorted)} leq"
                f" + {len(disjointness)} disjoint"
                f" + {una_count} UNA"
                f" = {total} axioms")

    if sibling_disjointness and dag_safe_mode and skipped_pairs:
        lines.append(f"% DAG-safe: suppressed {len(skipped_pairs)} sibling pairs:")
        for c1, c2, overlap in skipped_pairs:
            lines.append(f"%   {c1} ⊥⊥ {c2} (overlap: {', '.join(overlap)})")
    elif sibling_disjointness and not dag_safe_mode:
        lines.append(f"% NAIVE mode: ALL sibling pairs asserted (including problematic ones)")
        lines.append(f"% WARNING: This KB may be INCONSISTENT if it contains multi-parent concepts.")

    lines.append("%--------------------------------------------------------------------------")
        
    return "\n".join(lines)

# =============================================================================
# Main
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Generate TPTP Layer 0 axiom file from OWL ontology.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # DAG-safe mode (recommended)
  %(prog)s -i data/dpv/dpv-owl.ttl -o DPV000-0.ax -n "https://w3id.org/dpv#" \\
           -r Purpose -d taxonomic --sibling-disjointness --no-una
  
  # Naive mode (tree-assumed, may be unsound for DAGs)
  %(prog)s -i data/dpv/dpv-owl.ttl -o DPV000-0.ax -n "https://w3id.org/dpv#" \\
           -r Purpose -d taxonomic --sibling-disjointness --no-una \\
           --naive-sibling-disjointness
  
  # Geographic ontology
  %(prog)s -i data/geo/un-m49.ttl -o GEO000-0.ax -n "http://example.org/geo#" \\
           -r World -d mereological --sibling-disjointness --no-una
""")
    parser.add_argument("--input", "-i", required=True,
                        help="Path to OWL file (TTL, RDF/XML, OWL/XML)")
    parser.add_argument("--output", "-o", required=True,
                        help="Output TPTP axiom file path")
    parser.add_argument("--namespace", "-n", required=True,
                        help="Namespace URI (e.g., 'https://w3id.org/dpv#')")
    parser.add_argument("--root-class", "-r", required=True,
                        help="Root class local name (e.g., 'Purpose')")
    parser.add_argument("--domain", "-d", default="taxonomic",
                        choices=["taxonomic", "mereological", "nominal"],
                        help="Semantic domain (paper Def. 2)")
    parser.add_argument("--name", default="OWL Ontology",
                        help="Human-readable KB name for header")
    parser.add_argument("--source", default="",
                        help="Source URL for header")
    parser.add_argument("--format", "-f", default=None,
                        help="RDF format (turtle, xml, etc.). Auto-detected if omitted.")
    parser.add_argument("--version", default="0.1.0",
                        help="TPTP problem version string (default: 0.1.0)")
    parser.add_argument("--sibling-disjointness", action="store_true",
                        help="Generate pairwise disjointness for sibling concepts "
                             "(children of same parent). Uses DAG-safe mode by default.")
    parser.add_argument("--naive-sibling-disjointness", action="store_true",
                        help="Use NAIVE tree-assumed sibling disjointness (all siblings "
                             "disjoint, no multi-parent checking). May be unsound for DAGs.")
    parser.add_argument("--no-una", action="store_true",
                        help="Skip UNA axioms. Recommended when KB is a tree with "
                             "sibling disjointness — UNA is then implicit via "
                             "antisymmetry + disj_downward + disj_irrefl.")
    
    args = parser.parse_args()
    
    # Load ontology
    print(f"Loading {args.input}...", file=sys.stderr)
    g = Graph()
    try:
        g.parse(args.input, format=args.format)
    except Exception as e:
        print(f"ERROR: Failed to parse {args.input}: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"  Loaded {len(g)} triples", file=sys.stderr)
    
    root_iri = URIRef(args.namespace + args.root_class)
    print(f"  Root class: {root_iri}", file=sys.stderr)
    
    # Extract
    concepts, hierarchy, iri_map = extract_hierarchy(g, args.namespace, root_iri)
    print(f"  Found {len(concepts)} concepts, {len(hierarchy)} edges", file=sys.stderr)
    
    if not concepts:
        print("WARNING: No concepts found. Check --namespace and --root-class.",
              file=sys.stderr)
        print("  Namespaces in file:", file=sys.stderr)
        for prefix, ns in g.namespaces():
            print(f"    {prefix}: {ns}", file=sys.stderr)
        print("  Sample classes:", file=sys.stderr)
        for i, (s, _, _) in enumerate(g.triples((None, RDF.type, OWL.Class))):
            if i < 10:
                print(f"    {s}", file=sys.stderr)
    
    disjointness = extract_disjointness(g, args.namespace, concepts, iri_map)
    print(f"  Found {len(disjointness)} OWL disjointness assertions", file=sys.stderr)
    
    skipped_pairs = []
    dag_safe_mode = not args.naive_sibling_disjointness
    
    if args.sibling_disjointness:
        if dag_safe_mode:
            print(f"  Computing DAG-SAFE sibling disjointness...", file=sys.stderr)
            sibling_disj, skipped_pairs = compute_sibling_disjointness_dag_safe(
                concepts, hierarchy
            )
            print(f"  Generated {len(sibling_disj)} DAG-safe sibling pairs", file=sys.stderr)
            print(f"  Suppressed {len(skipped_pairs)} pairs due to multi-parent overlap", 
                  file=sys.stderr)
        else:
            print(f"  Computing NAIVE sibling disjointness (tree-assumed)...", file=sys.stderr)
            sibling_disj = compute_sibling_disjointness_naive(concepts, hierarchy)
            print(f"  Generated {len(sibling_disj)} sibling pairs", file=sys.stderr)
            print(f"  WARNING: Naive mode may be unsound for DAG-structured vocabularies",
                  file=sys.stderr)
        
        # Merge: union of OWL-sourced and sibling-inferred, deduplicated
        existing = set(disjointness)
        added = 0
        for pair in sibling_disj:
            if pair not in existing:
                existing.add(pair)
                disjointness.append(pair)
                added += 1
        disjointness = sorted(disjointness)
        print(f"  + {len(sibling_disj)} sibling pairs ({added} new)"
              f" → {len(disjointness)} total disjointness", file=sys.stderr)
    
    if args.no_una:
        print(f"  UNA: SKIPPED (--no-una, implicit from tree + disjointness)",
              file=sys.stderr)
    else:
        n_una = len(concepts) * (len(concepts) - 1) // 2
        print(f"  UNA: {n_una} pairwise axioms", file=sys.stderr)
    
    # Generate
    filename = Path(args.output).name
    tptp = generate_tptp(concepts, hierarchy, disjointness, iri_map,
                         args.name, args.source, args.domain, filename,
                         version=args.version,
                         sibling_disjointness=args.sibling_disjointness,
                         skip_una=args.no_una,
                         dag_safe_mode=dag_safe_mode,
                         skipped_pairs=skipped_pairs)
    
    # Write
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(tptp)
        f.write("\n")
    
    # Summary
    una_count = 0 if args.no_una else len(concepts) * (len(concepts) - 1) // 2
    total = len(concepts) + len(hierarchy) + len(disjointness) + una_count
    print(f"\nWritten: {args.output}", file=sys.stderr)
    print(f"  {len(concepts)} concepts, {len(hierarchy)} leq, "
          f"{len(disjointness)} disjoint, {una_count} UNA = {total} axioms",
          file=sys.stderr)
    
    if args.sibling_disjointness and dag_safe_mode and skipped_pairs:
        print(f"  DAG-safe: suppressed {len(skipped_pairs)} pairs", file=sys.stderr)
    
    if args.no_una:
        saved = len(concepts) * (len(concepts) - 1) // 2
        print(f"  (--no-una saved {saved} axioms)", file=sys.stderr)

if __name__ == "__main__":
    main()