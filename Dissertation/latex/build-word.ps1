[CmdletBinding()]
param(
    [string]$OutputPath = "Dissertation.docx",
    [switch]$Paginate
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$source = Join-Path $root "Dissertation.tex"
$bibliography = Join-Path $root "references.bib"
$reference = Join-Path $root "reference.docx"
$csl = Join-Path $root "ieee.csl"
$filter = Join-Path $root "word-review.lua"
$postprocessor = Join-Path $root "postprocess-word.py"

foreach ($tool in @("pandoc", "python")) {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "Required tool '$tool' was not found on PATH."
    }
}

foreach ($file in @($source, $bibliography, $reference, $csl, $filter, $postprocessor)) {
    if (-not (Test-Path -LiteralPath $file -PathType Leaf)) {
        throw "Required Word-export input is missing: $file"
    }
}

$tex = [System.IO.File]::ReadAllText($source)
$bib = [System.IO.File]::ReadAllText($bibliography)
$bibliographyKeys = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
foreach ($match in [regex]::Matches($bib, '(?m)^\s*@\w+\s*\{\s*([^,\s]+)')) {
    [void]$bibliographyKeys.Add($match.Groups[1].Value)
}
$citationKeys = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
foreach ($match in [regex]::Matches($tex, '\\cite\s*\{([^}]+)\}')) {
    foreach ($key in $match.Groups[1].Value.Split(',')) {
        $trimmedKey = $key.Trim()
        if ($trimmedKey) {
            [void]$citationKeys.Add($trimmedKey)
        }
    }
}
if ($bibliographyKeys.Count -eq 0 -or $citationKeys.Count -eq 0) {
    throw "Could not identify bibliography entries or LaTeX citation keys."
}
$missingKeys = @($citationKeys | Where-Object { -not $bibliographyKeys.Contains($_) })
$unusedKeys = @($bibliographyKeys | Where-Object { -not $citationKeys.Contains($_) })
if ($missingKeys.Count -or $unusedKeys.Count) {
    throw "Citation/bibliography mismatch. Missing entries: $($missingKeys -join ', '); uncited entries: $($unusedKeys -join ', ')."
}

$figurePaths = [regex]::Matches(
    $tex, '\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}'
)
foreach ($match in $figurePaths) {
    $figurePath = Join-Path $root $match.Groups[1].Value
    if (-not (Test-Path -LiteralPath $figurePath -PathType Leaf)) {
        throw "Referenced figure asset is missing: $figurePath"
    }
}

if ([System.IO.Path]::IsPathRooted($OutputPath)) {
    $output = [System.IO.Path]::GetFullPath($OutputPath)
} else {
    $output = [System.IO.Path]::GetFullPath((Join-Path $root $OutputPath))
}
$outputDirectory = [System.IO.Path]::GetDirectoryName($output)
if (-not (Test-Path -LiteralPath $outputDirectory -PathType Container)) {
    [void](New-Item -ItemType Directory -Path $outputDirectory -Force)
}
$token = [guid]::NewGuid().ToString("N")
$pandocOutput = Join-Path $outputDirectory ".word-$token-pandoc.docx"
$readyOutput = Join-Path $outputDirectory ".word-$token-ready.docx"
$backupOutput = Join-Path $outputDirectory ".word-$token-backup.docx"
$locationPushed = $false

