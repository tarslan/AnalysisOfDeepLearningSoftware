
November 1, 2026: 
Today’s next task: Task 1 — Freeze the research scope and claims

The schedule starts Week 1 on Monday, November 2. Its first deliverable is Tasks 1–3: the scope/claims register, target environment manifest, and evidence protocol. Since today is Sunday, use it for a bounded kickoff—don’t let “redoing the pipeline” expand into an unplanned full run.

Steps
1 - Draft the scope and claims register (Task 1). Map each research objective, RQ1–RQ7, H1–H7, and expected contribution to a planned experiment and metric or evidence protocol. Keep the contribution focused on UMSAF—not model accuracy or adversarial robustness.
Evidence: a concise register, with unresolved decisions marked rather than assumed complete.

2 - Freeze the target configuration (Task 2). Keep Windows x86_64, CPython 3.12.10, TensorFlow 2.21.0, and PE analysis as the primary baseline. Record the lockfile hash, tools, hardware/GPU status, and vulnerability-data sources. Distinguish the selected target from the verified installed environment; the latter comes from rebuilding and validating it in Week 2.

3 - Define the experiment/evidence protocol (Task 3). Specify run IDs and immutable output directories, input/output checksums, raw versus derived evidence, and confidence labels. Do a small dry run with an existing artifact. Also use this week to confirm official deadlines and review/defense availability.

4 - Do not rerun all six pipeline steps yet. The execution plan places that in Week 3, after baseline rebuild, workload preparation, and baseline regression tests. Running now against the existing environment would refresh results without first establishing the reproducible baseline.

November 1, 2026 — Task 3 protocol kickoff:

- Drafted [experiment_protocol.md](../docs/experiment_protocol.md) and [experiment_manifest.template.json](../docs/experiment_manifest.template.json), covering run IDs/directories, raw and derived evidence, checksums, validation, confidence labels, and external schedule confirmations.
- Performed read-only SHA-256 protocol dry runs on the existing [basic_cifar10_cnn.keras](../basic_cifar10_cnn.keras) artifact. The validated final record is run `20261102T034930Z_protocol-dryrun-validated_cnn-model_win-x64_target-v1` under [experiments/](experiments/20261102T034930Z_protocol-dryrun-validated_cnn-model_win-x64_target-v1): five source inputs and three snapshots were hashed, ten checksum-index entries were independently verified, and the manifest and all output hashes passed validation. Earlier attempts remain preserved separately and are not the validated record. The model was not loaded or executed.
- This is preparatory evidence only. Formal Task 3 completion remains pending review against the finalized Task 1 register and Task 2 target manifest; clean Task 5 environment verification is also still required before baseline experiments. Term-specific Graduate Studies snapshots have now been reviewed, but the exact August exam cutoff, candidacy path/status, earlier department deadlines, advisor/committee availability, and venue dates still require confirmation.

## November 2, 2026 — August 2027 graduation target

- Reviewed the attached May and August 2027 Graduate Studies deadline snapshots. The May candidacy application date (November 1) has passed; the user reports the comprehensive exam is pending and selected August 2027 as the active graduation goal.
- August snapshot dates: candidacy application February 1, 2027; graduation application June 11; Final Oral application/Near Final format-review rough draft July 16; latest defense July 29; final dissertation actions July 30. The exact seven-month comprehensive-exam cutoff and any earlier department requirements remain unconfirmed.
- Retained February 19 and March 19 paper submissions and March 31 as provisional internal stretch targets for research/manuscript completion and papers, not for defense or final deposit.
- The snapshots require the advisor-approved dissertation to reach the Reading Committee at least four weeks before the defense. Since the current Review 2 revisions end March 21, plan to send the approved manuscript by March 22 and treat April 19-22 as the earliest possible early-defense window, subject to eligibility, committee availability, required forms/format review, and approval.
- Preserve April-July for committee review, defense, corrections, deposit, and contingency; do not treat it as permission to defer required research or expand scope.

## November 3, 2026 — Deep-learning empirical focus clarified

- Reviewed [image_recognition_basic.py](../image_recognition_basic.py): it builds a TensorFlow/Keras CNN with convolutional and dense layers, trains it on CIFAR-10, evaluates/predicts, and saves a `.keras` model. This supports describing the primary workload as deep learning.
- Clarified the authoritative manuscript, proposal summary, scope/claims register, progress status, advisor notes, and Paper 1 schedule description: deep-learning software-ecosystem security is the primary empirical focus; ML/DL terminology remains for broader conceptual context and unvalidated applicability.
- Kept machine-learning-based risk prioritization as a distinct analysis technique, not the workload under study; it remains conditional on defensible labeled data, with rule-based scoring as the required approach.
- No source-code or experiment changes were made; conclusions are bounded by the workload(s) actually evaluated.