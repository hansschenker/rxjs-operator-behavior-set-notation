# Change Log

## Operator-family implementation roadmap — 2026-09-29

Added [the Operator-Family Implementation Plan](docs/FAMILY-IMPLEMENTATION-PLAN.md), revision 1.0: 34 bounded study packages across eight phases, an initial inventory of 146 qualified entries, dependency ordering, per-session specifications/comparisons/traces/evidence, completion gates, and a verified GitHub handoff policy.

The core inventory is reconciled against the RxJS 7.8.2 root and operator export lists. It distinguishes creation and pipeable APIs with the same spelling, retains legacy entry points, normalizes ordinary re-exports, and assigns three transport-adapter extension targets. Named-entry coverage is not all-overload coverage or proof of semantic equivalence.

The next session is F01 — Taking and dropping prefixes: takeWhile, skipWhile, take, and skip. Its brief includes boundary, empty/error/cancellation, callback-index, and synchronous execution checks. A minimal pinned TypeScript/RxJS trace-verification harness is planned as an explicit F01 verification extension; no compiler or replacement RxJS runtime is proposed.

Added README navigation and the initial checkpoint. All 34 families remain Planned. Existing examples are preserved as starting material, not relabeled as complete family packages.

Planning validation checked unique inventory ownership, ordered dependencies, roadmap status rows, delimiter balance, and relative targets against the inspected repository tree. It did not execute the full-repository documentation checker or an RxJS runtime suite. The shared notation, RxJS 7.8.2 baseline, and attribution are unchanged.

## ROB-SN conversation consolidation — 2026-09-29

Adopted **ROB-SN — RxJS Operator Behavior Set Notation** and recorded the working ChatGPT project name **ROB-SN RxJS Operator Set Notation**. The repository name and RxJS 7.8.2 baseline are unchanged.

Added the project guide and Model → Observe → Classify workflow; five-slot catalogue; 40 proposed transition templates in seven families; derived behavioral qualities and trace laws; lessons from Hickey's transducers; six sequence-processing behavior families; and scoped take(3)/bufferCount(3) profiles.

Preserved distinctions between configuration and behavior, event kinds and persistent states, requested actions and delivered notifications, state invariants and trace laws, domain functions and execution machinery, resource ownership and output status, and completion/error/cancellation/cleanup. Clarified that batching/run segmentation is not RxJS partition, and that a reducing-function transducer is not identical to an Observable-specific behavioral machine.

Expanded the README and operator-analysis template, linked all new material, and added a documentation checker plus a consolidation/evidence record. The existing FOUNDATION.md, EXECUTION-CONTRACT.md, REFERENCES.md, and CONTRIBUTING.md are retained without semantic replacement; new pages supply additional primary references directly.

This edition is still a proposed documentation/specification framework. Documentation validation is not RxJS runtime conformance. No exhaustive rule basis, executable interpreter, runtime suite, or theorem-prover result is claimed. See [the consolidation record](docs/CONSOLIDATION-2026-09-29.md) for coverage and validation scope.

Attribution remains **GPT-6 Astra is the main contributor of the project.**

## Initial documentation edition — 2026-09-29

Preserved the set-theoretic formulation of RxJS Operator Behavior Notation as a stateful transducer:

$$
\delta:S\times E\to S\times A^*,\qquad\delta(s,e)=(s',\alpha).
$$

Added the foundational reference, action-interpreter/execution contract, reusable operator-analysis template, pinned source references, and contribution guide.

The reference preserves the distinctions between state spaces and individual states, sets and ordered sequences, source and inner events, callback and event-processing indexes, readiness and completion, cancellation and completion, and behavioral versus execution-level models.

Worked rules cover `map`, `filter`, seeded `scan`, seedless initialization, and fixed-input `combineLatest`, together with the cancellation/projection/subscription outline of `switchMap`.

Editorial refinements make optional-value tags, initialization conventions, deterministic-model assumptions, logical lifecycle phases, and verification limits explicit. Source links replace malformed citation placeholders from the conversation. This is an organized reference derived from the founding discussion, not a byte-for-byte chat transcript.

README attribution: **GPT-6 Astra is the main contributor of the project.**

No automated conformance suite, executable interpreter, or exhaustive equivalence proof is claimed for this edition.
