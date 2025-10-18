# PowerShell version of the demo script (no jq needed)
$baseUrl = "http://localhost:8000/ingest"
Write-Host "Posting invoice_email.json ..."
Invoke-RestMethod -Method Post -Uri $baseUrl -ContentType "application/json" -InFile "demo_fixtures\invoice_email.json"
Write-Host "----"

Write-Host "Posting complaint_email.json ..."
Invoke-RestMethod -Method Post -Uri $baseUrl -ContentType "application/json" -InFile "demo_fixtures\complaint_email.json"
Write-Host "----"

Write-Host "Posting sheet_alert.json ..."
Invoke-RestMethod -Method Post -Uri $baseUrl -ContentType "application/json" -InFile "demo_fixtures\sheet_alert.json"
Write-Host "----"

Write-Host "Open the dashboard: http://localhost:8000"
