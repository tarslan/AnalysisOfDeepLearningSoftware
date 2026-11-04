# UMSAF Scope and Claims Register

**Version:** Draft 0.1  
**Prepared:** 2026-11-01  
**Status:** Working draft; unresolved decisions below require confirmation before they are treated as research commitments.  
**Research source:** [Dissertation_Research.md](writing/Dissertation_Research.md), especially Sections 3–5, 10–12.  
**Execution source:** [RESEARCH_TODO.md](../RESEARCH_TODO.md).

## Core research claim

This dissertation will design and empirically evaluate the Unified Multilayer Security Analysis Framework (UMSAF), centered on a TensorFlow/Keras deep-learning case, to test whether correlating evidence from existing security-analysis techniques across software-ecosystem layers provides additional **validated security visibility, characterization, traceability, or risk context** compared with selected isolated techniques. ML/DL ecosystems provide the broader research context; one deep-learning workload does not establish general effectiveness across them. The research does not assume that every vulnerability propagates, that every layer contributes in every case, or that UMSAF will outperform the baselines.

## Scope boundary

- **Primary empirical focus:** deep-learning software ecosystem security, evaluated with the TensorFlow/Keras CIFAR-10 CNN and its associated software ecosystem.
- **Broader context:** ML/DL software ecosystems motivate UMSAF, but broad applicability remains unvalidated unless additional workloads are evaluated.
- **Selected primary platform:** Windows x86_64, CPython 3.12.10, TensorFlow 2.21.0, Keras 3.x, NumPy 2.x, with PE `.pyd`/`.dll` analysis. The installed environment still requires fresh verification.
- **Analysis layers:** Application; Dependency/Supply Chain; ML/DL Framework; Serialization/Computational Graph; Native Binary; Runtime/Hardware; Operating System/Infrastructure.
- **Excluded as primary contributions:** improving model accuracy, adversarial robustness, federated learning security, privacy-preserving ML, hardware side-channel attacks, and formal neural-network verification.
- **Bound on generalization:** results from one primary Windows/TensorFlow deep-learning workload do not establish completeness or effectiveness for every ML/DL framework, platform, or deployment.

## Objective, question, hypothesis, experiment, and contribution crosswalk

IDs `O1`–`O10` refer to the objectives in Section 3; `RQ1`–`RQ7` to Section 5; `H1`–`H7` to Section 11.11. Candidate measures are drawn from Section 11.5. Metrics below are **candidate measures**, not results or fixed success thresholds. Define denominators, labeling rules, and any thresholds before the corresponding evaluation.

| Research commitment | Planned experiment / evidence protocol | Candidate measure or decision evidence | Expected contribution(s) |
|---|---|---|---|
| **O1–O3; RQ1:** identify dependencies, correlate vulnerability intelligence, and generate/analyze SBOMs. | Analyze the frozen TensorFlow/Keras deep-learning workload; compare discovered direct/transitive dependencies and native-bearing packages with the installed inventory; generate SBOM; correlate package/version records with selected CVE/OSV/NVD sources. Include known-vulnerable and clean controls after ground truth is approved. | Dependency identification and relationship coverage; SBOM-to-inventory coverage; component-to-advisory correlation coverage. Use TP/FP/FN only for independently verified labeled cases. | Reproducible evidence collection; controlled deep-learning case study. |
| **O4–O5; RQ3; H2:** identify native components and assess what targeted binary analysis/reverse engineering adds. | Inventory and hash PE binaries; justify a bounded sample; inspect selected binaries using Ghidra and a corroborating tool; record package attribution, imports/exports, symbols, and selected structural/control-flow observations. | Binary discovery/extraction and package-attribution rates; selected-sample analysis completion; observed structural facts with source/hash and confidence. Do not equate suspicious patterns with vulnerabilities. | Integrated testing and reverse-engineering methodology. |
| **O6; RQ4; H4:** inspect serialized models and computational structures. | Inspect the intact `.keras` artifact and controlled bit-flipped, metadata-modified, structurally changed, and unsupported-operation cases in an isolated process; preserve hashes and distinguish inspection from loading/execution. | Stable output for identical input; model/layer/operator inventory; detection of defined modifications; false alerts only where ground truth supports labels. No claim of malicious behavior without direct safe observation. | Serialized-model security analysis methodology. |
| **O7; RQ5; H5:** collect execution evidence not available from static analysis alone. | Repeat controlled clean and hardened workload runs with Windows process, file, network, resource, and loaded-DLL observation; include documented controls/anomalies where safe. Preserve raw traces and instrumentation settings. | Runtime event/component coverage; repeatability of expected events; controlled-anomaly detection only where labels are defensible; trace-to-binary inventory mapping. | Runtime security evidence integration. |
| **O8; RQ6; H3:** map and correlate evidence across layers; model candidate propagation paths. | Build a common evidence graph from dependency, vulnerability, model, binary, and runtime records. Test known toy paths, negative controls, and paths with a required edge removed; manually review a sample of mapped edges. | Layer/component mapping coverage; validated edge/path traceability; path outcomes by evidence-strength label; negative-control behavior. A path is `directly_observed` only with direct trace evidence. | Cross-layer interaction mapping; propagation methodology/model; empirical evidence of cross-layer relationships. |
| **O9; RQ6; H6:** prioritize risks using cross-layer context. | Compare a documented deterministic rule-based score with a severity-only baseline on the same labeled cases. Evaluate an ML prioritizer only if the ground-truth data supports leakage-resistant splits and meaningful comparison. | Ranking or classification measures selected before evaluation; score determinism, boundedness, explainability, and sensitivity; compare against severity-only baseline. Exact ranking metric and ML feasibility remain open. | Cross-layer risk classification and prioritization; empirical evaluation of integrated risk prioritization. |
| **O10; RQ2, RQ7; H1, H7:** evaluate integrated UMSAF against selected isolated approaches. | Run UMSAF and SCA/vulnerability/static/binary/model/runtime-only baselines on equivalent inputs and cases, with equivalent resource limits. Record both additional evidence and cases with no benefit. | Incremental validated findings; component/layer coverage; cross-layer traceability/context; defensible TP/FP/FN where labeled; time, memory, and storage. More raw findings alone do not establish improvement. | UMSAF framework and research prototype; comparative evaluation; overall cross-layer assurance contribution; evidence-based security guidance and DevSecOps blueprint. |
| **Cross-cutting theoretical claims:** seven-layer model, risk taxonomy, and threat/trust-boundary framing (Sections 6, 12.1, 12.5). | Apply the model and taxonomy to the controlled case and its findings; document unclassified components/findings and unresolved layer mappings; keep conceptual claims distinct from empirical validation. | Layer coverage and traceability audit; count/classification of unclassified or unresolved cases; documented rationale and limitations. | Multilayer security model; cross-layer taxonomy; integrated assurance paradigm; ecosystem threat-modeling framework. |

