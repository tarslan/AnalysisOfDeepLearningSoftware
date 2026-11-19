[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Path,
    [string]$OutputPath
)

$ErrorActionPreference = "Stop"
$inputPath = [System.IO.Path]::GetFullPath($Path)
if (-not (Test-Path -LiteralPath $inputPath -PathType Leaf)) {
    throw "Returned Word document was not found: $inputPath"
}
if (-not $OutputPath) {
    $OutputPath = [System.IO.Path]::ChangeExtension($inputPath, ".feedback.md")
} elseif (-not [System.IO.Path]::IsPathRooted($OutputPath)) {
    $OutputPath = [System.IO.Path]::GetFullPath(
        (Join-Path ([System.IO.Path]::GetDirectoryName($inputPath)) $OutputPath)
    )
}

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [System.IO.Compression.ZipFile]::OpenRead($inputPath)
try {
    $documentEntry = $archive.GetEntry("word/document.xml")
    if (-not $documentEntry) {
        throw "The input file is not a valid Word document: $inputPath"
    }
    $namespaceUri = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    $document = [System.Xml.XmlDocument]::new()
    $document.XmlResolver = $null
    $documentStream = $documentEntry.Open()
    try { $document.Load($documentStream) } finally { $documentStream.Dispose() }
    $documentManager = [System.Xml.XmlNamespaceManager]::new($document.NameTable)
    $documentManager.AddNamespace("w", $namespaceUri)

    $script:activeCommentRanges = [System.Collections.Generic.List[string]]::new()
    $script:commentRangeText = @{}
    function Visit-CommentRange([System.Xml.XmlNode]$node) {
        foreach ($child in $node.ChildNodes) {
            if ($child.NodeType -eq [System.Xml.XmlNodeType]::Element -and $child.LocalName -eq "commentRangeStart") {
                $id = $child.GetAttribute("id", $namespaceUri)
                [void]$script:activeCommentRanges.Add($id)
            } elseif ($child.NodeType -eq [System.Xml.XmlNodeType]::Element -and $child.LocalName -eq "commentRangeEnd") {
                $id = $child.GetAttribute("id", $namespaceUri)
                [void]$script:activeCommentRanges.Remove($id)
            } elseif ($child.NodeType -eq [System.Xml.XmlNodeType]::Text) {
                foreach ($id in $script:activeCommentRanges) {
                    $script:commentRangeText[$id] += $child.Value
                }
            } else {
                Visit-CommentRange $child
            }
        }
    }
    Visit-CommentRange $document.DocumentElement

    $comments = @()
    $commentsEntry = $archive.GetEntry("word/comments.xml")
    if ($commentsEntry) {
        $commentsDocument = [System.Xml.XmlDocument]::new()
        $commentsDocument.XmlResolver = $null
        $commentsStream = $commentsEntry.Open()
        try { $commentsDocument.Load($commentsStream) } finally { $commentsStream.Dispose() }
        $commentsManager = [System.Xml.XmlNamespaceManager]::new($commentsDocument.NameTable)
        $commentsManager.AddNamespace("w", $namespaceUri)
        foreach ($comment in $commentsDocument.SelectNodes("//w:comment", $commentsManager)) {
            $id = $comment.GetAttribute("id", $namespaceUri)
            $comments += [pscustomobject]@{
                Id = $id
                Author = $comment.GetAttribute("author", $namespaceUri)
                Date = $comment.GetAttribute("date", $namespaceUri)
                Selection = $script:commentRangeText[$id]
                Text = ($comment.SelectNodes(".//w:t", $commentsManager) |
                    ForEach-Object { $_.InnerText }) -join ""
            }
        }
    }

    $changes = @()
    foreach ($change in $document.SelectNodes("//w:ins | //w:del", $documentManager)) {
        $textNodes = $change.SelectNodes(".//w:t | .//w:delText", $documentManager)
        $changes += [pscustomobject]@{
            Type = if ($change.LocalName -eq "ins") { "Inserted" } else { "Deleted" }
            Author = $change.GetAttribute("author", $namespaceUri)
            Date = $change.GetAttribute("date", $namespaceUri)
            Text = ($textNodes | ForEach-Object { $_.InnerText }) -join ""
        }
    }
} finally {
    $archive.Dispose()
}

$report = [System.Collections.Generic.List[string]]::new()
$report.Add("# Word review report")
$report.Add("")
$report.Add("Source: ``$inputPath``")
$report.Add("")
$report.Add("This report extracts Word comments and tracked insertions/deletions. It does not merge edits into LaTeX.")
$report.Add("")
$report.Add("## Comments ($($comments.Count))")
$report.Add("")
if ($comments.Count) {
    foreach ($comment in $comments) {
        $report.Add("### Comment $($comment.Id) — $($comment.Author) $($comment.Date)")
        if ($comment.Selection) {
            $report.Add("")
            $report.Add("> Selected text: $($comment.Selection -replace '\s+', ' ')")
        }
        $report.Add("")
        $report.Add($comment.Text)
        $report.Add("")
    }
} else {
    $report.Add("No Word comments found.")
    $report.Add("")
}
$report.Add("## Tracked changes ($($changes.Count))")
$report.Add("")
if ($changes.Count) {
    foreach ($change in $changes) {
        $report.Add("- **$($change.Type)** — $($change.Author) $($change.Date): $($change.Text -replace '\s+', ' ')")
    }
} else {
    $report.Add("No tracked insertions or deletions found.")
}

[System.IO.File]::WriteAllLines(
    $OutputPath,
    $report,
    [System.Text.UTF8Encoding]::new($false)
)
Write-Host "Wrote review report: $OutputPath"
