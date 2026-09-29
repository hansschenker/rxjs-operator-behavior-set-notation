# Worked ROB-SN Profile: take(3)

**Baseline:** RxJS 7.8.2. **Level:** Behavioral macrosteps. **Evidence:** Source-reviewed; no runtime tests executed for this consolidation.

## What flows and why

Values arrive from one source. Forward at most the first three, then complete the output and release this execution's source subscription. Source completion before three values completes the output normally. Explicit consumer cancellation delivers neither an additional value nor completion.

The count is fixed at three. Other counts, invalid parameters, deprecated variants, reentrant interaction, teardown failure, mutable effects in consumer code, and an implementation-exact Subscriber model are outside this profile. An unshared source subscription is assumed; cancelling it is not a guarantee of physical cancellation of independent producer work.

## Slots and initialization

| Slot | Contents |
|---|---|
| Event | SourceNext(x), SourceComplete, SourceError(error), Unsubscribe |
| Memory | Number c of accepted source values |
| Lifecycle | This execution's identified upstream subscription and its teardown obligations |
| Execution Status | running, completed, errored, cancelled |
| Next Actions | Ordered Emit(x), Complete, Fail(error), DisposeOwned instructions |

Use a separate initializer. It creates fresh count bookkeeping with c=0, establishes the running scope and its cancellation relationship, and requests source subscription. Synchronous source delivery can begin during that subscription; the count and ownership relationship must already be ready. No Start event is used afterward.

Let $Q=\{\mathrm{running},\mathrm{completed},\mathrm{errored},\mathrm{cancelled}\}$ and $M=\{0,1,2,3\}$. Lifecycle state is owned by the execution interpreter. The table abbreviates $(q,\ell,c)$ to $(q,c)$ while listing lifecycle effects explicitly.

## Guarded transitions

| Current condition | Event | Logical post-state | Ordered actions |
|---|---|---|---|
| running, c<2 | SourceNext(x) | running, c+1 | [Emit(x)] |
| running, c=2 | SourceNext(x) | completed, 3 | [Emit(x), Complete, DisposeOwned] |
| running | SourceComplete | completed, c | [Complete, DisposeOwned] |
| running | SourceError(error) | errored, c | [Fail(error), DisposeOwned] |
| running | Unsubscribe | cancelled, c | [DisposeOwned] |
| Terminal and cleanup finished | Later ordinary input or repeated Unsubscribe | Unchanged | [] at the modeled downstream-delivery level |

These are alternative guarded reactions, not instructions to combine indiscriminately. The terminal post-state summarizes the completed macrostep: the third value is delivered before Complete. Do not set the actual Subscriber to closed before that Emit. DisposeOwned is an abstraction of the actual cleanup, not a second unsubscribe after terminal cleanup already performed by the runtime.

Stable running-state invariant: $0\le c<3$. Every terminal state has $0\le c\le3$. A terminal state caused by accepting the third value has c=3; earlier source completion, error, or cancellation may retain a smaller count.

A rule for impossible state/event pairs is not silently invented. The table specifies the reachable states and admitted event categories at this abstraction level. Post-terminal diagnostic callbacks are outside its observations.

## Discriminating traces

Events are in processing order; no additional scheduler is introduced.

| Incoming event | Before | After | Requested actions |
|---|---|---|---|
| SourceNext(a) | running, 0 | running, 1 | [Emit(a)] |
| SourceNext(b) | running, 1 | running, 2 | [Emit(b)] |
| SourceNext(c) | running, 2 | completed, 3 | [Emit(c), Complete, DisposeOwned] |

A compliant source subscription is stopped at this point. A later attempted notification is not delivered to this stopped output.

From `running, 2`, Unsubscribe instead gives `cancelled, 2` with only DisposeOwned. SourceComplete instead gives `completed, 2` with Complete and cleanup. This distinguishes the cause and resulting notifications.

## Catalogue and classification

L1 (or its separate-initializer equivalent), V4, V1, F1, F4, L3, and L4 contribute to the profile. V4 alone does not specify take: the guards and emit-before-complete order do.

Derived qualities: per-subscription bounded count memory; source-value trigger; one requested emission for each accepted prefix value; no introduced timing policy; normal early completion at the threshold; cancellation of participation through teardown; no implicit sharing. Classification: taking a bounded prefix with count-controlled termination.

## Verification evidence and limits

[RxJS take source](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/take.ts), blob `b2054e78b2d4805f01b8f1fa8618ee3e7fe569b9`, increments seen before emission and checks the completion condition after emission. The source includes a reentrancy-sensitive comparison; this profile does not claim to model every nested case.

[Subscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscriber.ts) distinguishes stopped notification delivery, completion/error, and unsubscription. [Upstream take tests](https://github.com/ReactiveX/rxjs/blob/7.8.2/spec/operators/take-spec.ts) are further verification targets, not tests claimed to have run here.

Proposed checks: fewer than three inputs, exactly three, more than three from a cancellation-aware synchronous producer, empty/never sources, source error, two independent subscriptions, and cancellation during an emission. The last case needs an execution-level refinement rather than this nonreentrant macrostep table.
