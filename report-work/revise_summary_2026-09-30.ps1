$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
$sourcePath = 'E:\AgentBackdoorAttack\Agent后门攻击_七大创新方向整理_提问式格式.docx'
$targetPath = 'E:\AgentBackdoorAttack\Agent后门攻击_七类候选研究方向整理_提问式格式_修订版_2026-09-30.docx'
$replacementPath = Join-Path $PSScriptRoot 'summary_revision_2026-09-30.json'
$replacements = Get-Content -LiteralPath $replacementPath -Raw -Encoding UTF8 | ConvertFrom-Json
$inputStream = [IO.File]::OpenRead($sourcePath)
$inputZip = [IO.Compression.ZipArchive]::new($inputStream,[IO.Compression.ZipArchiveMode]::Read,$false)
try {
    $reader = [IO.StreamReader]::new($inputZip.GetEntry('word/document.xml').Open())
    try { $doc = [xml]$reader.ReadToEnd() } finally { $reader.Dispose() }
} finally { $inputZip.Dispose(); $inputStream.Dispose() }
$ns = [Xml.XmlNamespaceManager]::new($doc.NameTable)
$ns.AddNamespace('w','http://schemas.openxmlformats.org/wordprocessingml/2006/main')
$paragraphs = @($doc.SelectNodes('//w:body//w:p',$ns) | Where-Object { (($_.SelectNodes('.//w:t',$ns) | ForEach-Object { $_.InnerText }) -join '').Length -gt 0 })
if ($paragraphs.Count -ne 54 -or $replacements.Count -ne 54) { throw 'Unexpected source or replacement paragraph count.' }
function Set-ParagraphText($paragraph,[string]$value) {
    $nodes = @($paragraph.SelectNodes('.//w:t',$ns))
    $nodes[0].InnerText = $value
    for ($j=1;$j -lt $nodes.Count;$j++) { $nodes[$j].InnerText = '' }
}
for ($i=0;$i -lt $paragraphs.Count;$i++) { Set-ParagraphText $paragraphs[$i] $replacements[$i] }
$intros = @(
    '修订说明：2026 年 9 月 30 日。在原总结基础上保留七大方向、十二个子方向及提问式结构，修正概念边界、威胁模型和结论强度。文献背景沿用 2026 年 9 月 29 日开题调研报告，本次修改不代表已完成新一轮全面查新。',
    '使用定位：以下内容是供导师讨论的候选问题，不是已经验证的新漏洞或已确认无人研究的创新。各方向是否属于后门，需要用植入、状态保留、指定条件触发与攻击后果的证据判断；单次提示影响、普通数据篡改或无攻击者操纵的系统错误不能直接等同于后门。',
    '范围与选题：全部拟开展方法限定为推理时攻击或防御，不训练或微调大模型。十二个子方向不等于十二篇独立论文；消费策略切换优先作为第一方向的扩展，因果判定优先作为所有课题的评测模块。其他方向也需通过最近邻比较和预实验，再决定是否独立成篇。'
)
$anchor = $paragraphs[0]
foreach ($intro in $intros) {
    $p = $paragraphs[2].CloneNode($true)
    $p.RemoveAttribute('paraId','http://schemas.microsoft.com/office/word/2010/wordml')
    $p.RemoveAttribute('textId','http://schemas.microsoft.com/office/word/2010/wordml')
    Set-ParagraphText $p $intro
    [void]$anchor.ParentNode.InsertAfter($p,$anchor)
    $anchor = $p
}
Copy-Item -LiteralPath $sourcePath -Destination $targetPath
$outputStream = [IO.File]::Open($targetPath,[IO.FileMode]::Open,[IO.FileAccess]::ReadWrite)
$outputZip = [IO.Compression.ZipArchive]::new($outputStream,[IO.Compression.ZipArchiveMode]::Update,$false)
try {
    $outputZip.GetEntry('word/document.xml').Delete()
    $entry = $outputZip.CreateEntry('word/document.xml')
    $writer = [IO.StreamWriter]::new($entry.Open(),[Text.UTF8Encoding]::new($false))
    try { $writer.Write($doc.OuterXml) } finally { $writer.Dispose() }
} finally { $outputZip.Dispose(); $outputStream.Dispose() }
$plain = @($doc.SelectNodes('//w:body//w:p',$ns) | ForEach-Object { ($_.SelectNodes('.//w:t',$ns) | ForEach-Object { $_.InnerText }) -join '' } | Where-Object { $_ }) -join "`r`n`r`n"
[IO.File]::WriteAllText(($targetPath -replace '\.docx$','.txt'),$plain,[Text.UTF8Encoding]::new($false))
[pscustomobject]@{Output=$targetPath;RevisedParagraphs=$replacements.Count;IntroParagraphs=$intros.Count;Characters=$plain.Length} | Format-List
