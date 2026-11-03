# ML/DL Program Security Pipeline

A preliminary research security-analysis pipeline for Python-based Machine Learning and Deep Learning programs.

## Research Plan and Status

The six scripts in [src/](src/) were run as a preliminary pipeline in April 2026. This is not a completed integrated UMSAF framework or final empirical evaluation.

- [Dissertation_Research.md](Dissertation/writing/Dissertation_Research.md): authoritative research scope, seven layers, RQ1-RQ7/H1-H7, and methodology.
- [RESEARCH_TODO.md](RESEARCH_TODO.md): 32 dependency-aware execution tasks.
- [Dissertation_Completion_Schedule.md](Dissertation/writing/Dissertation_Completion_Schedule.md): weekly calendar and **10 hours/week** maximum.
- [Work-Progress-Status.md](Dissertation/Work-Progress-Status.md): verified progress and missing evidence.

The graduation goal is **August 2027**, conditional on comprehensive-exam and candidacy eligibility. Provisional internal stretch targets are two paper submissions (**February 19 and March 19, 2027**) and research/manuscript completion by **March 31**. The advisor-approved dissertation must reach the Reading Committee at least four weeks before the defense; with the current review plan, an early defense cannot occur before **April 19-22**. August-term outside deadlines are **July 29** for the defense and **July 30** for final dissertation actions. The exact exam cutoff, department deadlines, and advisor/committee availability remain to be confirmed. The full retained scope is high-risk within approximately 203 available hours. Historical manuscripts/exports are not alternative active plans.

## Project Overview

This research project implements a repeatable "ML program security pipeline" that provides:

1. **Dependency Tree Analysis** — Full transitive dependency graph resolution
2. **Vulnerability Scanning** — CVE/OSV database checks for known vulnerabilities  
3. **SBOM Generation** — CycloneDX; SPDX skipped in the recorded run
4. **Integrity & Provenance Checks** — RECORD hashes and PyPI expected-digest metadata; no completed wheel-digest comparison or Sigstore verification
5. **Static Code Analysis** — Bandit/Ruff/custom ML checks; Semgrep skipped; containment policy generated, not enforced
6. **Binary Component Extraction** — Windows PE inventory/fingerprints for deeper analysis, not proof of runtime execution

## Project Structure

```
InventoryDependencyTree/
├── src/                          # step1_dep_tree.py through step6_binary_extraction.py
├── configs/                      # Tool configuration files
│   ├── bandit.yaml              # Static security scanning rules
│   ├── pip-audit.toml           # Vulnerability scanner config
│   └── ...                       # Additional tool configs
├── artifacts/                    # Output directory (gitignored)
│   ├── dep_tree.json            # Full dependency graph
│   ├── vulns_pip_audit.json     # Vulnerability findings
│   ├── sbom.cdx.json            # CycloneDX SBOM
│   ├── integrity_report.json    # Hashes & provenance
│   ├── static_report.json       # Code analysis findings
│   └── wheelhouse/              # Extracted binaries
├── tests/                        # Reserved; regression tests still to be implemented
├── image_recognition_basic.py   # Example ML program (test target)
├── requirements.in               # Auditable, direct dependency inputs
├── requirements-lock.txt         # Hash-verified, resolved dependency closure
├── requirements.txt              # Compatibility alias for the lockfile
├── pyproject.toml               # Project metadata + tool config
└── README.md                     # This file
```

## Environment Setup

### Prerequisites
- CPython 3.12.10 on Windows x86_64
- A new virtual environment; do not reuse an unrelated environment

### Install Dependencies

```bash
# Create and activate the recorded baseline (Windows PowerShell)
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install only the hash-verified dependency closure
python -m pip install --require-hashes -r requirements-lock.txt

# Confirm dependency metadata is internally consistent
python -m pip check
```

## Step 0: Deterministic Resolution Foundation

The foundation is a **fully resolved, hash-verified environment** for one declared platform baseline:

- **`requirements.in`** — the auditable list of direct application and pipeline dependencies
- **`requirements-lock.txt`** — the complete transitive closure, pinned to exact versions and protected by SHA-256 hashes
- **CPython 3.12.10 / Windows x86_64** — the exact, tested interpreter and platform baseline
- **`--require-hashes` installation** — `pip` rejects artifacts that do not match a lockfile hash
- **`pip check` validation** — confirms installed package metadata has no unsatisfied requirements

This gives the vulnerability, SBOM, integrity, static-analysis, and binary-extraction stages the same dependency identities on every clean installation of this baseline. The lock is intentionally a Windows/CPython 3.12.10 baseline; a separate lock must be generated and validated for each additional platform or Python version.

### Updating the Baseline

Dependency updates are deliberate changes to `requirements.in`. Regenerate the lock with CPython 3.12.10 and `pip-tools`, review the resulting diff, then validate it before committing:

```powershell
.\.venv\Scripts\python.exe -m pip install pip-tools==7.5.3
.\.venv\Scripts\pip-compile.exe --generate-hashes --allow-unsafe --strip-extras --output-file requirements-lock.txt requirements.in
.\.venv\Scripts\python.exe -m pip install --dry-run --require-hashes -r requirements-lock.txt
```

## Running the Preliminary Pipeline

After rebuilding the selected baseline, preserve previous artifacts before rerunning; the scripts write into the output directory. Task 3 defines immutable run/evidence rules, and Task 8 reconciles the refreshed reports with April results.

```powershell
python .\src\step1_dep_tree.py
python .\src\step2_vuln_scan.py
python .\src\step3_sbom.py
python .\src\step4_integrity.py
python .\src\step5_static_analysis.py
python .\src\step6_binary_extraction.py
```

Next research work is the contract/baseline refresh, model/runtime/targeted-binary evidence producers, integration, and evaluation in [RESEARCH_TODO.md](RESEARCH_TODO.md), not reimplementation of already-existing steps.

## Configuration Files

- **`pyproject.toml`** — Project metadata, dependencies, tool settings
- **`configs/bandit.yaml`** — Bandit (SAST) configuration
- **`configs/pip-audit.toml`** — pip-audit (vulnerability scanner) config
- **`.gitignore`** — Excludes `.venv/`, `artifacts/`, `__pycache__/`, etc.

## Example: Running Against a Test Program

```bash
# Test with the included example
python image_recognition_basic.py

# Run the six preliminary analysis scripts listed above.
# An integrated security_scanner command is not implemented.
```

## License

MIT (Assumed for research project)

## References

- [CycloneDX](https://cyclonedx.org/)
- [SPDX](https://spdx.dev/)
- [pip-audit](https://github.com/pypa/pip-audit)
- [Bandit](https://bandit.readthedocs.io/)
- [OSV](https://osv.dev/)
