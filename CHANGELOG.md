# Change Log

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
