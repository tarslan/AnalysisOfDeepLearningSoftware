# Work Progress Status — UMSAF Dissertation Research

**Status date:** 2026-10-31
**Repository:** InventoryDependencyTree
**Primary sources reviewed:** [Dissertation_Research.md](Dissertation/writing/Dissertation_Research.md), [RESEARCH_TODO.md](RESEARCH_TODO.md), [PIPELINE_SESSION_SUMMARY.md](PIPELINE_SESSION_SUMMARY.md), [src/](src), [artifacts/](artifacts), git history

---

## 1. Research Overview

**UMSAF — Unified Multilayer Security Analysis Framework** for ML/DL software ecosystems: cross-layer security analysis spanning seven layers (Application → Dependency/Supply Chain → ML/DL Framework → Serialization/Computational Graph → Native Binary → Runtime/Hardware → OS/Infrastructure), evaluated against a TensorFlow/Keras CIFAR-10 CNN workload ([image_recognition_basic.py](image_recognition_basic.py)).

- **Frozen baseline:** Windows x86_64, CPython 3.12.10, TensorFlow 2.21.0, Keras 3.x, NumPy 2.x, PE-format (`.pyd`/`.dll`) binary analysis. Linux/ELF is future comparative work only.
- **Timeline:** first research paper targeted **February 2027**; dissertation defense and final submission targeted **May 2027**.

---

## 2. Work Already Done ✅

### 2.1 Dissertation document fully drafted

[Dissertation_Research.md](Dissertation/writing/Dissertation_Research.md) (4,506 lines, last updated 2026-10-30) contains complete drafts of:

- Abstract, Introduction, Problem Statement, Research Objectives, Scope
- Research Questions RQ1–RQ7
- Threat Model (Section 6) — layer model, threat actors, surfaces, categories, trust boundaries, propagation
- Research Timeline (Section 7)
- Extensive Related Work (Section 8)
- Preliminary Study (Section 9)
- Proposed Framework design (Section 10)
- Research Methodology and Hypotheses H1–H7 (Section 11), including cross-layer propagation analysis design (11.12)
- Expected Contributions (Section 12), Limitations and Assumptions (Section 13), Conclusion, References

> **Note:** Sections 10–12 describe *planned* work. The integrated UMSAF framework itself has **not** been implemented.

### 2.2 Preliminary six-step Windows pipeline — implemented and run (2026-04-20)

| Step | Script | Result |
|---|---|---|
| 1. Dependency tree | [src/step1_dep_tree.py](src/step1_dep_tree.py) | 129 packages resolved (AST imports + pipdeptree) → [artifacts/dep_tree.json](artifacts/dep_tree.json) |
| 2. Vulnerability scan | [src/step2_vuln_scan.py](src/step2_vuln_scan.py) | pip-audit + OSV: **0 findings** (April 2026 snapshot) → [artifacts/vuln_scan_summary.json](artifacts/vuln_scan_summary.json) |
| 3. SBOM | [src/step3_sbom.py](src/step3_sbom.py) | CycloneDX, 124 components → [artifacts/sbom.cdx.json](artifacts/sbom.cdx.json). **SPDX skipped** |
| 4. Integrity/provenance | [src/step4_integrity.py](src/step4_integrity.py) | 127/127 RECORD + PyPI hash checks passed → [artifacts/integrity_summary.json](artifacts/integrity_summary.json). **PEP 740 / Sigstore verification not performed** |
| 5. Static analysis | [src/step5_static_analysis.py](src/step5_static_analysis.py) | Bandit 0, Ruff 5 (INFO), 10 custom ML rules → 7 findings (2 MEDIUM); runtime containment policy derived → [artifacts/static_report.json](artifacts/static_report.json), [artifacts/runtime_policy.json](artifacts/runtime_policy.json). **Semgrep skipped** |
| 6. Binary extraction | [src/step6_binary_extraction.py](src/step6_binary_extraction.py) | 409 PE binaries fingerprinted (1.4 GB), 84 unique system DLLs, 109 per-package manifests → [artifacts/binaries_report.json](artifacts/binaries_report.json), [artifacts/wheelhouse/](artifacts/wheelhouse) |

### 2.3 Supporting assets

