# Worked ROB-SN Profile: bufferCount(3)

**Baseline:** RxJS 7.8.2. **Configuration:** bufferCount(3) with default nonoverlapping cadence. **Level:** Behavioral macrosteps. **Evidence:** Source-reviewed; no runtime tests executed for this consolidation.

## What flows and why

Values arrive from one source. Remember consecutive values until there are three, then emit one array containing that batch. Source completion emits a remaining nonempty partial batch before completion. Source error and consumer cancellation discard pending values instead of flushing them.

This is one unshared execution with fresh private buffer bookkeeping, normal cleanup, no reentrancy or consumer mutation, and no custom startBufferEvery. Overlapping/gapped configurations, invalid numeric inputs, exact intermediate writes, and cleanup exceptions are excluded.

## Slots and initialization

| Slot | Contents |
|---|---|
| Event | SourceNext(x), SourceComplete, SourceError(error), Unsubscribe |
| Memory | Pending ordered sequence b with length below three between reactions |
| Lifecycle | Owned upstream subscription and cleanup obligation |
| Execution Status | running, completed, errored, cancelled |
| Next Actions | Emit(batch), Complete, Fail(error), DisposeOwned |

Choose a separate initializer: establish private b=[] and the running scope before source subscription can deliver. There is no implicit sharing and no seed emission.

For a payload domain X, use $M=\bigcup_{k=0}^{2}X^k$ for stable retained memory. Full batches are emitted and released within one behavioral reaction. Lifecycle bookkeeping is part of the full state but abbreviated in the table below.

## Guarded transitions

Write $b\mathbin{\|}[x]$ for sequence append in these equations; it is not set union. Let $b_x$ denote that appended sequence.

| Current condition | Event | Logical post-state | Ordered actions |
|---|---|---|---|
| running, length(b)<2 | SourceNext(x) | running, b_x | [] |
| running, length(b)=2 | SourceNext(x) | running, [] | [Emit(b_x)] |
| running, b nonempty | SourceComplete | completed, [] | [Emit(b), Complete, DisposeOwned] |
| running, b=[] | SourceComplete | completed, [] | [Complete, DisposeOwned] |
| running | SourceError(error) | errored, [] | [Fail(error), DisposeOwned] |
| running | Unsubscribe | cancelled, [] | [DisposeOwned] |
| Terminal and cleanup finished | Later ordinary input or repeated Unsubscribe | Unchanged | [] at the modeled downstream-delivery level |

The emitted container is not the subsequently reused pending buffer. Payload objects are not deep-cloned by this mathematical container description. A terminal post-state is the macrostep outcome, not a command to close the actual destination before emitting a final batch. Cleanup is represented once through DisposeOwned; the interpreter maps it to actual terminal teardown.

Stable-state invariant: while running, b contains zero, one, or two pending values; terminal memory is empty in this abstraction. The actual implementation can free its buffer variable rather than storing an empty sequence. The model abstracts that implementation representation.

## The discriminating same-memory experiment

After inputs 1 and 2, all alternatives begin at the same state: `running`, b=[1,2], with one owned source subscription.

| Next event | Requested output | Result |
|---|---|---|
| SourceNext(3) | Emit([1,2,3]) | Still running with empty pending memory |
| SourceComplete | Emit([1,2]), then Complete | Completed and cleaned up |
| SourceError(e) | Fail(e), no batch | Errored and cleaned up |
| Unsubscribe | No downstream notification | Cancelled and cleaned up |

These are alternative histories, not four consecutive events. They show why a generic stop state cannot replace completion, error, and cancellation rules.

## Catalogue and derived classification

Use B1/B2 for batch construction, F2 for partial final flush, F1 for completion without pending values, F4 for unrecovered error, and L3/L4 for cancellation and stopped delivery. Initialization is the separate equivalent of L1.

Derived qualities: at most two values retained between macrosteps; ordered batches preserving duplicates; source-count release trigger; zero or one requested emission per source-value reaction; an additional possible emission on completion; private state ownership; no introduced scheduler; completion flush but error/cancellation discard.

Classification: nonoverlapping count-based batching. This is not predicate splitting through RxJS partition, and it does not establish the behavior of every bufferCount configuration.

## Verification evidence and limits

[RxJS bufferCount source](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/bufferCount.ts), blob `1d82d2c213fd381bfa8301fdfb0331a955b5181e`, opens buffers on inputs, removes full buffers before delivery, flushes active buffers on completion, and releases storage in finalization. [Subscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscriber.ts) supports the cancellation/terminal distinction.

[Upstream bufferCount tests](https://github.com/ReactiveX/rxjs/blob/7.8.2/spec/operators/bufferCount-spec.ts) are reference targets only. Proposed checks include empty input, one/two/three/four inputs followed by completion, duplicate payloads, source error, explicit cancellation, independent subscriptions, and cancellation during delivery. No runtime outcomes are claimed here; exact interruption cases require the execution contract and additional microsteps.
