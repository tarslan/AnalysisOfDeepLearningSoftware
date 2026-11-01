# ML Program Security Pipeline – Session Summary

**Date:** April 20, 2026  
**Project:** InventoryDependencyTree  
**Target Program:** `image_recognition_basic.py` (CIFAR-10 CNN using TensorFlow/Keras/NumPy)

**Historical evidence notice (reconciled October 31, 2026):** The date above is the recorded preliminary run, not a current evaluation timestamp. The authoritative research source is [Dissertation_Research.md](Dissertation/writing/Dissertation_Research.md); current progress is in [Work-Progress-Status.md](Dissertation/Work-Progress-Status.md). The [completion schedule](Dissertation/writing/Dissertation_Completion_Schedule.md) targets two submissions and reviewed/defended/deposited dissertation completion by March 31, 2027 for May graduation. Model inspection, runtime tracing, Ghidra analysis, cross-layer integration, and final evaluation remain unimplemented. This report does not assert production readiness.

---

## Overview

This document summarizes a preliminary six-step pipeline run from foundation/scaffolding through binary extraction. Skipped tools, limited checks, and missing UMSAF capabilities prevent this from being a complete security evaluation.

**Goal:** Establish a repeatable, automated security audit process for Python-based machine learning code and its dependencies.

---

## Pipeline Steps Completed

### Step 0: Foundation & Scaffolding ✅
- Created `pyproject.toml` with project metadata and tool configurations
- Generated `requirements-lock.txt` (127 pinned packages, platform-specific)
- Set up directory structure: `src/`, `artifacts/`, `configs/`, `tests/`
- Configured tools:
  - **Bandit** (SAST security rules)
  - **Ruff** (Python linter with security checks)
  - **Semgrep** (custom ML-focused rules)
  - **pip-audit** (vulnerability scanning)
  - **CycloneDX** (SBOM generation)

**Key Files:**
- [pyproject.toml](pyproject.toml)
- [requirements-lock.txt](requirements-lock.txt)
- [.gitignore](.gitignore)
- [README.md](README.md)
- [configs/bandit.yaml](configs/bandit.yaml)
- [configs/pip-audit.toml](configs/pip-audit.toml)
- [configs/.semgrep.yml](configs/.semgrep.yml)

---

### Step 1: Dependency Tree ✅
**Purpose:** Resolve all direct and transitive dependencies from source code imports.

**Approach:**
- AST (Abstract Syntax Tree) parsing of `image_recognition_basic.py`
- Extraction of top-level imports: `numpy`, `tensorflow`
- Cross-reference with `pipdeptree` to build full transitive closure
- Output: JSON + human-readable text

**Results:**
- **Total packages resolved:** 129
- **Direct imports detected:** 2 (numpy, tensorflow)
- **TensorFlow direct dependencies:** 20 packages
- **NumPy direct dependencies:** 0 (vendored)

**Artifacts:**
- [artifacts/dep_tree.json](artifacts/dep_tree.json) – structured JSON graph
- [artifacts/dep_tree.txt](artifacts/dep_tree.txt) – human-readable tree

**Script:** [src/step1_dep_tree.py](src/step1_dep_tree.py)

---

### Step 2: Vulnerability Scanning ✅
**Purpose:** Detect known security vulnerabilities in pinned packages.

**Tools & Methods:**
- **Dual scanning:**
  - **pip-audit** – advisory scanning tool (126 packages reported scanned)
  - **OSV API** – remote, per-package queries (127 packages scanned)
- **Strategy:** Fallback to OSV HTTP API when CLI unavailable
- **Scope:** All 127 packages in lockfile against known CVE/advisory databases

**Results:**
- **Vulnerabilities found:** 0 (both tools agree)
- **Packages verified on PyPI:** 127/127 ✅
- **Yanked packages:** 0

**Artifacts:**
- [artifacts/vulns_pip_audit.json](artifacts/vulns_pip_audit.json) – pip-audit output
- [artifacts/vulns_osv.json](artifacts/vulns_osv.json) – OSV API results
- [artifacts/vuln_scan_summary.json](artifacts/vuln_scan_summary.json) – merged summary

**Script:** [src/step2_vuln_scan.py](src/step2_vuln_scan.py)

**Note:** This run reported zero findings in April 2026, not a vulnerability-free environment. Rebuild and refresh the baseline before final evaluation; reconcile differing graph/scan/SBOM populations.

---

### Step 3: SBOM Generation ✅
**Purpose:** Create a machine-readable Software Bill of Materials for supply-chain audits.

