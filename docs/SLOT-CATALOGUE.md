# ROB-SN Slot Catalogue

**Baseline:** RxJS 7.8.2. **Status:** Proposed, extensible vocabulary; not an exhaustive API-conformance claim.

The five slots contain different kinds of things. Only some are persistent state. This catalogue names possibilities; the [transition rules](TRANSITION-RULE-CATALOGUE.md) determine reactions.

| Slot | Space | Role |
|---|---|---|
| Event | $e\in E$ | The event currently being handled |
| Lifecycle | $\ell\in L$ | Retained resource and subscription bookkeeping |
| Memory | $m\in M$ | Retained processing information |
| Next Actions | $\alpha\in A^*$ | Ordered instructions produced by a reaction |
| Execution Status | $q\in Q$ | Whether a scoped execution is open, or how it ended |

## 1. Event Slot

Use tagged events with identities and payloads, not only unqualified names.

| Family | Forms | Meaning |
|---|---|---|
| Notifications | `Next(port, value)`, `Error(port, error)`, `Complete(port)` | A value, failure, or normal end from an identified input |
| Activation | `Start(scope)` | Activate a not-yet-started machine, if this convention is selected |
| Cancellation | `Unsubscribe(scope)` | End a subscriber's participation without a completion notification |
| Shared participation | `SubscriberJoined(id)`, `SubscriberLeft(id)` | Change membership of a modeled coordinator |
| Scheduled events | `TimerFired(timerId)` | Deliver an identified scheduled event |
| Function outcomes | `Returned(callId, value)`, `Threw(callId, error)` | Explicit return boundaries in detailed models |
| Action outcomes | `ActionFinished(actionId, result)` | A modeled action returns control |
| Resumption | `Resume(frameId)` | Resume previously suspended work |

Ports can represent the main source, a joined source, an inner subscription, notifier, duration signal, opening/closing boundary, or retry/reset control. A role is not an additional notification kind. `Next(source, 42)` and `Next(inner7, 42)` need not cause the same reaction.

For a port set $P$, port-specific payload sets $X_p$, and error set $\mathsf{Err}$:

$$
E_N=
\{\operatorname{Next}(p,x)\mid p\in P,\ x\in X_p\}
\uplus\{\operatorname{Error}(p,\xi)\mid p\in P,\ \xi\in\mathsf{Err}\}
\uplus\{\operatorname{Complete}(p)\mid p\in P\}.
$$

Add only the other event families needed by the chosen model. `SourceNext(x)`, `SourceError(e)`, and `SourceComplete` are readable aliases for notifications from the distinguished source port; the foundation also uses analogous inner-specific names.

`Unsubscribe` is lifecycle control, not a fourth Observable notification. `cancelled` is a status, not an arriving value. This distinction follows [Subscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscriber.ts).

Time can enrich an event as $(t,i,e)$, where $t$ is supplied by a declared clock and $i$ records processing order. These coordinates do not choose scheduler tie-breaking or replace nested execution semantics.

## 2. Lifecycle Slot

Lifecycle is usually a registry of several resources, not one global phase.

| Proposed resource phase | Meaning |
|---|---|
| Absent | No resource currently occupies the identified slot |
| Acquiring | Creation or connection has begun but has not returned |
| Active | The resource is available or subscription is participating |
| Releasing | Disposal is underway |
| Released | The modeled release operation has finished |

A record can contain identity, kind, owner, phase, parent/dependent relationships, participating subscribers, and ordered teardown obligations. Not every resource visits every phase. Exact models must add failed or interrupted-operation outcomes where relevant; this five-label list is not a complete lifecycle implementation.

Resource kinds include source/inner subscriptions, scheduled tasks, output channels, and shared connections. Owners are concrete execution scopes or coordinators, not an implicit global machine. Prefer one authoritative record per fact: an inner identity retained for selection may reference the lifecycle registry rather than duplicating its lifecycle status.

`Subscribe`, `Cancel`, `Schedule`, and `DisposeOwned` are actions affecting resource bookkeeping, not lifecycle phases. Disposal must be scope-relative. A participant leaving does not necessarily dispose a shared connection; [share](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/share.ts) has reference-count and reset policies.

The Lifecycle Slot includes retained facts. Setup and cleanup rules also appear in events, actions, and the execution contract. The five slots are explanatory views, not five isolated implementation modules.

## 3. Memory Slot

Define memory shapes and value domains rather than attempting a finite list of every payload.

