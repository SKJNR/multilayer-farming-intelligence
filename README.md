# Multilayer Farming Intelligence OS — Shared Decision Repository

**Purpose:** one version-controlled source of truth for architecture, scientific assumptions, experiments, decision records, and peer-review history for the multilayer farming intelligence work.

> **Important status note:** The repository now contains a **new audit-candidate** simulator under `simulation/`, tests, scripts, and candidate audit artifacts. It is **not** a reconstruction of the historical `v1.0.0-ref` claimed in AI-submitted reports. Historical source, original benchmark harness, and raw field observations remain missing. Candidate software checks do not establish physical validity, calibration, or farmer readiness; read `docs/validation/real-world-readiness-roadmap.md`.

## Start here

1. [`CURRENT_STATE.md`](CURRENT_STATE.md) — what is currently decided, what is only proposed, and what remains unverified.
2. [`docs/validation/real-world-readiness-roadmap.md`](docs/validation/real-world-readiness-roadmap.md) — staged evidence gates from synthetic prototype to field evaluation.
3. [`docs/validation/field-data-protocol.md`](docs/validation/field-data-protocol.md) and [`templates/field-pilot/`](templates/field-pilot/) — field measurements and normalized CSV templates.
4. [`docs/architecture/system-architecture.md`](docs/architecture/system-architecture.md) — target architecture.
5. [`docs/protocol/multi-agent-review-protocol.md`](docs/protocol/multi-agent-review-protocol.md) and [`docs/protocol/agent-hats-and-debate-template.md`](docs/protocol/agent-hats-and-debate-template.md) — specialist hats, adversarial review, and evidence rules.
6. [`docs/protocol/evidence-and-reproducibility.md`](docs/protocol/evidence-and-reproducibility.md) — claims, execution, and provenance.
7. [`docs/decisions/`](docs/decisions/) — decision records and their status.
8. [`docs/history/conversation-history.md`](docs/history/conversation-history.md) — concise timeline of the debate.
9. [`source-drops/`](source-drops/) — archived reports supplied in conversation; inputs, not automatically verified results.

## Current high-level decision

- Retain the explicit two-layer simulator in `simulation/` as a **candidate reference prototype** for software and synthetic experiments; it is not field-calibrated.
- Do not build an ML surrogate until a measured workload demonstrates a material need. AI-submitted benchmark reports say the surrogate was slower to develop, provided limited speed benefit, and produced unacceptable raw constraint violations; see [`docs/decisions/DR-004-surrogate-benchmark.md`](docs/decisions/DR-004-surrogate-benchmark.md).
- Repair and systematically test synthetic scenario coverage before using generated datasets for model training.
- Do not claim agricultural validity until parameters and model behaviour have been evaluated against relevant real observations.
- The knowledge graph and farmer-compliance model are future work; they should not be blocked indefinitely if independent work can proceed safely, but no unvalidated simulation output may be treated as field truth.

## Shared work with ChatGPT, Qwen, and other models

GitHub is the **shared memory store**; it does not automatically synchronize private chat histories. At the start of every session, give the model the repository URL and ask it to read `README.md`, `CURRENT_STATE.md`, the relevant decision records, and the evidence register. At the end, require a proposed Markdown diff or file contents to commit. Only claim that a model can see the repository if its GitHub connection, permissions, or public access actually allow it.

Copy [`templates/START-OF-SESSION-PROMPT.md`](templates/START-OF-SESSION-PROMPT.md) into a new ChatGPT/Qwen conversation. Use [`templates/END-OF-SESSION-CHECKLIST.md`](templates/END-OF-SESSION-CHECKLIST.md) before accepting any claimed experiment.

## Repository visibility and sensitive data

The repository was verified as **public** when this snapshot was reviewed. Treat every committed file as public. Do not commit farmer names, phone numbers, exact identifiable farm coordinates, consent forms, credentials, or non-public field records. Use pseudonymous IDs and keep identifiable data in a separately controlled store. If active project IP or field confidentiality requires a private repository, change visibility in GitHub settings after reviewing collaborators/integrations; do not assume the current repository is private.

See [`docs/protocol/github-sharing-workflow.md`](docs/protocol/github-sharing-workflow.md) for session and repository operations.

## Repository truth labels

Use these labels in documents and issues:

- **INDEPENDENTLY VERIFIED** — source, environment, commands, and outputs are present and another run reproduced the stated result.
- **REPRODUCIBLE CLAIM — NOT YET RE-RUN HERE** — sufficient artifacts are provided by a source but this team has not independently rerun them.
- **REPORTED, ARTIFACTS MISSING** — a model/user report claims results, but source or logs needed to verify them are absent.
- **PROPOSED** — a design or experiment has been suggested but not executed.
- **FIELD-VALIDATED** — evaluated against appropriate independent field observations with documented methodology. Do not use this label for synthetic-only tests.

## Scope note

The repository preserves committed reports, decisions, code, and test artifacts; it cannot automatically export private ChatGPT/Qwen histories or hidden model state. Add any future report needed for provenance as a source artifact and label it as reported until independently reproduced.

## Latest recorded update

The latest submitted Qwen report is archived in [`source-drops/qwen-sprint2-closure-generator-repair-and-calibration-gate.md`](source-drops/qwen-sprint2-closure-generator-repair-and-calibration-gate.md). Its reported historical `v1.0.0-ref` source/harness and raw run artifacts have not been recovered. The new candidate is separately identified, readiness requirements are tracked in `docs/validation/real-world-readiness-roadmap.md` and DR-007, and DR-008 records the adversarial review of the drainage-rate law before calibration.
