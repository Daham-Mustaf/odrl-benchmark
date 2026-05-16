Right answer. We have a week, the goal is dual: ISWC §10 evaluation + TPTP benchmark library submission. Both deserve clean, defensible artifacts that you can also reuse for future papers. Let me lay out the architecture and propose a plan.

## Why we need to think this through, not just patch

The two destinations have different requirements:

**ISWC §10 (paper evaluation):**
- Cross-prover concordance is the central claim
- Verdict aggregation should be *in the prover*, not Python — otherwise the concordance claim weakens
- Wall-time and pass-rate numbers go in the table
- A reviewer must be able to run `uv run run_audit.py` and reproduce the table

**TPTP benchmark library:**
- Files must follow TPTP conventions exactly (header format, file naming `<Domain><N>+<V>.p`, axiom factoring)
- BSR(BD) classification matters for the SPC tag
- Each problem must compile under tptp4X without warnings
- Geoff Sutcliffe and the TPTP curators review every submission against strict format rules
- Axiom files separate from problem files (already what we do — good)
- Self-test convention: each problem and axiom file standalone, no inter-file order dependencies

Both work from the same source. The question is what "best" means architecturally.

## My proposed architecture

```
Generators/AxisDecomposition/
├── policy/                      # Source-of-truth ODRL policy definitions
│   ├── single_axis.py           # One file per category
│   ├── box.py
│   ├── policy_quality.py
│   ├── boundary.py
│   ├── composition.py
│   ├── ...
│   └── _schema.py               # The dataclass / dict schema with validation
├── axioms/                      # Axiom-file generators
│   ├── ord.py                   # ORD000, ORD001
│   ├── axis.py                  # AXIS000
│   ├── prec.py                  # PREC000
│   ├── wf.py                    # WF000
│   ├── proj.py                  # PROJ000
│   ├── comp.py                  # COMP000
│   ├── compl.py                 # COMPL000
│   └── subs.py                  # SUBS000
├── encoders/                    # One encoder per output format
│   ├── fof.py                   # FOF + axiomatized order (TPTP-safe)
│   ├── tff.py                   # TFF + $real (for dense-arithmetic)
│   ├── smt.py                   # SMT-LIB (LRA + UF for verdict algebra)
│   └── ttl.py                   # ODRL policy in Turtle
├── header.py                    # Header rendering (single source)
├── validate.py                  # Lints every artifact:
│                                #   - .p files: syntax check via tptp4X
│                                #   - .smt2: syntax check via z3 -parse-only
│                                #   - .ttl:  parse via rdflib
│                                #   - SZS expectations consistent with verdict
│                                #   - axiom signatures match problem usage
├── audit.py                     # Run all provers, build CSV + summary
└── gen.py                       # CLI: regenerate, validate, audit, package
```

Each policy is defined **once** in `policy/<category>.py` as a structured Python dict. The encoders translate the same policy to FOF, TFF, SMT-LIB, and TTL. The validator runs after every regeneration. The audit harness reads structured CSV output.

The principle: **one source of truth, multiple encodings, validated end-to-end**.

## Plan: 6 phases over 5 days

| Day | Phase | Outcome |
|---|---|---|
| Day 1 | Phase A: validation infrastructure | A `validate.py` that catches everything: header consistency, include presence, axiom-signature match, TPTP/SMT/TTL syntax, SZS-vs-verdict polarity. Single pass over 247 problems takes <30s. Says "all clear" or lists exact failures. |
| Day 2 | Phase B: axiom hardening | Walk every axiom file with the paper next to us. For each predicate, write the biconditional from the paper definition. Document each axiom's paper provenance in its comment. Add the trichotomy + box_verdict_total + axis_subsumes_def fixes from the reviews. Goal: each axiom file is a verbatim FOL translation of one paper definition. |
| Day 3 | Phase C: encoder split | Refactor writers.py into encoders/fof.py + encoders/tff.py + encoders/smt.py + encoders/ttl.py. Each encoder is self-contained, takes a policy dict, emits one format. TFF encoder uses $real for dense-arithmetic problems. Run all four encoders, validate, audit. |
| Day 4 | Phase D: per-category cleanup | Attack the 131 failures from this morning. For each category that fails: open the policy file, the axiom file, and the paper section side-by-side, find the divergence, fix. Goal: 0 unexpected failures (just the documented eprover density timeouts). |
| Day 5 | Phase E: paper §10 + TPTP submission package | Update §10 prose with final numbers. Write AUDIT_METHODOLOGY.md. Write README.md for reviewers. Package separately for TPTP submission with correct file naming, header conventions, axiom factoring. |
| Day 5 evening | Phase F: anonymization | For ISWC: replace Source/Authors with `anonymous`, refs become `[Anonymous26]`. Push to anonymous.4open.science. For TPTP: keep real names, submit through normal channels post-ISWC. |

## What I propose right now (next 1-2 hours)

**Phase A — build the validation harness first**, before fixing anything else. Reason: every fix we make will need re-validation. Doing this once means we always know exactly where we stand.

The validator does five checks per problem:

1. **Header consistency** — Status / Verdict / Relation fields present and self-consistent (Status="Theorem" iff Verdict in {Compatible, Conflict}, Relation has expected polarity for verdict)
2. **Include completeness** — every predicate used in conjecture and decls is defined in an included axiom file
3. **Syntax** — `.p` parses via tptp4X, `.smt2` parses via z3, `.ttl` parses via rdflib
4. **Cross-format consistency** — the SMT and FOF encode the same claim under the polarity table
5. **Audit-light** — quick 5s vampire + z3 spot-check; record SZS vs expected

It outputs one CSV: `problem_id, header_ok, includes_ok, fof_syntax, smt_syntax, ttl_syntax, fof_smt_consistent, fof_szs, smt_szs, status`.

That CSV is then the **ground truth** for what's working. We sort by failure type and attack each cluster.

Want me to write Phase A now? About 200 lines of Python. Ready to run in 20 minutes.

Or do you want me to write the full plan as a document first, then we proceed phase by phase?