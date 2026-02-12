# LNG000-0.ax — BCP 47 Language KB

**Operand:** `odrl:language` · **Domain:** Taxonomic · **Relation:** `subClassOf`

## Source

IETF BCP 47 (RFC 5646) subtag refinement + ISO 639-3 macrolanguages.
Subtag refinement modeled as taxonomic subsumption: `de-AT` refines `de` → `subClassOf(de_AT, de)`.

> Underscores replace hyphens for TPTP identifier syntax.

## Concept Hierarchy (10 tags)

```
de ─┬─ de_AT  (Austrian German)
    └─ de_CH  (Swiss German)

en ─┬─ en_US  (American English)
    └─ en_GB  (British English)

fr              (French, no subtags)

ar ─┬─ arb    (Standard Arabic, ISO 639-3)
    └─ arz    (Egyptian Arabic, ISO 639-3)
```

4 primary tags, 6 subtags. No shared refinements across branches.

## Axiom Summary

| Category | Count | Example |
|---|:---:|---|
| Structural (refl, trans) | 2 | `∀X: subClassOf(X,X)` |
| Positive refinements | 6 | `subClassOf(de_AT, de)` |
| Negative (cross-branch) | 12 | `~subClassOf(de, en)` |
| **Total** | **20** | |

## Disjointness

Negative facts at primary level only (de↔en, de↔fr, de↔ar, en↔fr, en↔ar, fr↔ar). Leaf cross-branch disjointness (e.g., `~subClassOf(de_AT, en)`) is derivable via transitivity contrapositive but not explicitly stated.

## Benchmark Problems

| Problem | Operator | Policy → Request | SZS | Verdict |
|---|---|---|:---:|:---:|
| ODRL050-1 | isA | `de` → `de_AT` | Theorem | Compatible |
| ODRL051-1 | isA | `de` → `fr` | Theorem | Conflict |
| ODRL052-1 | isAnyOf | `{de,en}` → `fr` | Theorem | Conflict |
| ODRL053-1 | isA | `ar` → `arz` | Theorem | Compatible |
| ODRL054-1 | isAnyOf | `{de,en}` → `en_GB` | Theorem | Compatible |
| ODRL055-1 | cross-DS | 3-KB (spatial+purpose+lang) | CounterSat | Unknown |
| ODRL056-1 | diagnostic | isolate language pair | Theorem | Conflict |

## Scenarios

All scenarios from German cultural dataspaces (Datenraum Kultur):

- **BSB** (Bayerische Staatsbibliothek) — German-language manuscripts, Arabic collection
- **HK** (Hamburger Kunsthalle) — multilingual artwork metadata
- **Cross-dataspace** — BSB ↔ French archive, HK ↔ Louvre, HK ↔ British Museum

## Paper Mapping

| Paper Section | What LNG validates |
|---|---|
| Definition 2 (KB) | Taxonomic domain with `subClassOf` |
| Definition 5 (Denotation) | isA, isAnyOf on language operand |
| Contribution 3 | Third high-priority operand (spatial, purpose, **language**) |
| Table 1 (motivating) | ODRL055-1 extends to three dimensions |

## Semantic Extension Note

BCP 47 defines subtag *refinement*, not class *subsumption*. Our modeling treats refinement as taxonomic subsumption (paper Section 9). This is a semantic extension — standard ODRL `isA` on language would require flat BCP 47 tag matching.
