# Operator Analysis Template

Copy this file for each new operator or configuration profile. Replace every placeholder and retain explicit exclusions. An unfilled field is not a specified behavior.

## 1. Identity and scope

**Operator:** `<name>`  
**RxJS baseline:** `7.8.2`  
**Overload/configuration:** `<exact overload and parameters>`  
**Model level:** `<behavioral macrosteps / execution microsteps>`  
**Status:** `<proposal / source-reviewed / selectively tested>`

State what is excluded: deprecated overloads, invalid parameters, reentrant callbacks, scheduler variants, or other cases. Do not claim full-API coverage when only one configuration is modeled.

## 2. What flows over time?

Describe the data input, output, and any notifier, timer, inner, or lifecycle inputs. Explain what a new value does before introducing equations.

**Behavior policy:** `<for example: keep the latest inner, queue inputs, remember a running state>`

**Why this operator:** `<which required behavior its policy implements>`

## 3. Parameters and function assumptions

Define the fixed parameter set or record $\theta$.

Record callback types, indexes, purity, termination, possible throws, and mutable-reference assumptions. Include the selected clock and scheduler when relevant. Externally changing state must be modeled or explicitly excluded.

## 4. Spaces and identities

### State space

$$
S=\text{<explicit product, sum, sequence, or other declared space>}.
$$

Explain every component, who owns it, and what it remembers. A memoryless core uses a singleton, not the empty set.

### Event space

$$
E=\text{<tagged source, inner, timer, lifecycle, and internal events>}.
$$

Declare source ports, inner identities, timer identities, and each payload space. State the admissible input protocol.

### Action alphabet

$$
A=\text{<individual action constructors>}.
$$

The output of a reaction is $\alpha\in A^*$, an ordered finite sequence. Define empty output as `[]`.

### Initial state and activation

$$
s_0=\text{<initial state>}\in S.
$$

Choose a separate initializer or an explicit `Start` transition. List initial actions and subscription order. State whether setup can synchronously notify.

## 5. Transition signature and rules

$$
\delta_\theta:S\times E\to S\times A^*,\qquad\delta_\theta(s,e)=(s',\alpha).
$$

Alternatively declare a restricted domain $D\subseteq S\times E$ explicitly.

| Incoming event and guard | Next state | Ordered actions | Explanation |
|---|---|---|---|
| Source next | `<...>` | `<...>` | `<...>` |
| Source completion | `<...>` | `<...>` | `<...>` |
| Source error | `<...>` | `<...>` | `<...>` |
| Callback return/failure, when modeled | `<...>` | `<...>` | `<...>` |
| Inner next/completion/error, when applicable | `<...>` | `<...>` | `<...>` |
| Timer/notifier event, when applicable | `<...>` | `<...>` | `<...>` |
| Downstream unsubscription | `<...>` | `<...>` | `<...>` |
| Later events after a terminal phase | `<...>` | `<...>` | `<...>` |

Remove inapplicable categories with a stated reason. Add any missing event variants. Make guards exhaustive and nonoverlapping, or state rule priority.

Separate source completion from output completion. Never infer a completion notification from cancellation.

## 6. Invariants

$$
\mathrm{Inv}=\{s\in S\mid\text{<validity conditions>}\}.
$$

Explain why $s_0\in\mathrm{Inv}$ and why permitted transitions preserve validity. Distinguish stable-state invariants from transient execution conditions.

## 7. Execution contract

Define $\mathcal I_\theta$ or identify a previously defined contract precisely.

Record state-commit timing; action interpretation; reentrancy and suspended work; callback failures; clock and same-time order; cancellation and teardown; resource ownership; sharing/reset policy; and snapshot/reference semantics.

For timed events use $(t,i,e)$ only after defining $t$ and $i$. Keep the event-processing index separate from callback indexes.

Do not describe a macrostep as implementation-faithful until nested synchronous execution and intermediate writes have been addressed.

## 8. Discriminating trace

| Clock time | Processing order | Incoming event | State before | State after | Actions |
|---|---|---|---|---|---|
| `<t>` | `<i>` | `<e>` | `<s>` | `<s'>` | `<α>` |

Choose a trace that distinguishes this operator from a nearby alternative, not only a happy path. Examples include cancellation during replacement, completion before readiness, a synchronous inner, or a timer/source tie.

For reentrancy, record microsteps or nested entry/resume events rather than flattening each handler into an assumed atomic reaction.

## 9. Verification evidence

**Pinned implementation:** `<source URL or immutable commit>`  
**Relevant upstream tests:** `<test path and case>`  
**Checks actually executed:** `<commands and outcomes, or none>`  
**Observations compared:** `<values, order, timing, indexes, subscriptions, teardown>`  
**Known limitations:** `<not-yet-specified or untested cases>`

Distinguish a proposed test from a passing test, source inspection from execution, and selected checks from exhaustive proof.

## 10. Final behavioral statement

> `<One precise paragraph: what is remembered, what arrives, what state changes, what actions occur, and when execution ends.>`

$$
\mathcal O_\theta=(S,E,A,s_0,\delta_\theta,\mathcal I_\theta,\mathrm{Inv}).
$$
