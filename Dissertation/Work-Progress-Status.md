# Work Progress Status — UMSAF Dissertation Research

**Status date:** 2026-11-03
**Repository:** InventoryDependencyTree
**Primary sources reviewed:** [Dissertation_Research.md](writing/Dissertation_Research.md), [RESEARCH_TODO.md](../RESEARCH_TODO.md), [Dissertation_Completion_Schedule.md](writing/Dissertation_Completion_Schedule.md), [PIPELINE_SESSION_SUMMARY.md](../PIPELINE_SESSION_SUMMARY.md), [src/](../src), [artifacts/](../artifacts), git history

**Authority:** This report records verified status as of the date above. The research manuscript owns scope/methodology, the task list owns dependencies, and the completion schedule owns the calendar. Planning dates are targets, not completed work or confirmed institutional deadlines.

---

## 1. Research Overview

**UMSAF — Unified Multilayer Security Analysis Framework** for cross-layer software-ecosystem security: its primary empirical focus is a deep-learning workload, the TensorFlow/Keras CIFAR-10 CNN ([image_recognition_basic.py](../image_recognition_basic.py)). The broader ML/DL ecosystem is research context, not a claim of general validation. Planned analysis spans seven layers (Application → Dependency/Supply Chain → ML/DL Framework → Serialization/Computational Graph → Native Binary → Runtime/Hardware → OS/Infrastructure).

- **Selected baseline:** Windows x86_64, CPython 3.12.10, TensorFlow 2.21.0, Keras 3.x, NumPy 2.x, PE-format (`.pyd`/`.dll`) analysis. Exact installed versions and hashes still need a fresh verified manifest; the April installation is not automatically the final frozen environment. Linux/ELF is future comparative work only.
- **Timeline:** **August 2027 graduation goal**, conditional on the pending comprehensive exam and candidacy eligibility. May is not the active target; its candidacy application deadline (**November 1**) has passed. August snapshot dates: candidacy application **February 1**, graduation application **June 11**, Final Oral application/Near Final rough draft **July 16**, latest defense **July 29**, and final dissertation actions **July 30**. The exact seven-month exam cutoff, department deadlines, and advisor/committee availability still require confirmation. Provisional internal targets remain: complete draft **February 7**; Paper 1 **February 19**; Paper 2 **March 19**; Review 1 **February 8-21** with revisions **February 22-28**; Review 2 **March 1-14** with revisions **March 15-21**; submit the advisor-approved dissertation to the Reading Committee by **March 22**; research/manuscript stretch completion by **March 31**. Because the committee must receive the dissertation at least four weeks before the defense, an early defense cannot be before **April 19-22** if it is sent by March 22. Deposit follows the defense.
- **Capacity:** maximum **10 hours/week**; approximately **203 available hours** including reserve under the schedule's two lighter-week allowances. The full retained scope is high-risk; no task has been completed or removed to make the calendar fit.

---

## 2. Work Already Done ✅

### 2.1 Substantial research manuscript drafted; final results still missing

[Dissertation_Research.md](writing/Dissertation_Research.md) contains drafts of:

- Abstract, Introduction, Problem Statement, Research Objectives, Scope
- Research Questions RQ1–RQ7
- Threat Model (Section 6) — layer model, threat actors, surfaces, categories, trust boundaries, propagation
- Research Timeline (Section 7)
- Extensive Related Work (Section 8)
- Preliminary Study (Section 9)
- Proposed Framework design (Section 10)
- Research Methodology and Hypotheses H1–H7 (Section 11), including cross-layer propagation analysis design (11.12)
- Expected Contributions (Section 12), Limitations and Assumptions (Section 13), Conclusion, References

> **Note:** Sections 10–12 describe *planned* work. Section 9 mixes recorded preliminary evidence with explicitly marked planned extensions; it is not evidence that model inspection, runtime tracing, Ghidra analysis, or cross-layer integration has been completed. The integrated UMSAF framework and final empirical results have **not** been implemented/completed.

### 2.2 Preliminary six-step Windows pipeline — implemented and run (2026-04-20)

