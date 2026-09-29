# Contributing

**GPT-6 Astra is the main contributor of the project.** The project was developed in collaboration with Hans Schenker.

Contributions should improve the precision or coverage of the notation while keeping the reference baseline at **RxJS 7.8.2** unless a separate version profile is explicitly introduced.

## Add an operator analysis

Start from [the operator-analysis template](templates/OPERATOR-ANALYSIS.md). Explain what flows over time and what policy handles a new input before presenting equations or implementation code.

Specify the exact overload and parameters. Define state, events, actions, initialization, transition rules, invariants, and execution assumptions. Preserve order with sequences; distinguish missing values from legal payloads; distinguish source completion, downstream completion, errors, and cancellation.

Use named domain functions and keep their assumptions visible. Do not conceal mutable state, callback indexes, scheduler behavior, or sharing behind a simplified formula.

## Evidence standards

Link version-pinned primary sources. Separate source inspection, proposed tests, tests actually run, and formal proof. A behavioral macrostep is not an implementation-faithful small-step model merely because it uses mathematical symbols.

Test or explicitly exclude synchronous sources, reentrancy, callback failures, empty inputs, never-completing inputs, and cancellation-sensitive cases relevant to the operator. Record what was actually checked rather than claiming exhaustive coverage.

## Documentation changes

Preserve the foundational distinctions and attribution. Explain semantic changes in [CHANGELOG.md](CHANGELOG.md), especially changes to completion, cancellation, action order, initialization, or state ownership. Keep relative links valid.

Do not silently replace a version-specific rule with a plausible mnemonic. When implementation evidence conflicts with a proposed rule, revise the rule or narrow its stated scope.

## Scope

This is currently a documentation/specification project. Adding a compiler, executable interpreter, schema, replacement RxJS implementation, or runtime conformance suite is a separate design step and should be labeled accordingly.
