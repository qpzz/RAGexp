param([string]$InputPath, [string]$PdfPath)
$ErrorActionPreference = 'Stop'
$wordApp = $null
$openedDoc = $null
try {
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $openedDoc = $wordApp.Documents.Open($InputPath, $false, $true)
    $openedDoc.Repaginate()
    $pageCount = $openedDoc.ComputeStatistics(2)
    $openedDoc.ExportAsFixedFormat($PdfPath, 17)
    Write-Output ('Rendered pages: ' + $pageCount)
    Write-Output ('PDF: ' + $PdfPath)
} finally {
    if ($null -ne $openedDoc) {
        $openedDoc.Close(0)
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($openedDoc)
    }
    if ($null -ne $wordApp) {
        if ($wordApp.Documents.Count -eq 0) { $wordApp.Quit() }
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp)
    }
}
