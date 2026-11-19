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

Run this command from `Dissertation\latex` to generate `Dissertation.docx`:

```powershell
.\build-word.ps1
```

The build requires Pandoc, Python 3, and the files in this directory. It checks
that every `\cite{...}` key has one matching entry in `references.bib`, checks
that referenced figure images exist, converts with Pandoc Citeproc and
`ieee.csl`, applies `reference.docx` and `word-review.lua`, adds Word section
and page-number fields, and validates the finished DOCX. Temporary files are
created beside the output; an existing DOCX is replaced only after conversion
and validation succeed. Use `-OutputPath` to create a commit-specific review
copy, for example:

```powershell
$commit = git rev-parse --short HEAD
.\build-word.ps1 -OutputPath "reviews\Dissertation-$commit-baseline.docx"
```

`reference.docx` sets US Letter pages, 1.5-inch top/left and 1-inch
bottom/right margins, 12-point Times New Roman, double-spaced body text,
first-line paragraph indents, and upper-right page numbers. Chapter and section
headings are 14.5-point bold and left-aligned; subsection and subsubsection
headings are 12-point bold and left-aligned. The title page follows the PDF's
order (`title`, `by`, author, degree/manuscript, institution, adviser, location,
date); its title is 12-point uppercase, regular weight. The Research Status
heading is centered at 12 points. The abstract starts with the centered
uppercase dissertation title and author/institution block, followed by the
left-aligned adviser line; it has no extra visible "Abstract" heading. The
contents include Research Status, Abstract, and List of Figures. Both formats
use bold top-level entries without leaders, indented subordinate entries with
separate number and title columns, and right-aligned page numbers. Wrapped
titles align under the start of the title, not under its number.

The PDF uses Latin Modern; Times New Roman is a widely available serif
substitute, so glyphs, line breaks, and pagination will not be identical. To
change Word formatting, open `reference.docx` in Word and modify its named
styles (`Normal`, `Title`, `Title Page Body`, `Abstract Title`, `Abstract
Author`, `Abstract Institution`, `Abstract Adviser`, `Research Status Heading`,
`Heading 1`--`Heading 4`, `Image Caption`, `Bibliography`, and `TOC 1`--`TOC
4`). Preserve the page margins and save the template; the next build uses its
styles.

The IEEE CSL style renders citations as numeric text and orders bibliography
entries by first citation, matching the PDF's numeric citation approach. These
are not native, dynamically editable Word citation fields. Headings are native
Word heading styles; tables and supported equations are editable; diagrams
remain images with editable captions. Figure and section references are
hyperlinks with numbers derived from the manuscript structure. The TOC is a
built-in Word TOC field based on Heading 1--4 and hidden `TC` fields for
Research Status and Abstract; its page numbers and links are recalculated by
Word. Run `.\build-word.ps1 -Paginate` on Windows with desktop Microsoft Word to
save the recalculated TOC when generating a copy for distribution. Without
`-Paginate`, the build leaves the TOC ready for its first update in Word. Field
updates are enabled on open. After editing, click inside the TOC,
choose its **Update Table** control, and select **Update entire table** to
refresh entries and page numbers. The List of Figures also has editable Word
entries with page-reference fields. The generated `PAGE` and `PAGEREF` fields
are internal, not external-file fields.
Word will reflow pages differently from LaTeX; exact pagination, line breaks,
and font metrics are not guaranteed.

### Advisor review and revision reconciliation

1. Commit the LaTeX and bibliography changes to review, then build a baseline
   DOCX using that commit in its filename. Keep this baseline unchanged.
2. Ask the advisor to save a separate returned copy, use **Review > Track
   Changes**, and add comments. Do not have multiple reviewers overwrite the
   same file.
3. Extract comments and tracked insertions/deletions without changing the
   returned DOCX:

   ```powershell
   .\extract-word-review.ps1 `
       -Path "reviews\Dissertation-<commit>-returned.docx"
   ```

   This writes a `.feedback.md` report. For direct edits made with Track
   Changes off, use Word's **Review > Compare > Compare** against the unchanged
   baseline; those edits cannot be reliably recovered from revision markup.
4. Review each suggestion and incorporate accepted changes manually into
   `Dissertation.tex` and, where needed, `references.bib`. Resolve comments
   and reject changes that are not accepted. Never convert the returned DOCX
   back over the LaTeX source.
5. Preserve the baseline and returned DOCX with their commit identifiers for
   review history. Commit accepted source changes and regenerate both outputs:

   ```powershell
   latexmk -xelatex Dissertation.tex
   .\build-word.ps1
   ```

The review extractor reports Word comments and tracked insertions/deletions;
it does not decide which suggestions to accept or merge Word edits into LaTeX.

#### Optional PDF-matched visual copy (not editable text)

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
images and must not be updated in Word. It is generated output and is
git-ignored; retain or share it separately if needed.

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

For this manuscript, use `.\build-word.ps1` as documented above.

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

For the dissertation, build both formats from the same LaTeX source:

```powershell
latexmk -xelatex Dissertation.tex
.\build-word.ps1
```

**Generated files:**

- `Dissertation.pdf` — LaTeX-built document.
- `Dissertation.docx` — Editable Word review document.

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

Pandoc uses the dissertation's `reference.docx` to control styles and formatting.
Edit its named styles in Word to update the template. For a generic document,
Pandoc supports the same option:

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
2. **Build Word:** Runs `build-word.ps1` with IEEE numeric citations, the Word reference template, and WordprocessingML postprocessing.
3. **Build PDF and Word:** Executes both tasks sequentially.

The tasks use the current `.tex` file's directory. The Word task calls
`build-word.ps1`; the combined task runs the PDF build first and then creates
the Word draft.

To generate this dissertation's documents:

1. Open `Dissertation.tex` in VS Code.
2. Press `Ctrl+Shift+B`.
3. Select **Build PDF and Word**, if prompted.
4. Open `Dissertation.tex` when using the Word task; it builds this dissertation's fixed source.
5. Verify that both output files were generated in `Dissertation\latex`.

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
- Use `reference.docx` when consistent DOCX styling is necessary.
- Review generated Word documents for formatting differences, especially equations, tables, figures, and citations.
- Keep generated documents separate from source files when organizing larger dissertation projects.
- Treat the LaTeX source and `references.bib` as authoritative; reconcile advisor revisions manually.

**Important:** Pandoc does not guarantee perfect bidirectional conversion between LaTeX and Word. The recommended workflow is to maintain LaTeX as the primary source and generate PDF or Word documents as needed.
