# Execution Contract

**Reference baseline: RxJS 7.8.2.** This document records the assumptions an operator analysis must make explicit. It is a specification checklist and interpretation guide, not a complete runtime implementation.

The core equation is:

$$
\delta(s,e)=(s',\alpha).
$$

The equation alone does not define when state is committed, how actions are interpreted, or what happens when an action synchronously triggers another event. Those responsibilities belong to $\mathcal I_\theta$, the declared execution contract.

## 1. Activation and initialization

Choose one initialization convention.

**Separate initializer:** `initialize(parameters, environment) = (s0, initialActions)`. Interpret those actions according to the same ordering and reentrancy rules as later actions. The resulting machine then handles ordinary notifications and lifecycle events.

**Explicit activation event:** include a not-started phase and `Start` in the event space. `Start` creates the required state and setup actions. Specify what a second `Start` means, or exclude it as an invalid event.

An analysis must say which subscriptions exist before each initial action can notify. This is particularly important for a sequence of subscriptions to synchronous sources. RxJS's [combineLatest implementation](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/observable/combineLatest.ts) sets up inputs in a loop, so subscription order contributes to notification order.

Do not equate a subscription with starting every producer. Subscription to an existing producer may only establish a delivery relationship. See [Observable](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Observable.ts).

## 2. State-commit policy

A behavioral model may say “replace the old state and perform the listed actions” under a nonreentrant reaction assumption. Label that as a macrostep convention.

An implementation-faithful model must expose writes that are visible during synchronous nested execution. It cannot simply choose a final state, install it in advance, and claim equivalence.

For each potentially observable action boundary, record the state already written and the work not yet performed. A useful small-step configuration has data state, a processing phase, suspended frames, and resource state.

The frames are ordered. Replacing them with a set would lose the nesting/resumption discipline.

## 3. Action interpretation

Every action constructor needs an operational meaning.

| Action | Questions its contract must answer |
|---|---|
| `Emit(value)` | Which downstream destination receives it? Can that delivery synchronously cancel or reenter? |
| `Complete` / `Fail(error)` | When does the destination stop accepting further notifications? What cleanup follows? |
| `Subscribe(id, input)` | When is the identity allocated and stored? Can subscribing notify before returning? |
| `Cancel(id)` | Which subscription is disconnected? What teardown code runs and in what order? |
| `Schedule(id, deadline)` | Which clock and scheduler are used? What determines same-time ordering? |
| `CancelTimer(id)` | What happens to an already pending timer event? Are generation identities needed? |
| `DisposeOwned` | Which resources belong to this scope? Which remain alive because another scope owns them? |

This vocabulary is extensible. It is not permission to treat every action as asynchronous or to insert a queue between every pair of operators.

## 4. Nested synchronous execution

RxJS subscription and notification delivery can be synchronous. Subscription and teardown can run user-controlled code. See [Observable](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Observable.ts), [Subscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscriber.ts), and [Subscription](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscription.ts).

For each possible nested reaction, specify:

1. Which operation causes the nesting and what state is visible at entry.
2. Which execution is suspended and what resumes after the nested work returns.
3. Whether cancellation or failure has changed what the suspended work may still do.

These are execution questions, not questions answered by a timestamp alone.

### `switchMap` as a discriminating example

In the ordinary replacement path, RxJS 7.8.2 cancels the previous inner before evaluating the new projection. It converts the projection result and creates/stores the new inner subscriber before subscribing to it. See [switchMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/switchMap.ts).

Preserve each of these distinctions:

```text
previous-inner cancellation
projection invocation and result conversion
new-subscriber creation and assignment
new-inner subscription
```

A rule that evaluates the projection first changes observable behavior when projection or teardown has effects. A rule that queues every inner notification until subscription returns changes synchronous behavior. A rule that assumes all reentrant outer inputs are processed after the current outer handler finishes also needs justification.

This edition preserves the outline and the modeling obligation; it does not claim a fully enumerated microstep model for every reentrant `switchMap` scenario.

## 5. Callback assumptions and failures

The simple `map`, `filter`, and `scan` equations assume pure, terminating, nonthrowing functions that ignore callback indexes unless an index is explicitly modeled.

For wider coverage, specify normal callback returns and throws separately. An execution model may introduce `CallbackReturned(id, value)` and `CallbackThrew(id, error)` events so the call site and resumption order remain explicit.

Capture all behaviorally relevant callback inputs: current value, accumulator, callback index, and any declared environment. A function that reads time or external mutable state requires a broader model than a pure function of its displayed arguments.

RxJS's [OperatorSubscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/OperatorSubscriber.ts) handles throws from its operator handlers. That does not establish one universal rule for consumer-handler errors, conversion errors, finalizers, and teardown exceptions. Identify the exception's origin and actual destination.

The existence of a transition function does not establish termination of user code or guarantee that an infinite synchronous source will return control.

## 6. Three meanings of order

Keep these separate:

**Clock time:** the chosen source/scheduler timestamp $t$.

**Event-processing order:** the trace position $i$ used to distinguish occurrences, including those with equal timestamps.

**Nested execution order:** the call/resumption structure and intermediate writes that explain what happens inside a reaction.

An operator callback index is a fourth, different counter. For example, `map` increments its own projection index; it is not a global graph-event number. See [map](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/map.ts).

For virtual-time tests, record the scheduler and insertion/subscription ordering relevant to ties. For real execution, do not turn a particular observed tie into an unsupported universal priority rule.

## 7. Lifecycle and resource ownership

Model source completion, output completion, source error, output error, and downstream unsubscription as distinct events or effects.

`Unsubscribe` does not imply `Complete`. Completing the outer source of `switchMap` does not immediately complete its result while a current inner remains. See [Subscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscriber.ts) and [switchMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/switchMap.ts).

Logical terminal phases may be sufficient for a behavioral model. An exact model may need separate stopped, closed, terminal-delivery, and disposal stages. Cleanup can continue after the last downstream notification. Ignoring later source notifications must not erase required cleanup actions.

`DisposeOwned` is scope-relative. For a shared execution, leaving one downstream subscription need not dispose the shared upstream connection. Specify reference counting, replay state, and reset conditions when the analysis includes them. See [share](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/share.ts).

Cancellation means the modeled subscription is disconnected and its specified teardown is performed. It does not automatically mean that every independent producer, Promise-backed operation, or server-side effect is physically stopped.

## 8. Snapshot and aliasing policy

State is a mathematical value in the simplest model. JavaScript implementations can retain mutable references.

Declare whether an emitted container is a snapshot, whether payload references are shared, and whether callback mutation is excluded. `combineLatest` copies its values array for delivery rather than deep-cloning all payloads. See [combineLatest](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/observable/combineLatest.ts).

Per-subscription initialization of bookkeeping is not the same as deep-copying a captured seed object. For stateful examples, prefer immutable domain updates or state explicitly how a fresh seed is obtained.

## 9. Conformance and honest scope

To compare the model with RxJS, compare more than final values. Relevant observations include notification order, timestamps, terminal events, callback invocation order/indexes, subscription lifetimes, and teardown order.

For each claimed equivalence, state which of those observations it preserves and under which assumptions. A matching happy-path marble diagram is not evidence for untested reentrancy or teardown behavior.

A future test suite should include empty sources, never-completing sources, synchronous sources, same-time notifications, callback failures, immediate inner completion, inner replacement, and downstream cancellation during delivery. This is a suggested coverage plan, not a claim that those tests are already implemented or passing.

Use the [operator-analysis template](../templates/OPERATOR-ANALYSIS.md) to record the model's assumptions and its actual evidence.
