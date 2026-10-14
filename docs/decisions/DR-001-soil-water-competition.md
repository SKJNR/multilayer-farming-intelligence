# DR-001 — Layered Soil-Water Competition Primitive

**Status:** PROVISIONAL REFERENCE DESIGN; code-level and field validation pending.  
**Supersedes:** earlier narrative-only claims of a "locked" or "proven" primitive.

## 1. Problem and objective

Represent shared below-ground water competition between a shallow-rooted annual (example: groundnut) and a deeper-rooted perennial (example: papaya), including layer water balance, root distribution, drought stress, aeration stress, inter-layer movement and a restrictive layer.

## 2. Competing proposals

- **Single aggregate bucket:** computationally simple, but may hide vertical moisture differences important to different rooting depths.
- **Richards-equation-based detailed model:** potentially richer representation, with greater parameter/data and computational demands.
- **Layered water-balance MVP:** explicit storage and fluxes in a small number of layers; chosen as a candidate prototype, not presumed universally superior.

AquaCrop is a compartmentalized crop-water model; it should not be described as a single-layer bucket. Its fit for intercropped, crop-specific root competition must be assessed separately.

## 3. Specialist review

Agricultural review requires crop- and soil-dependent root distributions, distinct stress mechanisms, and shared extraction limits. Systems review favours simplicity until a measured workload justifies more complex solving. Adversarial review targets hardpan, waterlogging, threshold crossings, depleted water, and flux-accounting gaps.

## 4. Required governing concepts

For layer `j`, calculate potential uptake demands for each crop from the time-step state, root allocation and relevant stress modifiers. Allocate actual uptake across the shared available budget; applying `min(demand, available)` separately to each crop does not prevent aggregate overdraw.

A proportional baseline can use:

`Q_j = sum_i(q_i,j)`

`alpha_j = min(1, W_available,j / Q_j)` when `Q_j > 0`

`U_i,j = alpha_j * q_i,j`

where `q_i,j` is potential demand after the specified modifiers and `W_available,j` is defined consistently with the model's water budget. This proportional rule is a baseline approximation, not a universal biological law.

Specify explicitly:

- time-step convention (e.g. stress and fluxes calculated from the beginning-of-step state);
- the complete layer and profile water balances;
- rainfall, infiltration, runoff, evaporation, irrigation, inter-layer drainage, deep drainage and all root uptake;
- storage bounds and the hardpan flow law;
- moisture thresholds, units, their sources and uncertainty;
- whether oxygen/aeration stress and drought stress are independently represented.

## 5. Verification requirements

- Reproduce exact boundary fixtures from committed code.
- Compute layer residuals and total-profile residual, with internal transfers cancelling at profile scale.
- Verify shared uptake never exceeds the available budget.
- Verify hardpan factor zero prevents the represented inter-layer flow.
- Test saturation/overflow, drought shutdown and storage bounds.
- Make monotonicity relations conditional where physical mechanisms can reverse the expected direction (e.g. reduced rain alleviating waterlogging).
- Evaluate flux plausibility and state trajectories separately from conservation accounting.

## 6. Decision

Continue with the layered model as the reference prototype because it is a practical, testable baseline. It is not yet certified as an agronomically valid recommendation engine in this repository.

## 7. Uncertainty

The actual simulator code and logs referenced by AI reports are absent from this bundle. Local hydraulic parameters, root distributions, waterlogging thresholds and papaya–groundnut competition behaviour need evidence. Two-layer homogeneous assumptions may miss horizontal variability, preferential flow, salinity and other processes.

## 8. Next experiment

Commit source, tests, parameter registry, scenario generator and logs from the claimed run. Independently reproduce numerical checks; then compare the model against suitable multi-depth observations. State exactly what a candidate dataset can and cannot identify.
