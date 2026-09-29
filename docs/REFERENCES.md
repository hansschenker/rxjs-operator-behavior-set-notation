# Primary References and Evidence

**Baseline: RxJS 7.8.2.** All implementation links below point to the fixed `7.8.2` tag rather than a moving development branch.

The mathematical definitions in this project are proposed definitions. The links below support the version-specific RxJS observations used to motivate and constrain those definitions.

## Value transformation and accumulated state

| Source | Relevant behavior |
|---|---|
| [map.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/map.ts) | Projection, callback index, and result forwarding |
| [filter.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/filter.ts) | Predicate, source index, and conditional forwarding |
| [scan.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/scan.ts) | Seed detection and scan configuration |
| [scanInternals.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/scanInternals.ts) | Accumulated state, first seedless input, and index progression |

## Multiple inputs and inner subscriptions

| Source | Relevant behavior |
|---|---|
| [combineLatest.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/observable/combineLatest.ts) | Per-input slots, readiness, independent completion counter, snapshot arrays, and subscription setup order |
| [switchMap.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/switchMap.ts) | Previous-inner cancellation before projection, inner assignment/subscription, and delayed result completion |
| [innerFrom.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/observable/innerFrom.ts) | ObservableInput conversion and source-specific subscription behavior |

## Lifecycle and sharing

| Source | Relevant behavior |
|---|---|
| [Observable.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Observable.ts) | Subscription activation and source execution |
| [Subscriber.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscriber.ts) | Notification handling, stopped/closed distinctions, and terminal cleanup |
| [Subscription.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscription.ts) | Resource ownership, finalizers, unsubscription, and teardown failures |
| [OperatorSubscriber.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/OperatorSubscriber.ts) | Operator handler error handling and finalization |
| [share.ts](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/share.ts) | Shared connection state, reference counting, and reset policies |

## Upstream tests for future conformance work

- [combineLatest operator/creation tests](https://github.com/ReactiveX/rxjs/blob/7.8.2/spec/observables/combineLatest-spec.ts)
- [switchMap tests](https://github.com/ReactiveX/rxjs/blob/7.8.2/spec/operators/switchMap-spec.ts)
- [scan tests](https://github.com/ReactiveX/rxjs/blob/7.8.2/spec/operators/scan-spec.ts)
- [map tests](https://github.com/ReactiveX/rxjs/blob/7.8.2/spec/operators/map-spec.ts)
- [filter tests](https://github.com/ReactiveX/rxjs/blob/7.8.2/spec/operators/filter-spec.ts)

These are reference locations, not a statement that every case in those files has been reviewed or executed for this project.

## Initial-edition verification record

During repository preparation on 29 September 2026, the following source content was retrieved directly through the GitHub connector:

| Inspected file | Retrieved blob SHA | Review focus |
|---|---|---|
| `src/internal/operators/switchMap.ts` | `0ded7ba9fd788249045b40abd6aa5b61f2bfc703` | Replacement sequence and result-completion condition |
| `src/internal/observable/combineLatest.ts` | `9044060faa6fb4a50a0020cac92490d02fb96a89` | Implementation section containing input setup, readiness, and completion counters |
| `src/internal/operators/scanInternals.ts` | `f2c2e5a4e98888976e9df78edc90bb2481043a56` | Seedless initialization and callback-index progression |

The remaining source links preserve supporting primary-reference pointers from the founding explanation or identify follow-up inspection targets. They are not represented as newly executed checks.

**No automated RxJS runtime tests, theorem-prover checks, or complete small-step equivalence proof were run as part of this documentation-only initialization.** The worked equations are scoped behavioral models; the reentrancy discussion records obligations for a future execution-level model.

A future conformance result must record its exact RxJS version, selected configuration, executed command, observations, result, and remaining limitations. Never turn an intended test into a claimed passing test.
