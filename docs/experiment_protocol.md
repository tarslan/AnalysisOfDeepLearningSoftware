# UMSAF Experiment and Evidence Protocol

**Version:** Draft 0.1  
**Prepared:** 2026-11-01  
**Status:** Protocol and checksum dry run prepared. Formal Task 3 completion remains subject to its Task 2 prerequisite and review of this protocol.  
**Research scope:** Windows x86_64 / CPython 3.12.10 primary configuration; PE `.pyd`/`.dll` analysis. See [the target environment manifest](../Dissertation/environment_manifest_target_2026-11-01.json).  
**Research basis:** Sections 11.8 and 11.12 of [Dissertation_Research.md](../Dissertation/writing/Dissertation_Research.md).

## 1. Purpose and evidence rule

This protocol makes experiment runs identifiable, reproducible, and auditable. Every reported result must resolve to a run ID, command, environment, timestamp, input hash, output hash, and source evidence. Preserve tool output before summarizing it. A planned capability, tool status, or structurally plausible relationship is not an observed result.

The protocol applies to the selected Windows baseline. Linux/ELF comparative work, if later approved, requires its own platform-specific manifest, lockfile, tool records, and run evidence.

## 2. Run identity and directory layout

Use a unique UTC run ID:

`YYYYMMDDThhmmssZ_<study>_<case>_<platform>_<config>`

Use lowercase ASCII letters, digits, and hyphens in the final four fields. Example:

`20261102T034432Z_protocol-dryrun_cnn-model_win-x64_target-v1`

Create one new directory per attempt:

```text
Dissertation/experiments/<run_id>/
├── manifest.json
├── manifest.sha256
├── checksums.sha256
├── raw/
└── derived/
```

- Never reuse, overwrite, or silently clean a run directory. If an attempt fails, preserve its partial evidence, mark the manifest `failed` or `incomplete`, and use a new run ID for a retry.
- Store unmodified tool outputs, logs, traces, and permitted input snapshots under `raw/`. Store normalized records, calculations, tables, and plots under `derived/`.
- The manifest and checksum index are control records. Hash every input and payload output in the manifest and `checksums.sha256`; `manifest.sha256` contains the SHA-256 of the finalized manifest. A checksum file does not hash itself.
- Record repository-relative source paths and hashes. Copy small inputs into `raw/inputs/` when licensing and storage permit. For large or restricted inputs, reference a controlled immutable source location and record its hash, size, access conditions, and version. Never rely on a mutable path alone.
- Do not place credentials, access tokens, private keys, personal data, or unrestricted environment dumps in evidence. Redact secrets without changing raw research results; record that redaction occurred.

## 3. Required manifest fields

Start from [`experiment_manifest.template.json`](experiment_manifest.template.json). Each run manifest records:

1. **Identity and status:** run ID, experiment/case, protocol version, status, operator, UTC start/end times, local time and offset.
2. **Source state:** repository, commit, dirty-worktree flag, and patch/diff hash when applicable.
3. **Environment:** OS/version/architecture, interpreter path and exact version, packaging tag, lockfile path/SHA-256, installed package inventory or inventory artifact, hardware, accelerator visibility, tool versions, and allowlisted relevant environment variables.
4. **Inputs:** repository-relative or controlled-source path, role, size, SHA-256, version/provenance, and whether a snapshot was archived.
5. **Execution:** exact command/arguments, working directory, start/end time, exit code, captured stdout/stderr artifact paths (or `null` when not captured), resource limits, network/filesystem isolation, and deviations. Do not label a generated execution note as stdout/stderr; record such notes separately as execution metadata.
6. **Data sources:** source/tool/service name, endpoint or configured database, tool version, query/scan time, and source-reported update timestamp when available. Do not invent a feed timestamp when the service does not provide one.
7. **Outputs:** raw/derived classification, path, size, SHA-256, producing command/tool, and validation status.
8. **Interpretation:** claims/RQ/H IDs addressed, evidence-strength label for each finding or relationship, limitations, and validation commands/results.

Use `null` or `not_collected` for unavailable facts and explain why. Do not substitute the target configuration for an observed environment. A manifest created before the clean Task 5 rebuild must say that it describes a selected target or existing-environment observation.

## 4. Integrity and validation procedure

For each run:

