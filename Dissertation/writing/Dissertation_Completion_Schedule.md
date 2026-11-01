# Dissertation and Two-Paper Completion Schedule

**Prepared:** October 31, 2026

**Graduation goal:** May 2027

**Working completion deadline:** March 31, 2027, including two dissertation review rounds, defense, final dissertation submission, and two paper submissions.

## 1. Constraints and feasibility

This plan uses the actual progress described in [Work-Progress-Status.md](../Work-Progress-Status.md), the research commitments in [Dissertation_Research.md](Dissertation_Research.md), and Tasks 1-32 in [RESEARCH_TODO.md](../../RESEARCH_TODO.md).

This document owns the working calendar; the research manuscript owns scope/methodology, the task list owns execution dependencies, and the progress report owns verified status. Historical drafts and April pipeline reports are not competing schedules or final evaluation evidence.

The six-step preliminary pipeline exists, but its evidence needs refreshing. Model inspection, runtime observation, targeted reverse engineering, cross-layer integration, propagation analysis, risk scoring, and empirical evaluation remain unfinished. The existing dissertation text is a substantial starting draft, not a final evidence-backed dissertation.

**Keeping all current commitments at 10 hours/week is high-risk. This is a capacity-constrained target schedule, not evidence that the full scope is achievable.** The first three weeks must establish actual implementation speed and an advisor-approved feasibility assessment. A calendar cannot resolve a mismatch between workload and available hours.

Confirmed planning constraints:

- Maximum 10 focused hours/week: one hour each weekday and five hours across the weekend.
- Two dissertation review rounds, each allowing two weeks for reviewers and one week for revisions.
- Two paper **submissions** required. Acceptance/publication dates cannot be guaranteed.
- All current research commitments retained. No capability or research question is silently removed.

Provisional assumptions to confirm by November 8:

- The advisor and committee can review during the reserved windows.
- A defense can be booked for March 22-26, with final corrections and deposit completed by March 31.
- Official graduate-school, department, committee, and graduation-application deadlines permit these dates. Earlier official deadlines override this plan.
- November 23-29 and December 21-27 are lighter, five-hour weeks. These are allowances, not assumptions about personal holiday plans.
- Target venues accept submissions at the scheduled times. Conference deadlines may require earlier submission or a different suitable venue.

Do not treat May as extra research time: it is the graduation goal, not the working research deadline. [proposal.md](../proposal.md) and Section 7 of [Dissertation_Research.md](Dissertation_Research.md) now use this March completion target. This documentation alignment does not imply advisor/committee approval or confirmation of official deadlines.

## 2. Weekly routine and capacity

| Day | Available time | Regular assignment |
|---|---:|---|
| Monday | 1 hour | Select one weekly deliverable; prepare inputs and the next small implementation step. |
| Tuesday | 1 hour | Implement or analyze one bounded part of the deliverable. |
| Wednesday | 1 hour | Test/check evidence and resolve the highest-priority blocker. |
| Thursday | 1 hour | Write a methods/results paragraph, figure caption, or paper subsection using verified evidence. |
| Friday | 1 hour | Review progress, update the evidence/task record, and send a concise advisor update. Use for a meeting when needed. |
| Saturday | 3 hours | One uninterrupted implementation, experiment-analysis, or revision block. |
| Sunday | 2 hours | Reserve for overruns, reruns, or feedback. If unused, stop rather than expand scope. |

Normal weeks contain **8 planned hours plus 2 reserve hours**. The two provisional lighter weeks contain four planned hours plus one reserve hour. During writing/review weeks, use Tuesday, Wednesday, and Saturday for writing, revisions, or defense preparation instead of coding.

November 2-March 28 contains 21 full weeks. March 29-31 adds three weekday hours:

- Absolute capacity at 10 hours every full week: **213 hours**.
- Capacity with the two lighter weeks: **203 hours**.
- Planned work with those allowances: **163 hours**.
- Reserve within that capacity: **40 hours**, distributed across weeks, not an additional bank of time to use after March 31.

