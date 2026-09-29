# Change Log

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