| Step | Script | Result |
|---|---|---|
| 1. Dependency tree | [src/step1_dep_tree.py](../src/step1_dep_tree.py) | Reported 129 packages (AST imports + pipdeptree) → [artifacts/dep_tree.json](../artifacts/dep_tree.json) |
| 2. Vulnerability scan | [src/step2_vuln_scan.py](../src/step2_vuln_scan.py) | pip-audit + OSV: **0 findings** (April 2026 snapshot) → [artifacts/vuln_scan_summary.json](../artifacts/vuln_scan_summary.json); not proof of absence |
| 3. SBOM | [src/step3_sbom.py](../src/step3_sbom.py) | CycloneDX, 124 components → [artifacts/sbom.cdx.json](../artifacts/sbom.cdx.json). **SPDX skipped** |
| 4. Integrity/provenance | [src/step4_integrity.py](../src/step4_integrity.py) | Reported 127/127 RECORD checks/PyPI expected-digest lookups → [artifacts/integrity_summary.json](../artifacts/integrity_summary.json). PyPI `verified` means digest metadata retrieved, **not a wheel-digest comparison**. No attestations found by the probe; Sigstore verification not performed. Not proof of authenticated provenance |
| 5. Static analysis | [src/step5_static_analysis.py](../src/step5_static_analysis.py) | Bandit 0, Ruff 5 (INFO), 10 custom ML rules → 7 findings (2 MEDIUM); containment policy derived, not enforced → [artifacts/static_report.json](../artifacts/static_report.json), [artifacts/runtime_policy.json](../artifacts/runtime_policy.json). **Semgrep skipped** |
| 6. Binary extraction | [src/step6_binary_extraction.py](../src/step6_binary_extraction.py) | Reported 409 PE binaries (1,410.94 MB), 84 unique system DLL imports, 109 manifest groups → [artifacts/binaries_report.json](../artifacts/binaries_report.json), [artifacts/wheelhouse/](../artifacts/wheelhouse). Group-to-distribution attribution and runtime reachability still require validation |

Counts refer to different report populations (dependency graph, scan/installation checks, SBOM components, binary manifest groups); they are not interchangeable or automatically evidence of complete dependency coverage. Task 8 must reconcile them against the refreshed environment.

### 2.3 Supporting assets

- Trained model artifact: [basic_cifar10_cnn.keras](../basic_cifar10_cnn.keras); not completed model-inspection evidence
- Hash-pinned lockfile: [requirements-lock.txt](../requirements-lock.txt); project config: [pyproject.toml](../pyproject.toml)
- Tool configurations: [configs/](../configs) (Bandit, pip-audit, Semgrep rules)
- **32-task** execution plan: [RESEARCH_TODO.md](../RESEARCH_TODO.md) (Phases 0–5), including Task 32's two paper submissions, review rounds, defense, and deposit

---

## 3. Work That Must Be REPEATED 🔁

The recorded preliminary run is from **2026-04-20 (~6 months stale)**. Not every individual report carries a timestamp; final evidence must include per-run provenance:

1. **Re-run Steps 1–6 end to end** (RESEARCH_TODO Task 8). Vulnerability intelligence changes continuously — the "0 findings" result is valid only for the April 2026 snapshot and must be regenerated and reconciled against the original artifacts.
2. **Rebuild the clean baseline environment** (Tasks 2, 5): fresh venv from [requirements-lock.txt](../requirements-lock.txt) with `--require-hashes`, `python -m pip check`, and exact installed-version verification. Task 2 selects the target manifest; Task 5 verifies the rebuilt installation. **No verified environment manifest exists yet.**
3. **Re-verify integrity and binary inventory** against the rebuilt environment so the 409-binary fingerprint set maps to the frozen baseline, not the April install.
4. **Reconcile refreshed documentation** (Task 10): [README.md](../README.md), [WHAT_WE_BUILT.md](../WHAT_WE_BUILT.md), and [PIPELINE_SESSION_SUMMARY.md](../PIPELINE_SESSION_SUMMARY.md) now distinguish the preliminary prototype from final UMSAF. The initial wording/link/timeline corrections are done; reconciliation against fresh reports, the capability matrix, and final supported claims remains pending.

---

## 4. Work Still To Be Completed ❌

### Phase 0 — Research contract (Tasks 1–4)

- [ ] Scope and claims register mapping objectives/RQs/hypotheses to experiments and metrics. Draft at [Scope-and-Claims-Register.md](Scope-and-Claims-Register.md); open decisions remain for review.
- [ ] Environment target manifest at [environment_manifest_target_2026-11-01.json](environment_manifest_target_2026-11-01.json) records the selected configuration, lock hash, current tools, and hardware observation. Source timestamps/required NVD scope remain unresolved; fresh installation verification belongs to Task 5.
- [ ] Experiment protocol at [docs/experiment_protocol.md](../docs/experiment_protocol.md), manifest template, and checksum dry run at [run manifest](experiments/20261102T034930Z_protocol-dryrun-validated_cnn-model_win-x64_target-v1/manifest.json) are drafted/validated. Formal Task 3 completion remains pending Task 2 prerequisite review and official schedule confirmations.
- [ ] Ground-truth dataset: known-vulnerable package versions, manipulated model artifacts, modified binaries, runtime anomalies, with TP/FP/FN criteria

### Phase 1 — Baseline corrections (Tasks 5–10)

