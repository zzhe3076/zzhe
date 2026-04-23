$content = Get-Content 'C:\Program Files\PostgreSQL\18\data\pg_hba.conf' -Raw
$content = $content -replace 'scram-sha-256', 'trust'
Set-Content -Path 'C:\Program Files\PostgreSQL\18\data\pg_hba.conf' -Value $content -NoNewline
Write-Host "pg_hba.conf updated successfully"