These are available hours, not estimates that the remaining tasks fit. Meetings, troubleshooting, literature checks, paper formatting, submission forms, and dissertation revisions all count against the same limit. Unattended experiments may run between sessions when safe; setup, monitoring, failures, and analysis still consume work time.

Consistency rules:

1. End every session by recording the next concrete action.
2. Save commands, inputs, hashes, tool versions, raw outputs, and validation results alongside each experiment.
3. Write while researching. Do not postpone all results and methods writing until February.
4. Count a weekly deliverable as complete only when its validation passes and its evidence is saved.
5. Use the reserve for recovery, not new features. Do not compensate for missed work by exceeding 10 hours the following week.
6. If a deliverable is unfinished, carry it forward explicitly and reassess dependent dates. Never mark it complete to keep the calendar looking on track.

## 3. Paper strategy

Discuss both contributions and venue fit with the advisor by November 15.

| Paper | Proposed distinct contribution | Required evidence | Target submission |
|---|---|---|---|
| Paper 1 | Reproducible Windows ML/DL ecosystem characterization: dependency/SBOM/integrity evidence linked to native binary structure and runtime reachability. | Refreshed baseline, justified PE sample, runtime/API mappings, validated quantitative results, and limitations. | February 19, 2027 |
| Paper 2 | Integrated UMSAF evidence correlation, confidence-aware propagation, and risk prioritization compared with isolated-analysis baselines. | Validated integrated artifact, controlled cases, baseline comparisons, hypothesis analysis, and scalability results. | March 19, 2027 |

These are candidate paper boundaries, not guaranteed publishable contributions. Novelty must be checked against related work. Using the same environment is acceptable only when the contributions and analyses are genuinely distinct; disclose overlap, cite related submissions as venue policy permits, and avoid duplicate text or presenting the same result as two independent contributions.

Paper 1 should not claim that an inventory or a clean vulnerability scan alone establishes novelty. Paper 2 must not claim observed exploitation or propagation from a correlation graph alone.

Prepare manuscript skeletons in November. Add methods and figures as evidence becomes available. Have a full Paper 1 draft by February 7 and a full Paper 2 draft by March 7. Request paper reviews separately from the two dissertation review rounds; reviewer availability must be confirmed rather than assumed.

## 4. Weekly deliverables

Task references below point to [RESEARCH_TODO.md](../../RESEARCH_TODO.md). Task 7 milestone **7a** validates existing baseline capabilities before Task 8; **7b** adds new-module tests during Tasks 11-21 and must pass before Task 21 is complete. Task 18 requires Task 17's validated graph, not merely Task 16's schema. Some tasks span multiple weeks: early drafts do not replace their final validation or prerequisites. The research weeks are ambitious timeboxes and must pass the checkpoints in Section 5.