**Standards Implemented:**
- **CycloneDX 1.4** (primary) – comprehensive component inventory
- **SPDX** (optional) – deferred (requires CLI not installed)

**Results:**
- **SBOM format:** CycloneDX JSON
- **Components catalogued:** 124 packages
- **Serialization:** UUID-based BOM reference (`urn:uuid:111f4d11-...`)
- **Timestamp:** 2026-04-20T16:16:43

**Artifacts:**
- [artifacts/sbom.cdx.json](artifacts/sbom.cdx.json) – full CycloneDX XML/JSON SBOM
- [artifacts/sbom_summary.json](artifacts/sbom_summary.json) – metadata + generation timestamp

**Script:** [src/step3_sbom.py](src/step3_sbom.py)

**Use Cases:**
- License compliance audits (SBOM includes licenses)
- Dependency provenance tracking
- Third-party risk assessment

---

### Step 4: Integrity & Provenance Verification ✅
**Purpose:** Verify that installed packages have not been tampered with post-download.

**Three Layers of Verification:**

#### Layer 1: Installed RECORD Integrity
- Re-hash every file listed in each package's `.dist-info/RECORD`
- Compare supported hashes against recorded digests
- **Recorded result:** 127/127 packages reported OK. This is RECORD self-consistency, not proof that every installed file is trusted or unchanged from an authenticated distribution.

#### Layer 2: PyPI Hash Cross-Check
- Query `https://pypi.org/pypi/<name>/<version>/json` for each package
- Retrieve expected distribution-digest metadata for the selected package/version
- **Recorded result:** 127 `verified` statuses, 0 yanked, 0 missing. The code marks digest availability as verified without comparing a retrieved wheel; authenticated package provenance is not established.

#### Layer 3: PEP 740 Attestations (Emerging)
- Probe `https://pypi.org/integrity/<project>/<version>/<filename>` for Sigstore bundles
- **Recorded result:** 0 attestations found by the probe; Sigstore verification not performed
- **Limit:** Probe results are not proof of upstream attestation availability/adoption

#### PEP 458/480 (Long-term Repository Signing)
- **PEP 458** (TUF on PyPI): Accepted, **not deployed**
- **PEP 480** (TUF e2e signing): **Deferred** pending PEP 458

**Artifacts:**
- [artifacts/integrity_report.json](artifacts/integrity_report.json) – full per-package audit
- [artifacts/integrity_summary.json](artifacts/integrity_summary.json) – summary counts

**Script:** [src/step4_integrity.py](src/step4_integrity.py)

**Recorded verdict:** **PASS** for the implemented checks only. Do not interpret it as wheel-digest comparison, authenticated provenance, or a clean chain of custody.

---

### Step 5: Static Code Analysis + Proposed Runtime Policy ✅
**Purpose:** Identify code-level security and ML-specific risks; derive runtime constraints.

#### 5A: Bandit (SAST)
- Ran 80+ CWE-mapped rules on `image_recognition_basic.py`
- **Findings:** 0 security violations

#### 5B: Ruff (Linter)
- Python code quality + security-relevant rules
- **Findings:** 5 (all INFO severity)
  - 4× `T201` – use of `print()` instead of logging framework
  - 1× `W292` – missing newline at EOF

#### 5C: Semgrep
- Custom SAST rule set from [configs/.semgrep.yml](configs/.semgrep.yml)
- **Status:** Skipped (CLI not in PATH; can install: `pip install semgrep`)

#### 5D: ML-AST Custom Checks (10 rules)
- Purpose-built checks for ML-specific reproducibility and safety risks
- **Findings:** 7
  - **ML-001 (MEDIUM):** No global random seed → non-deterministic training
  - **ML-002 (LOW):** `np.random.choice()` without seeded RNG
  - **ML-003 (MEDIUM):** `model.save()` without SHA-256 hash → silent replacement risk
  - **ML-005 (LOW):** Full dataset into RAM without size cap → OOM risk
  - **ML-006 (LOW):** No GPU memory growth config → VRAM starvation
  - **ML-009 (LOW):** Model saved to CWD (relative path) → unpredictable location
  - **ML-010 (INFO):** No EarlyStopping callback → compute waste

#### 5E: Runtime Containment Policy
- Derived 7 containment controls + 6 ML-specific controls
- **Risk level:** MEDIUM (no HIGH findings, 2 MEDIUM)
- Generated policy only: enforcement and runtime observation have not been demonstrated.

**Artifacts:**
- [artifacts/static_report.json](artifacts/static_report.json) – all findings per tool
- [artifacts/runtime_policy.json](artifacts/runtime_policy.json) – containment controls + remediation

