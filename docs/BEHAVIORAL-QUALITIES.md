# Behavioral Qualities and Trace Laws

**ROB-SN, RxJS 7.8.2.** These are proposed observation functions and specification obligations. They do not automatically certify an implementation.

## From model to observations

Given a scoped operator specification, derive what its transitions imply. Compare those predictions with actual execution evidence before claiming runtime conformance. Classify from the resulting qualities, not from the operator name alone.

| Quality | What the analysis must expose |
|---|---|
| Source and activation | What starts or joins this execution? Which producer lifetimes are independent? |
| Input roles and triggers | Which source, inner, notifier, timer, or lifecycle events can cause output? |
| Value behavior | Which values are transformed, selected, retained, combined, or replayed? |
| Cardinality | How many actions, requested emissions, and delivered notifications occur per event and per output? |
| Memory | Shape, growth bounds, initialization, update, reset, and release rules |
| Ownership | Which subscription/coordinator owns each memory component and resource? |
| Time | Clock, scheduling policy, deadlines, and same-time ordering assumptions |
| Concurrency | Admission capacity, overlap, queueing, replacement, or rejection |
| Cancellation | Who can stop which subscription, when, and with what teardown effects? |
| Termination | Conditions for output completion/error and what happens to pending work |
| Sharing and distribution | Connection scope, membership, replay, reference counts, and reset conditions |
| Execution sensitivity | Callback indexes, failures, reentrancy, intermediate writes, and aliasing |

These refine the earlier Source, Trigger, Value, Cardinality, Time, Concurrency, Cancellation, and Termination policy questions. Memory and ownership make the dependencies behind those policies visible; they do not imply a new disjoint taxonomy.

## Requested emissions are a projection of actions

For a designated output $o$, define:

$$
\operatorname{out}_o:A^*\to Y_o^*
$$

by retaining the payloads of `Emit(o, value)` in their original order, including duplicates. For $\delta_\theta(s,e)=(s',\alpha)$:

$$
c^{\mathrm{requested}}_{\theta,o}(s,e)=\operatorname{length}(\operatorname{out}_o(\alpha)).
$$

```text
Actions                              Action count   Requested emissions
[]                                        0                  0
[Emit(a)]                                 1                  1
[Emit(a), Emit(a), Complete]               3                  2
[Cancel(old), Subscribe(new, input)]       2                  0
[Emit([])]                                1                  1
```

This is event-dependent and output-dependent. A new outer value can request a subscription; later inner events can request emissions. Synchronous subscription may cause those inner events before the outer action returns. Do not silently flatten the whole nested execution into a one-input/one-reaction cardinality statistic.

Actual delivery is observed from the interpreted trace. In a direct forward-delivery model, cancellation during an earlier Emit may suppress a later Emit from the same action program. A general relationship between requested and delivered counts requires a declared target, event boundary, and interpreter; multicast and nested reactions prevent naive global counting.

A behavioral quality can be bounded over reachable admitted reactions, for example $c(s,e)\in\{0,1\}$. Such a bound is not a complete characterization: a predicate filter and a latest-value sampler can both satisfy it under suitable event boundaries yet have different triggers and memory.

## State invariants versus trace laws

A state invariant $\mathrm{Inv}\subseteq S$ constrains a single state. For a stable nonoverlapping buffer of size three, retained length is less than three. That does not prove that output preceded completion or that a cancelled subscriber received no later values.

A trace records ordered event handling, delivered notifications, and relevant lifecycle actions. Detailed traces also record nested entry/resumption and visible intermediate writes. Trace laws constrain these histories.

| Law | Scope and obligation |
|---|---|
| Terminal exclusivity | For each downstream subscription, at most one terminal notification is delivered: complete or error. |
| Post-termination silence | No later next notification is delivered to that subscription after terminal delivery or unsubscription. |
| Ordered finalization | When policy requires a final flush, eligible emissions precede completion; cancellation during flushing can prevent later delivery. |
| State succession | A subsequent nonreentrant reaction starts from the established preceding state; suspended work respects state changes made by nested reactions. |
| Cancellation discipline | Work that resumes after cancellation rechecks the permissions required by the execution model. |
| Ownership discipline | Disposal affects the resources owned or explicitly controlled by that scope, not every independent producer. |
| Emission justification | Each delivered value has an explanation in the model, including initialization, timer, inner, replay, or completion reactions where applicable. |

The first two laws are downstream consequences of [Subscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscriber.ts). They do not forbid stopped-notification diagnostics included in a broader model. Unsubscription need not deliver a terminal notification, so the law says **at most one**, not exactly one. A machine can also remain open indefinitely.

The other laws are ROB-SN specification obligations requiring operator-specific interpretations. Cleanup can continue after the final output notification and can itself fail. Do not erase cleanup when suppressing future output.

## Termination and pending-state matrix

Every stateful profile must separately answer:

| Trigger | Required questions |
|---|---|
| Source completion | Flush, emit an accumulated result, wait for other work, continue with another source, or terminate now? |
| Source error | Forward, recover, retry, transform, or discard pending state under which rule? |
| Consumer unsubscription | Which work becomes ineligible and which owned resources are disposed? |
| Operator-induced early completion | Which output is completed and which input subscriptions are disposed? |
| Inner/notifier completion | Does this release capacity, change a gate, have no effect, or permit output termination? |

No generic on-stop rule is adequate without showing these cases equivalent for the chosen profile. See [bufferCount(3)](../examples/BUFFER-COUNT-3.md) for differing reactions from the same pending memory and [switchMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/switchMap.ts) for outer completion while inner work remains.

## Composition observations

An upstream `Emit(x)` can become downstream `SourceNext(x)`; `Complete` and `Fail` similarly become input events for the next machine. The receiving operator determines its own reaction. No artificial queue is implied by this conceptual wiring.

Cancellation follows subscription/resource relationships, not an additional value-notification channel. Observe both directions: values and terminal notifications toward consumers; disposal requests toward controlled subscriptions. Preserve synchronous effects and sharing boundaries.

## Evidence and classification

Useful discriminating checks include independent subscriptions, partial-buffer completion versus cancellation, cancellation during delivery, callback errors, outer completion with an active inner, synchronous inner completion, same-time source/timer events, and shared ref-count transitions.

Label each result as predicted, source-reviewed, selectively runtime-tested, or proved under explicitly stated assumptions. Matching values alone does not validate timing, subscription lifetime, callback indexes, or teardown order.

After the observations, write the classification with its reason: for example, a batching family with count-triggered release, private partial-buffer memory, completion flush, and cancellation discard. Refer to [Behavior Families](BEHAVIOR-FAMILIES.md); one profile can have multiple family memberships.