| Week | Dates | Primary deliverable and completion check |
|---|---|---|
| 1 | Nov 2-8 | Tasks 1-3: scope/claims register, selected-platform target manifest, and evidence protocol. Task 5 will validate the installed environment in week 2. Verify official deadlines; reserve review and defense windows. Map every RQ, hypothesis, and contribution to evidence and a metric. |
| 2 | Nov 9-15 | Tasks 4-6: verified ground-truth case matrix, rebuilt baseline, and control/hardened workload runs with documented repeatability. Agree on both paper contributions and target venues. |
| 3 | Nov 16-22 | Complete Task 7 milestone 7a; then complete Tasks 8-10 once their prerequisites pass: refreshed six-step evidence, discrepancy table, omitted-tool decisions/implementation, and reconciled preliminary documentation. Initial wording corrections do not replace refreshed-report validation. Record actual hours and reassess feasibility. |
| 4 | Nov 23-29 (lighter) | Task 11: model-inspection implementation and fixtures, including safe metadata handling and modification detection. Continue Task 7 tests as new modules become available. If this does not fit four planned hours, record the carryover immediately. |
| 5 | Nov 30-Dec 6 | Task 12: all protocol-defined model scenarios with hashes, expected/observed outcomes, and evidence labels. Complete model-related regression tests. Draft the corresponding methods subsection. |
| 6 | Dec 7-13 | Task 13: reproducible Windows runtime capture for control/hardened workloads, raw traces, event summary, and binary-inventory mapping. Document instrumentation limits and variable events. |
| 7 | Dec 14-20 | Task 14: justified PE sample, Ghidra exports, selected-function analysis, and evidence-backed findings. Save Paper 1 figures and table drafts. |
| 8 | Dec 21-27 (lighter) | Task 15: API/framework/native/runtime mappings from completed evidence, with confidence labels and manually checked sample edges. Unresolved mappings remain explicitly unresolved. |
| 9 | Dec 28-Jan 3 | Task 16: validated common evidence/component schema after Tasks 8-15. Begin Task 17 graph joins only once the schema passes validation. Update dissertation architecture/methods with implemented behavior. |
| 10 | Jan 4-10 | Tasks 17-18: validated cross-layer graph and propagation paths; toy-path, missing-edge, and negative-control tests. Check that no unsupported path is labeled directly observed. |
| 11 | Jan 11-17 | Tasks 19-21: explainable scoring with sensitivity checks, Task 20 data-adequacy decision, and an integrated evidence-indexed report. Finish Task 7 tests. Gate: integrated artifact ready for evaluation. |
| 12 | Jan 18-24 | Tasks 22-24: repeated controlled workloads, verified security cases, and isolated-analysis baseline outputs with equivalent inputs/resource limits. Save normalized comparison records. |
| 13 | Jan 25-31 | Complete Tasks 25, 27, 26, then 28: reproducible metrics, scalability/cross-configuration evidence, H1-H7 decisions using those results, and validity audit. Freeze main results; document negative and inconclusive results. Gate: evaluation complete. |
| 14 | Feb 1-7 | Tasks 29-31: finish the evidence-backed dissertation, reconcile active versions/claims, and package the reproducibility archive. Assemble the already-written sections into a complete review-ready draft. Finish full Paper 1 draft. Send dissertation for Review 1 by Feb 7. |
| 15 | Feb 8-14 | Dissertation Review 1, week 1. Request Paper 1 feedback, check novelty/citations/venue requirements, and revise manuscript. Resolve only essential reproducibility issues. |
| 16 | Feb 15-21 | Dissertation Review 1, week 2. Finalize and submit Paper 1 by Feb 19. Log feedback in a response matrix; begin Paper 2 assembly from the completed evaluation. Review 1 feedback due Feb 21. |
| 17 | Feb 22-28 | Address Review 1 in one week. Save a revised dissertation and response matrix; send the complete revision for Review 2 by Feb 28. |
| 18 | Mar 1-7 | Dissertation Review 2, week 1. Complete Paper 2 draft using frozen results; send it for paper-specific feedback by Mar 7. Start defense slides from dissertation figures. |
| 19 | Mar 8-14 | Dissertation Review 2, week 2. Revise Paper 2, check venue requirements, and build the defense narrative. Review 2 feedback due Mar 14. Confirm defense logistics. |
| 20 | Mar 15-21 | Address Review 2, obtain required approvals, and finalize the defense manuscript. Submit Paper 2 by Mar 19. Finish slides and rehearse within the weekly time limit. |
| 21 | Mar 22-28 | Target defense Mar 22-26, subject to official approval. Address defense corrections, complete formatting/deposit checks, and finalize the evidence archive. Aim to finish deposit by Mar 26 rather than use every remaining day. |
| Final partial week | Mar 29-31 | Three-hour contingency for minor corrections, deposit confirmation, and checking both paper submission receipts and all graduation requirements. Not a research or major-revision window. |

