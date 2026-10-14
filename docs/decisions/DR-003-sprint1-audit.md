# DR-003 — Sprint 1 Parameter Sampling and Metamorphic Tests

**Status:** reported as passing by an AI response; NOT independently verified here because source files and logs are referenced but not included.

## Reported history

An initial supplied report contained a custom LHS sampler returning values in `[0,1]`, but fed those values directly into physical parameter slots without applying the declared bounds. It also omitted the simulator call and hard-coded example outputs for its metamorphic tests. That implementation did not substantiate its pass claims.

A later report said the test suite was re-executed and reported:

- core version `0.2.1-sprint1-verified`;
- source hashes for `agrisim_core.py`, `mr_tests.py`, and `run_sprint1.py`;
- 100 requested scenarios, 81 passing scenario gates, 19 rejected;
- 81/81 passes for several metamorphic relations;
- profile mass-balance residual and hardpan/drought test summaries.

These statements are preserved from the supplied source drop. The corresponding source files and full logs were not supplied, so the reported execution cannot be reproduced from this repository yet.

## Correct design principles

- Scale unit-cube samples into physical bounds with an explicit affine transformation.
- Check constraints and distributions after scaling.
- Use boolean pass/fail/skip semantics safely with NumPy booleans.
- Keep invalid-input fixtures separate from valid physical scenarios.
- Pair comparisons so only the variable of interest changes.
- State preconditions for metamorphic relations. Reduced rainfall does not universally reduce uptake if aeration stress may also change.
- Test zero inter-layer drainage when the hardpan parameter is explicitly set to zero.
- Test runoff using a deliberately saturating fixture rather than assuming ordinary rainfall must cause overflow.
- Use independent state/flux accounting where possible; a residual computed from the same update terms is not proof that those terms represent reality.

## Closure criteria

This record can be upgraded to independently verified only after the source files named in the source drop are committed and a fresh run reproduces the relevant logs.
