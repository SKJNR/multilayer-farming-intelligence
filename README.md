# Multilayer Farming Intelligence OS — Shared Decision Repository

**Purpose:** one version-controlled source of truth for architecture, scientific assumptions, experiments, decision records, and peer-review history for the multilayer farming intelligence work.

> **Important status note:** This repository begins as a documentation and provenance package. It does **not** include the actual soil-water simulator source code, test harnesses, raw scenario datasets, or machine-generated logs described in some AI-submitted reports. Claims about those executions remain attributed reports until the underlying artifacts are added and independently reproduced.

## Start here

1. [`CURRENT_STATE.md`](CURRENT_STATE.md) — what is currently decided, what is only proposed, and what remains unverified.
2. [`docs/architecture/system-architecture.md`](docs/architecture/system-architecture.md) — target architecture.
3. [`docs/protocol/multi-agent-review-protocol.md`](docs/protocol/multi-agent-review-protocol.md) — standing review process.
4. [`docs/protocol/evidence-and-reproducibility.md`](docs/protocol/evidence-and-reproducibility.md) — rules for claims, code execution, and provenance.
5. [`docs/decisions/`](docs/decisions/) — decision records and their current status.
6. [`docs/history/conversation-history.md`](docs/history/conversation-history.md) — concise timeline of the debate so far.
7. [`source-drops/`](source-drops/) — verbatim source text files provided in the conversation. These are archived inputs, not automatically verified results.

## Current high-level decision

- Retain a simple layered soil-water simulator as a **reference prototype** while its implementation and tests are assembled in this repository.
- Do not build an ML surrogate until a measured workload demonstrates a material need. AI-submitted benchmark reports say the surrogate was slower to develop, provided limited speed benefit, and produced unacceptable raw constraint violations; see [`docs/decisions/DR-004-surrogate-benchmark.md`](docs/decisions/DR-004-surrogate-benchmark.md).
- Repair and systematically test synthetic scenario coverage before using generated datasets for model training.
- Do not claim agricultural validity until parameters and model behaviour have been evaluated against relevant real observations.
- The knowledge graph and farmer-compliance model are future work; they should not be blocked indefinitely if independent work can proceed safely, but no unvalidated simulation output may be treated as field truth.

## Shared work with ChatGPT, Qwen, and other models

GitHub is the **shared memory store**; it does not automatically synchronize private chat histories. At the start of every session, give the model the repository URL and ask it to read `README.md`, `CURRENT_STATE.md`, the relevant decision records, and the evidence register. At the end, require a proposed Markdown diff or file contents to commit. Only claim that a model can see the repository if its GitHub connection, permissions, or public access actually allow it.

Copy [`templates/START-OF-SESSION-PROMPT.md`](templates/START-OF-SESSION-PROMPT.md) into a new ChatGPT/Qwen conversation. Use [`templates/END-OF-SESSION-CHECKLIST.md`](templates/END-OF-SESSION-CHECKLIST.md) before accepting any claimed experiment.

## Suggested repository setup

Keep the actual GitHub repository **private initially** because this is active project IP. Create `multilayer-farming-intelligence` in GitHub, then upload or push these files. Grant access only to accounts or integrations that should read it. If a model cannot access a private repository, either connect that model to the repo or explicitly give it the relevant files. Making it public improves link-based access but exposes the project to everyone.

See [`docs/protocol/github-sharing-workflow.md`](docs/protocol/github-sharing-workflow.md) for setup and ongoing operations.

## Repository truth labels

Use these labels in documents and issues:

- **INDEPENDENTLY VERIFIED** — source, environment, commands, and outputs are present and another run reproduced the stated result.
- **REPRODUCIBLE CLAIM — NOT YET RE-RUN HERE** — sufficient artifacts are provided by a source but this team has not independently rerun them.
- **REPORTED, ARTIFACTS MISSING** — a model/user report claims results, but source or logs needed to verify them are absent.
- **PROPOSED** — a design or experiment has been suggested but not executed.
- **FIELD-VALIDATED** — evaluated against appropriate independent field observations with documented methodology. Do not use this label for synthetic-only tests.

## Scope note

This repository captures the currently available multilayer farming / synthetic-data conversation and the three text files supplied with it. It cannot automatically export every other ChatGPT or Qwen conversation, hidden model state, or unrelated prior project discussion. Add those conversations or relevant summaries explicitly if they should become part of this source of truth.

## Latest recorded update

The latest submitted Qwen report is archived in [`source-drops/qwen-sprint2-closure-generator-repair-and-calibration-gate.md`](source-drops/qwen-sprint2-closure-generator-repair-and-calibration-gate.md). It claims generator repairs and a `v1.0.0-ref` freeze, but the underlying source and logs are not present here, so those execution claims remain unverified. See [`CURRENT_STATE.md`](CURRENT_STATE.md) and [DR-004.1](docs/decisions/DR-0041-generator-coverage-and-reference-freeze.md) for current status.