Task 32 spans paper preparation, both formal dissertation review/revision rounds, defense, and deposit. Its preparatory work starts in November; final review cannot start before a complete evidence-backed dissertation/archive is ready. Two paper submission receipts and two review response records are required completion evidence, not optional additions.

### Scope preservation

- Retain all RQ1-RQ7/H1-H7 mappings, model scenarios, runtime event categories, targeted reverse engineering, cross-layer correlation, propagation, scoring, isolated baselines, and scalability evaluation.
- Task 20 is already conditional in the execution plan: implement/evaluate ML prioritization if defensible labeled data exists; otherwise document the methodological decision and what it means for the hypothesis. This is not a blanket waiver of an advisor-required ML contribution.
- Task 9 requires explicit decisions for SPDX, Semgrep, Sigstore/PEP 740, NVD enrichment, and binary-signature validation. Required capabilities must be implemented and validated; unavailable data or optional checks must be reported honestly. No scheduled checkbox converts a skipped check into a completed analysis.
- Preserve the existing Windows primary scope. Do not add Linux/ELF or new frameworks merely to make a paper appear broader; those are optional/future work in the existing execution plan.
- If required ML experiments, omitted-tool completion, or the full scenario/scalability matrix cannot fit their timeboxes, the plan must be reforecast. Do not silently reduce them.

## 5. Feasibility gates and escalation

| Checkpoint | Required evidence | Action if missing |
|---|---|---|
| Nov 8 | Official deadline checks and review/defense availability. | Shift the calendar earlier if necessary; do not assume a March defense is administratively possible. |
| Nov 22 | Reproducible refreshed baseline, initial tests, agreed paper novelty, and actual time records. | Estimate remaining work by task with the advisor. If it exceeds remaining capacity, explicitly renegotiate scope, deadline, or authorized support. |
| Dec 27 | Model/runtime/binary evidence producers and mappings validated. | Reforecast integration and evaluation before continuing. March completion is no longer a credible assumption if these prerequisites are missing. |
| Jan 17 | Integrated UMSAF artifact and tests passing. | Escalate immediately; do not substitute planned architecture for implementation evidence. |
| Jan 31 | Full evaluation, hypotheses, scalability, and validity audit complete. | A Feb 7 complete draft is at risk. Do not start two formal final-draft reviews on a manuscript missing its main results. |
| Feb 7 | Complete evidence-backed dissertation sent for Review 1. | Review/revision windows cannot be compressed without reviewer agreement. Reassess March completion. |
| Feb 28 | Review 1 addressed; complete revision sent for Review 2. | Contact reviewers/committee immediately; do not silently eliminate a review round. |
| Mar 21 | Review 2 addressed, approvals secured, two submissions completed, defense ready. | Follow institutional rules and advisor guidance; do not treat a booked defense as permission to defend unfinished work. |

At each checkpoint:

1. Record planned versus actual hours and which evidence is complete.
2. Estimate remaining hours for **all** unfinished required tasks, including papers, reviews, defense, and deposit.
3. Compare that estimate with the remaining calendar capacity after breaks and reserve.
4. Keep the 10-hour maximum. If the estimate exceeds capacity, the constraints are incompatible until something is explicitly changed.

Because all current commitments are retained, the schedule's fallback is **an early, explicit feasibility decision**, not an automatic scope reduction or an unrealistic promise. Authorized help may reduce effort only for appropriate tasks; authorship, research integrity, and personal responsibility for the dissertation remain unchanged.

## 6. Weekly progress record

Use a short entry each Friday:

```text
Week:
Deliverable:
Planned hours / actual hours:
Completed evidence and validation:
Dissertation/paper paragraph or figure added:
Remaining blocker:
Advisor decision needed:
Next session's first action:
Impact on milestone dates:
```

The objective is sustained progress with verifiable outputs, not hours alone. April and May remain for graduation-related follow-through or later paper reviews; neither is assumed available to rescue unfinished March requirements.