| Shape | Value space | Interpretation |
|---|---|---|
| Memoryless core | $\{\star\}$ | No retained processing data; never use the empty state space |
| Flag | $\{\mathrm{false},\mathrm{true}\}$ | A retained condition |
| Counter | $\mathbb N_0$ or a declared bounded domain | Number of relevant events |
| Accumulator | $Z$ | A domain-specific running value |
| Optional value | $\operatorname{Option}(X)$ | No value yet, or a retained value |
| Fixed slots | $M_1\times\cdots\times M_n$ | Several positioned facts |
| Buffer/history | $X^*$ | An ordered sequence preserving repetition |
| Queue | $X^*$ with declared insertion/removal rules | Ordered pending work |
| Finite set | $\mathcal P_{\mathrm{fin}}(X)$ | Membership when order is irrelevant |
| Finite dictionary | $K\rightharpoonup_{\mathrm{fin}}V$ | Keyed values |
| Time information | $T$, $\operatorname{Option}(T)$, or a record | Deadlines or observed activity times |
| Continuation | $\mathsf{Frame}^*$ | Suspended work in an execution-level model |
| Composite | Products and tagged unions of these spaces | Multiple kinds of memory together |

Use:

$$
\operatorname{Option}(X)=\{\operatorname{None}\}\uplus\{\operatorname{Some}(x)\mid x\in X\},
\qquad X^*=\bigcup_{n\ge0}X^n.
$$

`None` differs from `Some(undefined)` and `Some(null)`. An empty sequence is a value. A missing value is a different alternative. The same sequence shape can implement a buffer or queue, but its transition rules give it that role.

Unbounded mathematical counters and buffers create infinite state spaces. This does not prevent specifying the spaces by a finite definition; it means the model is not necessarily a finite-state machine. JavaScript numeric precision and finite resources require narrower domains for implementation-exact claims.

For every component, record initial value, owner, updates, read triggers, reset conditions, and release conditions. Fresh bookkeeping does not deep-clone captured seed objects. A value-only `map` can have singleton processing memory, while its indexed RxJS implementation needs a counter; see [map](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/map.ts).

## 4. Next Actions Slot

| Family | Constructors |
|---|---|
| Delivery | `Emit(target, value)` |
| Terminal delivery | `Complete(target)`, `Fail(target, error)` |
| Subscriptions | `Subscribe(id, input)`, `Cancel(id)` |
| Scheduling | `Schedule(timerId, deadline, scheduler)`, `CancelTimer(timerId)` |
| Output resources | `CreateOutput(id, specification)` |
| Teardown | `RegisterTeardown(scope, operation)`, `DisposeOwned(scope)` |
| Function invocation, detailed models | `Invoke(callId, function, arguments)` |

These are notation-level instructions, not literal RxJS APIs. Omit `target` when there is only one output. Each constructor requires an interpretation. Model individual writes as actions only when that execution detail is needed; normally memory changes are in $s'$.

```text
[]                                  no instructions
[Emit([])]                          one instruction emitting an empty array
[Emit(undefined)]                   one instruction emitting undefined
[Emit(a), Emit(a)]                   two ordered emissions
[Cancel(old), Subscribe(new, input)] two resource-control instructions
```

Action sequences preserve order and repetition. Requested emission count differs from total action count and potentially from delivered notification count. Cancellation during the first delivery can make a later delivery ineligible. See [Behavioral Qualities](BEHAVIORAL-QUALITIES.md).

## 5. Execution Status Slot

For one activated downstream execution:

$$
Q=\{\mathrm{running},\mathrm{completed},\mathrm{errored},\mathrm{cancelled}\}.
$$

`running` means open, including silent waiting. `completed` and `errored` describe terminal output outcomes. `cancelled` describes ended participation without that output terminal notification. Add `notStarted` only when activation is an explicit event; otherwise use a separate initializer.

These are logical outcomes, not direct aliases for RxJS's `closed` and `isStopped`. Completion/error initiate unsubscription as cleanup; that does not overwrite the original outcome with `cancelled`. Cleanup can continue after terminal delivery. A source can complete while the output remains running, as in [switchMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/switchMap.ts).

In a macrostep table, a terminal post-state describes the outcome after the listed delivery actions. Do not install a closed downstream subscriber before a preceding `Emit`. Detailed models may need completing, delivery, and disposal phases rather than treating the reaction as atomic.

A shared coordinator may create a fresh connection generation. It must not reopen an already terminated subscriber. Scope status separately for each participant and owned execution.

## 6. Combinations, transitions, and constraints

A useful ambient persistent state space is $S=Q\times L\times M$, restricted by declared invariants. More detailed execution components can refine it.

$$
\delta_\theta((q,\ell,m),e)=((q',\ell',m'),\alpha).
$$

The transition graph is:

$$
\mathcal R_\theta=\{(s,e,s',\alpha)\mid\delta_\theta(s,e)=(s',\alpha)\}.
$$

Each entry relates a current configuration and event to a next configuration and ordered actions. The actions are not independently chosen after the fact. Define admissible inputs, valid state combinations, initial states, and reachable histories; not every Cartesian-product combination is meaningful.

At `seen=0`, `running`, with one source connection, `take(3)` and `skip(3)` can have the same abstract state and incoming value but different emissions. Their rules, not their slot shapes, distinguish them. See [take](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/take.ts) and [skip](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/skip.ts).

> Slot spaces define possibilities. Rules and the execution contract define behavior. Completeness must be argued per declared operator profile, not inferred from the length of this catalogue.
