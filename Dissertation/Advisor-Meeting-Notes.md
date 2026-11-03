# Advisor Meeting Notes — UMSAF Dissertation

**Prepared:** November 2, 2026  
**Purpose:** Reintroduce the research after a long gap, report verified progress, get feedback on scope/feasibility, and agree on immediate next steps.  
**Status reminder:** These notes distinguish proposed work from completed evidence. Planning dates and expected contributions are not confirmed results.

**Graduation target:** August 2027, conditional on comprehensive-exam and candidacy eligibility. The comprehensive exam is pending; the exact seven-month cutoff and candidacy path need confirmation. May is not the active target.

## 1. Opening

> It has been about nine months since we last met. I would like to give you a concise overview of the dissertation from its motivation through the current state, then get your guidance on scope, feasibility, and the next milestones. I have a substantial research draft and a preliminary six-step Windows pipeline, but I have not yet implemented or evaluated the integrated UMSAF framework.

## 2. Research overview — brief spoken version

Modern ML/DL applications are not just Python source code. A TensorFlow/Keras application also relies on third-party packages, native C/C++ libraries, serialized models, runtime components, and operating-system infrastructure. Security tools often inspect these parts separately, so a vulnerability or behavior that crosses layers may be hard to contextualize or trace.

My proposed dissertation is to design and empirically evaluate the **Unified Multilayer Security Analysis Framework (UMSAF)**. Its contribution is not a new dependency scanner, binary-analysis tool, or model-accuracy technique. The proposed contribution is a common method and research prototype for collecting and correlating evidence from existing techniques across seven layers:

1. Application
2. Dependency / Software Supply Chain
3. ML/DL Framework
4. Serialization / Computational Graph
5. Native Binary
6. Runtime / Hardware
7. Operating System / Infrastructure

The central question is whether this cross-layer correlation adds validated security visibility, characterization, traceability, or risk context compared with selected isolated analyses. I do not assume that every vulnerability propagates, that all layers add value in every case, or that UMSAF will outperform every baseline.

The primary controlled case is a TensorFlow/Keras CIFAR-10 CNN on Windows x86_64, using CPython 3.12.10 and PE-format `.pyd`/`.dll` analysis. The dissertation is about software-ecosystem security, not improving CNN accuracy or adversarial robustness.

## 3. Research design at a glance

- **Evidence producers:** dependency/SBOM and vulnerability analysis; package/artifact integrity; static analysis; PE inventory and targeted reverse engineering; serialized-model inspection; controlled Windows runtime observation.
- **Integration:** a common evidence schema and cross-layer graph; relationships and candidate propagation paths labeled by evidence strength; interpretable rule-based risk scoring.
- **Evaluation:** compare integrated UMSAF with selected isolated-analysis baselines on equivalent inputs and controlled cases. Measure component/layer coverage, traceability, validated findings where ground truth permits, runtime relevance, resource cost, and repeatability.
- **Machine-learning risk prioritization:** not assumed to be appropriate. First establish whether there is enough defensible labeled data; compare to rule-based and severity-only baselines. This remains an advisor decision because H6 and Objective 9 need to be interpreted consistently.
- **Expected result:** an empirical answer about where integration helps, where it does not, and what evidence remains uncertain—not a presumption of success.

## 4. Work completed so far

### Research and planning

- [Dissertation_Research.md](writing/Dissertation_Research.md) is the authoritative research draft. It contains the problem statement, objectives, RQ1–RQ7, seven-layer threat model, related work, preliminary study, proposed UMSAF architecture, methodology, H1–H7, expected contributions, and limitations.
- The task dependencies and required evidence are organized in [RESEARCH_TODO.md](../RESEARCH_TODO.md); the calendar and capacity limits are in [Dissertation_Completion_Schedule.md](writing/Dissertation_Completion_Schedule.md).
- A draft [Scope-and-Claims-Register.md](Scope-and-Claims-Register.md) maps objectives, questions, hypotheses, proposed experiments, and candidate measures. Open decisions are explicitly marked.
- A selected-target environment record and an experiment/evidence protocol have been drafted: [environment manifest](environment_manifest_target_2026-11-01.json), [experiment protocol](../docs/experiment_protocol.md), and [manifest template](../docs/experiment_manifest.template.json). A protocol checksum dry run was performed on the existing model artifact; it hashed the file but did not inspect, load, or execute it.
- The official term-specific snapshots give August deadlines of **February 1** for candidacy application, **June 11** for graduation application, **July 16** for the Final Oral application/Near Final format-review draft, **July 29** for the latest defense, and **July 30** for final dissertation actions. The May candidacy deadline was November 1; the August exam cutoff and any earlier department dates still need confirmation.

### Preliminary six-step pipeline

A preliminary Windows run was performed on April 20, 2026:

| Existing capability | Recorded preliminary result | Important qualification |
|---|---|---|
| Dependency inventory | 129 packages reported | Must be reconciled against a fresh environment. |
| Vulnerability scan | 0 findings from pip-audit and OSV | April snapshot only; not proof of no vulnerabilities today. |
| SBOM | 124 CycloneDX components | SPDX was skipped. |
| Integrity checks | 127/127 RECORD checks and PyPI digest lookups reported | PyPI digest metadata was retrieved; a downloaded wheel was not compared against it, and authenticated provenance was not established. |
| Static checks | Bandit 0; Ruff 5 informational; custom ML rules reported 7 findings | Semgrep was skipped; containment policy was generated, not enforced. |
| Native binary inventory | 409 PE binaries, 84 unique system DLL imports, 109 manifest groups | Inventory is not evidence that each component was loaded or executed. |