1. Confirm the run ID does not already exist; create a new directory.
2. Capture the selected environment and repository state. Record only the allowlisted environment variables required for interpretation.
3. Hash each input with SHA-256 before execution. For large immutable references, hash the source in place and record the location and access conditions.
4. Record the exact command, tool versions, working directory, source timestamps, and isolation/resource controls before interpreting output.
5. Save raw outputs unchanged. Record failures and nonzero exit codes; do not turn errors or skipped tools into clean findings.
6. Hash every input and output. Where practical, re-hash inputs after execution and compare to their starting hashes.
7. Create the checksum index and finalize the manifest. Hash the finalized manifest into `manifest.sha256`.
8. Validate that all listed paths exist, hashes match, commands and timestamps are present, JSON/CSV outputs parse, and summaries reconcile with raw evidence.
9. Preserve the completed run. Corrections, reruns, or new vulnerability-feed snapshots receive a new run ID; link related runs rather than editing old evidence.

SHA-256 is used for reproducible identity and change detection; it does not by itself establish publisher authenticity, artifact provenance, or that a file is safe.

## 5. Evidence-strength labels

Assign a label to each finding or relationship, not as a blanket label for an entire experiment. Record the supporting artifact(s) and rationale.

| Label | Use when | Do not infer |
|---|---|---|
| `directly_observed` | A primary trace or explicit structural record directly supports the narrowly stated fact, with the relevant component/artifact identified. Example: a captured process trace records a specific DLL load. | A DLL import table alone does not prove that the DLL was loaded or executed. Package presence does not prove runtime reachability or exploitability. |
| `strongly_correlated` | At least two independent evidence sources consistently link the entities or behavior, but the key edge was not directly observed. Name the missing direct observation. | Multiple reports derived from the same underlying source are not independent corroboration. |
| `potential` | Available structural or contextual evidence makes the relationship plausible, but evidence is incomplete or indirect. State the unverified steps. | Plausibility is not a confirmed vulnerability, execution path, or impact. |
| `unconfirmed` | Evidence is absent, insufficient, conflicting, or cannot distinguish among reasonable interpretations. Preserve the uncertainty and the reason. | Do not count as a validated positive or silently omit it from limitations. |

These are evidence categories, not probabilities. They do not replace vulnerability severity, exploitability assessment, or ground-truth labels.

## 6. Raw and derived evidence; repeatability

- Preserve original scanner JSON, command output, raw runtime traces, binary metadata exports, model hashes, and source-data snapshots where permitted.
- Derived evidence must identify the input run/artifact hashes, transformation script and version, parameters, and output hash.
- Record repeated-trial IDs and shared configuration. Report stable and variable observations separately. A difference between trials is not automatically an anomaly.
- Record vulnerability-data service/query time for every scan. Advisory databases change; results are time-bounded snapshots, not proof that no vulnerability exists.
- Treat model artifacts as untrusted. Static container/metadata inspection must be distinguished from model loading or execution. Isolate any approved loading/scenario test and record the restrictions.
- Preserve failed/partial runs; state whether any data was dropped, normalized, redacted, or manually classified.

## 7. Dry-run record

A checksum workflow dry run was performed against the existing tracked model artifact [`basic_cifar10_cnn.keras`](../basic_cifar10_cnn.keras). It verifies path identity, file size, SHA-256 capture, output indexing, and manifest traceability only. It does **not** inspect or load the model, validate a fresh environment, test vulnerability scanning, or establish model safety.

The corrected saved record is under [`Dissertation/experiments/`](../Dissertation/experiments/). Input hashes are checked against their sources, captured hash-command output and the derived summary are indexed, and each manifest has a detached checksum. The first attempt is preserved as a separate run; its generated execution note was incorrectly labeled as stdout, so the corrected run records actual formatted hash output. The current `.venv` and target-manifest limitations are recorded; neither dry run is evidence that Task 5 passed.

## 8. Schedule and external confirmations

The schedule marks the following as unconfirmed planning assumptions, with a target confirmation date of **November 8, 2026**:

- Official graduate-school, department, graduation-application, defense, and final-deposit deadlines.
- Advisor/committee availability for the planned dissertation review windows and defense week.
- Venue fit and submission deadlines for the two planned papers.

The researcher must verify each item with the authoritative institutional office, advisor, committee, or venue. Record the source, contact/response date, applicable deadline or availability, and any resulting schedule change in the completion schedule or work log. Do not treat the target dates as confirmed merely because they appear in project documents.

## 9. Completion checklist

- [x] Protocol draft and manifest template created.
- [x] Existing-artifact SHA-256 dry run and traceable run record created.
- [ ] Review protocol against the finalized Task 1 scope register and Task 2 target manifest.
- [ ] Verify the actual clean Task 5 environment before using it as a run baseline.
- [ ] Confirm institutional/reviewer/venue dates and record the evidence.
- [ ] Mark Task 3 complete only after its prerequisite and validation conditions are satisfied.
