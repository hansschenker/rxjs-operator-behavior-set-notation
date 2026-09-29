# ROB-SN Transition-Rule Catalogue

**Baseline:** RxJS 7.8.2. **Status:** 40 proposed templates in seven families. These are neither a minimal basis nor a claim of complete operator/overload coverage.

[Slots](SLOT-CATALOGUE.md) say what can exist. A transition rule says what happens when an event meets specified conditions. A catalogue row is a reusable pattern, not an executable rule until its parameters, guards, state updates, and action interpretation are supplied.

## Rule schema

| Field | Obligation |
|---|---|
| Identity | Stable rule ID and readable name |
| Scope and event | Which execution, port, or resource receives what event? |
| Guard | Exactly when does this rule apply? |
| State update | What changes in execution status, lifecycle bookkeeping, and memory? |
| Ordered actions | What is requested, in which order? |
| Interpretation | Where can callbacks, nested delivery, cancellation, or failures intervene? |
| Evidence | Source reference, tested trace, or explicit proposal status |

$$
\delta_\theta((q,\ell,m),e)=((q',\ell',m'),\alpha).
$$

State not mentioned by an update is preserved only if the concrete specification says so. An omitted state/event case is not automatically a no-op. Use exhaustive nonoverlapping guards, or an explicit priority/combination rule. Choose a separate initializer or `Start`, not both silently.

## L — Activation and lifecycle

| ID | Rule | Event and condition → reaction |
|---|---|---|
| L1 | Initialize execution | On Start in a not-started scope: initialize owned bookkeeping, set the initial open phase, and perform ordered setup. |
| L2 | Record resource-operation completion | On an identified acquisition/release outcome: update that lifecycle record. Handle failure separately; preserve unrelated execution outcomes. |
| L3 | Cancel execution | On Unsubscribe while open: end scoped participation, abandon ineligible pending work, and dispose owned resources without a downstream completion notification. |
| L4 | Suppress delivery after termination | When a notification targets a stopped output: do not deliver it there. Preserve cleanup and diagnostic obligations included by the execution contract. |

The notification/disposal distinction is grounded in [Subscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscriber.ts). An internal unsubscribe after terminal delivery is cleanup, not a new cancelled outcome. L4 is a downstream-delivery rule, not a claim that no internal diagnostic callback can occur.

## V — Values and basic memory

| ID | Rule | Event and condition → reaction |
|---|---|---|
| V1 | Forward | On an eligible value x: request Emit(x), retaining the selected processing state. |
| V2 | Transform | On x: obtain y=f(x) and request Emit(y). Account for indexes, throws, and invocation boundaries when in scope. |
| V3 | Select or suppress | On x: test the predicate and request an emission only for acceptance. Rejection is no emission, not an empty-valued emission. |
| V4 | Count and branch | On a counted event: update the counter and select the reaction for the declared threshold condition. |
| V5 | Accumulate | On x: replace z with f(z,x); emit or retain the new accumulator according to an explicit output policy. |
| V6 | Remember the latest value | On x: replace the retained value. Memory change alone does not require emission. |
| V7 | Expand a finite input | For a declared finite expansion y1,…,yn: request the corresponding ordered emissions, possibly none. Preserve interruption boundaries. |

[map](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/map.ts) and [filter](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/filter.ts) have callback indexes even when value-only models omit them. [scanInternals](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/scanInternals.ts) separates accumulator updates from emission on input or before completion.

V7 is not one infinite action list. Potentially unbounded or asynchronous production needs source/inner events or smaller execution steps. Infinite execution is compatible with finite action lists per step.

## B — Buffers, coordination, and output channels

| ID | Rule | Event and condition → reaction |
|---|---|---|
| B1 | Append to a buffer | On an accepted value: append it to each applicable ordered buffer and retain it pending a release condition. |
| B2 | Release a batch | On a count/boundary/other release condition: capture the selected contents, update/remove the buffer, and request its emission. Specify whether empty batches are allowed. |
| B3 | Update an input slot and test readiness | On input p: update p's slot. Emit a combined result only when readiness and this event's trigger policy both hold. |
| B4 | Consume queued input combinations | When every required queue has an item: remove the selected items and emit their combination. Repeat through additional steps where appropriate. |
| B5 | Open an output channel | On an opening condition or qualifying new key: create/register the channel and expose it downstream when required. |
| B6 | Route to output channels | On a value: determine eligible channels and deliver to them in the declared order. |
| B7 | Close an output channel | On its closing condition: complete that channel and update its resource record, without necessarily completing the main output. |

Readiness asks whether required information exists; triggering asks whether this event may cause an output. The distinction is important in [combineLatest](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/observable/combineLatest.ts). B1/B2 specialize to the [bufferCount(3) profile](../examples/BUFFER-COUNT-3.md). General overlapping buffers require more state than that nonoverlapping example.

## T — Time and gate control

| ID | Rule | Event and condition → reaction |
|---|---|---|
| T1 | Arm a scheduled event | When required timed work has no applicable task: record its identity and request scheduling using a declared clock/scheduler. |
| T2 | Move the effective deadline | On qualifying new input: update pending data/activity time and the effective deadline; ensure later scheduled work checks the revised deadline. |
| T3 | Continue waiting | When scheduled work runs before the effective deadline: retain pending state and arrange another check without emission. |
| T4 | Release when due | When the applicable deadline is reached: release selected pending output, update memory, and renew/cancel scheduling as specified. |
| T5 | Change a gate | On an opening/closing signal: change the acceptance condition. Subsequent values are forwarded, retained, or suppressed under the declared policy. |
| T6 | Ignore obsolete scheduled work | If an event's timer/generation identity is obsolete: do not apply it to the current pending work. |

T2 is not universally cancel-and-recreate-a-timer. RxJS 7.8.2 [debounceTime](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/debounceTime.ts) remembers the latest activity time and allows an existing task to check and reschedule. This catalogue distinguishes the effective timing policy from implementation bookkeeping. T6 requires the model to define which identities can become stale; it does not claim every RxJS operator uses generation IDs.

Time comes from sources and schedulers. Equal timestamps alone do not order a value and a timer firing.

## C — Inner subscriptions and concurrency

| ID | Rule | Event and condition → reaction |
|---|---|---|
| C1 | Admit work when capacity exists | On an admissible outer value: evaluate its projection at the specified point, register the inner execution, and subscribe. |
| C2 | Queue while busy | On an outer value at capacity under queueing: retain the outer value in order without starting its inner execution. |
| C3 | Replace active work | On new outer input under latest-only: cancel the previous inner before evaluating/subscribing to the replacement, preserving exact ordering when effects are in scope. |
| C4 | Ignore while busy | On an outer value during exclusive inner activity: do not enqueue it, invoke its projection, or start replacement work. |
| C5 | Forward an eligible inner value | On a value from an inner still allowed to contribute: request its downstream emission. |
| C6 | Release capacity and reconsider work | On normal inner completion and required finalization: update active-work bookkeeping, admit queued work when allowed, and recheck output completion. |

[mergeInternals](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/mergeInternals.ts) admits work below capacity, otherwise queues outer values, and drains after successful inner completion/finalization. Cancellation and failure must not blindly take the same queue-draining path. [concatMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/concatMap.ts) uses the merge policy with concurrency one.

[switchMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/switchMap.ts) cancels the old inner before invoking the new projection. [exhaustMap](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/exhaustMap.ts) does not invoke the projection while busy. Simple one-active-inner summaries here exclude reentrant projection/teardown anomalies; exact parity needs intermediate-state and continuation modeling.

## F — Completion, failure, and continuation

| ID | Rule | Event and condition → reaction |
|---|---|---|
| F1 | Complete now | When the output-completion condition holds and required work is finished: request Complete, dispose owned resources, and record the completed outcome. |
| F2 | Emit pending results, then complete | On the applicable completion condition: request permitted pending emissions in order, then Complete, then cleanup. |
| F3 | Record input completion and wait | When an input completes but required work remains: record that input's completion while keeping the output open. |
| F4 | Fail the output | On an unrecovered failure covered by this rule: abandon work as specified, request Fail(error), dispose owned resources, and record errored. |
| F5 | Recover with replacement input | On a recoverable input error: clean up the old input as required and establish the replacement without first terminating the downstream output. |
| F6 | Resubscribe under retry/repeat policy | On the qualifying error/completion with continuation allowed: update attempt state and arrange another source subscription, immediately or after declared control input. |

These are alternative policy templates. Error-handling operators need not forward source errors. [catchError](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/catchError.ts), [retry](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/retry.ts), and [repeat](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/repeat.ts) are primary inspection targets for concrete F5/F6 specifications; these rows are not complete models of their overloads.

F3 keeps an output open; it does not resurrect a terminal subscriber. F4 must name the failure origin. Source errors, operator callback throws, consumer-handler exceptions, and teardown exceptions are not automatically one event. See [OperatorSubscriber](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/OperatorSubscriber.ts) and [Subscription](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/Subscription.ts).

## S — Sharing, distribution, and replay

| ID | Rule | Event and condition → reaction |
|---|---|---|
| S1 | Attach a participant | On arrival: register the participant and establish an upstream connection only when the connection policy requires it. |
| S2 | Distribute a notification | On a shared notification: deliver to eligible participants under declared ordering and membership rules. |
| S3 | Replay retained information | On a replay trigger: deliver eligible retained values and any applicable cached terminal notification in order. |
| S4 | Detach and apply disconnect/reset policy | On departure or configured reset trigger: update membership and disconnect/reset only under the corresponding conditions. |

State ownership, replay age/size, notification order, reference counting, and reset-generation policies must be specified independently. See [share](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/share.ts), [shareReplay](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/operators/shareReplay.ts), and [ReplaySubject](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/internal/ReplaySubject.ts). These references do not make a single universal sharing state machine.

## Combining templates correctly

A concrete operator analysis specifies a guarded reaction, not an unordered bag of IDs. V4 and V1 together do not determine whether the counter is tested before or after incrementing; the [take(3) profile](../examples/TAKE-3.md) resolves that choice explicitly.

Require coverage of admitted state/event pairs, unambiguous guards, invariant preservation, and an execution interpretation. A finite action list can be interrupted by synchronous nested work; cancellation can invalidate later delivery. Do not atomically install a terminal output state before executing an earlier emission in the same behavioral summary.

Use the [analysis template](../templates/OPERATOR-ANALYSIS.md) to connect rules with evidence, derived qualities, and classification. Add a new rule when justified, preserve existing IDs, and explain changed semantics in the changelog. Forty templates are an initial organizing catalogue, not a completeness theorem.
