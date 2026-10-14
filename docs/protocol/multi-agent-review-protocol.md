# Standing Multi-Agent Review Protocol

## Roles

- **Agricultural / physical systems reviewer (Aris role):** crop/soil/hydrology constraints, domain applicability, biological realism, field practicality.
- **AI / systems reviewer (Turing role):** architecture, algorithm choice, computational cost, data design, implementation and evaluation.
- **Adversarial reviewer (Murphy role):** counterexamples, failure modes, OOD conditions, leakage, false certainty, and verification of claims.
- **Task-specific experts:** invoke a statistician, hydrologist, agronomist, software tester, economist or other specialist when the task requires it.

These are review perspectives/personas, not evidence of separate humans or independently executing agents. If another model is actually queried, record which model/tool was used and include its output as a source artifact.

## Required 8-point decision record

1. Problem and objective.
2. Competing proposals.
3. Specialist review.
4. Adversarial findings.
5. Verification evidence.
6. Decision (accepted / rejected / conditional / deferred).
7. Uncertainty and limits.
8. Next experiment or acceptance criteria.

## Techniques to use selectively

- **Step-back prompting:** clarify objective, assumptions and invariants.
- **Tree of Thoughts:** compare genuinely different solution branches.
- **Graph of Thoughts:** map dependencies, feedback and cross-component effects.
- **ReAct:** retrieve evidence or run tools, observe the results, then revise.
- **Program of Thoughts:** use executable calculations for quantitative checks.
- **Self-consistency:** compare independent candidate solutions; agreement is not proof.
- **Adversarial subagent / chess-move analysis:** seek realistic counterexamples and second-order effects.
- **Multi-agent consensus:** document convergence or preserve unresolved disagreement.

Do not force every technique into every task. Use the simplest process proportional to risk and uncertainty.

## Evidence standard

- A compelling explanation is not an execution log.
- A code fragment containing `...`, omitted logic, or hard-coded sample outputs is not a reproducible experiment.
- A hash is useful only when the corresponding source file is available to verify it.
- Passing a mass-balance calculation validates accounting consistency, not the physical accuracy of its flux equations.
- Synthetic-to-simulator performance is not real-world performance.
- Never use "proved," "verified," "executed," "field-validated" or "production-ready" beyond what artifacts and tests support.
- On disagreement, write the counterexample, expected behaviour, tested behaviour, and exact acceptance criterion.
