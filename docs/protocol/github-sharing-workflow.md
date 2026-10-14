# Shared GitHub Workflow for ChatGPT, Qwen, and Other Reviewers

## What GitHub solves—and what it does not

GitHub can hold the common documents and artifacts. It does **not** automatically ingest or synchronize all chat histories, hidden system memory, or private model context. Each assistant must be given the repository URL and must have a way to access its contents.

- **Private repo:** preferred for active project IP. ChatGPT's GitHub integration and any other model/tool need explicit permission to read it. If Qwen cannot access private GitHub, explicitly upload the current files or connect it using a supported GitHub integration.
- **Public repo:** any person or model that can browse the web may be able to read it. Use only if that disclosure is acceptable. Never place secrets, credentials, private personal information or proprietary datasets in public.
- **Chat context:** give each session the repo URL and the session prompt in `templates/START-OF-SESSION-PROMPT.md`. At the end, commit the accepted record and update `CURRENT_STATE.md`.

## Create the repository

1. Sign into GitHub in a browser and create a new repository named `multilayer-farming-intelligence`.
2. Keep it **Private** initially. Do not add a README/license/gitignore during setup if you plan to push this prepared folder as the initial commit; alternatively, use the web UI to upload these files.
3. Download one of the prepared ZIP bundles. The **with-git** bundle includes the existing local Git history; the clean bundle contains only the files. Extract it, then open a terminal in the extracted `multilayer-farming-intelligence` directory.

   **If you downloaded the with-git bundle:**

```bash
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/multilayer-farming-intelligence.git
git push -u origin main
```

   **If you downloaded the clean bundle:**

```bash
git init
git add .
git commit -m "docs: establish shared farming intelligence decision repository"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/multilayer-farming-intelligence.git
git push -u origin main
```

4. Replace `YOUR-USERNAME` with your GitHub account. Authenticate with GitHub's supported login/credential workflow; never put a token in a source file or chat message. If GitHub says the remote already has a README or other commit, either create an empty repository before pushing or reconcile the histories deliberately rather than force-pushing.
5. Enable the GitHub connection for each assistant you expect to read the private repository, or provide the relevant files directly.
6. Send the exact repository URL to both assistants and ask each to read `README.md`, `CURRENT_STATE.md`, all relevant decision records and the evidence register before proposing changes.

## End-of-session update flow

1. Ask the model for a proposed patch to relevant `.md` files, not just a narrative summary.
2. Check each new claim against source code, test output or primary references.
3. Commit accepted changes with a descriptive message.
4. Update the status table and open questions in `CURRENT_STATE.md`.
5. If a model cannot commit directly, copy its proposed file content into the repository yourself.
6. Never say a result is verified just because an AI report has labelled it verified.

## Recommended branch/record pattern

- `main`: accepted records and current state.
- Optional `review/<topic>` branch: proposals and changes not yet accepted.
- One decision record per substantial architecture/science decision.
- Raw model responses go into `source-drops/` or a time-stamped archive and are cited from the synthesized decision record.
