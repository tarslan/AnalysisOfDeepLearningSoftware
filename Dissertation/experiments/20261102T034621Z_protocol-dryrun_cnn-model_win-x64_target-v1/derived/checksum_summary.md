# Protocol Checksum Dry Run

- Run ID: 20261102T034621Z_protocol-dryrun_cnn-model_win-x64_target-v1
- Started: 2026-11-01T21:46:21.954-06:00 (2026-11-02T03:46:21.954Z)
- Purpose: verify recording and hashing of existing research inputs; this is not a model-inspection or security-analysis result.
- Model handling: the `.keras` file was read only for metadata and SHA-256; it was not deserialized, loaded, or executed.

## Inputs

| Repository-relative path | Bytes | SHA-256 |
|---|---:|---|
System.Object[]

## Validation

- All listed input paths existed and were readable.
- Input hashes were rechecked after report generation and matched their initial values.
- The derived report and raw command record are included in `checksums.sha256`.
- This dry run does not establish a fresh `--require-hashes` installation, `pip check`, vulnerability-feed state, model safety, or Task 5 completion.