**Script:** [src/step5_static_analysis.py](src/step5_static_analysis.py)

**Sample Remediation (ML-001):**
```python
import tensorflow as tf
import numpy as np

# Call at entry point, before any data loading:
tf.random.set_seed(42)
np.random.seed(42)
```

---

### Step 6: Binary Component Extraction & Fingerprinting ✅
**Purpose:** Fingerprint all native binaries (.pyd, .dll); map system dependencies; enable supply-chain verification.

**Approach:**
- Recursive scan of `.venv/Lib/site-packages/` for `.pyd` and `.dll` files
- PE (Portable Executable) format analysis using `pefile` library
- Hash every binary; extract DLL import table; catalog exported symbols

**Results:**

| Metric | Count |
|--------|-------|
| **Total binaries** | 409 |
| **Total size** | 1,410.94 MB |
| **Manifest groups reported as packages** | 109 (distribution attribution still to be validated) |
| **System DLL dependencies** | 84 unique |
| **Analysis errors** | 0 |

**ML Package Binaries:**

| Package | Binaries | Size | Arch | Notable Exports |
|---------|----------|------|------|-----------------|
| **OpenCV (cv2)** | 2 | 98.61 MB | x64 | 2,337 C++ symbols |
| **TensorFlow** | 2 | 0.02 MB | x64 | Wrapping layer |
| **NumPy** | — | — | — | No row attributed in this report; NumPy has compiled extensions, so absence is not proof of pure Python |
| **Keras** | — | — | — | Pure Python |

**OpenCV (cv2.pyd) Imports:**
- python3.dll (Python runtime)
- ole32.dll (Component Object Model)
- KERNEL32.dll, ADVAPI32.dll (Windows core)
- GDI32.dll, USER32.dll, WSOCK32.dll (Graphics, UI, networking)
- MFPlat.DLL, MF.dll, MFReadWrite.dll (Windows Media Foundation – video codec support)
- dxgi.dll, d3d11.dll (DirectX for GPU graphics)
- SHLWAPI.dll (Shell utilities)

**Top System DLLs (by usage frequency):**
- api-ms-win-crt-string-l1-1-0.dll (225 binaries)
- api-ms-win-crt-time-l1-1-0.dll (126 binaries)
- api-ms-win-crt-math-l1-1-0.dll (68 binaries)
- msvcr120.dll (32 binaries)