- [ ] Hardened CNN workload variant (seeding, model hashing, input validation, resource bounds) alongside the intentionally vulnerable control
- [ ] Automated regression tests — **[tests/](../tests) is currently empty**. Task 7a validates existing baseline code before Task 8; Task 7b adds tests with the new modules and completes before Task 21
- [ ] Re-run and reconcile Steps 1–6 (see Section 3)
- [ ] Correct integrity-result interpretation; implement actual wheel-digest comparison if claimed. Decide/implement skipped capabilities: SPDX, Semgrep, Sigstore/PEP 740 verification, NVD enrichment, binary-signature validation
- [ ] Refreshed-report/capability reconciliation (see Section 3); initial documentation alignment is complete, not final Task 10 validation

### Phase 2 — Missing UMSAF evidence producers (Tasks 11–15) — none implemented

- [ ] **Serialized-model inspection** module for `.keras` artifacts (hashing, metadata, layer/operator inventory, tamper detection) + controlled model-manipulation scenarios (Dissertation §10.3.5, §11.7)
- [ ] **Controlled runtime observation** on Windows (ETW / Process Monitor: processes, threads, file/network events, dynamically loaded DLLs) for control and hardened runs (§10.3.6)
- [ ] **Targeted reverse engineering** of selected PE binaries with Ghidra (imports/exports, strings, control flow, function analysis) — §9.6 asserts feasibility only; no Ghidra artifacts exist (§10.3.4)
- [ ] **Python API → framework → native binary mapping** with confidence labels (§10.3.7)

### Phase 3 — Integrated UMSAF artifact (Tasks 16–21) — the core contribution, not started

- [ ] Common evidence/component schema with provenance
- [ ] Cross-layer evidence graph (`cross_layer_graph.json`)
- [ ] Propagation analysis with confidence levels: directly_observed / strongly_correlated / potential / unconfirmed (§11.12)
- [ ] Interpretable rule-based integrated risk scoring (`risk_scores.json`) with severity-only baseline
- [ ] ML-based prioritization only if labeled data justifies it (H6)
- [ ] Integrated UMSAF report (`umsaf_report_<experiment_id>.json`)

### Phase 4 — Empirical evaluation (Tasks 22–27)

- [ ] Controlled workload trials (clean + hardened CNN, repeated runs)
- [ ] Known-vulnerable and controlled security cases in isolated environments
- [ ] Isolated-analysis baselines (SCA-only, vuln-only, static-only, binary-only, model-only, runtime-only)
- [ ] Metrics: detection, coverage, traceability, performance, scalability, reproducibility (§11.5)
- [ ] Hypothesis analysis H1–H7 (supported / partially supported / not supported), after Task 27 scalability results
- [ ] Scalability and cross-configuration analysis

### Phase 5 — Interpret, document, submit, and defend (Tasks 28–32)

- [ ] Threats-to-validity and reproducibility audit
- [ ] Results and discussion chapters (keep April preliminary findings separate from final results)
- [ ] Final evidence-backed reconciliation and export audit in [Dissertation/writing/](writing). The authoritative source is now designated as [Dissertation_Research.md](writing/Dissertation_Research.md); dated/Old drafts remain historical
- [ ] Reproducibility and defense archive with checksums and reproduction log
- [ ] Task 32: two distinct paper submissions/receipts, two dissertation review/revision records, defense and corrections, final-deposit confirmation

---

## 5. Bottom Line

The **writing and planning are mature**, and a solid **preliminary six-step pipeline exists** covering the dependency, SBOM, vulnerability, integrity, static-analysis, and binary layers. However, the **differentiating research — serialized-model inspection, runtime tracing, reverse engineering, cross-layer correlation, propagation analysis, risk scoring, and the entire empirical evaluation — has not been started**, and all April 2026 pipeline evidence must be **regenerated on a freshly rebuilt, frozen baseline** before it can be used in the dissertation.

**Next milestones (per the completion schedule, not evidence of completion):**

1. November 2-8: research contract/target manifest/protocol and official deadline checks
2. By November 22: rebuilt baseline, passing Task 7a tests, refreshed Steps 1-6, and feasibility reforecast
3. By December 27: validated model/runtime/targeted-Ghidra evidence and API/native mappings
4. By January 17: validated integrated UMSAF artifact and Task 7b tests
5. By January 31: final evaluation, scalability, hypotheses, and validity audit
6. By February 7: complete evidence-backed dissertation draft and review archive; two review/revision rounds through March 21
7. February 19 / March 19: provisional Paper 1 / Paper 2 submissions; March 22: send advisor-approved dissertation to the Reading Committee; March 31: research/manuscript stretch completion; April 19-22 or later: earliest early-defense window under the four-week committee-review rule; final deposit after defense, no later than the August-term July 30 deadline
