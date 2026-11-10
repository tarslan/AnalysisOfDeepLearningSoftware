# LaTeX dissertation working manuscript

`Dissertation.tex` is the editable LaTeX version of the research manuscript. It preserves the proposal and preliminary-study content; it is not a completed-results dissertation. The Markdown file in `../writing/` is retained as the pre-conversion source snapshot.

The layout follows the example dissertation's chapter-based organization and numbered bibliography, but is not an official UNL Graduate Studies template. Confirm current formatting requirements with Graduate Studies before submission.

## Formatting and citations

- 12-point, letter-size report layout with a 1.5-inch left margin and 1-inch other margins.
- Double-spaced body text; Roman-numbered front matter and Arabic-numbered chapters.
- Numeric citations and bibliography using `biblatex` with Biber.
- This is a focused initial bibliography of 20 sources, not the 50--70-source final bibliography envisioned in the Markdown snapshot. Publisher/Crossref metadata for scholarly references was checked on November 8, 2026. One preprint and two standards specifications are explicitly distinguished from peer-reviewed research.
- Off-topic and duplicate PDFs remain untouched in the Articles folders; they were not carried into the core bibliography. Add further sources as the identified SBOM-quality, runtime-tracing, and native TensorFlow/XLA binary-analysis gaps are researched.

## Build

The configured tools are TeX Live 2026, PDFLaTeX, LaTeXmk 4.88, Pandoc 3.13, and Visual Studio Code. To compile this dissertation with its citations and cross-references, run these commands from this directory:

```powershell
latexmk -pdf Dissertation.tex
```

LaTeXmk runs the required compilation steps, including Biber for the bibliography. For a manual build, run:

```powershell
pdflatex Dissertation.tex
biber Dissertation
pdflatex Dissertation.tex
pdflatex Dissertation.tex
```

The manuscript contains Unicode symbols, so use XeLaTeX instead if PDFLaTeX reports encoding errors. The LaTeX source and bibliography were checked for matching citation keys; a PDF build should be run after configuring the installed tools.

## LaTeX to PDF and Word Conversion Guide

### 1. Overview

The following tools are installed and configured for converting LaTeX (`.tex`) files into PDF (`.pdf`) and Microsoft Word (`.docx`) documents:

- **TeX Live 2026:** LaTeX distribution for generating PDF documents.
- **PDFLaTeX:** Compiles `.tex` files into PDF documents.
- **LaTeXmk 4.88:** Automates LaTeX compilation and dependency processing.
- **Pandoc 3.13:** Converts LaTeX documents into Microsoft Word and other formats.
- **Visual Studio Code:** Development environment for editing and compiling LaTeX documents.

### 2. Convert LaTeX to Word

Use Pandoc to convert a `.tex` file into a Microsoft Word document:

```powershell
pandoc test.tex -o test.docx
```

**Output:** `test.docx`

Replace `test.tex` with `Dissertation.tex` to convert this manuscript. This basic command may need extra options for bibliography processing or custom LaTeX features.

### 3. Convert LaTeX to PDF

Use PDFLaTeX to compile the LaTeX source file:

```powershell
pdflatex test.tex
```

**Output:** `test.pdf`

For documents containing cross-references, citations, or multiple dependencies, LaTeXmk is recommended:

```powershell
latexmk -pdf test.tex
```

LaTeXmk is recommended for this dissertation because its bibliography uses Biber.

### 4. Generate PDF and Word Documents

Run the following commands to generate both formats from the same LaTeX source:

```powershell
latexmk -pdf test.tex
pandoc test.tex -o test.docx
```

**Generated files:**

- `test.pdf` — PDF document.
- `test.docx` — Microsoft Word document.

### 5. Convert to Word with Formatting Options

For more control over the conversion process, specify the input and output formats explicitly:

```powershell
pandoc test.tex `
    --from=latex `
    --to=docx `
    --standalone `
    --output=test.docx
```

This command enables standalone document generation and preserves supported LaTeX structures, including headings, tables, and mathematical equations. Custom LaTeX packages, specialized layouts, and some citation configurations may need additional adjustments.

### 6. Apply a Microsoft Word Reference Template

Pandoc supports a Word reference document to control styles and formatting:

```powershell
pandoc test.tex -o test.docx --reference-doc=reference.docx
```

The `reference.docx` file can define Word styles for headings, paragraphs, tables, and other document elements. This is useful when preparing dissertation drafts that must follow institutional formatting requirements.

### 7. Configure VS Code for Automated Builds

The workspace task configuration is located at:

```text
.vscode\tasks.json
```

This path is relative to the repository root opened in VS Code. The file defines three build tasks:

1. **Build PDF:** Uses LaTeXmk to generate a PDF document.
2. **Build Word:** Uses Pandoc to generate a DOCX document.
3. **Build PDF and Word:** Executes both tasks sequentially.

To generate both documents:

1. Open the desired `.tex` file in VS Code.
2. Press `Ctrl+Shift+B`.
3. Select **Build PDF and Word**, if prompted.
4. Verify that both output files were generated in the same directory as the source file.

The `Ctrl+Alt+B` shortcut may invoke LaTeX Workshop's PDF build operation instead of the custom VS Code task.

### 8. Recommended Document Formats for a PhD Dissertation

| Format | Recommended use |
|---|---|
| `.tex` | Primary source for dissertation writing and academic research |
| `.pdf` | Dissertation submission, formal review, and publication |
| `.docx` | Sharing editable drafts with advisors and collaborators |
| `.bib` | Managing bibliography entries and academic references |

### 9. Best Practices

- Maintain `.tex` files as the authoritative source for dissertation content.
- Use LaTeXmk for reliable PDF compilation, particularly for larger documents.
- Use Pandoc to generate editable Word versions when required.
- Maintain bibliography references in `.bib` files.
- Use a Word reference template when consistent DOCX styling is necessary.
- Review generated Word documents for formatting differences, especially equations, tables, figures, and citations.
- Keep generated documents separate from source files when organizing larger dissertation projects.

**Important:** Pandoc does not guarantee perfect bidirectional conversion between LaTeX and Word. The recommended workflow is to maintain LaTeX as the primary source and generate PDF or Word documents as needed.
