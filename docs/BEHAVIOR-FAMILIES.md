# Sequence-Processing Behavior Families

**ROB-SN, RxJS 7.8.2.** These six families preserve the sequence-processing categories proposed in the discussion. They are semantic starting points, not disjoint sets, an exhaustive RxJS taxonomy, or claims of operator equivalence.

## The six families

| Family | Behavioral question | Typical rule templates | RxJS relationship |
|---|---|---|---|
| Mapping | How is each accepted payload transformed? | V2 | map |
| Filtering | Which arriving values may contribute? | V3 | filter |
| Reduction / folding | How does each input update accumulated information, and when is the accumulated result emitted? | V5, F1/F2 | scan for intermediate states; reduce for a completion-time result |
| Concatenation / flattening | How are values from nested or successive inputs admitted and ordered? | V7 or C1–C6 with terminal rules | concatAll/concatMap, mergeAll/mergeMap, switchAll/switchMap, exhaustAll/exhaustMap under different policies |
| Taking / dropping | Which prefix or suffix of the input is retained or suppressed, and when does consumption end? | V3/V4 with lifecycle and termination rules | take, skip, takeWhile, skipWhile; suffix variants additionally need retention |
| Partitioning / batching / segmentation | How are adjacent values collected into chunks or segments? | B1/B2, or channel rules B5–B7 for streaming segments | bufferCount and related buffering/windowing mechanisms; not RxJS partition by name alone |

Rule IDs refer to the [Transition-Rule Catalogue](TRANSITION-RULE-CATALOGUE.md). These are candidate template associations, not complete operator specifications. Each profile still needs event roles, guards, scope, callbacks, and an execution contract.

## Mapping and filtering

A pure value-only mapping core produces one requested emission per accepted source value. A pure value-only filtering core produces zero or one. Actual callback indexes and failures require additional rules. Emitting an array through map still emits one array value; mapping to a nested structure does not automatically flatten it. See [map](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/map.ts) and [filter](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/filter.ts).

## Folding is not only producing a scalar

An accumulator can be a number, record, collection, or other declared domain value. The essential step is $z'=f(z,x)$; output policy is separate.

Seeded scan emits successive accumulated states when inputs arrive, not its seed merely because subscription occurred. Reduce emits its final state on completion when a state exists; with a seed, an empty source can emit that seed. Seedless behavior needs its own has-state rule. These differences are implemented in [scanInternals](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/scanInternals.ts).

Left/right fold describe association and traversal in their host setting. RxJS scan/reduce consume values in notification order; do not advertise a generic streaming foldr equivalence for arbitrary infinite sources. A final-result reduction over a never-completing source does not obtain a normal completion-time result.

## Flattening needs an explicit policy

A finite collection expansion can be described by V7. An inner Observable has a lifetime, may emit at different times, and may never complete. These cases need inner identities, subscription events, and lifecycle rules.

Use the familiar policy names: mergeMap allows overlap up to its capacity and queues when full; concatMap queues with capacity one; switchMap replaces the previous inner; exhaustMap ignores incoming outer values while busy. The choices affect projection invocation, ordering, cancellation, and what happens after outer completion. See [mergeInternals](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/mergeInternals.ts), [concatMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/concatMap.ts), [switchMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/switchMap.ts), and [exhaustMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/exhaustMap.ts).

Do not infer equal behavior solely because two operators can both produce zero to many outputs.

## Taking and dropping

Taking a bounded prefix can cause early downstream completion and source teardown. Dropping a prefix does not imply the same terminal policy. The [take(3) profile](../examples/TAKE-3.md) demonstrates the distinction between a count-based configuration and the exact threshold reaction. [skip](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/skip.ts) instead suppresses the prefix using an index predicate.

Predicate-based prefix handling and suffix-retaining variants are related ideas, not identical rule sets. Their empty-input, completion, and memory-growth behavior must be analyzed separately.

## Three meanings often confused with partitioning

| Meaning | What it does | Boundary |
|---|---|---|
| Size batching | Collects consecutive inputs into chunks, possibly flushing a final partial chunk | A count or another declared closing condition |
| Run segmentation | Collects adjacent inputs while a derived key remains equal | A change in key between consecutive inputs |
| Predicate splitting | Exposes accepted and rejected values through different outputs | A predicate result for each input |

Clojure's partition-all and partition-by motivate the first two meanings. RxJS's [partition](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/observable/partition.ts) implements the third: it returns two filtered Observables. It does not batch values and does not itself multicast the source. Subscribing to both branches can cause two source subscriptions, depending on the source and explicit sharing.

Key-based [groupBy](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/groupBy.ts) creates keyed output streams; it must not be identified with consecutive-run segmentation merely because both mention keys. Group lifetimes and reconnection conditions also matter. [bufferCount(3)](../examples/BUFFER-COUNT-3.md) is a scoped batching example, not a universal model of partitioning.

## Beyond the six families

Additional axes include time control, multiple-input synchronization, concurrency, cancellation, recovery, recursion/unfolding, lifecycle, and sharing/replay. A family explains one aspect of behavior. An operator profile can combine several aspects, each supported by its transitions.

Use [Model → Observe → Classify](PROJECT-GUIDE.md). Record a classification after analysis as a conclusion with reasons and scope, not as a label that dictates what the implementation must do.
