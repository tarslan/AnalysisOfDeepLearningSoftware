# Validated Protocol Checksum Dry Run

- Run ID: 20261102T034930Z_protocol-dryrun-validated_cnn-model_win-x64_target-v1
- Started UTC: 2026-11-02T03:49:30.383Z
- Completed UTC: 2026-11-02T03:49:30.517Z
- This run validates the evidence-recording workflow only; it is not a UMSAF security result.
- Model operation: read-only file hashing. No deserialization, loading, or execution.
- Three small mutable metadata inputs were snapshotted. Model and lockfile source identity is bound to the recorded repository commit.

## Inputs

| Repository-relative path | Bytes | SHA-256 | Snapshot |
|---|---:|---|---|
| `basic_cifar10_cnn.keras` | 2048191 | `f2a86a64203a59f26cb030e00aa6c0b3829af0a1feeedf852ac5d4a2b10f1dce` | tracked at commit |
| `requirements-lock.txt` | 77310 | `1f0ec7143991d62b39f27c2ee751e374d0a2becdf32fff93589a5d6c056ec330` | tracked at commit |
| `Dissertation/environment_manifest_target_2026-11-01.json` | 6571 | `b10b9ac49898263a534d65b6245644f0bf270ed87d1d3df7a69ea6ea71c01700` | yes: raw/inputs/environment_manifest_target_2026-11-01.json.snapshot |
| `docs/experiment_protocol.md` | 10869 | `a14787500c0afc8cc1b26167ce4ce2c07bcb993f2c6c8bb6874c837802286002` | yes: raw/inputs/experiment_protocol.md.snapshot |
| `docs/experiment_manifest.template.json` | 2592 | `c7f3e02b98cf3f1648757384bd4e2faf634ea9b14d9c26c02023fff0c1c84e09` | yes: raw/inputs/experiment_manifest.template.json.snapshot |

## Validation

- All source input hashes were recomputed after the operation and remained unchanged.
- Archived metadata snapshots match the source hashes.
- Every path and digest in `checksums.sha256` was resolved from the repository root and verified.
- The clean hash-verified Task 5 environment, `pip check`, and vulnerability scans were not tested.
