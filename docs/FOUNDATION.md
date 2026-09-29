# Set-Theoretic Foundations of RxJS Operator Behavior

**Main contributor: GPT-6 Astra**  
**Reference baseline: RxJS 7.8.2**  
**Initial documentation edition: 29 September 2026**

This reference preserves and organizes the foundational discussion that led to `rxjs-operator-behavior-set-notation`. The definitions are proposals for our notation, not an official RxJS standard.

> Sets describe the possible states, events, and actions. Transition rules describe behavior. Ordered sequences and an execution contract preserve the order in which that behavior happens.

## 1. The central distinction: sets and their members

An informal formula such as `f(S, E) -> (S', A)` expresses the right intuition but mixes sets of possibilities with individual members of those sets.

The function signature is:

$$
\boxed{\delta:S\times E\longrightarrow S\times A^*}
$$

One application of that function is:

$$
\boxed{\delta(s,e)=(s',\alpha)}
$$

| Symbol | Meaning |
|---|---|
| $S$ | The set of possible machine states |
| $s\in S$ | The current state |
| $s'\in S$ | The next state |
| $E$ | The set of possible incoming events |
| $e\in E$ | The event currently being processed |
| $A$ | The set of individual actions |
| $\alpha\in A^*$ | An ordered finite sequence of actions |
| $\delta$ | The transition function |

The Cartesian product $S\times E$ contains pairs consisting of one state and one event. The state space does not change from $S$ to a different $S'$. The machine moves between members of the same declared space:

$$
s\in S\quad\longrightarrow\quad s'\in S.
$$

Our practical reading is:

```text
What is remembered + What arrived
                  ↓
What must now be remembered + What must happen next
```

The plus signs are explanatory, not arithmetic.

For fixed operator parameters $\theta$, define the core machine:

$$
\mathcal M_\theta=(S,E,A,s_0,\delta_\theta).
$$

The parameters can include a projection, predicate, seed, duration, scheduler selection, or concurrency policy. The initial state satisfies $s_0\in S$.

An Observable/operator definition describes behavior; it is not itself the running subscription instance. State ownership and activation belong to the execution contract. In particular, subscription to an existing hot producer must not be confused with starting that producer. See [Observable](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Observable.ts) and [share](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/share.ts).

## 2. Actions form a sequence, not an unordered set

Define:

$$
A^*=\bigcup_{n\in\mathbb N_0}A^n.
$$

This is the set of all finite sequences of actions. In particular, $A^0=\{[]\}$ contains the empty sequence.

```text
[]                                  no actions
[Emit(10)]                          one action
[Emit(10), Emit(20)]                two ordered actions
[Emit(10), Emit(10)]                one action repeated twice
[Cancel(old), Subscribe(new)]       ordered control actions
```

Order matters:

$$
[\operatorname{Cancel}(old),\operatorname{Subscribe}(new)]
\neq
[\operatorname{Subscribe}(new),\operatorname{Cancel}(old)].
$$

An ordinary set cannot express this difference:

$$
\{\operatorname{Cancel}(old),\operatorname{Subscribe}(new)\}
=
\{\operatorname{Subscribe}(new),\operatorname{Cancel}(old)\}.
$$

Sets also discard multiplicity:

$$
\{\operatorname{Emit}(10),\operatorname{Emit}(10)\}
=\{\operatorname{Emit}(10)\}.
$$

Therefore, $A$ is the action alphabet and $A^*$ contains the possible action programs produced by reactions. Never replace an action program with a powerset of actions.

Typical action constructors include `Emit(value)`, `Complete`, `Fail(error)`, `Subscribe(id, input)`, `Cancel(id)`, `Schedule(timerId, deadline)`, `CancelTimer(timerId)`, and `DisposeOwned`. These are notation-level instructions, not literal RxJS APIs. A particular model declares only the instructions it needs and gives them an interpretation.

Sequence concatenation, written $\alpha\cdot\beta$, preserves order and repetition. It is associative and has `[]` as its identity. This observation concerns action-sequence algebra; it does not prove that arbitrary RxJS pipelines or reentrant executions can be simplified by treating reactions as atomic blocks.

Event histories and buffered values likewise need sequences when order and repetition matter. A whole execution may be infinite even though an individual small step produces a finite action list.

## 3. Event spaces are tagged unions

A useful event space is:

$$
E=E_{\mathrm{source}}\uplus E_{\mathrm{inner}}\uplus E_{\mathrm{timer}}\uplus E_{\mathrm{lifecycle}}.
$$

The disjoint union symbol $\uplus$ means that every alternative carries a tag. Different event categories remain distinguishable even when their payloads happen to be equal.

### Source notifications

For values in $X$ and error values in $\mathsf{Err}$:

$$
\begin{aligned}
E_{\mathrm{source}}={}&\{\operatorname{SourceNext}(x)\mid x\in X\}\\
&\uplus\{\operatorname{SourceError}(\xi)\mid\xi\in\mathsf{Err}\}\\
&\uplus\{\operatorname{SourceComplete}\}.
\end{aligned}
$$

Set-builder notation $\{f(x)\mid x\in X\}$ means the set of all such $f(x)$ for elements $x$ of $X$.

For multiple sources, identify the input port:

```text
SourceNext(sourceId, value)
SourceError(sourceId, error)
SourceComplete(sourceId)
```

Each port can have its own payload space. A notifier, duration input, or boundary stream must also be identifiable; it is not interchangeable with a data input simply because both emit `next` notifications.

### Inner notifications

Higher-order behavior needs identities for inner subscription instances:

```text
InnerNext(innerId, value)
InnerError(innerId, error)
InnerComplete(innerId)
```

The identity belongs to the event. It must not be inferred from the emitted value.

### Timer and lifecycle events

For timer identities in $R$:

$$
E_{\mathrm{timer}}=\{\operatorname{TimerFired}(r)\mid r\in R\}.
$$

A lifecycle vocabulary may include:

$$
E_{\mathrm{lifecycle}}=\{\operatorname{Start},\operatorname{Unsubscribe}\}.
$$

`Start` provides a place for subscription setup and initial scheduling. A model using it must define a not-started phase and handle activation exactly once. Alternatively, define a separate initializer that returns $(s_0,\alpha_0)$ and omit `Start` from subsequent input events. Do not mix the two conventions silently.

**Unsubscription is not completion.** RxJS 7.8.2's `unsubscribe()` stops and disposes the subscription without invoking the downstream completion handler. See [Subscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscriber.ts).

A more detailed execution model can add callback-return, callback-failure, action-return, and internal-resume events. Not every operator needs every event category.

## 4. State spaces describe exactly what is retained

Instead of saying “the operator has internal state,” specify the set of which that state is a member.

### Memoryless behavioral core

Use a singleton:

$$
S=\{\star\}.
$$

There is one possible state. The placeholder $\star$ carries no remembered data.

Do not use $S=\varnothing$: an empty state space would have no initial state and no running instance.

### Accumulated state

For accumulator values in $Z$:

$$
S=Z.
$$

A mathematical running sum might use $Z=\mathbb Z$. This is an abstract arithmetic domain, not a claim that JavaScript `number` implements unbounded integers exactly.

### Optional retained value

Use a tagged optional space:

$$
\operatorname{Option}(X)=\{\operatorname{None}\}\uplus\{\operatorname{Some}(x)\mid x\in X\}.
$$

For readability, later examples write $\bot$ for `None` and write $x$ for `Some(x)` when the distinction is unambiguous. The missing-value marker is separate from every valid payload, including JavaScript `undefined` and `null`.

### Several facts remembered together

Use a Cartesian product:

$$
S=S_1\times S_2\times\cdots\times S_n.
$$

For example:

$$
S=\operatorname{Option}(X)\times\mathbb N_0\times\{\mathrm{false},\mathrm{true}\}.
$$

A state $(\bot,0,\mathrm{false})$ could contain a pending value, counter, and completion flag.

| Retained structure | Representation |
|---|---|
| Ordered buffer of values | $X^*$ |
| Optional current inner identity | $\operatorname{Option}(J)$ |
| Unordered finite collection of identities | $\mathcal P_{\mathrm{fin}}(J)$ |
| One optional value slot per input | $\prod_{j\in I}\operatorname{Option}(X_j)$ |
| Ordered suspended work | $\mathsf{Frames}^*$ |

Use a finite powerset only when the order of members is irrelevant. For example, membership in a completed-input set can be unordered; teardown traversal may require an ordered structure instead.

These spaces need not be finite. An unbounded accumulator or buffer gives a general stateful transducer, not necessarily a finite-state machine.

## 5. Behavior as a set of transitions

The transition function can itself be represented by its graph:

$$
\mathcal R_\delta=\{(s,e,s',\alpha)\in S\times E\times S\times A^*\mid\delta(s,e)=(s',\alpha)\}.
$$

The relation contains each permitted combination of current state, incoming event, next state, and action sequence.

For a deterministic, total function:

$$
\forall s\in S,\ \forall e\in E,\quad\exists!(s',\alpha)\in S\times A^*
$$

such that $(s,e,s',\alpha)\in\mathcal R_\delta$. The symbol $\exists!$ means “there exists exactly one.”

This creates a useful completeness question:

> Have we defined exactly one reaction for every state/event pair in the declared model?

A specification can instead restrict itself to an explicitly defined domain $D\subseteq S\times E$ of admissible pairs. Then write $\delta:D\to S\times A^*$ and state the protocol assumptions that define $D$.

Do not silently interpret an omitted rule as an empty action list. Distinguish a deliberate no-op, an invalid input, and an unspecified case. Piecewise rules need exhaustive, nonoverlapping guards, or an explicit rule-priority policy.

A state-validity condition is represented by $\mathrm{Inv}\subseteq S$. Require $s_0\in\mathrm{Inv}$ and preservation of validity for every transition in scope. For a microstep model, distinguish stable-state invariants from conditions allowed to be temporarily false during an operation.

## 6. Worked value-handling rules

Unless stated otherwise, these examples describe a behavioral core with pure, terminating, nonthrowing callbacks, no reentrant external interaction, and no use of callback indexes. Lifecycle rules are added in Section 7. These simplifications are explicit boundaries, not claims about every legal RxJS program.

### 6.1 `map`: change the emitted value

Let $g:X\to Y$ and $S=\{\star\}$. Then:

$$
\delta(\star,\operatorname{Next}(x))=(\star,[\operatorname{Emit}(g(x))]).
$$

The state is unchanged; the emission payload changes. This corresponds to the projection-and-forward behavior of [map](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/map.ts).

RxJS 7.8.2 also maintains a callback index. An indexed behavioral model is:

$$
\delta(j,\operatorname{Next}(x))=(j+1,[\operatorname{Emit}(g(x,j))]),\qquad j\in\mathbb N_0.
$$

Therefore, “stateless map” refers to the value-only core under its declared assumptions. It does not mean that the full implementation has no counter or lifecycle state.

### 6.2 `filter`: decide whether an emission exists

Let $p:X\to\{\mathrm{true},\mathrm{false}\}$ and $S=\{\star\}$. Then:

$$
\delta(\star,\operatorname{Next}(x))=
\begin{cases}
(\star,[\operatorname{Emit}(x)])&p(x)=\mathrm{true},\\
(\star,[])&p(x)=\mathrm{false}.
\end{cases}
$$

A rejected input produces no emission action. It does not become another payload. RxJS's [filter](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/filter.ts) also supplies an index to its predicate, so a full indexed model retains and increments it even for rejected inputs.

### 6.3 Seeded `scan`: change memory and emit the new memory

Let $\rho:Z\times X\to Z$, $S=Z$, and $s_0=z_0$. Define $z'=\rho(z,x)$. Then:

$$
\delta(z,\operatorname{Next}(x))=(z',[\operatorname{Emit}(z')]).
$$

For a running sum:

```text
Current state    Event       Next state    Actions
------------------------------------------------------
0                Next(2)     2             [Emit(2)]
2                Next(3)     5             [Emit(5)]
5                Next(4)     9             [Emit(9)]
```

The output is derived from the new state, not just the incoming value. The seed initializes memory; subscription alone does not emit it. Source completion does not re-emit the accumulator. An empty seeded scan emits no `next` value. See [scan](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/scan.ts) and [scanInternals](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/scanInternals.ts).

For a homogeneous seedless model with values and accumulated states in $X$, use $S=\operatorname{Option}(X)$ and $s_0=\bot$:

$$
\delta(\bot,\operatorname{Next}(x))=(x,[\operatorname{Emit}(x)]).
$$

Later values use the accumulator rule. The first input becomes the state without calling the accumulator. A fuller indexed model retains the source index: RxJS increments that index on every input, including the first seedless input, so the accumulator's first invocation uses index 1. Heterogeneous accumulator overloads require a correspondingly richer state and output space. These details are visible in [scanInternals](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/scanInternals.ts).

### 6.4 `combineLatest`: update a slot and test readiness

Scope: a fixed list of $n\geq1$ input observables, without the deprecated scheduler/result-selector variants. Inputs obey their notification protocol. Subscription setup and exact synchronous propagation remain part of the execution contract.

Let $I=\{1,\ldots,n\}$ and:

$$
S_{\mathrm{values}}=\prod_{j\in I}\operatorname{Option}(X_j),\qquad L_0=(\bot,\ldots,\bot).
$$

Define:

$$
\operatorname{ready}(L)\iff\forall j\in I,\ L_j\neq\bot.
$$

For an input from port $j$, first set $L'=L[j\leftarrow x]$. Then:

$$
\delta(L,\operatorname{Next}_j(x))=
\begin{cases}
(L',[\operatorname{Emit}((L'_1,\ldots,L'_n))])&\operatorname{ready}(L'),\\
(L',[])&\neg\operatorname{ready}(L').
\end{cases}
$$

The emitted tuple is a snapshot of the current slots. Updating a later slot must not mutate the previously emitted tuple container; payload objects themselves need not be deep-cloned. RxJS 7.8.2 uses a copied values array for delivery. See [combineLatest implementation](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/observable/combineLatest.ts).

```text
Current memory    Event         New memory    Actions
----------------------------------------------------------------
(⊥, ⊥)            Next₁(10)      (10, ⊥)       []
(10, ⊥)           Next₂(20)      (10, 20)      [Emit((10, 20))]
(10, 20)          Next₁(11)      (11, 20)      [Emit((11, 20))]
```

The memory is a tuple of input-specific slots, not a set of received values. The tuple `(10, 10)` preserves two input positions; the set `{10}` does not.

For completion, add $C\subseteq I$, the completed-input set. The full stable-state memory can be $(L,C)$, initially $(L_0,\varnothing)$. On completion of port $j$, set $C'=C\cup\{j\}$ and preserve its latest slot. Complete the result when $C'=I$; otherwise remain open without emitting a tuple just because a source completed.

**Readiness and completion are separate predicates.** In RxJS 7.8.2, a port that completes without a value does not by itself trigger immediate downstream completion. Consequently, `combineLatest([EMPTY, NEVER])` remains silent and open. The active-input counter and first-value counter are independent in the [implementation](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/observable/combineLatest.ts). This detail must not be replaced by the intuitive but inaccurate rule “a tuple is impossible, therefore complete immediately.”

The zero-input overload is outside this particular $n\geq1$ model and must be specified separately when analyzing the whole API.

## 7. Lifecycle is part of the model

For a simple seeded `scan` behavioral model, define logical phases:

$$
Q=\{\mathrm{running},\mathrm{completed},\mathrm{errored},\mathrm{cancelled}\},\qquad\widehat S=Q\times Z.
$$

After successful initialization, the running initial state is $(\mathrm{running},z_0)$. This section uses a separate initializer; it does not process a second `Start` event in a running state.

Representative terminal macro-rules are:

| Event while running | Next logical state | Ordered actions |
|---|---|---|
| `SourceComplete` | `(completed, z)` | `[Complete, DisposeOwned]` |
| `SourceError(ξ)` | `(errored, z)` | `[Fail(ξ), DisposeOwned]` |
| `Unsubscribe` | `(cancelled, z)` | `[DisposeOwned]` |

`DisposeOwned` abstracts release of resources owned by the execution. The distinction between notification delivery and cleanup is supported by [Subscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscriber.ts) and [Subscription](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscription.ts).

For later ordinary input events at this downstream-behavior level:

$$
q\neq\mathrm{running}\implies\delta((q,z),e)=((q,z),[]).
$$

The terminal action produced while entering the terminal phase is still executed. This rule suppresses subsequent ordinary reactions; it must not suppress the already-issued terminal delivery or required cleanup.

The phases are notation-level classifications. They are not a claim that RxJS's `closed` and `isStopped` fields are identical or change at the same moment. Teardown may have observable effects, may interact with shared execution, and may throw. A detailed execution model must retain those distinctions.

### Completion rules are operator-specific

Source completion is not universally downstream completion. `switchMap` records outer completion and completes the result only when no current inner subscription remains. A source-error rule also cannot be generalized blindly across operators that recover, retry, or transform error notifications. See [switchMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/switchMap.ts).

### Callback failures need their own rule

Earlier value equations assume nonthrowing callbacks. A fuller model can use explicit results:

$$
\operatorname{Result}(Y)=\{\operatorname{Return}(y)\mid y\in Y\}\uplus\{\operatorname{Throw}(\xi)\mid\xi\in\mathsf{Err}\}.
$$

It must define both reactions rather than leaving $\delta$ accidentally undefined. In RxJS 7.8.2, [OperatorSubscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/OperatorSubscriber.ts) catches exceptions from its configured handlers and passes them to destination error handling. Do not infer from this that consumer-handler exceptions, teardown failures, and every exception elsewhere are identical kinds of operator errors.

## 8. Time and processing order are different coordinates

Enrich events with a clock coordinate and an ordering coordinate:

$$
E_{\mathrm{timed}}=T\times\mathbb N_0\times E,\qquad\widehat e=(t,i,e).
$$

For example:

```text
(1000, 17, SourceNext(value))
(1000, 18, TimerFired(timerId))
```

The timestamp is the same; the processing positions differ. This $i$ is an event-processing index, not an operator callback index such as `map`'s projection index.

The enriched signature is:

$$
\delta:S\times E_{\mathrm{timed}}\to S\times A^*.
$$

An order number records, or is assigned by, an execution policy. It does not replace that policy. To predict an execution, specify the relevant source, subscription order, scheduler, and tie-breaking behavior. Do not invent a universal same-time priority such as “source values always precede timer firings.”

For example, `combineLatest` subscribes to inputs in an explicit loop; synchronous inputs can emit during that setup. See [combineLatest](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/observable/combineLatest.ts). The trace's order must reflect such execution, not only an unordered collection of timestamped values.

Choose a declared clock domain for $T$. An abstract monotonic logical clock is not automatically the same thing as JavaScript wall-clock readings. Sources and schedulers supply timing; the operator's timing policy specifies how those facilities are used.

## 9. Ordered actions are necessary but not sufficient for exact execution

The relevant control-flow outline of RxJS 7.8.2 `switchMap` is:

```text
Cancel the previous inner subscription
    ↓
Evaluate the projection and convert its result
    ↓
Create and store the new inner subscriber
    ↓
Subscribe to the new inner input
```

The previous inner is unsubscribed before the new projection is evaluated. The new inner subscriber is assigned before its subscription can synchronously notify. This sequence is visible in [switchMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/switchMap.ts).

This outline is not an atomic implementation specification. Subscribing can synchronously notify; projection can execute user code; unsubscription runs teardown code. Such execution can reenter the graph before the interrupted work resumes. See [Observable](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Observable.ts), [Subscription](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscription.ts), and [switchMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/switchMap.ts).

Therefore, the following interpreter is not generally sufficient for exact RxJS parity:

```text
Compute the entire next state.
Install it atomically.
Execute every action afterward without interruption.
```

An exact model must specify where nested reactions occur, what state has already been written, and what suspended work resumes afterward. A total ordering of event arrivals alone does not tell us which intermediate state a nested reaction sees.

Refine the state space when needed:

$$
S_{\mathrm{execution}}=S_{\mathrm{data}}\times\mathsf{Phase}\times\mathsf{Frames}^*\times\mathsf{Resources}.
$$

`Phase` records the current processing step, `Frames` the work suspended by nested execution, and `Resources` the relevant subscription and timer state. These are suggested components, not a completed small-step specification of every RxJS operator.

The same signature remains available:

$$
\delta_{\mathrm{execution}}:S_{\mathrm{execution}}\times E_{\mathrm{execution}}\to S_{\mathrm{execution}}\times A^*.
$$

Use smaller transitions, explicit callback-result events, and the appropriate continuation state. A behavioral transition can summarize several such steps only under stated assumptions.

| Level | Purpose |
|---|---|
| Behavioral model | Explain memory, triggering events, output rules, and policies |
| Execution model | Account for intermediate writes, synchronous callbacks, reentrancy, cancellation, and teardown order |

Neither level should be mistaken for the other. A model with one active-inner identity is useful for ordinary “latest only” behavior but is not by itself proof of exact semantics under every reentrant projection or teardown.

Unsubscribing an inner also does not guarantee physical cancellation of every underlying operation. Cancellation is limited by the source's teardown behavior and any independent or shared producer lifetime. Model the disconnection and the underlying resource effect separately.

## 10. State ownership and sharing are explicit

Separate per-downstream-subscription state, shared connection/coordinator state, producer-owned state, and externally mutable callback state. Do not merge them into an unexplained single record.

For example, placing `scan` before versus after a sharing boundary changes which executions own the accumulator bookkeeping. [scanInternals](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/scanInternals.ts) initializes its bookkeeping per subscription; [share](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/share.ts) maintains shared coordination state.

Fresh bookkeeping does not imply deep-copying every seed or payload object. A captured seed reference may be shared; immutable updates or an explicit state factory are needed when independent mutable objects are required.

A “closed” downstream instance does not imply that a shared coordinator and every producer in the graph have ceased to exist. Ownership determines what `DisposeOwned` actually disposes.

## 11. The complete specification framework

Use:

$$
\boxed{\mathcal O_\theta=(S,E,A,s_0,\delta_\theta,\mathcal I_\theta,\mathrm{Inv})}.
$$

The first five components define the core machine. The action interpreter and execution contract $\mathcal I_\theta$ specify initialization, action ordering, callback failure, scheduling, nested execution, resource ownership, and sharing. The subset $\mathrm{Inv}\subseteq S$ identifies valid states.

A deterministic $\delta$ requires sufficient information in the state/event model. A callback that reads hidden mutable state is not a mathematical function of only its declared arguments. Either assume purity, model that environment explicitly, or represent callback outcomes as incoming events. Unspecified scheduling likewise remains an assumption, not something equations magically resolve.

For one fixed event $e$, the function:

$$
\delta_e:S\to S\times A^*
$$

is a state transformer that also produces actions. We retain **stateful transducer** as the name for the complete machine reacting to a stream of events.

The framework is not restricted to plain value transforms. Delivery, retained state, connections, clocks, lifecycle, and distribution can all be represented, provided the declared event/state spaces and execution contract are rich enough. Merely writing the signature does not establish that richness or prove equivalence with RxJS.

## 12. The reusable conclusion

> An RxJS operator's behavior is modeled as a stateful transducer over explicitly defined state and event spaces. Each reaction selects a new state and an ordered action sequence. An execution contract determines how those actions interact with subscriptions, time, cancellation, sharing, and reentrant events.

$$
\boxed{\underbrace{s\in S}_{\text{What is remembered}}\quad+\quad\underbrace{e\in E}_{\text{What arrived}}\quad\xrightarrow{\delta}\quad\underbrace{s'\in S}_{\text{What must be remembered}}\quad+\quad\underbrace{\alpha\in A^*}_{\text{What happens next}}}
$$

The formal application remains $\delta(s,e)=(s',\alpha)$; the plus signs above are reading aids.

Mathematical notation does not eliminate assumptions, replace tests, or prove parity by itself. It makes assumptions, omissions, and proof obligations visible.

Continue with the [execution contract](EXECUTION-CONTRACT.md), the [operator-analysis template](../templates/OPERATOR-ANALYSIS.md), and the [version-pinned references](REFERENCES.md).
