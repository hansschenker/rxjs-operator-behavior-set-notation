# RxJS Operator Behavior — Set Notation

**GPT-6 Astra is the main contributor of the project.**

Developed in collaboration with Hans Schenker to preserve and extend our RxJS Operator Behavior Notation.

**Reference baseline:** RxJS **7.8.2**.  
**Status:** Proposed specification, initial documentation edition, 29 September 2026.

> What is remembered + What arrived → What must be remembered + What happens next.

The plus signs in this reading aid mean “together with,” not arithmetic addition. The formal definition is:

$$
\boxed{\delta:S\times E\longrightarrow S\times A^*}
$$

$$
\boxed{\delta(s,e)=(s',\alpha)}
$$

An operator's behavior is modeled as a **stateful transducer**: a current state and an incoming event determine a new state and an **ordered finite sequence of actions**.

## Why this repository exists

The notation makes the operator's normally hidden behavior explicit: retained values, readiness conditions, counters, inner-subscription identities, timers, completion, errors, cancellation, and sharing boundaries.

Sets define the possibilities. Transition rules define the reactions. An execution contract explains how the actions actually run.

**Sets alone are not enough.** Event histories, buffers, and action programs must preserve order and repetition. In particular:

```text
[Cancel(old), Subscribe(new)] ≠ [Subscribe(new), Cancel(old)]
```

The project preserves the foundational discussion rather than reducing it to a collection of operator slogans.

## Start here

| Document | Purpose |
|---|---|
| [Foundational reference](docs/FOUNDATION.md) | Complete explanation of sets, state, events, actions, transitions, and worked operator rules |
| [Execution contract](docs/EXECUTION-CONTRACT.md) | Subscription, initialization, time, callback failures, reentrancy, teardown, and sharing |
| [Operator-analysis template](templates/OPERATOR-ANALYSIS.md) | Reusable structure for specifying another operator |
| [Primary references](docs/REFERENCES.md) | Source links pinned to RxJS 7.8.2 and explicit verification limits |
| [Contribution guide](CONTRIBUTING.md) | How to extend the notation without changing its meaning silently |
| [Change log](CHANGELOG.md) | Changes to the project's specification |

The foundational reference includes `map`, `filter`, seeded and seedless `scan`, `combineLatest`, and the ordered control-flow outline of `switchMap`.

## The core vocabulary

| Symbol | Meaning |
|---|---|
| $S$ | State space |
| $s,s'\in S$ | Current state and next state |
| $E$ | Event space |
| $e\in E$ | One incoming event |
| $A$ | Alphabet of individual actions |
| $A^*$ | All finite ordered action sequences, including the empty sequence |
| $\alpha\in A^*$ | The actions produced by one reaction |
| $s_0\in S$ | Initial state |
| $\delta$ | Transition function |
| $\theta$ | Fixed operator parameters and declared policies |
| $\mathcal I_\theta$ | Action interpreter and execution contract |
| $\mathrm{Inv}\subseteq S$ | Set of valid states |

The complete specification framework is:

$$
\boxed{\mathcal O_\theta=(S,E,A,s_0,\delta_\theta,\mathcal I_\theta,\mathrm{Inv})}
$$

These are project definitions, not names of internal RxJS APIs.

## Two levels of description

**Behavioral model.** Explain what flows over time, what must be remembered, which event triggers output, and which policy determines the reaction.

**Execution model.** Add intermediate writes, callback invocation and failure, nested synchronous reactions, subscriber state, scheduling, and resource ownership when exact runtime behavior matters.

An ordered action list does **not** imply that the entire reaction is atomic. Merely assigning order numbers to events does not establish an execution policy.

## Modeling commitments

- Distinguish sets from their members: $S$ versus $s$, $E$ versus $e$, and $A^*$ versus $\alpha$.
- Use ordered sequences where order or multiplicity matters; use a singleton state space, not an empty set, for a memoryless core.
- Separate source completion, downstream completion, error, and cancellation.
- Make time, callback indexes, event-processing order, subscription ownership, and sharing explicit.
- Keep domain meaning in supplied functions; declare the assumptions under which those functions are modeled.
- State the abstraction level and verify version-specific claims against pinned sources and discriminating tests.

The domain can change. The stream-processing mechanism stays the same.

## Scope and evidence

This repository is a **proposed notation**, not an official RxJS standard, a replacement RxJS implementation, a compiler, or a proof that every operator has been modeled completely.

Its equations are explicit definitions of an abstraction. RxJS-specific claims are linked to primary sources. The initial edition is documentation-only: it does not claim an automated conformance suite or exhaustive reentrancy coverage. Consult [References](docs/REFERENCES.md) for the exact evidence level.

Future operator descriptions should begin with the [analysis template](templates/OPERATOR-ANALYSIS.md) and distinguish an illustrative equation from an implementation-faithful specification.

## Attribution

**GPT-6 Astra is the main contributor of the project.** Hans Schenker initiated the project, supplied the motivating questions, and collaborates on its development.

This credit records contribution to this project; it does not present the notation as an official RxJS or OpenAI standard.
