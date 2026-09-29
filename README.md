# ROB-SN — RxJS Operator Behavior Set Notation

**GPT-6 Astra is the main contributor of the project.**

Developed in collaboration with Hans Schenker. **Reference baseline: RxJS 7.8.2.**  
**Status:** Proposed specification; expanded documentation and family-roadmap edition, 29 September 2026.  
**Working ChatGPT project:** ROB-SN RxJS Operator Set Notation.

> Represent operator behavior, observe its qualities, and make classification the conclusion of the analysis.

ROB-SN models an operator's behavior as a stateful transducer over explicitly defined spaces. It is not an official RxJS standard, replacement implementation, compiler, or claim of exhaustive operator equivalence.

$$
\boxed{\delta_\theta:S\times E\longrightarrow S\times A^*}
$$

$$
\boxed{\delta_\theta(s,e)=(s',\alpha)}
$$

What is remembered together with what arrived determines what must now be remembered and what must happen next. A reaction produces an **ordered finite sequence of actions**, not an unordered set.

## Model → Observe → Classify

```text
MODEL       Represent a scoped operator/configuration as a transducer.
  |
OBSERVE     Derive qualities from reactions; compare with execution evidence.
  |
CLASSIFY    Identify justified behavior families and policies.
```

The [project guide](docs/PROJECT-GUIDE.md) explains this workflow. **Language for teaching; algebra for precise semantics.**

## Family-by-family implementation

The [Operator-Family Implementation Plan](docs/FAMILY-IMPLEMENTATION-PLAN.md) organizes the next work into **34 bounded study packages across eight phases**, with a qualified API inventory, dependencies, per-session deliverables, completion gates, and a durable GitHub handoff.

**Next session: F01 — Taking and dropping prefixes**, using `takeWhile` as the reference and comparing `skipWhile`, `take`, and `skip`.

Each session implements scoped ROB-SN specifications, compares related operators, records source and trace evidence, and saves a verified checkpoint to `main`. Study families organize the investigation; classification remains its conclusion. The plan proposes a small RxJS 7.8.2 trace-verification harness in F01, not an operator replacement or compiler.

**Planning checkpoint:** 0 of 34 family packages complete. The roadmap is saved; family implementation and its new runtime checks have not started. Use the current roadmap checkpoint rather than this initial announcement when resuming later sessions.

## The five-slot view

| Slot | Question |
|---|---|
| Event | What arrived? |
| Memory | What must be remembered? |
| Lifecycle | What is connected, owned, or being released? |
| Execution Status | Is this scoped execution open, or how did it end? |
| Next Actions | What must happen next, in which order? |

Persistent state can be decomposed as $s=(q,\ell,m)$: status, lifecycle bookkeeping, and processing memory. Events arrive and action sequences are produced; neither is automatically a persistent-state field. Detailed execution models can add intermediate phases and suspended frames.

**A combination of slot contents describes a configuration. Transition rules and their execution contract describe behavior.**

## Reading path

| Document | Purpose |
|---|---|
| [Project guide](docs/PROJECT-GUIDE.md) | Purpose, teaching vocabulary, and Model → Observe → Classify |
| [Operator-family implementation plan](docs/FAMILY-IMPLEMENTATION-PLAN.md) | Session order, API assignments, progress, completion gates, and the F01 brief |
| [Slot catalogue](docs/SLOT-CATALOGUE.md) | Five slots, value spaces, identities, memory shapes, and ownership |
| [Transition-rule catalogue](docs/TRANSITION-RULE-CATALOGUE.md) | 40 proposed templates across seven families |
| [Behavioral qualities and trace laws](docs/BEHAVIORAL-QUALITIES.md) | Triggers, cardinality, timing, concurrency, cancellation, termination, sharing, and valid histories |
| [Sequence-processing behavior families](docs/BEHAVIOR-FAMILIES.md) | Mapping, filtering, folding, flattening, taking/dropping, and batching/segmentation |
| [Lessons from Hickey's transducers](docs/TRANSDUCER-LESSONS.md) | Shared contracts without conflating reducing-function transformers and Observable machines |
| [Foundational reference](docs/FOUNDATION.md) | Set-theoretic definitions and original operator examples |
| [Execution contract](docs/EXECUTION-CONTRACT.md) | Initialization, synchronous nesting, callbacks, clocks, cancellation, teardown, and sharing |
| [Operator-analysis template](templates/OPERATOR-ANALYSIS.md) | Scope, slots, guarded transitions, evidence, derived qualities, and final classification |
| [take(3) profile](examples/TAKE-3.md) | Count-controlled prefix acceptance and early completion |
| [bufferCount(3) profile](examples/BUFFER-COUNT-3.md) | Same pending memory, different completion/error/cancellation reactions |
| [Primary references](docs/REFERENCES.md) | Initial-edition pinned sources and evidence limits; newer pages link their additional sources directly |
| [Consolidation and verification record](docs/CONSOLIDATION-2026-09-29.md) | Coverage of this discussion, corrections, and checks actually performed |
| [Contribution guide](CONTRIBUTING.md) | Standards for extending the notation |
| [Change log](CHANGELOG.md) | Specification history |

The original foundation and execution contract remain intact. Original examples include map, filter, seeded/seedless scan, combineLatest, and the switchMap control-flow outline. The new catalogues organize and extend those foundations; they do not replace their qualifications.

## Core vocabulary

| Symbol | Meaning |
|---|---|
| $S$; $s,s'\in S$ | State space; current and next states |
| $E$; $e\in E$ | Event space; one incoming event |
| $A$; $\alpha\in A^*$ | Individual action alphabet; ordered finite action sequence |
| $s_0\in S$ | Initial state |
| $\theta$ | Fixed operator parameters and declared policies |
| $\delta_\theta$ | Guarded transition function |
| $\mathcal I_\theta$ | Action interpreter and execution contract |
| $\mathrm{Inv}\subseteq S$ | Valid states |

$$
\boxed{\mathcal O_\theta=(S,E,A,s_0,\delta_\theta,\mathcal I_\theta,\mathrm{Inv})}
$$

Sets alone do not preserve histories, buffer order, or action multiplicity:

```text
[Cancel(old), Subscribe(new)] != [Subscribe(new), Cancel(old)]
[Emit(a), Emit(a)]            contains two emissions, not one
[]                           is not [Emit([])]
```

A memoryless processing core uses a singleton state space, not an empty set. Memory spaces may be infinite even when their definitions are finite. A template catalogue does not prove that every operator profile is covered.

## Execution commitments

Separate source completion, downstream completion, error, cancellation, and cleanup. Cancellation is not a fourth Observable notification. Define state ownership, sharing/reset boundaries, callback indexes, supplied-function assumptions, timing, and event-processing order explicitly.

An ordered action list is not an uninterruptible transaction. Notification delivery, subscription, projection, and teardown can synchronously reenter the graph. Logical terminal post-states in behavioral tables do not mean closing the destination before a preceding emission. Exact execution models must account for visible intermediate writes and suspended work.

The domain can change. The stream-processing mechanism stays the same.

## Evidence and checks

This is a documentation/specification project. The new worked profiles are scoped behavioral models supported by pinned source inspection, not runtime conformance proofs. No RxJS runtime suite or theorem prover was executed for this consolidation.

A dependency-free documentation check is available:

```sh
python3 scripts/check_docs.py
```

It checks local Markdown target paths, code/display-math delimiter balance, pinned RxJS implementation links, and the 40 unique rule IDs. It does not validate external URL availability, all Markdown rendering, RxJS semantics, or runtime equivalence. See the [verification record](docs/CONSOLIDATION-2026-09-29.md) for the exact checks run during preparation.

## Attribution

**GPT-6 Astra is the main contributor of the project.** Hans Schenker initiated the project, supplied the motivating questions, and collaborates on its development. This credit does not present ROB-SN as an official RxJS or OpenAI standard.
