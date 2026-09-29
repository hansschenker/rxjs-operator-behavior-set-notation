# ROB-SN Operator Analysis Template

Copy this file for one exact operator/configuration profile. Replace placeholders, retain explicit exclusions, and record evidence honestly. An unfilled field is not a specified behavior.

## 1. Identity and scope

**Operator:** `<name>`  
**RxJS baseline:** `7.8.2`  
**Overload/configuration:** `<exact overload and parameters>`  
**Model level:** `<behavioral macrosteps / execution microsteps>`  
**Status:** `<proposal / source-reviewed / selectively runtime-tested / proved under stated assumptions>`  
**Execution scope:** `<one downstream subscription / shared coordinator / identified connection generation>`

Declare excluded overloads, invalid parameters, reentrant callbacks, scheduler variants, mutation, or failure paths. Do not claim full-API coverage for one profile. Distinguish an operator definition, a running subscription, and an independent producer.

## 2. What flows over time?

Describe values, their input roles, and the required output policy before equations or code. Explain what happens on a new value and why this policy is required. Do not use the proposed classification as a substitute for analyzing the behavior.

**Behavior policy:** `<keep latest inner, queue while busy, retain a running state, etc.>`  
**Why this operator:** `<required behavior>`

## 3. Parameters and function assumptions

Define $\theta$: functions, count, seed, duration, scheduler, concurrency, reset choices, and any other fixed configuration. Record callback types/indexes, purity, termination, throws, external reads, and mutable-reference assumptions. Include the selected clock. Hidden environmental variation must be modeled or excluded.

## 4. Slot spaces, identities, and initialization

Use the [Slot Catalogue](../docs/SLOT-CATALOGUE.md), selecting only relevant constructs.

| Slot | Exact definition | Required explanation |
|---|---|---|
| Event E | `<tagged notifications, controls, timers, internal events>` | Ports, payload domains, identities, admissible protocol |
| Memory M | `<products, options, sequences, counters, etc.>` | Meaning, owner, growth bound, reset/release rules |
| Lifecycle L | `<resource registry and teardown state>` | Owners, phases, membership, resource relationships |
| Execution Status Q | `<open and terminal states at this scope>` | Meaning and distinction from stopped/closed implementation fields |
| Next Actions A* | `<ordered programs over declared alphabet A>` | Interpretation of each constructor and empty output [] |

A useful decomposition is $S=Q\times L\times M$, restricted by validity conditions; refine it with processing phases and continuation frames where required. Events and next actions are not automatically persistent state.

**Initialization convention:** `<separate initializer or explicit Start>`.

Define $s_0\in S$ and any initial actions. State which bookkeeping and ownership relationships exist before each source can synchronously notify. Do not silently mix both initialization conventions. Fresh bookkeeping does not imply deep-cloning a captured seed.

## 5. Transition rules

