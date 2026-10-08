param(
    [string]$InputPath = (Join-Path $PSScriptRoot 'Agent后门攻击_硕士开题报告.md'),
    [string]$OutputPath = (Join-Path $PSScriptRoot 'Agent后门攻击_硕士开题报告.docx')
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression

function Escape-Xml([string]$Value) {
    return [System.Security.SecurityElement]::Escape($Value)
}

function Add-ZipEntry($Archive, [string]$Name, [string]$Content) {
    $entry = $Archive.CreateEntry($Name, [System.IO.Compression.CompressionLevel]::Optimal)
    $stream = $entry.Open()
    $writer = New-Object System.IO.StreamWriter($stream, (New-Object System.Text.UTF8Encoding($false)))
    try { $writer.Write($Content) }
    finally { $writer.Dispose() }
}

function New-Paragraph([string]$Value, [string]$Style = 'Normal', [bool]$PageBreak = $false) {
    $escaped = Escape-Xml $Value
    $breakXml = if ($PageBreak) { '<w:r><w:br w:type="page"/></w:r>' } else { '' }
    return '<w:p><w:pPr><w:pStyle w:val="' + $Style + '"/></w:pPr>' + $breakXml + '<w:r><w:t xml:space="preserve">' + $escaped + '</w:t></w:r></w:p>'
}

function New-Table($Rows) {
    if ($Rows.Count -eq 0) { return '' }
    $cols = $Rows[0].Count
    $width = [int][Math]::Floor(9000 / $cols)
    $grid = [System.Text.StringBuilder]::new()
    for ($col = 0; $col -lt $cols; $col++) { [void]$grid.Append('<w:gridCol w:w="' + $width + '"/>') }
    $xml = [System.Text.StringBuilder]::new()
    [void]$xml.Append('<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="6"/><w:left w:val="single" w:sz="6"/><w:bottom w:val="single" w:sz="6"/><w:right w:val="single" w:sz="6"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders><w:tblCellMar><w:top w:w="90" w:type="dxa"/><w:left w:w="90" w:type="dxa"/><w:bottom w:w="90" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>' + $grid.ToString() + '</w:tblGrid>')
    for ($rowIndex = 0; $rowIndex -lt $Rows.Count; $rowIndex++) {
        [void]$xml.Append('<w:tr>')
        if ($rowIndex -eq 0) { [void]$xml.Append('<w:trPr><w:tblHeader w:val="true"/></w:trPr>') }
        foreach ($cell in $Rows[$rowIndex]) {
            $shade = if ($rowIndex -eq 0) { '<w:shd w:fill="DCE6F1"/>' } else { '' }
            $bold = if ($rowIndex -eq 0) { '<w:rPr><w:b/></w:rPr>' } else { '' }
            [void]$xml.Append('<w:tc><w:tcPr><w:tcW w:w="' + $width + '" w:type="dxa"/>' + $shade + '</w:tcPr><w:p><w:pPr><w:pStyle w:val="TableText"/></w:pPr><w:r>' + $bold + '<w:t xml:space="preserve">' + (Escape-Xml $cell) + '</w:t></w:r></w:p></w:tc>')
        }
        [void]$xml.Append('</w:tr>')
    }
    [void]$xml.Append('</w:tbl>')
    return $xml.ToString()
}

function Parse-TableRow([string]$Line) {
    return ,@($Line.Trim().Trim('|').Split('|') | ForEach-Object { $_.Trim() })
}

$source = Get-Content -LiteralPath $InputPath -Raw -Encoding UTF8
$lines = $source -split "`r?`n"
$body = [System.Text.StringBuilder]::new()
$tableRows = [System.Collections.ArrayList]::new()
$firstTitle = $true
$firstChapter = $true

function Flush-Table {
    if ($tableRows.Count -gt 0) {
        [void]$body.Append((New-Table $tableRows))
        $tableRows.Clear()
    }
}

foreach ($rawLine in $lines) {
    $line = $rawLine.Trim()
    if ($line -match '^\|') {
        if ($line -notmatch '^\|\s*:?-{3,}') { [void]$tableRows.Add((Parse-TableRow $line)) }
        continue
    }
    Flush-Table
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    if ($line -match '^# (.+)$') {
        if ($firstTitle) {
            [void]$body.Append((New-Paragraph $Matches[1] 'Title'))
            $firstTitle = $false
        } else {
            [void]$body.Append((New-Paragraph $Matches[1] 'Heading1' $firstChapter))
            $firstChapter = $false
        }
    } elseif ($line -match '^## (.+)$') {
        [void]$body.Append((New-Paragraph $Matches[1] 'Heading2'))
    } else {
        [void]$body.Append((New-Paragraph $line))
    }
}
Flush-Table

$document = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>' +
    $body.ToString() +
    '<w:sectPr><w:footerReference w:type="default" r:id="rId1"/><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>'

$styles = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="SimSun" w:hAnsi="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault></w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:ind w:firstLine="480"/></w:pPr><w:rPr><w:rFonts w:eastAsia="SimSun"/><w:sz w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:before="520" w:after="600"/><w:ind w:firstLine="0"/></w:pPr><w:rPr><w:rFonts w:eastAsia="SimHei"/><w:b/><w:sz w:val="36"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="360" w:after="180"/><w:ind w:firstLine="0"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:eastAsia="SimHei"/><w:b/><w:sz w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="260" w:after="140"/><w:ind w:firstLine="0"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:rFonts w:eastAsia="SimHei"/><w:b/><w:sz w:val="28"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0" w:line="300" w:lineRule="auto"/><w:ind w:firstLine="0"/></w:pPr><w:rPr><w:rFonts w:eastAsia="SimSun"/><w:sz w:val="21"/></w:rPr></w:style>
</w:styles>
'@

$footer = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>
'@

$contentTypes = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>
'@

$rootRels = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>
'@

$documentRels = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>
'@

$core = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Agent 后门攻击研究——硕士学位论文开题报告</dc:title><dc:subject>Agent 推理时后门攻击与防护选题调研</dc:subject></cp:coreProperties>
'@

$app = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Office Word</Application></Properties>
'@

$parts = @{
    '[Content_Types].xml' = $contentTypes
    '_rels/.rels' = $rootRels
    'word/document.xml' = $document
    'word/styles.xml' = $styles
    'word/footer1.xml' = $footer
    'word/_rels/document.xml.rels' = $documentRels
    'docProps/core.xml' = $core
    'docProps/app.xml' = $app
}

foreach ($part in $parts.Values) { $xml = New-Object System.Xml.XmlDocument; $xml.LoadXml($part) }

$outputDirectory = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $outputDirectory)) { New-Item -ItemType Directory -Path $outputDirectory | Out-Null }
$file = [System.IO.File]::Open($OutputPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write)
try {
    $archive = New-Object System.IO.Compression.ZipArchive($file, [System.IO.Compression.ZipArchiveMode]::Create, $false)
    try {
        foreach ($name in $parts.Keys) { Add-ZipEntry $archive $name $parts[$name] }
    } finally { $archive.Dispose() }
} finally { $file.Dispose() }

Write-Output "Created: $OutputPath"
Write-Output "Characters: $($source.Length)"
