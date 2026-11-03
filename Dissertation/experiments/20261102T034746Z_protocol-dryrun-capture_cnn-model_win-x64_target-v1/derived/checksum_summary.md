# Corrected Protocol Checksum Dry Run

- Run ID: 20261102T034746Z_protocol-dryrun-capture_cnn-model_win-x64_target-v1
- Started UTC: 2026-11-02T03:47:46.792Z
- Completed UTC: 2026-11-02T03:47:46.955Z
- Purpose: validate checksums, directory structure, captured hash-command output, and manifest traceability only.
- Model handling: read-only metadata/hash; no deserialization, loading, or execution.
- Correction: the first dry-run record remains preserved; this run stores the formatted hash results as stdout rather than labeling an execution note as stdout.

## Input digests

| Repository-relative path | Bytes | SHA-256 |
|---|---:|---|
| `basic_cifar10_cnn.keras` | 2048191 | `f2a86a64203a59f26cb030e00aa6c0b3829af0a1feeedf852ac5d4a2b10f1dce` |
| `requirements-lock.txt` | 77310 | `1f0ec7143991d62b39f27c2ee751e374d0a2becdf32fff93589a5d6c056ec330` |
| `Dissertation/environment_manifest_target_2026-11-01.json` | 6571 | `b10b9ac49898263a534d65b6245644f0bf270ed87d1d3df7a69ea6ea71c01700` |
| `docs/experiment_protocol.md` | 10669 | `c300047829fb36236105835eff7fbc401d9eacf1396b6fa4ddad7c74fce53482` |
| `docs/experiment_manifest.template.json` | 2592 | `c7f3e02b98cf3f1648757384bd4e2faf634ea9b14d9c26c02023fff0c1c84e09` |
| `Dissertation/experiments/20261102T034621Z_protocol-dryrun_cnn-model_win-x64_target-v1/manifest.json` | 7469 | `0fb80095e2b9e0f73b8ff2b7d6e53eb78ddf5332032eb2226b896a1f8f7880e7` |

## Validation

- All six inputs existed and their hashes remained unchanged after the read-only operation.
- Captured stdout, this derived summary, and the checksum index are hashed.
- This workflow dry run is not model inspection, vulnerability analysis, or Task 5 environment verification.
