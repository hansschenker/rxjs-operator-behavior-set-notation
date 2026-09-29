# ROB-SN Project Guide

**ROB-SN — RxJS Operator Behavior Set Notation**  
**Baseline:** RxJS 7.8.2. **Edition:** 29 September 2026, conversation consolidation.  
**Status:** Proposed notation and classification method, not an official RxJS standard.

The working ChatGPT project is named **ROB-SN RxJS Operator Set Notation**. The formal notation retains **Behavior** in its expanded name. The repository remains `rxjs-operator-behavior-set-notation`.

## Purpose

Represent an operator's behavior through explicitly defined state spaces, events, transition rules, and ordered actions. Derive behavioral qualities from that representation and use them to justify classification.

> Classification is the conclusion of the analysis, not its starting assumption.

```text
RxJS operator and exact configuration
                  |
                  v
MODEL: a behavioral representation as a stateful transducer
  Event Slot             What arrived?
  Memory Slot            What must be remembered?
  Lifecycle Slot         What is connected, owned, or being released?
  Execution Status Slot  Is this scoped execution still open?
  Next Actions Slot      What must happen next, in which order?
                  |
                  v
OBSERVE: derive qualities; compare predictions with execution evidence
  memory, triggers, cardinality, value selection, time,
  concurrency, cancellation, termination, ownership, sharing
                  |
                  v
CLASSIFY: assign justified families and behavior-control policies
```

The [execution contract](EXECUTION-CONTRACT.md) applies throughout. It explains how the action instructions interact with clocks, subscriptions, user functions, nested synchronous execution, and disposal.

## Model

A model is a behavioral representation, not merely an operator name or a drawing of its output. State exactly what flows, what a new event does, what must be retained, and which execution scope owns that information.

For fixed parameters $\theta$, retain the foundation:

$$
\delta_\theta:S\times E\to S\times A^*,\qquad
\delta_\theta(s,e)=(s',\alpha).
$$

A useful persistent-state decomposition is $s=(q,\ell,m)$: execution status, lifecycle bookkeeping, and processing memory. Events arrive and action sequences are produced; they are not automatically additional persistent memory. Detailed execution models may also retain phases and suspended frames.

A combination of slot contents describes a configuration. The permitted transitions between configurations describe reactions. The execution contract interprets those reactions. Choosing five slot values is not sufficient to specify an operator.

## Observe

Observation has two distinct meanings in this project. **Model observation** extracts predicted qualities from transitions. **Execution observation** records what a pinned RxJS implementation actually does. A prediction is not automatically a measured fact; compare the two using discriminating traces.

The earlier sensor metaphor is a teaching aid: the model exposes qualities that were difficult to see. A mathematical model is not itself a tracing instrument and does not prove that a runtime follows its predictions.

Use [Behavioral Qualities and Trace Laws](BEHAVIORAL-QUALITIES.md) to distinguish requested actions, actual delivered notifications, state invariants, and valid execution histories.

## Classify

An operator can belong to several families. Do not require disjoint categories or infer a complete behavior from a name suffix. A finite expansion, an asynchronous inner stream, and an unbounded unfolding can all produce many values, yet require different timing, lifetime, and cancellation models.

The six sequence-processing families in [Behavior Families](BEHAVIOR-FAMILIES.md) are a useful starting layer, not an exhaustive classification of RxJS. Time, concurrency, recovery, lifecycle, and distribution are additional dimensions.

## Mechanism, domain, and execution

| Layer | Responsibility |
|---|---|
| Parameters and supplied functions | Projection, predicate, accumulator, key selection, and other domain calculations |
| Transition rules | Whether to forward, retain, wait, subscribe, cancel, or terminate |
| Execution contract | How those instructions run and what can happen at their boundaries |

The operator machinery handles packages without embedding their domain meaning. Supplied functions may inspect values; their purity, indexes, errors, external reads, and mutation assumptions must be declared. No equivalence claim should silently erase these effects.

A pipeline describes participation before it is subscribed. A subscription may start an independent execution or join an already existing producer. Fresh execution bookkeeping is not automatically a fresh deep copy of captured objects. See [Observable](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Observable.ts), [scanInternals](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/scanInternals.ts), and [share](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/share.ts).

## Language for teaching; algebra for precise semantics

The [Slot Catalogue](SLOT-CATALOGUE.md) supplies vocabulary. The [Transition-Rule Catalogue](TRANSITION-RULE-CATALOGUE.md) supplies reusable reaction patterns. An operator specification selects spaces, parameters, guarded rules, and an execution interpretation.

The grammar analogy does not replace mathematical semantics. Input notifications and lifecycle control must remain distinguishable even when described using familiar words such as stop or finish.

> The slots tell us what can exist. The transition rules tell us what can happen. The execution contract tells us how it happens.

Begin a new analysis with the [operator-analysis template](../templates/OPERATOR-ANALYSIS.md). The [take(3)](../examples/TAKE-3.md) and [bufferCount(3)](../examples/BUFFER-COUNT-3.md) profiles demonstrate the workflow at a scoped behavioral level.