- Trained model artifact: [basic_cifar10_cnn.keras](basic_cifar10_cnn.keras)
- Hash-pinned lockfile: [requirements-lock.txt](requirements-lock.txt); project config: [pyproject.toml](pyproject.toml)
- Tool configurations: [configs/](configs) (Bandit, pip-audit, Semgrep rules)
- 31-task execution plan: [RESEARCH_TODO.md](RESEARCH_TODO.md) (Phases 0–5)

---

## 3. Work That Must Be REPEATED 🔁

All pipeline artifacts are dated **2026-04-20 (~6 months stale)** as of this status:

1. **Re-run Steps 1–6 end to end** (RESEARCH_TODO Task 8). Vulnerability intelligence changes continuously — the "0 findings" result is valid only for the April 2026 snapshot and must be regenerated and reconciled against the original artifacts.
2. **Rebuild the clean baseline environment** (Tasks 2, 5): fresh venv from [requirements-lock.txt](requirements-lock.txt) with `--require-hashes`, `python -m pip check`, verify interpreter/platform/TensorFlow versions match the frozen manifest. **No environment manifest exists yet.**
3. **Re-verify integrity and binary inventory** against the rebuilt environment so the 409-binary fingerprint set maps to the frozen baseline, not the April install.
4. **Reconcile preliminary documentation** (Task 10): [README.md](README.md), [WHAT_WE_BUILT.md](WHAT_WE_BUILT.md), and [PIPELINE_SESSION_SUMMARY.md](PIPELINE_SESSION_SUMMARY.md) describe the prototype as "complete / production-ready"; this must be revised to "preliminary research prototype" until final evidence supports stronger claims.

---

## 4. Work Still To Be Completed ❌

### Phase 0 — Research contract (Tasks 1–4)

- [ ] Scope and claims register mapping objectives/RQs/hypotheses to experiments and metrics
- [ ] Environment manifest (`environment_manifest_<id>.json`)
- [ ] Experiment protocol (`docs/experiment_protocol.md`), run-directory/evidence rules, evidence-strength labels
- [ ] Ground-truth dataset: known-vulnerable package versions, manipulated model artifacts, modified binaries, runtime anomalies, with TP/FP/FN criteria

### Phase 1 — Baseline corrections (Tasks 5–10)

- [ ] Hardened CNN workload variant (seeding, model hashing, input validation, resource bounds) alongside the intentionally vulnerable control
- [ ] Automated regression tests — **[tests/](tests) is currently empty**
- [ ] Re-run and reconcile Steps 1–6 (see Section 3)
- [ ] Decide/implement skipped capabilities: SPDX, Semgrep, Sigstore/PEP 740 verification, NVD enrichment, binary-signature validation
- [ ] Documentation reconciliation (see Section 3)

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
- [ ] Hypothesis analysis H1–H7 (supported / partially supported / not supported)
- [ ] Scalability and cross-configuration analysis

### Phase 5 — Interpret, document, finish (Tasks 28–31)

- [ ] Threats-to-validity and reproducibility audit
- [ ] Results and discussion chapters (keep April preliminary findings separate from final results)
- [ ] Reconcile the multiple dissertation versions in [Dissertation/writing/](Dissertation/writing) into one authoritative source; remove stale claims
- [ ] Reproducibility and defense archive with checksums and reproduction log

---

## 5. Bottom Line

The **writing and planning are mature**, and a solid **preliminary six-step pipeline exists** covering the dependency, SBOM, vulnerability, integrity, static-analysis, and binary layers. However, the **differentiating research — serialized-model inspection, runtime tracing, reverse engineering, cross-layer correlation, propagation analysis, risk scoring, and the entire empirical evaluation — has not been started**, and all April 2026 pipeline evidence must be **regenerated on a freshly rebuilt, frozen baseline** before it can be used in the dissertation.

**Next near-term milestones (per Section 7 timeline):**

1. Rebuild baseline environment + re-run Steps 1–6 (stale-evidence refresh)
2. Phase 2 evidence producers, starting with model inspection and runtime observation
3. Targeted Ghidra reverse engineering (Dec 2026 – Jan 2027)
4. First research paper submission (Feb 2027)
