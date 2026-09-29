# ROB-SN Operator-Family Implementation Plan

**Revision:** 1.0 — 29 September 2026.  
**Baseline:** RxJS **7.8.2**, without a version migration.  
**Repository:** `hansschenker/rxjs-operator-behavior-set-notation`.  
**Delivery model:** One bounded study family per user-initiated session; save the session's completed work to `main`.  
**Attribution:** GPT-6 Astra is the main contributor of the project, in collaboration with Hans Schenker.

> Organize the work familywise. Specify each operator profile precisely. Derive classification from evidence.

## 1. What “implement a family in ROB-SN” means

Implement a source-backed **behavioral specification**, not a replacement RxJS library. Each operator/configuration profile must explain what flows, what arrives, what is remembered, what changes, and which ordered actions follow. It uses the existing notation:

$$
\delta_\theta:S\times E\longrightarrow S\times A^*,\qquad
\delta_\theta(s,e)=(s',\alpha).
$$

The resulting state specifies what is retained; the ordered actions specify what must be done. The execution contract determines when state writes occur, how actions run, and how cancellation or synchronous re-entry can interrupt them.

The deliverable is a specification corpus, family comparisons, and recorded verification. **A compiler, generic ROB-SN interpreter, generated operators, npm publication, and RxJS 8/9 migration are not part of this plan.**

A small TypeScript trace-conformance harness against the real `rxjs@7.8.2` is a **planned verification extension**, introduced explicitly in F01. It is not present or claimed to run merely because this roadmap exists. The existing contribution guide treats a runtime suite as a separate design step; F01 must document that step and keep the distinction between specification, implementation evidence, and proof.

Use the existing [project guide](PROJECT-GUIDE.md), [execution contract](EXECUTION-CONTRACT.md), [operator-analysis template](../templates/OPERATOR-ANALYSIS.md), [slot catalogue](SLOT-CATALOGUE.md), and [transition-rule catalogue](TRANSITION-RULE-CATALOGUE.md). Preserve the existing foundation and worked examples; extend or link them rather than silently replacing their scope.

## 2. Current checkpoint

| Field | Current value |
|---|---|
| Planning work | Roadmap prepared; family implementation has not started under this plan |
| Completed family packages | **0 / 34** |
| Next session | **F01 — Taking and dropping prefixes** |
| F01 reference operator | **takeWhile** |
| Other F01 operators | skipWhile, take, skip |
| Default branch | main |
| Existing material to reuse | take(3), bufferCount(3), foundation examples, catalogues, and execution contract |
| Existing runtime verification | No family conformance suite established by this planning change |

Existing explanations or examples are useful seeds, not evidence that a complete family package has already passed this plan's completion gate. There is no timed or background execution: subsequent sessions begin when the user requests them.

## 3. Scope and inventory rules

The inventory below assigns **146 named entries** to an initial owning family: **113 normalized pipeable implementation entries**, **30 creation/source entries including EMPTY and NEVER**, and **3 transport-adapter targets**. These are bookkeeping entries, not 146 distinct semantic machines or all possible overloads.

The core names were reconciled against the pinned [rxjs/operators export index](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/operators/index.ts) and [rxjs root export index](https://github.com/ReactiveX/rxjs/blob/7.8.2/src/index.ts). Inspected blob identities were `5b190197e57d8cf63ceb33e4a99a66876253af07` and `1805341dfb6861b5aed6a04517705eac51173ba5`, respectively. Transport entry points are explicit extension targets; inspect their exports and implementations when their sessions begin.

**Inventory prefixes are notation for this plan, not import syntax:**

- `P:name`: pipeable implementation/API entry.
- `C:name`: creation function, source constant, or connection-creation entry.
- `X:name`: transport entry point (`rxjs/ajax`, `rxjs/fetch`, or `rxjs/webSocket`).

The same spelling can designate different public APIs. For example, `C:zip` and the legacy `P:zip` must not be collapsed. Ordinary root re-exports and `rxjs/operators` re-exports of the same implementation are counted once. The `rxjs/operators` export named `onErrorResumeNext` is tracked under its implementation/root-export name `P:onErrorResumeNextWith`; the creation `C:onErrorResumeNext` remains separate.

Legacy or deprecated entries remain in their owning families. For aliases and wrappers, inspect the delegation and record configuration/type/behavior limits; do not assume equivalence from a similar name. Compatibility may be documented in an appendix to a canonical profile, but every listed name needs an explicit disposition.

Core classes, interfaces, error classes, scheduler objects, `pipe`, `identity`, `noop`, `isObservable`, global configuration, testing utilities, and `firstValueFrom`/`lastValueFrom` are **supporting or out-of-corpus APIs**, not silently missing operator families. Subject and scheduler behavior must still be modeled where an operator depends on it. Instance methods and all overload combinations are not claimed covered by this name inventory.

### Families organize investigation, not final classification

These are **34 study packages across eight phases**, not 34 disjoint behavioral classes. A package can contain closely related subfamilies or contrasting implementations. An operator has one owning package for progress tracking and may receive multiple justified classification tags. Cross-family behavior is linked, not implemented twice.

For every named entry, declare concrete profiles: input kinds, overload/configuration, callback assumptions, scheduler, ownership, and observation scope. A profile can be parameterized where the rules justify it. An undocumented case is unspecified, not implicitly supported. Completing named-entry coverage is different from covering the entire API surface or proving equivalence.

## 4. Session sequence and progress tracker

**All rows initially have status Planned.** Change a row only when its evidence warrants the new status. The default sequence is F01 → F34; dependencies shown in each row must be available before that package is completed. Supporting test sources may be used before their full source-family specification is written, but their required fixture behavior must be declared and pinned.

Each row identifies a reference operator, its initial owning inventory, and the central distinction to establish. Its detailed completion criteria also include the shared checklist in section 7.

### A. Single-source behavior

| Session / status | Family and reference | Assigned entries | Required distinctions / dependencies |
|---|---|---|---|
| **F01** — Planned | **Taking and dropping prefixes**; reference: `takeWhile` | `P:takeWhile`, `P:skipWhile`, `P:take`, `P:skip` | Count versus predicate boundary; inclusive boundary; index advancement; early completion versus continued participation. Dependencies: existing foundation. |
| **F02** — Planned | **Mapping and per-value selection**; reference: `map` | `P:map`, `P:filter`, `P:ignoreElements`, `P:mapTo`, `P:pluck` | Value transformation versus selection; callback indexes and exceptions; unchanged payload identity; compatibility forms. Dependencies: F01. |
| **F03** — Planned | **Distinctness and adjacent-value memory**; reference: `distinctUntilChanged` | `P:distinctUntilChanged`, `P:distinctUntilKeyChanged`, `P:distinct`, `P:pairwise` | Last emitted key versus accumulated keys versus previous input; comparator/key-selector failure; reset notifier. Dependencies: F02. |
| **F04** — Planned | **Search and cardinality constraints**; reference: `first` | `P:first`, `P:last`, `P:elementAt`, `P:find`, `P:findIndex`, `P:single` | Early answer versus completion-dependent answer; empty/default/error policies; zero, one, or multiple matches. Dependencies: F02. |
| **F05** — Planned | **Folding and aggregation**; reference: `scan` | `P:scan`, `P:reduce`, `P:count`, `P:min`, `P:max`, `P:toArray` | Seeded and seedless initialization; retained accumulation versus emission policy; completion flush; empty input. Dependencies: F02. |
| **F06** — Planned | **Boolean queries and empty-input policies**; reference: `every` | `P:every`, `P:isEmpty`, `P:defaultIfEmpty`, `P:throwIfEmpty` | Early decision versus completion-time decision; defaults, predicate failure, and empty-sequence errors. Dependencies: F04, F05. |
| **F07** — Planned | **Sequence boundaries and retained tails**; reference: `takeLast` | `P:takeLast`, `P:skipLast`, `P:startWith`, `P:endWith` | Retained suffix versus delayed forwarding; prepend/append ordering; source subscription and completion boundaries. Dependencies: F01, F05. |

### B. Activation, sources, and clocks

| Session / status | Family and reference | Assigned entries | Required distinctions / dependencies |
|---|---|---|---|
| **F08** — Planned | **Finite and terminal source creation**; reference: `of` | `C:of`, `C:range`, `C:EMPTY`, `C:NEVER`, `C:throwError`, `C:pairs`, `C:empty`, `C:never` | Construction versus activation; synchronous progression and interruption; empty, never, error; legacy entry points. Dependencies: F01. |
| **F09** — Planned | **Input adaptation and scheduled conversion**; reference: `from` | `C:from`, `C:scheduled` | Array-like, Iterable, Promise-like, Observable/interop, AsyncIterable and ReadableStream profiles; identity, pull/push, teardown and scheduling. Dependencies: F08. |
| **F10** — Planned | **Deferred selection and callback adaptation**; reference: `defer` | `C:defer`, `C:iif`, `C:bindCallback`, `C:bindNodeCallback` | Factory timing, callback invocation and reuse, error-first callback adaptation, repeated subscriptions, and captured versus fresh work. Dependencies: F08, F09. |
| **F11** — Planned | **External-event source adaptation**; reference: `fromEvent` | `C:fromEvent`, `C:fromEventPattern` | Listener identities, registration/removal, argument packaging, construction failures, and producer ownership. Dependencies: F08. |
| **F12** — Planned | **Clock sources, scheduling and temporal metadata**; reference: `timer` | `C:timer`, `C:interval`, `C:animationFrames`, `P:observeOn`, `P:subscribeOn`, `P:timestamp`, `P:timeInterval` | Driver events and scheduler identity; subscription versus notification scheduling; timestamps versus processing order; cancellation. Dependencies: F08, F09. |

### C. Notifiers and temporal controls

| Session / status | Family and reference | Assigned entries | Required distinctions / dependencies |
|---|---|---|---|
| **F13** — Planned | **Notifier-controlled participation**; reference: `takeUntil` | `P:takeUntil`, `P:skipUntil` | Notifier next, complete, and error as separate events; subscription order; synchronous notifier; open versus close policy. Dependencies: F01, F11. |
| **F14** — Planned | **Silence and lockout selection**; reference: `debounce` | `P:debounce`, `P:debounceTime`, `P:throttle`, `P:throttleTime` | Duration-selected versus fixed-time control; leading/trailing combinations; boundary replacement; completion/error/cancellation. Dependencies: F12, F13. |
| **F15** — Planned | **Window-end selection and sampling**; reference: `audit` | `P:audit`, `P:auditTime`, `P:sample`, `P:sampleTime` | Duration-end selection versus sampling triggers; readiness and retained values; notifier termination; synchronous boundaries. Dependencies: F12, F13. |
| **F16** — Planned | **Delivery delays and deadlines**; reference: `delayWhen` | `P:delay`, `P:delayWhen`, `P:timeout`, `P:timeoutWith` | Per-value release versus deadline failure/fallback; pending work; subscriptionDelay; first/each timeout and cancellation. Dependencies: F09, F12, F13. |

### D. Batches and streaming segments

| Session / status | Family and reference | Assigned entries | Required distinctions / dependencies |
|---|---|---|---|
| **F17** — Planned | **Buffered batches**; reference: `bufferCount` | `P:bufferCount`, `P:buffer`, `P:bufferTime`, `P:bufferToggle`, `P:bufferWhen` | Count/time/notifier/open-close boundaries; overlap; empty batches; partial flush; boundary failures and disposal. Dependencies: F05, F12, F13. |
| **F18** — Planned | **Streaming windows**; reference: `windowCount` | `P:windowCount`, `P:window`, `P:windowTime`, `P:windowToggle`, `P:windowWhen` | Output Observable identities and lifetimes versus array snapshots; overlapping windows; cancellation and completion scopes. Dependencies: F17. |

### E. Coordination, inner streams, and feedback

| Session / status | Family and reference | Assigned entries | Required distinctions / dependencies |
|---|---|---|---|
| **F19** — Planned | **Multi-source value joins**; reference: `combineLatest` | `C:combineLatest`, `P:combineLatestWith`, `P:combineLatest`, `C:zip`, `P:zipWith`, `P:zip`, `C:forkJoin`, `P:withLatestFrom`, `P:sequenceEqual` | Port readiness, queues versus latest slots, source completion, missing first values, final joins, and subscription order. Dependencies: F05, F09. |
| **F20** — Planned | **Stream assembly and competition**; reference: `concat` | `C:concat`, `P:concatWith`, `P:concat`, `C:merge`, `P:mergeWith`, `P:merge`, `C:race`, `P:raceWith`, `P:race` | Sequential activation versus overlap versus winner selection; synchronous termination; losing-source cancellation. Dependencies: F19. |
| **F21** — Planned | **Inner-stream admission policies**; reference: `mergeAll` | `P:mergeAll`, `P:concatAll`, `P:switchAll`, `P:exhaustAll`, `P:exhaust` | Allow overlap, queue, latest only, ignore while busy; capacity; outer completion with pending/active inners; aliases. Dependencies: F20. |
| **F22** — Planned | **Projected inner-stream admission**; reference: `mergeMap` | `P:mergeMap`, `P:concatMap`, `P:switchMap`, `P:exhaustMap`, `P:flatMap`, `P:mergeMapTo`, `P:concatMapTo`, `P:switchMapTo` | Projection invocation versus admission; cancellation before replacement; queue payloads, capacity and callback indexes; legacy forms. Dependencies: F02, F21. |
| **F23** — Planned | **Higher-order value joins**; reference: `combineLatestAll` | `P:combineLatestAll`, `P:zipAll`, `P:combineAll` | Collection of input Observables versus their later subscriptions; outer completion dependency; inner lifetimes; alias. Dependencies: F19, F21. |
| **F24** — Planned | **Generation, recursion and higher-order accumulation**; reference: `expand` | `C:generate`, `P:expand`, `P:mergeScan`, `P:switchScan` | Fold versus unfold; feedback, seed/current state, recursion scheduling, concurrent state updates, and latest-only cancellation. Dependencies: F05, F12, F22. |
| **F25** — Planned | **Keyed groups and predicate splitting**; reference: `groupBy` | `P:groupBy`, `C:partition`, `P:partition` | Keyed output lifetimes, duration closure/reappearance and ownership; two filtered branches are not batching or implicit sharing. Dependencies: F02, F18. |

### F. Recovery, repetition, and lifecycle

| Session / status | Family and reference | Assigned entries | Required distinctions / dependencies |
|---|---|---|---|
| **F26** — Planned | **Error recovery and error-driven resubscription**; reference: `catchError` | `P:catchError`, `P:retry`, `P:retryWhen`, `C:onErrorResumeNext`, `P:onErrorResumeNextWith` | Replacement versus resubscription; retry count/delay/reset; notifier termination; error provenance; continuation without conflating completion. Dependencies: F10, F12, F21. |
| **F27** — Planned | **Completion-driven resubscription**; reference: `repeat` | `P:repeat`, `P:repeatWhen` | Completion versus error triggers; finite/infinite repetitions; delay/notifier semantics; synchronous loops and cancellation. Dependencies: F26. |
| **F28** — Planned | **Notifications as stream values**; reference: `materialize` | `P:materialize`, `P:dematerialize` | Notification objects versus actual next/error/complete delivery; terminal ordering and invalid notification profiles. Dependencies: F02, F08. |
| **F29** — Planned | **Lifecycle observation and resource scoping**; reference: `finalize` | `P:finalize`, `P:tap`, `C:using` | Terminal notification versus finalization; source/user-handler/teardown error origins; resource-factory acquisition and release. Dependencies: F10, F26, F28. |

### G. Connections, sharing, and replay

| Session / status | Family and reference | Assigned entries | Required distinctions / dependencies |
|---|---|---|---|
| **F30** — Planned | **Connection ownership and multicast primitives**; reference: `connect` | `P:connect`, `C:connectable`, `P:multicast`, `P:refCount` | Subscriber versus coordinator scope; manual connection, selectors, connection generations, reference counting, and legacy signatures. Dependencies: F21, F29. |
| **F31** — Planned | **Sharing and reset policies**; reference: `share` | `P:share` | Subscriber membership; upstream connection ownership; reset on error/complete/refCount zero; reset notifier identities and interruption. Dependencies: F30. |
| **F32** — Planned | **Replay and publication policies**; reference: `shareReplay` | `P:shareReplay`, `P:publish`, `P:publishBehavior`, `P:publishLast`, `P:publishReplay` | Replay buffer/time scope; refCount and reset rules; completed/error cache states; seed/last-value publication and compatibility. Dependencies: F12, F30, F31. |

### H. Transport boundaries

| Session / status | Family and reference | Assigned entries | Required distinctions / dependencies |
|---|---|---|---|
| **F33** — Planned | **HTTP transport sources**; reference: `fromFetch` | `X:fromFetch`, `X:ajax` | Request creation versus subscription; response/body-selection profiles; cancellation/abort ownership; adapter and transport errors. Dependencies: F09, F29. |
| **F34** — Planned | **WebSocket channels**; reference: `webSocket` | `X:webSocket` | Shared socket/output/input ownership; open/close/error events; outgoing buffers; multiplex participation and reconnection boundaries. Dependencies: F11, F30, F31, F32. |

## 5. Repeatable workflow for every session

### A. Resume and freeze the session scope

Read the current repository version of this plan, the previous completed package's evidence, the family comparison pages needed by dependencies, and the shared execution contract. Never rely on remembered chat text as the only source of project status.

Select the next Planned family whose dependencies are satisfied, or resume the current In progress/Blocked family first. State the exact family ID, named entries, proposed configuration profiles, and exclusions. Do not silently expand a family or change the RxJS baseline.

### B. Consult source first, then express the behavior

Read the pinned 7.8.2 implementations, delegated helpers, and relevant upstream specs. Follow public wrappers to the actual producer/coordinator/handler. For example, a tiny creation function can delegate its important loop or teardown behavior elsewhere.

Record a source-to-model map: configuration; initialization; persistent processing memory; resource ownership; incoming events; temporary/frame-local values; state writes; ordered actions; inherited notification/teardown rules. Source code provides evidence, not a requirement to reproduce its variable layout.

Explain the behavior in ordinary stream language first. Then specify the full ROB-SN profile with the existing operator-analysis template. Model first; extract qualities and classify afterward.

### C. Build one complete reference, then compare its neighbors

Fully describe the reference profile. Introduce the nearest contrast, ideally changing one policy at a time. Reuse a rule only when its guards, action order, lifecycle, callback behavior, and observation scope remain valid. An operator-specific page must remain understandable through explicit cross-references, not an unexplained “same as operator X.”

Produce a family comparison matrix covering inputs/triggers, memory, resulting state, actions, cardinality, timing, concurrency, cancellation, termination, and ownership/sharing. Include at least one trace that distinguishes each neighboring behavior.

### D. Compare predictions with real execution

Write expected traces from the model; run matching cases against pinned RxJS. Capture outputs, order, terminal kind, and the relevant callback indexes, subscription lifetimes, resource disposal, or nested execution. Separate model-predicted actions from delivered observations.

Use RxJS TestScheduler for virtual-time cases and direct synchronous tests where callback order or re-entry matters. Use deterministic fakes for browser/transport contracts; label adapter-level mock checks separately from real browser/network integration. Do not use sleep-based timing as the default evidence mechanism.

Callback-dependent business logic belongs in named, typed functions. Prefer functional TypeScript examples and small explicit trace recorders. Do not add `tap` as unexplained diagnostic machinery; F29 may of course test `tap` itself.

### E. Save a coherent package and hand off

Update the family page, operator profiles, tests/traces, evidence record, coverage index, this plan's status/checkpoint, and CHANGELOG. Update shared catalogues only when a genuinely reusable construct is needed, explaining the change rather than silently modifying earlier semantics.

Validate, commit to `main`, and read back the saved files or immutable commit. Finish the session with: completed scope; exclusions/open questions; exact checks and outcomes; changed paths; verified commit SHA; and the next family ID. If publishing or verification fails, report it and leave the package unfinished rather than claiming it is saved.

## 6. Repository deliverables

The following **future paths are conventions**, not a claim that files already exist:

```text
families/
  F01-prefix-selection.md               family explanation and comparison matrix
operators/
  pipeable/takeWhile.md                  canonical entry; named configuration profiles
  pipeable/skipWhile.md
  pipeable/take.md
  pipeable/skip.md
  creation/<name>.md                     source/creation/connection profiles
  transport/<name>.md                    transport adapter profiles
traces/
  F01-prefix-selection.md                expected trace tables and discriminating cases
tests/
  conformance/F01-prefix-selection.spec.ts
  support/                              shared trace and resource recorders
evidence/
  F01-prefix-selection.md                sources inspected, checks run, limits, results
docs/
  OPERATOR-COVERAGE.md                   initialized in F01 from this inventory
  FAMILY-IMPLEMENTATION-PLAN.md          this roadmap and current checkpoint
```

Use a single authoritative profile for each API identity. Aliases may link to it with an explicit compatibility record. Keep the distinction between `operators/pipeable/zip.md` and `operators/creation/zip.md`. Preserve existing `examples/TAKE-3.md` and `examples/BUFFER-COUNT-3.md`; link or extend them with scope and history intact.

The coverage index must record: qualified API entry, owning family, profile IDs/configurations, evidence level, source/helper references, verification cases, exclusions, and profile path. Classification tags are separate from the owning family. Extend the index when a new overload profile is deliberately added; never inflate “covered” from name recognition alone.

### One-time verification setup in F01

Document and add a minimal development-only harness: exact `rxjs: 7.8.2`, locked TypeScript/tooling dependencies, typed tests using Node's test runner, and TestScheduler support. No operator reimplementation is needed. Record the actual supported Node/tooling versions when established; do not invent them in the evidence file.

Introduce commands with these contracts:

```sh
python3 scripts/check_docs.py           # already available: documentation only
npm ci                                 # once package.json and lockfile exist
npm run typecheck                      # introduced and verified in F01
npm run test:family -- F01              # runner accepts a family ID; created in F01
npm test                               # all implemented family regression tests
```

The npm commands above are **planned interfaces**, not currently available or already passing commands. F01 must implement and verify them. Update CONTRIBUTING/README accurately when the verification extension lands. Preserve the distinction between documentation checks, runtime trace checks, and proof.

## 7. Completion gate: when a family is complete

A family is **Complete (declared scope)** only when all the following hold:

1. Every assigned entry has a source-backed canonical profile or an explicit verified alias/compatibility disposition. No assigned entry is simply omitted. Configuration/input-kind exclusions are visible in the coverage index.
2. Each profile defines parameters, event/state/action spaces, initialization, guarded transitions, invariants, execution assumptions, and termination/resource behavior. State/phase names are not falsely equated with Subscriber's concrete stopped/closed fields.
3. The event domain covers normal input, source termination, callback failures, cancellation, and relevant notifier/inner/timer events; omitted categories have reasons. Rules are exhaustive for that declared domain, with nonoverlapping guards or explicit precedence.
4. The family comparison and discriminating traces distinguish nearby alternatives. Passing-value-only examples are insufficient. Empty, never-ending, singleton, boundary, source-error, and cancellation cases are addressed when applicable.
5. Runtime checks for the declared core profiles were actually executed and match the model's observations. Exceptions, callback indexes, same-time ordering, synchronous subscription, re-entry, and teardown are tested or explicitly scoped out with a reason. Known mismatches are not concealed by changing expectations to match the implementation without revisiting the model.
6. Complete/error/cancel remain distinct. Ordered actions are interruptible. State-commit timing is explicit wherever re-entry can observe it; a terminal macrostep result never suppresses its own earlier pending Emit. Creation models distinguish construction-time throws, activation, driving events, and ownership. Shared models distinguish subscriber and coordinator scope.
7. Documentation/type checks, the current family tests, and all previously implemented regression tests pass. Any unavailable environment-dependent verification remains a named limitation; core validation failure blocks completion.
8. Evidence, coverage, roadmap/checkpoint, and change log are updated, the changes are saved to GitHub, and the saved revision is verified. Source inspection or proposed tests alone cannot be reported as completed runtime verification.

**Complete is not a proof of full API equivalence.** It means the package satisfies the gate for its explicitly declared profiles. Parameter space, all overloads, all schedulers, all browser integrations, and arbitrary reentrant programs are not automatically covered.

### Status vocabulary and interruption policy

`Planned` → `In progress` → `Source reviewed` → `Trace tested` → `Complete (declared scope)`.

Use `Blocked` with a concrete reason when necessary. Intermediate statuses may be checkpointed. Do not mark a family complete to keep a schedule. One session targets one bounded family; this is a unit of work, not a promised duration. If a package needs continuation, resume it under the same family ID before starting a new unrelated family. A planned split must be recorded as a subfamily with explicit reassignment; do not hide unfinished work.

## 8. F01: exact first-session brief

**Family:** Taking and dropping prefixes.  
**Reference:** `takeWhile`.  
**Scope:** Four pipeable APIs, one downstream subscription per execution, no introduced sharing, RxJS 7.8.2.

### Profiles to establish

| Entry | Initial profile coverage |
|---|---|
| takeWhile | Boolean-returning indexed predicate; inclusive false/default and true; normal return and predicate throw |
| skipWhile | Indexed predicate; initial skipping and subsequent forwarding phases; predicate evaluation stops at the boundary |
| take | Nonnegative integer counts, including 0, 1, and a parameterized positive count |
| skip | Nonnegative integer counts, including 0, 1, and a parameterized positive count |

Treat negative/fractional/NaN/Infinity counts, non-Boolean runtime returns, overload-specific narrowing, and unmodeled external mutation as explicit profile extensions or exclusions, not hidden claims. Document the valid typed API and the selected runtime assumptions separately.

Read the four operator implementations, `operate`, `OperatorSubscriber`, `Subscriber`, `Subscription`, their relevant source-subscription machinery, and upstream tests. Reuse [the existing take(3) example](../examples/TAKE-3.md) without treating it as full take API coverage.

### Required discriminating traces

Use fresh independent subscriptions to the same declared input history. For the pure predicate `value < 5`, compare source values `2, 4, 7, 1`, followed by completion: default takeWhile, inclusive takeWhile, and skipWhile must have separately justified traces. Add a filter comparison as a narrowly scoped contrast fixture; do not mark F02 complete from that fixture.

Also cover: predicate false on the first value; always true until source completion; empty and never sources; source error; predicate throw; predicate indexes; take(0) versus skip(0) source-subscription behavior; count boundary; explicit downstream unsubscription; and a cooperative synchronous source's stopped production.

Include a synchronous cancellation-during-inclusive-emission trace and a bounded re-entry example, or clearly label the macrostep exclusion and add a separate execution-order note demonstrating why atomic state installation would be wrong. The failing inclusive value is requested before completion; the stored index advances before predicate invocation. Tests must distinguish requested completion from completion actually delivered after cancellation.

### F01 acceptance

The reference and three neighboring profiles, their comparison page, traces, executed tests, harness setup, evidence record, initial coverage index, updated progress/checkpoint, and verified repository save must all exist. The next default family is **F02 — Mapping and per-value selection**.

## 9. Creation and compatibility rules that apply throughout

Creation APIs are distributed into the family where their machinery is studied. Primitive source profiles appear in F08–F12; joins and stream assembly in F19–F20; generation in F24; resource creation in F29; connections in F30; transports in F33–F34. They are not all treated as machines with no inputs.

Every creation profile distinguishes function call/construction, subscription activation, the actual driving events, and owned resources. A fresh subscription does not imply a fresh independent producer. Cancellation identifies the listener/task/subscription/operation affected and does not promise to undo external side effects.

For direct creation and pipeable variants of joins, compare input ordering, argument shape, subscription order, scheduler/selector variants, and completion behavior. Similar names and wrappers do not by themselves establish identical full APIs. Legacy entries are valid baseline subjects; no migration to a future major version is part of this work.

## 10. Closing audit after F34

Run one explicit cross-family integration/coverage checkpoint after the family sessions. This is an audit, not a 35th invented operator family.

Reconcile all 146 planned names and any newly discovered entry-point/profile adjustments. Audit aliases and same-name creation/pipeable forms. List unsupported overloads, environment dependencies, unresolved reentrancy cases, and residual conformance gaps. Verify every classified quality is justified by a model/evidence reference.

Run the full available regression suite and selected cross-family pipelines exercising source activation, early cancellation, nested delivery, time boundaries, recovery, and sharing. Review changes to reused transition templates against earlier profiles. Publish a coverage report separating named-entry coverage, profile coverage, selectively checked traces, and any actual proofs.

Do not declare “all RxJS behavior implemented” merely because every inventory row has a document.

## 11. GitHub save and session handoff policy

Use the current `main` branch unless the user changes that policy. Read current file contents and blob SHAs before replacement; preserve unrelated edits and attribution. Prefer one coherent family commit where the connector supports it; otherwise use a short ordered commit sequence and identify its final verified checkpoint. Do not force-push or rewrite history.

Suggested family commit message:

```text
docs(rob-sn): implement F01 prefix-selection profiles and trace checks

Co-Authored-By: GPT-6 Astra <noreply@openai.com>
```

The family evidence file records the inspected source versions, run environment, commands, outcomes, and limitations. Report the newly verified commit SHA in the session response; do not invent a self-referential commit hash inside the commit being created. Repository history and the updated tracker are the durable resume point.

Use this instruction to start the next session:

> Read docs/FAMILY-IMPLEMENTATION-PLAN.md from main. Implement F01 — Taking and dropping prefixes, following the first-session brief and the existing ROB-SN operator-analysis template. Derive the rules from RxJS 7.8.2 source, compare and validate the selected profiles, update progress and evidence, save the work to this repository, and verify the commit.

For subsequent sessions:

> Read the current plan and evidence from main. Resume any unfinished family; otherwise implement the next Planned family whose dependencies are satisfied. Keep the declared scope, run the required checks, update the checkpoint, and save and verify the work in this repository.

## 12. Planning evidence and limits

This planning change reviewed the repository tree, README, contribution guide, change log, and pinned public root/operator export lists. The existing foundation, execution contract, and family/classification principles are preserved. Assignment checks require each inventoried name to have exactly one owning family and every declared dependency to precede its consumer.

The plan records future semantic investigations, not source-reviewed verdicts for every operator in its tables. Family conformance tests have not been created or executed in this planning session. Local roadmap validation concerns its structure, assignment consistency, and relative targets; it is not execution of the repository-wide documentation checker or an RxJS test suite.

**Next action: begin F01. No operator family is marked complete by this roadmap commit.**
