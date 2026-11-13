$word = New-Object -ComObject Word.Application
$word.Visible = $false
Write-Host "Word COM created"
$doc = $word.Documents.Open("C:\Users\sumit\Downloads\rio\report_final.docx")
Write-Host "Document opened"
$doc.ExportAsFixedFormat("C:\Users\sumit\Downloads\rio\report_final.pdf", 17)
Write-Host "Exported PDF"
$doc.Close([ref]$false)
$word.Quit()
Write-Host "All done"

