# What We Built: ML Security Pipeline – Plain Language Summary

**Historical run:** April 20, 2026. **Interpretation reconciled:** October 31, 2026. This describes the preliminary six-step prototype, not a production-ready system or completed UMSAF evaluation. [Work-Progress-Status.md](Dissertation/Work-Progress-Status.md) owns current evidence status, [RESEARCH_TODO.md](RESEARCH_TODO.md) owns dependencies, and [Dissertation_Completion_Schedule.md](Dissertation/writing/Dissertation_Completion_Schedule.md) owns the March 31, 2027 completion target for May graduation and two paper submissions.

## The Goal

We created a **preliminary six-script security-analysis pipeline**. It analyzes `image_recognition_basic.py` and its installed environment to investigate these questions, subject to each tool's coverage and the recorded snapshot:

1. ✅ What software dependencies does it use?
2. ✅ Are any of those dependencies known to have security flaws?
3. Can installed-file hashes be checked and expected distribution digests retrieved?
4. ✅ Does the code itself have any security risks?
5. ✅ What runtime security controls should we put in place?
6. What native/compiled files are present? (Actual runtime loading remains to be traced.)

---

## What We Created: A 6-Step Pipeline

### **Step 1: Dependency Tree** 
**"What software does this program actually need?"**

- Analyzed the Python code and found it imports: **NumPy** and **TensorFlow**
- Traced all dependencies of those packages to build the complete tree
- **Result:** 129 total packages required (including indirect dependencies)
- **Output:** `dep_tree.json` and `dep_tree.txt` (readable list)

---

### **Step 2: Vulnerability Scanning**
**"Are any of these 129 packages known to have security problems?"**

- Checked all packages against two databases:
  - **pip-audit** (advisory scanning tool)
  - **OSV API** (online vulnerability database)
- Both tools agreed on the same answer
- **Result:** **Zero findings in the April 2026 snapshot**, not proof that all packages are vulnerability-free

---

### **Step 3: Software Bill of Materials (SBOM)**
**"Create an official inventory of what's installed"**

- Generated a machine-readable list of all 124 components
- Used CycloneDX standard (industry-standard format)
- Includes versions, licenses, and identifiers
- **Purpose:** Can be shared with security teams, auditors, or customers
- **Output:** `sbom.cdx.json` (machine-readable inventory)

---

### **Step 4: Integrity & Provenance Check**
**"Have these packages been tampered with since they were downloaded?"**

Three layers of verification:

1. **Layer 1 – File Hashing:** Re-checked the SHA-256 hash of every single installed file (13,000+ files total)
   - **Recorded result:** 127 packages reported OK against their RECORD entries. Self-consistency is not authenticated provenance or proof that every installed file is trusted.

2. **Layer 2 – PyPI Expected-Digest Lookup:** Retrieved distribution digest metadata
   - **Recorded result:** 127 `verified` statuses mean an expected digest was available. The code did not compare a retrieved wheel's digest; this does not authenticate the installed packages.

3. **Layer 3 – Provenance Bundles:** Looked for cryptographic signatures (emerging standard)
   - **Recorded result:** No attestations found by the probe; Sigstore verification not performed. This does not establish upstream availability or adoption.

**Overall:** The report emitted **PASS** for its checks. That status does not establish chain of custody, wheel verification, or authenticated provenance; Task 9 must validate any stronger claim.

---

### **Step 5: Static Code Analysis**
**"Does the code itself have any security problems?"**

Recorded three completed analyses and one skipped tool for `image_recognition_basic.py`:

1. **Bandit** (finds dangerous Python patterns)
   - ✅ Clean – no dangerous patterns found

2. **Ruff** (code quality checker)
   - ⚠️ 5 minor issues (mostly: using `print()` instead of a logging framework)

3. **Semgrep** (advanced pattern matching)
   - Skipped (optional tool not installed)

4. **ML-Specific Custom Checks** (our own rules for ML safety)
   - ⚠️ 7 findings: 2 MEDIUM, 4 LOW, and 1 INFO:
     - ❌ No random seed set → model training is not reproducible
     - ❌ Model saved without hash → file could be secretly replaced
     - ⚠️ GPU memory not capped → could crash shared hardware
     - ⚠️ No data size limits → could run out of RAM

**Also Generated:** Runtime containment policy
This is a proposed policy, not evidence of enforced containment or runtime tracing.
- What network connections should be allowed? (only to Google for dataset download)
- What filesystem access? (only to `artifacts/` folder)
- What CPU/GPU limits? (cap memory and threads)

**Output:** `static_report.json` and `runtime_policy.json`

---

### **Step 6: Binary Component Extraction**
**"What compiled native files are present?"**

- Found all native binary files (.pyd, .dll – compiled C/C++ code)
- Fingerprinted each one with SHA-256 hash
- Mapped all system library dependencies
- **Results:**
  - **409 native binaries** found
  - **1,410 MB** of compiled code
  - **84 unique system DLL imports** (not demonstrated runtime loading)
  - **OpenCV alone:** 98.6 MB, exports 2,337 functions

**Output:** `binaries_report.json` + per-package manifests in `wheelhouse/`

**Why this matters:** Saved fingerprints support later change comparisons. Package attribution and runtime reachability still require validation.

---

## Summary of Findings

### Recorded Preliminary Findings (Not an Overall Security Assurance Verdict)

| Check | Result | Severity |
|-------|--------|----------|
| Known vulnerabilities | **0 in April snapshot** | Snapshot only |
| File integrity | **127 RECORD checks reported OK; expected PyPI digests retrieved** | No authenticated provenance |
| SBOM available | **Generated** | ✅ |
| Code quality issues | 5 minor (logging) | ℹ️ |
| ML safety issues | 7 (2 MEDIUM, 4 LOW, 1 INFO) | ⚠️ |
| Bandit findings | **0 under configured rules** | Not proof of no malicious code |
| Binary component tracking | **409 PE fingerprints recorded** | Attribution/reachability pending |

---

## What You Can Now Do

### 1. **Share a Security Report**
- Email the SBOM to stakeholders
- Disclose the check definitions, skipped capabilities, and April snapshot date
- Do not claim complete verification or authenticated provenance

### 2. **Reproduce Exactly**
- The `requirements-lock.txt` pins all versions
- Rebuild only the declared Windows/CPython baseline using hash-verified installation
- Save a manifest and verify outputs; byte-identical runtime/model outputs are not guaranteed

### 3. **Detect Tampering**
- Re-run the pipeline anytime
- Explain hash changes against package versions and the selected baseline
- Early warning system

### 4. **Monitor for New Vulnerabilities**
- Run Step 2 (vulnerability scan) monthly
- New CVEs appear regularly
- Automatic detection

### 5. **Secure Containerization**
- Treat `runtime_policy.json` as input to a separately implemented and tested containment mechanism
- Restrict network, filesystem, CPU, GPU
- Enforcement has not been demonstrated; Linux container settings are not Windows runtime evidence

### 6. **Track Supply Chain**
- Every binary has a fingerprint
- Inventory of present files, not an audit trail of actual runtime execution
- No compliance certification or production-readiness claim

---

## The Artifacts (Outputs)

All results are in the `artifacts/` folder:

| File | Purpose | Size | Format |
|------|---------|------|--------|
| `dep_tree.json` | Full dependency graph | ~50 KB | JSON |
| `dep_tree.txt` | Readable dependency tree | ~30 KB | Text |
| `vulns_pip_audit.json` | Vulnerability scan (pip-audit) | ~15 KB | JSON |
| `vulns_osv.json` | Vulnerability scan (OSV) | ~20 KB | JSON |
| `sbom.cdx.json` | CycloneDX SBOM | ~200 KB | JSON |
| `integrity_report.json` | File hash verification | ~500 KB | JSON |
| `static_report.json` | Code analysis findings | ~50 KB | JSON |
| `runtime_policy.json` | Containment controls | ~100 KB | JSON |
| `binaries_report.json` | Native code inventory | ~900 KB | JSON |
| `wheelhouse/*/manifest.json` | Per-package binaries | ~500 KB | JSON |

**Total:** ~2.5 MB of detailed security data

---

## How to Re-Run

Preserve earlier artifacts before rerunning; the current scripts write into the output directory. Follow the immutable evidence rules required by Task 3 and the baseline setup in [README.md](README.md). Historical timing is not a validated performance estimate.

### Run the preliminary scripts:
```bash
python src/step1_dep_tree.py
python src/step2_vuln_scan.py
python src/step3_sbom.py
python src/step4_integrity.py
python src/step5_static_analysis.py
python src/step6_binary_extraction.py
```

### Or refresh the vulnerability snapshot:
```bash
python src/step2_vuln_scan.py
```

### After modifying code:
```bash
python src/step5_static_analysis.py  # Just re-analyze code
```

---

## Key Takeaway

The preliminary run produced inspectable dependency, SBOM, static, integrity-check, and PE inventory records:

- Dependency and SBOM populations differ and require reconciliation.
- RECORD/hash checks have limits; expected PyPI digests are not actual wheel comparisons.
- Vulnerability results are snapshot-specific.
- Binary inventories do not establish runtime reachability.
- Reproducibility must be demonstrated on a fresh recorded environment.

This is a **preliminary research prototype**. Model inspection, runtime tracing, targeted reverse engineering, integration, and empirical evaluation remain unfinished.

---

## Research Follow-Up (Not All Optional)

Task 9 determines which omitted tools are required by the evaluation. Installing a tool alone is not proof of an implemented or validated check. Follow deliberate baseline updates in [README.md](README.md), not ad hoc changes to the frozen environment. Tasks 11-28 cover the missing core UMSAF work; the examples below are suggestions, not completed capabilities.

1. **Install Semgrep** for advanced pattern matching
   ```bash
   pip install semgrep
   python src/step5_static_analysis.py  # Re-run
   ```

2. **Install Sigstore** for cryptographic provenance verification
   ```bash
   pip install sigstore
   python src/step4_integrity.py  # Re-run
   ```

3. **Fix the 7 ML safety issues** in code (recommended)
   - Add random seeds
   - Hash model files
   - Cap GPU memory
   - Add data size limits

4. **Containerize** using the `runtime_policy.json`:
   ```dockerfile
   FROM tensorflow:2.21.0
   WORKDIR /app
   COPY --chown=1000:1000 . .
   # Apply security policy: --read-only, --cpus=4, --memory=8g, etc.
   CMD ["python", "image_recognition_basic.py"]
   ```

5. **Set up CI/CD** to re-run pipeline on every code commit:
   - GitHub Actions: `.github/workflows/security-audit.yml`
   - Detect new vulnerabilities immediately
   - Block merges if issues found

---

**Status:** Preliminary six-step run recorded; integrated UMSAF evaluation incomplete

**Date:** April 20, 2026  
**All Artifacts:** Stored in `artifacts/` + documented in `PIPELINE_SESSION_SUMMARY.md`