These are preliminary and now stale results. They establish that some evidence producers have been prototyped; they do **not** establish completion or effectiveness of UMSAF.

## 5. Work not yet completed

- Rebuild the clean baseline with the pinned lockfile and `--require-hashes`; run `pip check` and compare installed packages to the lock.
- Complete baseline regression tests, prepare reproducible control/hardened CNN workloads, then rerun and reconcile the six steps without overwriting April evidence.
- Decide and report the treatment of skipped/partial capabilities such as SPDX, Semgrep, NVD enrichment, wheel-digest comparison, Sigstore/PEP 740, and binary signatures.
- Implement and validate model inspection, controlled Windows runtime observation, and targeted Ghidra analysis.
- Build the common evidence model, cross-layer graph, propagation analysis, risk scoring, and integrated report.
- Define defensible ground-truth cases, run isolated baselines, calculate metrics, evaluate H1–H7, and write evidence-backed results.

The integrated UMSAF artifact and final empirical evaluation are **not implemented/completed**. Expected contributions in the manuscript remain proposed until supported by saved and validated evidence.

## 6. Decisions and feedback requested

### Highest priority — scope and feasibility

1. **Is the proposed dissertation contribution focused and sufficiently distinct?** Is the integration/correlation contribution, with a controlled TensorFlow/Keras case study, the right center?
2. **Is the retained scope feasible under the current schedule and capacity?** The working calendar allows at most 10 hours per week (about 203 hours including reserve) and labels the full scope high-risk. Should we reforecast scope, support, or completion dates rather than assume everything fits?
3. **Which commitments are essential for the dissertation?** In particular, should the primary evaluation retain all model-inspection, runtime, reverse-engineering, propagation, risk-scoring, baseline-comparison, and scalability elements?

### Research-design decisions

4. **Risk prioritization:** Is rule-based integrated scoring the required baseline, with ML prioritization conditional on enough labeled data, or do you require an ML model regardless?
5. **H1 and H7:** They overlap in testing integrated analysis. Should they remain separate, and what operational distinction would make each independently testable?
6. **Vulnerability intelligence:** Is NVD enrichment required in addition to the planned CVE/OSV sources? What minimum ground-truth set and success measures would be defensible?
7. **Platform:** Is Windows x86_64/PE an acceptable primary platform, with Linux/ELF explicitly left as future comparative work?
8. **Practical output:** Are evidence-based guidelines and a documented DevSecOps blueprint sufficient, or is an implemented integration expected?

### Supervision and milestones

9. **Review/defense availability:** Can the committee review the complete dissertation by March 22, after the planned March 15–21 revisions? The official rule requires the advisor-approved dissertation at least four weeks before defense, so April 19–22 is the earliest compatible early-defense window. Are those dates plausible, and should I contact committee members directly?
10. **Eligibility and official requirements:** What is the exact seven-month comprehensive-exam cutoff for August 2027, and what candidacy application/status steps remain? Do any department deadlines precede the snapshot dates, and are the August deadlines and committee availability confirmed?
11. **Paper venues:** Can we identify suitable venues and confirm whether the provisional February 19 and March 19 submission dates are realistic?
12. **Meeting cadence:** Given the long gap and the remaining implementation/evaluation work, what meeting frequency and progress artifacts would be most useful?

## 7. Immediate proposed next steps

Subject to your guidance:

1. Resolve the scope and hypothesis decisions in the claims register.
2. Finalize the target environment and protocol; complete the clean environment rebuild before treating any refreshed pipeline result as baseline evidence.
3. Confirm the exact August exam/candidacy requirements, department deadlines, review availability, and paper venues; update the calendar from authoritative responses.
4. Reassess feasibility after the first implementation milestones, using actual hours and validated outputs.

## 8. Suggested meeting agenda (30–45 minutes)

1. **5 min:** Research motivation and UMSAF contribution.
2. **5 min:** Research questions, seven layers, and evaluation approach.
3. **5 min:** What exists—the manuscript and April preliminary pipeline—and what it does not prove.
4. **10–20 min:** Scope, H1/H7, risk-prioritization, ground truth, and feasibility decisions.
5. **5 min:** Official milestones, meeting cadence, and agreed actions with owners/dates.

## 9. Bring or share

- [Dissertation_Research.md](writing/Dissertation_Research.md) — research framing and methodology.
- [Work-Progress-Status.md](Work-Progress-Status.md) — verified current state and remaining work.
- [RESEARCH_TODO.md](../RESEARCH_TODO.md) and [Dissertation_Completion_Schedule.md](writing/Dissertation_Completion_Schedule.md) — dependencies and working timeline.
- [Scope-and-Claims-Register.md](Scope-and-Claims-Register.md) — draft crosswalk and unresolved choices.
- [environment_manifest_target_2026-11-01.json](environment_manifest_target_2026-11-01.json) — selected baseline vs. current environment observation.

**Record during the meeting:** decision, rationale, action owner, due date, and any approved scope/schedule change. Update the execution plan and progress status afterward; do not mark research work complete solely because it was discussed.
