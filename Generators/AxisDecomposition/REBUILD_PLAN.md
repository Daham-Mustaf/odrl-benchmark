Good. Let me write the full plan as a document so we have it pinned, then start Phase A right after.

# OAX Benchmark Rebuild Plan
**Goal:** Produce a clean, defensible benchmark artifact for two destinations:
1. ISWC 2026 paper §10 (Evaluation): cross-prover concordance over 247 problems
2. TPTP problem library submission (post-ISWC): standalone benchmark contribution

**Timeline:** 5 days. Currently at day 1 (Ubuntu rebuild post-water-damage).

**Current state:** 247 problems generated, 1254/1485 prover runs passing,
131 unexpected failures distributed across categories.

---

## Architecture: one source of truth, multiple encodings

```
Generators/AxisDecomposition/
├── policy/                 Source-of-truth: per-category policy definitions
├── axioms/                 Axiom-file generators (one per axiom file)
├── encoders/               One encoder per output format
│   ├── fof.py              FOF + axiomatized order (TPTP-safe)
│   ├── tff.py              TFF + $real (dense-arithmetic problems only)
│   ├── smt.py              SMT-LIB
│   └── ttl.py              ODRL policy in Turtle
├── header.py               Header rendering (single source)
├── validate.py             Lints every artifact end-to-end
├── audit.py                Runs all provers, builds CSV + summary
└── gen.py                  CLI: regenerate, validate, audit, package
```

Principle: each policy defined once, encoders translate to all formats,
validator catches drift, audit produces the §10 numbers.

---

## Phases

### Phase A — Validation infrastructure (Day 1)
Build `validate.py` that catches every kind of drift:
- Header consistency (Status / Verdict / Relation correctly set)
- Include completeness (every predicate has a defining axiom in scope)
- Syntax (TPTP via tptp4X, SMT via z3 -parse-only, TTL via rdflib)
- Cross-format consistency (SMT and FOF encode the same claim)
- Audit-light (quick spot-check, SZS vs expected)

Output: single CSV `validate_<timestamp>.csv` with one row per problem and
columns for each check. This becomes the ground truth for what's broken.

**Acceptance**: validator runs in <30s, lists every failure with row+column.

### Phase B — Axiom hardening (Day 2)
Walk every axiom file with the paper next to us. For each predicate, write
the biconditional from the paper definition. Document paper provenance in
each axiom's comment.

Apply known fixes:
- ORD000: trichotomy on val/1 (Bug 1)
- AXIS000: box_verdict_total (Bug 3)
- SUBS000: axis_subsumes_def global biconditional (Bug 6)
- WF000: per-op biconditionals matching Def 4.4
- PREC000: prec/4 biconditional matching Def 5.5
- PROJ000: in_box2/3 biconditionals matching Thm 5.10
- COMPL000: completion_compatible/3 + completion_conflict/4 biconditionals
- COMP000: or_verdict + xone_verdict with totality
- ORD001: density (loaded only when needs_density=True)

**Acceptance**: each axiom file has a docstring citing the paper definition
it encodes. Each fof formula has a comment naming the paper line.

### Phase C — Encoder split (Day 3)
Refactor writers.py into encoders/fof.py + tff.py + smt.py + ttl.py.
Each encoder is self-contained, takes a policy dict, emits one format.

TFF encoder used **only for 4 dense-arithmetic problems** (ODRL347, ODRL413,
ODRL414, HARD001+1) where density is part of the theory rather than an axiom.
Everything else stays on FOF.

**Acceptance**: regen + validate + audit produces same numbers as before
encoder split, plus 4 working TFF supplemental files.

### Phase D — Per-category cleanup (Day 4)
Attack the 131 failures from current audit, category by category, in
descending failure-count order:
1. SAT (40 failures)
2. ConflictCriterion (29)
3. Completion (23)
4. Projection (16)
5. Box2D + Box3D (10)
6. WellFormedness (5)
7. Hard (5 — accept eprover density timeouts as documented)
8. BoxContainment + Boundary (3)

For each: open policy + axiom + paper section side-by-side, find
divergence, fix, re-validate, re-audit.

**Acceptance**: 0 unexpected failures. Only retained failures are the
documented eprover density timeouts (Hard + maybe ODRL347/414 if TFF
supplemental doesn't catch them).

### Phase E — Paper §10 + TPTP package (Day 5 morning)
- Update §10 prose with final numbers from clean audit
- Write AUDIT_METHODOLOGY.md (documents retained failures with root cause)
- Write README.md for reviewers (5-min quick-start)
- Package separately for TPTP submission:
  - Rename to TPTP convention `<Domain><Number>+<Variant>.p`
  - Verify under tptp4X
  - Add Bibtex entries to references
  - Coordinate with Geoff Sutcliffe via existing email thread

**Acceptance**: paper compiles, audit reproduces, reviewers can verify.

### Phase F — Anonymization (Day 5 evening)
For ISWC submission:
- Source: "anonymous"
- Authors: "anonymous"
- Refs: "[Anonymous26]" placeholder
- Push to anonymous.4open.science

For TPTP submission (post-ISWC): keep real names, submit through
normal TPTP channels.

---

## Acceptance criteria (overall)

Before submitting:
- All 247 problems present in 4 formats (.p, .tff.p where applicable, .smt2, .ttl)
- `uv run validate.py` reports 0 issues
- `uv run audit.py --timeout 60 --workers 4` reports 245+/247 verified
- Retained failures are documented in AUDIT_METHODOLOGY.md
- §10 numbers in paper match the audit CSV
- Repository is anonymized for review

---

## Reuse for future papers
This same architecture serves:
- The KGC paper (concept-valued grounding) - separate generator dir, shared header/validate
- Future ODRL profile extensions - new policy/ files, no architecture change
- General ODRL benchmark library - the TPTP-submitted version becomes the long-term home
MDEOF

# Sanity check
wc -l REBUILD_PLAN.md
head -20 REBUILD_PLAN.md
```

Now Phase A. The validation harness:

