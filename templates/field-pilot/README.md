# Field pilot templates (headers only)

These templates contain no actual farmer data. Use generated/pseudonymous IDs; never add names, phone numbers, or raw personal identifiers to public research CSVs.

| File | One row represents | Intended use |
|---|---|---|
| `site_horizons.csv` | One sampled soil horizon per plot | Soil profile geometry and measured/estimated hydraulic properties with method/provenance. |
| `daily_weather_management.csv` | One plot-day | Raw/observed weather and water-management inputs, preserving rainfall and irrigation separately. |
| `soil_moisture_observations.csv` | One sensor/sample observation at one time and depth | Calibration/validation labels with sensor identity, units, uncertainty and quality status. |
| `derived_model_forcing.csv` | One plot-day supplied to a model version | Actual inputs passed to `TwoLayerSoilWaterModel.step()` plus a reproducible demand/root-fraction derivation reference. Do not label derived quantities as measurements. |
| `management_events.csv` | One discrete field event | Planting, irrigation event detail, amendment, disturbance, harvest, observed stress/disease, sensor maintenance, etc. |

`evidence_class` values should follow the repository's evidence protocol (for example `Measured`, `Officially_Reported`, `Research_Derived`, `Estimated`, `Inferred`, `Unknown`). Do not overwrite raw observations with cleaned values; add a derived dataset version and transformation code. Local timestamps must have a documented time zone. Keep a separate data dictionary and record units/methods.