$$
\delta_\theta:S\times E\to S\times A^*,\qquad\delta_\theta(s,e)=(s',\alpha).
$$

Alternatively declare an admissible domain $D\subseteq S\times E$. Use [catalogue IDs](../docs/TRANSITION-RULE-CATALOGUE.md) as cross-references, not substitutes for fully specified rules.

| Rule IDs | Event and guard | Next state | Ordered actions | Explanation |
|---|---|---|---|---|
| `<...>` | Source next | `<...>` | `<...>` | `<...>` |
| `<...>` | Source completion | `<...>` | `<...>` | `<...>` |
| `<...>` | Source error | `<...>` | `<...>` | `<...>` |
| `<...>` | Callback return/failure, if modeled | `<...>` | `<...>` | `<...>` |
| `<...>` | Inner/notifier next/completion/error, if applicable | `<...>` | `<...>` | `<...>` |
| `<...>` | Timer or boundary event, if applicable | `<...>` | `<...>` | `<...>` |
| `<...>` | Downstream unsubscription | `<...>` | `<...>` | `<...>` |
| `<...>` | Post-terminal events | `<...>` | `<...>` | `<...>` |

Remove inapplicable categories with reasons; add missing variants. Guards must be exhaustive and nonoverlapping or have an explicit priority/combination policy. Separate deliberate no-op, invalid input, and unspecified case. Ordered actions can be interrupted; terminal post-states are not instructions to suppress an earlier pending Emit.

## 6. Invariants and trace laws

$$
\mathrm{Inv}=\{s\in S\mid\text{declared validity conditions}\}.
$$

Explain initialization and invariant preservation. Distinguish stable-state conditions from transient implementation states.

Specify applicable [trace laws](../docs/BEHAVIORAL-QUALITIES.md): terminal exclusivity, post-termination silence, finalization order, state succession, cancellation, ownership, and emission justification. Name each observation scope and excluded diagnostics. State validity alone does not establish a valid history.

## 7. Termination and pending work

| Trigger | Pending memory | Output notifications | Resource action / continuation |
|---|---|---|---|
| Source completion | `<flush/discard/retain>` | `<...>` | `<...>` |
| Source error | `<...>` | `<forward/recover/retry/etc.>` | `<...>` |
| Consumer unsubscription | `<...>` | `<none to the cancelled subscriber>` | `<...>` |
| Operator-induced early completion | `<...>` | `<...>` | `<...>` |
| Inner/notifier completion, if applicable | `<...>` | `<...>` | `<...>` |

Input completion is not universally output completion. Cleanup after complete/error is not a new cancelled outcome. Recovery and retry do not reopen a terminal downstream subscriber; they must prevent that terminal delivery while continuing.

## 8. Execution contract

Define $\mathcal I_\theta$ or name a precise existing contract. Record state-commit timing, action interpretation, synchronous nesting/resumption, callback failures, clocks/tie ordering, cancellation/teardown, ownership/sharing/reset, and snapshot/reference semantics.

For $(t,i,e)$, define t and i; do not confuse event order with callback indexes or the nested execution stack. Distinguish logical outcome from stopped, closed, terminal-delivery, and disposal phases when needed. Cancellation disconnects modeled participation; physical work stops only as supported by source teardown.

## 9. Discriminating traces and evidence

| Clock | Processing order | Incoming event | State before | State after | Requested actions / delivered observations |
|---|---|---|---|---|---|
| `<t>` | `<i>` | `<e>` | `<s>` | `<s'>` | `<...>` |

Choose a trace that distinguishes a nearby alternative. Include relevant partial completion, cancellation, same-time ties, synchronous inners, callback failures, reentrancy, and independent/shared subscription cases. For nested work, record microsteps rather than assuming atomic macrosteps.

**Pinned implementation and inspected scope:** `<source URLs, optional blob SHAs>`  
**Upstream tests:** `<paths/cases, with inspection/execution status>`  
**Checks actually executed:** `<commands and actual outcomes, or none>`  
**Observations compared:** `<values/order/time/indexes/lifetimes/teardown>`  
**Known limitations:** `<unmodeled or untested cases>`

Documentation checks are not runtime tests. A suggested test is not a passing test. Selected matching traces are not an exhaustive proof.

## 10. Derived behavioral qualities — Observe

Record source/activation, value behavior, input roles/triggers, per-event/per-output cardinality, memory, time, concurrency, cancellation, termination, ownership, and sharing. Separate model predictions from execution observations; requested emissions can differ from delivered notifications under interruption.

## 11. Classification — the conclusion

**Families:** `<justified memberships>`  
**Behavior-control policies:** `<explicit choices>`  
**Reason:** `<qualities and transitions supporting each label>`  
**Scope:** `<configuration and observation limits>`

Use [Behavior Families](../docs/BEHAVIOR-FAMILIES.md) as a starting vocabulary, not a complete partition of operators. Several classifications may apply.

## 12. Final behavioral statement

> `<What is remembered, what arrives, what changes, which ordered actions occur, and when this scoped execution ends.>`

$$
\mathcal O_\theta=(S,E,A,s_0,\delta_\theta,\mathcal I_\theta,\mathrm{Inv}).
$$

Model → Observe → Classify. The classification follows the analysis.