### Coverage check

- **Objectives:** O1–O3 → first row; O4–O5 → second; O6 → third; O7 → fourth; O8 → fifth; O9 → sixth; O10 → seventh.
- **Research questions:** RQ1 → first row; RQ2/RQ7 → seventh; RQ3 → second; RQ4 → third; RQ5 → fourth; RQ6 → fifth and sixth.
- **Hypotheses:** H1/H7 → integrated comparison; H2 → binary analysis; H3 → cross-layer mapping; H4 → model inspection; H5 → runtime analysis; H6 → prioritization.
- **Expected contributions:** The rows cover the named theoretical, methodological, empirical, practical, and supporting contributions in Sections 12.1–12.5, including reproducible evidence, case study, prototype, guidelines, and DevSecOps blueprint. The overall contribution in Section 12.6 is evaluated through the integrated comparison, not presumed.

## Explicitly unresolved — do not silently assume

1. **Risk prioritization vs. machine learning:** Objective 9 says “automated risk classification,” while the execution plan makes ML conditional on adequate labeled data and requires a rule-based baseline. Working interpretation: rule-based integrated scoring is required; ML classification is conditional. Confirm that this interpretation is acceptable and that H6 does not require an ML model regardless of data adequacy.
2. **Vulnerability sources:** Objective 2 names CVE, OSV, and NVD; the execution plan separately calls for a decision on NVD enrichment. Confirm which sources are required and how unavailable/stale data will be recorded.
3. **Ground truth and metrics:** The vulnerable/clean case set, inclusion criteria, TP/FP/FN labels, metric definitions, and any success thresholds are not yet fixed. Establish these before running evaluation cases; do not report classification metrics without defensible labels.
4. **H1 vs. H7:** Both concern integrated analysis versus isolated approaches. Proposed distinction: H1 tests incremental visibility/characterization from integration; H7 evaluates the broader ecosystem-level assurance and traceability result. Confirm or revise to avoid duplicate hypotheses.
5. **Practical contributions:** Treat guidelines and the DevSecOps blueprint as evidence-derived recommendations, not proof of production deployment or operational effectiveness. Confirm whether either requires an implementation beyond a documented blueprint.
6. **Platform/generalization:** Linux/ELF is not part of the primary evaluation under the current plan. Any comparative platform study requires separate approval, lockfile, manifest, and results.
7. **Binary and model claims:** Confirm the bounded Ghidra sample and safe model-manipulation scenarios when defining Task 4 ground truth. Do not imply full-framework reverse engineering or malicious model execution.

## Completion criteria for this register

- Every O, RQ, H, and named expected contribution in the authoritative manuscript is mapped above.
- Each empirical claim has a planned comparison or controlled evidence protocol and a candidate measure.
- Metric definitions, denominators, ground-truth labels, and thresholds are finalized before outcome data is examined.
- Unresolved items remain visibly marked until decided; a planned task or expected contribution is not reported as completed evidence.
- Advisor/committee scope changes, if any, are recorded with rationale rather than silently inferred from schedule pressure.