**Artifacts:**
- [artifacts/binaries_report.json](artifacts/binaries_report.json) – complete inventory (891 KB)
- [artifacts/wheelhouse/*/manifest.json](artifacts/wheelhouse/) – 109 per-package manifests

**Script:** [src/step6_binary_extraction.py](src/step6_binary_extraction.py)

**Use Cases:**
- Binary provenance whitelisting (hash checks on re-installs)
- Symbol-level attack detection (exported function tampering)
- Platform-specific build verification (x64 vs x86 mismatch detection)
- Containerization validation (Dockerfile COPY verification)

---

## Installation & Setup

### Prerequisites
- Selected primary baseline: CPython 3.12.10 on Windows x86_64
- Fresh virtual environment from the hash-verified lockfile; do not reuse an unrelated environment
- Exact installed versions and tools recorded in a verified environment manifest
- Linux/ELF is future comparative work, not a dissertation prerequisite
- Use [README.md](README.md) for current setup; preserve previous artifacts before rerunning

### Quick Start
```bash
# Activate venv
.\.venv\Scripts\Activate.ps1

# Run full pipeline
python src/step1_dep_tree.py
python src/step2_vuln_scan.py
python src/step3_sbom.py
python src/step4_integrity.py
python src/step5_static_analysis.py
python src/step6_binary_extraction.py
```

Or run an individual step:
```bash
python src/step5_static_analysis.py  # Just static analysis
```

### Key Dependencies
- **pipdeptree** – dependency graph resolution
- **pip-audit** – vulnerability scanning
- **cyclonedx-python-lib** – SBOM generation
- **bandit** – SAST rules
- **ruff** – code linting
- **pefile** – Windows binary analysis
- **semgrep** (optional) – advanced SAST

All installed via `requirements.txt` / `requirements-lock.txt`.

---

## Project Structure

```
InventoryDependencyTree/
├── image_recognition_basic.py      # Target ML program (CIFAR-10 CNN)
├── pyproject.toml                  # Project metadata + tool configs
├── requirements.in                 # Auditable direct dependency inputs
├── requirements.txt                # Compatibility alias for the lockfile
├── requirements-lock.txt           # Hash-verified Windows baseline
├── README.md                       # Full pipeline documentation
├── .gitignore                      # Exclude .venv, artifacts, cache
│
├── src/
│   ├── step1_dep_tree.py           # Dependency tree builder
│   ├── step2_vuln_scan.py          # Vulnerability scanner
│   ├── step3_sbom.py               # SBOM generator
│   ├── step4_integrity.py          # Integrity verifier
│   ├── step5_static_analysis.py    # Static analysis + containment policy
│   └── step6_binary_extraction.py  # Binary fingerprinter
│
├── configs/
│   ├── bandit.yaml                 # Bandit SAST rule config
│   ├── pip-audit.toml              # Pip-audit output config
│   └── .semgrep.yml                # Semgrep custom rules
│
├── artifacts/                      # Pipeline outputs (auto-generated)
│   ├── dep_tree.json
│   ├── vulns_pip_audit.json
│   ├── vuln_scan_summary.json
│   ├── sbom.cdx.json
│   ├── integrity_report.json
│   ├── static_report.json
│   ├── runtime_policy.json
│   ├── binaries_report.json
│   └── wheelhouse/
│       └── <package>/manifest.json
│
├── .venv/                          # Python virtual environment
└── tests/                          # (Reserved for future test suites)
```

---

## Key Findings & Recommendations

### Preliminary Check Results (Not an Overall Assurance Verdict)

| Category | Status | Notes |
|----------|--------|-------|
| Known advisories | 0 found in April snapshot | Rebuild/re-scan; not proof of absence |
| Integrity | 127 RECORD/PyPI statuses reported | RECORD self-consistency and expected-digest retrieval only |
| Static code | ⚠ WARN | 2 MEDIUM severity ML-specific issues; easy fixes |
| Provenance | Incomplete | Probe found no attestations; no Sigstore verification |
| Binaries | Inventory recorded | 409 fingerprints; 84 system DLL imports, not proven runtime loading |

### Top Remediation Actions

1. **ML-001: Add Global Random Seed** (MEDIUM)
   - Affects: Training reproducibility, audit trails
   - Fix: `tf.random.set_seed(42)` + `np.random.seed(42)` at entry

2. **ML-003: Saved Model Integrity** (MEDIUM in the recorded run)
   - Affects: Supply-chain security, model tampering detection
   - Fix: Hash all saved models; verify before loading

3. **ML-006: GPU Memory Management** (LOW in the recorded run)
   - Affects: Resource isolation, co-located workload fairness
   - Fix: Enable `set_memory_growth()` for all GPUs

4. **Runtime Containment** (See runtime_policy.json)
   - Network: Restrict to `storage.googleapis.com` (CIFAR-10 cache)
   - Filesystem: Mount `artifacts/` RW-only; everything else read-only
   - Process: Linux seccomp suggestions are not implemented Windows containment; select and validate Windows-appropriate isolation
   - Resource: Cap CPU threads, GPU memory

---

## Re-running the Pipeline

Do not overwrite the frozen inputs or historical artifacts. Use the hash-verified setup and deliberate lock-regeneration procedure in [README.md](README.md), then save dated raw reports and compare populations/results under Tasks 3 and 8 in [RESEARCH_TODO.md](RESEARCH_TODO.md). No validated end-to-end runtime estimate exists yet.

```powershell
python .\src\step1_dep_tree.py
python .\src\step2_vuln_scan.py
python .\src\step3_sbom.py
python .\src\step4_integrity.py
python .\src\step5_static_analysis.py
python .\src\step6_binary_extraction.py
```

---

## References & Further Reading

- **CycloneDX:** https://cyclonedx.org/ (SBOM standard)
- **Recording installed projects:** https://packaging.python.org/en/latest/specifications/recording-installed-packages/ (RECORD specification; PEP 627 is not the RECORD-format specification)
- **PEP 740:** https://www.python.org/dev/peps/pep-0740/ (Provenance attestations)
- **Bandit:** https://bandit.readthedocs.io/
- **Ruff:** https://docs.astral.sh/ruff/
- **pip-audit:** https://github.com/pypa/pip-audit
- **Sigstore:** https://docs.sigstore.dev/ (code signing)
- **NIST ML Security:** https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf

---

## Contact & Support

**Project maintainer:** [Your Name/Email]  
**Recorded run:** 2026-04-20

**Documentation reconciled:** 2026-10-31

**Pipeline version:** 1.0  
**Status:** Preliminary prototype; integrated research/evaluation incomplete

---

*This security pipeline was generated by an AI agent as part of a research project on ML program security auditing.*
