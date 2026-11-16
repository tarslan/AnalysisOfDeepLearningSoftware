# LaTeX dissertation working manuscript

`Dissertation.tex` is the editable LaTeX version of the research manuscript. It preserves the proposal and preliminary-study content; it is not a completed-results dissertation. The Markdown file in `../writing/` is retained as the pre-conversion source snapshot.

The layout follows the example dissertation's chapter-based organization and numbered bibliography, but is not an official UNL Graduate Studies template. Confirm current formatting requirements with Graduate Studies before submission.

## Formatting and citations

- 12-point, letter-size report layout with 1.5-inch left and top margins and 1-inch right and bottom margins.
- Page numbers appear in the upper-right header, including chapter-opening pages.
- Centered 12-point title-page text and an abstract title/author/adviser block follow the example's front-matter layout without claiming degree completion.
- Research Status remains a separate page with a centered 12-point heading and the working-manuscript notice.
- Numbered chapters, Table of Contents, List of Figures, and Bibliography use 14.4-point bold headings.
- Section, subsection, and subsubsection headings are left-aligned, with section headings larger than subsection headings.
- Double-spaced body text; Roman-numbered front matter and Arabic-numbered chapters.
- The List of Figures is generated from figure captions. No empty List of Tables is added because the current tables have no captions.
- Code listings use a smaller monospaced font to fit within the text margins.
- Numeric citations and bibliography using `biblatex` with Biber.
- This is a focused initial bibliography of 20 sources, not the 50--70-source final bibliography envisioned in the Markdown snapshot. Publisher/Crossref metadata for scholarly references was checked on November 8, 2026. One preprint and two standards specifications are explicitly distinguished from peer-reviewed research.
- Off-topic and duplicate PDFs remain untouched in the Articles folders; they were not carried into the core bibliography. Add further sources as the identified SBOM-quality, runtime-tracing, and native TensorFlow/XLA binary-analysis gaps are researched.

## Build

The configured tools are TeX Live 2026, PDFLaTeX, XeLaTeX, LaTeXmk 4.88, Pandoc 3.13, and Visual Studio Code. This manuscript uses Unicode characters, so compile it with XeLaTeX and its citations and cross-references with:

```powershell
latexmk -xelatex Dissertation.tex
```

`Dissertation.tex` loads `references.bib` with `\addbibresource{references.bib}`. LaTeXmk detects the BibLaTeX configuration and runs Biber as needed. For a manual build, run:

```powershell
xelatex Dissertation.tex
biber Dissertation
xelatex Dissertation.tex
xelatex Dissertation.tex
```

The LaTeX source and bibliography were checked for matching citation keys.

### Word draft for advisor and committee review

#### Editable document (recommended for review)

Run this command from `Dissertation\latex` to generate `Dissertation.docx`
with editable text, headings, tables, and Word equations. Advisors can add
comments, revise text, change formatting, and use Word's Track Changes:

```powershell
pandoc Dissertation.tex `
    --from=latex `
    --to=docx `
    --standalone `
    --bibliography=references.bib `
    --citeproc `
    --metadata=reference-section-title:Bibliography `
    --lua-filter=word-review.lua `
    --number-sections `
    --toc `
    --output=Dissertation.docx
```

The Word-export filter removes unsupported LaTeX title-page boilerplate,
restores the Research Status and Abstract headings, and labels figure captions
with the chapter/figure numbers used by the manuscript's cross-references.
The editable Word draft retains embedded diagrams, tables, equations, and a
processed bibliography. It uses Pandoc's default Word and author-date citation
styles, not the PDF's exact layout or numeric citation style.
Diagrams remain embedded images; their captions and surrounding text are editable.

Open the document in Word and update the table of contents (right-click it and
choose **Update Field**) before sharing. Treat the LaTeX source as authoritative;
Word edits and comments must be incorporated back into the source separately.

#### PDF-matched visual copy (not editable text)

For an optional page-image copy, run:

```powershell
python build-word-visual.py
```

This generates `Dissertation-visual.docx` directly from `Dissertation.pdf`,
embedding one full-page 300-DPI PNG per PDF page at its original letter-size
dimensions. It does not overwrite the editable `Dissertation.docx`.
The script uses Python's standard library and TeX Live's `pdfinfo` and
`pdftoppm`; it replaces the output only after all pages have been rendered and
packaged successfully. Rebuild the PDF first whenever the LaTeX source changes.

The visual copy preserves the PDF's appearance but has no editable/searchable
text, live table of contents, or clickable citations. Do not use it for text
revisions or accessible text review. Its table of contents is part of the page
images and must not be updated in Word.

### Diagrams

The diagram sources are `figures/malicious-package-propagation.tex`,
`figures/serialized-model-propagation.tex`, `figures/ecosystem-layer-model.tex`,
`figures/cnn-execution-path.tex`, `figures/serialized-model-execution-path.tex`,
`figures/umsaf-analytical-architecture.tex`,
`figures/vulnerability-oriented-path.tex`,
`figures/native-component-propagation.tex`, and
`figures/runtime-correlation-path.tex`.
The dissertation uses their PNG renderings so they can also appear in Word exports.
After editing a diagram source,
regenerate its PNG from the `figures` directory. For example:

```powershell
xelatex -interaction=nonstopmode -halt-on-error malicious-package-propagation.tex
pdftoppm -png -r 300 -singlefile malicious-package-propagation.pdf malicious-package-propagation
```

Use the corresponding source name in place of `malicious-package-propagation`
to regenerate another diagram. Then rebuild the dissertation from this directory.

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

For this manuscript, use the editable review command above. It includes
bibliography processing and the manuscript-specific front-matter and
figure-caption fixes.

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

For this dissertation, use XeLaTeX through LaTeXmk so Unicode text is supported and Biber is run for the bibliography:

```powershell
latexmk -xelatex Dissertation.tex
```

### 4. Generate PDF and Word Documents

Run the following commands to generate both formats from the same LaTeX source:

```powershell
latexmk -xelatex test.tex
pandoc test.tex `
    --from=latex `
    --to=docx `
    --standalone `
    --bibliography=references.bib `
    --citeproc `
    --output=test.docx
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

1. **Build PDF:** Uses LaTeXmk with XeLaTeX to generate a PDF document and runs Biber for BibLaTeX bibliographies.
2. **Build Word:** Uses Pandoc to generate a DOCX document with `references.bib` citations processed.
3. **Build PDF and Word:** Executes both tasks sequentially.

These are generic conversion tasks. For the dissertation review draft, use
the editable command above to apply the manuscript-specific front-matter and
caption fixes. The optional visual-copy script writes a separate file.

To generate both documents:

1. Open the desired `.tex` file in VS Code.
2. Press `Ctrl+Shift+B`.
3. Select **Build PDF and Word**, if prompted.
4. Verify that both output files were generated in the same directory as the source file.

The `Ctrl+Alt+B` shortcut may invoke LaTeX Workshop's PDF build operation
instead of the custom VS Code task. For this manuscript, set
`latex-workshop.latex.recipe.default` to `latexmk (xelatex)` in workspace
settings, or select that recipe with LaTeX Workshop's **Build with recipe**
command. The workspace's `.vscode` files are ignored by Git and must be
configured on each machine.

If a failed or interrupted build reports a corrupt `.aux` file, close any
running LaTeX builds, delete `Dissertation.aux`, and rebuild with XeLaTeX.
Do not run the VS Code task and LaTeX Workshop build simultaneously against
the same output directory.

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
