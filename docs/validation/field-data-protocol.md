# Field Data Protocol for Soil-Water Model Calibration and Validation

**Status:** Draft protocol; local agronomist/soil scientist review and participant consent required before use.

## Purpose and scope

Collect independent observations to test daily soil-moisture predictions from the two-layer candidate. This protocol does not certify the model or authorize a field recommendation. It assumes the research question and layer geometry are pre-registered before inspecting validation results.

## Data principles

- Preserve immutable raw records; clean/derive data in versioned scripts.
- Use pseudonymous `site_id` and `plot_id`. Keep names, phone numbers and precise farm coordinates outside analysis/public artifacts unless required, consented, and access-controlled.
- Every measured/estimated/inferred value has a unit, method/source, timestamp, uncertainty or quality flag, and `evidence_class`.
- Do not label SoilGrids, NASA POWER, PTF outputs, or model estimates as field-measured values.
- Record irrigation separately from rainfall. Record the daily potential evaporation/transpiration inputs to the simulator and the method/version used to derive them; current model code does not derive these demands from weather.
- Do not delete inconvenient events. Flag outliers with a reason and report results both with and without exclusions when justified.

## Sequence

1. Obtain consent, assign IDs, map plot/horizon boundaries, and document crop/management context.
2. Dig/inspect representative soil profiles; set layer boundaries from measured horizons/rooting/restrictive layers. Do not assume the default 0–30 cm and 30–80 cm layers suit every field.
3. Sample each horizon for texture fractions, bulk density, organic matter/organic carbon (label which), and water-retention / hydraulic measurements available. Record sample ID, lab, method, units, and date.
4. Install and calibrate soil-moisture sensors at locations that represent each modeled layer; record depth, sensor ID, soil-specific calibration, clock/time-zone, and data gaps. Arrange periodic independent checks, such as gravimetric measurements, when practical.
5. Collect daily rain-gauge and irrigation records; retain source files for meteorological/ET data and version the transformation used to compute model forcing.
6. Capture planting, crop stage, root observations if available, irrigation, mulch/cover, pruning, weeding, soil amendments, pest/disease observations, harvest, and unusual field events.
7. Define training/calibration plots or periods and independent holdouts **before** tuning. Hold out complete plot/field/season/event groups; do not randomly split daily rows from a trajectory.
8. Lock cleaning rules and scoring criteria before opening the validation labels. Report sensor uncertainty, bias/MAE/RMSE per layer, wetting-peak/timing and dry-down performance, uncertainty coverage, failed events, and comparison to a baseline.

## Quality checks before model use

- Units and physical ranges: rainfall/irrigation/ET in mm per stated period; volumetric moisture in m³/m³; depths in cm or mm with explicit conversions; crop-demand inputs non-negative.
- Date-time integrity: time zone stated; duplicated timestamps and gaps flagged; rain accumulation window aligned with model timestep.
- Soil texture fractions sum approximately to 100% under the chosen lab method; bulk density and organic-matter units are not silently mixed.
- Sensor: calibrations traceable; drift/failure/movement flagged; a failure period is not silently treated as a genuine drought/waterlogging event.
- Forcing: derived evaporation/transpiration demand and root fractions have method/version/source; do not infer them only from simulated output.
- Provenance: every row retains site, plot, horizon/sensor/event IDs and source record.

## Decision boundary

If records cannot support the required input demands or independent moisture observations, the run remains synthetic/sensitivity analysis. If the model matches one measured layer but no deeper observations exist, report only the evaluated layer. Crop stress, yield, disease and intervention success require separate outcome evidence and are not implied by moisture fit.

## Templates

See `templates/field-pilot/` for normalized CSV headers: site/horizon properties, daily weather and management forcing, soil-moisture observations, derived model inputs, and discrete management events. These are templates, not real data.