try {
    Push-Location $root
    $locationPushed = $true
    $arguments = @(
        $source,
        "--from=latex",
        "--to=docx",
        "--standalone",
        "--bibliography=$bibliography",
        "--citeproc",
        "--csl=$csl",
        "--reference-doc=$reference",
        "--lua-filter=$filter",
        "--metadata=reference-section-title:Bibliography",
        "--resource-path=$root",
        "--toc",
        "--toc-depth=3",
        "--output=$pandocOutput"
    )
    & pandoc @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Pandoc failed with exit code $LASTEXITCODE."
    }
    if (-not (Test-Path -LiteralPath $pandocOutput -PathType Leaf)) {
        throw "Pandoc completed without creating a Word document."
    }

    & python $postprocessor --input $pandocOutput --output $readyOutput
    if ($LASTEXITCODE -ne 0) {
        throw "WordprocessingML postprocessing failed with exit code $LASTEXITCODE."
    }
    if (-not (Test-Path -LiteralPath $readyOutput -PathType Leaf)) {
        throw "WordprocessingML postprocessing did not create an output file."
    }

    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [System.IO.Compression.ZipFile]::OpenRead($readyOutput)
    try {
        $documentPart = $archive.GetEntry("word/document.xml")
        $settingsPart = $archive.GetEntry("word/settings.xml")
        if (-not $documentPart -or -not $settingsPart) {
            throw "Generated DOCX is missing required WordprocessingML parts."
        }
        $document = [System.Xml.XmlDocument]::new()
        $document.XmlResolver = $null
        $documentStream = $documentPart.Open()
        try { $document.Load($documentStream) } finally { $documentStream.Dispose() }

        $namespaces = [System.Xml.XmlNamespaceManager]::new($document.NameTable)
        $namespaces.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
        $namespaces.AddNamespace("m", "http://schemas.openxmlformats.org/officeDocument/2006/math")
        $namespaces.AddNamespace("wp", "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing")
        $bibliographyCount = $document.SelectNodes(
            "//w:p[w:pPr/w:pStyle[@w:val='Bibliography']]", $namespaces
        ).Count
        $figureCount = $document.SelectNodes(
            "//w:p[w:pPr/w:pStyle[@w:val='ImageCaption']]", $namespaces
        ).Count
        $tableCount = $document.SelectNodes("//w:tbl", $namespaces).Count
        $equationCount = $document.SelectNodes("//m:oMath", $namespaces).Count
        $imageCount = $document.SelectNodes("//wp:inline | //wp:anchor", $namespaces).Count
        $sectionCount = $document.SelectNodes("//w:sectPr", $namespaces).Count
        $tocFieldInstructions = @(
            $document.SelectNodes("//w:instrText", $namespaces) |
                Where-Object { $_.InnerText -match '^\s*TOC\b' }
        )
        $tocControlCount = $document.SelectNodes(
            "//w:sdt[w:sdtPr/w:docPartObj/w:docPartGallery[@w:val='Table of Contents']]",
            $namespaces
        ).Count
        $customTocEntryCount = @(
            $document.SelectNodes("//w:instrText", $namespaces) |
                Where-Object {
                    $_.InnerText -match '^\s*TC\s+"' -and
                    ($_.InnerText.Contains('"Research Status"') -or
                     $_.InnerText.Contains('"Abstract"'))
                }
        ).Count
        $extraAbstractHeadingCount = $document.SelectNodes(
            "//w:p[w:pPr/w:pStyle[@w:val='Heading1'] and .//w:t[normalize-space(.)='Abstract']]",
            $namespaces
        ).Count
        $pageReferenceCount = $document.SelectNodes(
            "//w:instrText[contains(., 'PAGEREF')]", $namespaces
        ).Count
        $settings = [System.Xml.XmlDocument]::new()
        $settings.XmlResolver = $null
        $settingsStream = $settingsPart.Open()
        try { $settings.Load($settingsStream) } finally { $settingsStream.Dispose() }
        $settingsNamespaces = [System.Xml.XmlNamespaceManager]::new($settings.NameTable)
        $settingsNamespaces.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
        $updateFields = $settings.SelectSingleNode("//w:updateFields", $settingsNamespaces)
        $chapterCount = [regex]::Matches($tex, '\\chapter\s*\{').Count
        $protection = $document.SelectSingleNode("//w:documentProtection", $namespaces)

        if ($bibliographyCount -ne $bibliographyKeys.Count) {
            throw "Expected $($bibliographyKeys.Count) bibliography entries; found $bibliographyCount."
        }
        if ($figureCount -ne $figurePaths.Count) {
            throw "Expected $($figurePaths.Count) figure captions; found $figureCount."
        }
        if ($tableCount -eq 0 -or $equationCount -eq 0 -or $imageCount -eq 0) {
            throw "Generated Word document is missing tables, equations, or embedded figures."
        }
        if ($sectionCount -ne 3 -or $chapterCount -eq 0 -or
            $tocFieldInstructions.Count -ne 1 -or $tocControlCount -ne 1 -or
            $tocFieldInstructions[0].InnerText -notmatch '\\o\s+"1-4"' -or
            $tocFieldInstructions[0].InnerText -notmatch '\\f\s+C' -or
            $customTocEntryCount -ne 2 -or
            $pageReferenceCount -ne $figureCount -or
            -not $updateFields -or
            $updateFields.GetAttribute("val", "http://schemas.openxmlformats.org/wordprocessingml/2006/main") -ne "true" -or
            $extraAbstractHeadingCount -ne 0) {
            throw "Generated Word document is missing the dynamic TOC field, front-matter entries, or page-update settings."
        }
        if ($protection) {
            throw "Generated Word document unexpectedly restricts editing."
        }
        Write-Host "Validated $bibliographyCount numeric-style bibliography entries, $chapterCount chapters, one dynamic Word TOC with front-matter entries, $figureCount dynamically numbered figure-list references, $tableCount tables, $equationCount equations, $imageCount embedded images, and Roman/Arabic page sections."
    } finally {
        $archive.Dispose()
    }

    if ($Paginate) {
        $word = New-Object -ComObject Word.Application
        try {
            $word.DisplayAlerts = 0
            $wordDocument = $word.Documents.Open($readyOutput)
            try {
                if ($wordDocument.TablesOfContents.Count -ne 1) {
                    throw "Microsoft Word did not recognize the native TOC."
                }
                $toc = $wordDocument.TablesOfContents.Item(1)
                $wordDocument.Repaginate()
                $toc.Update()
                $wordDocument.Repaginate()
                $toc.UpdatePageNumbers()
                if ($toc.Range.Text -notmatch '(?m)^Research Status\ti\r' -or
                    $toc.Range.Text -notmatch '(?m)(?:^|\r)Abstract\tii\r') {
                    throw "Microsoft Word did not paginate the TOC front matter as expected."
                }
                $wordDocument.Save()
            } finally {
                $wordDocument.Close(0)
            }
        } finally {
            $word.Quit(0)
        }
    } else {
        Write-Warning "TOC page results are not populated. Use -Paginate with desktop Word or update the entire table before sharing."
    }

    if (Test-Path -LiteralPath $output -PathType Leaf) {
        [System.IO.File]::Replace($readyOutput, $output, $backupOutput)
        Remove-Item -LiteralPath $backupOutput -Force
    } else {
        [System.IO.File]::Move($readyOutput, $output)
    }
    Write-Host "Created editable Word document: $output"
} catch {
    Write-Error "Word build failed; the previous output was not replaced. $($_.Exception.Message)"
    exit 1
} finally {
    if ($locationPushed) { Pop-Location }
    foreach ($temporaryFile in @($pandocOutput, $readyOutput, $backupOutput)) {
        if (Test-Path -LiteralPath $temporaryFile -PathType Leaf) {
            Remove-Item -LiteralPath $temporaryFile -Force
        }
    }
}
