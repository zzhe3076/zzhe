Restart-Service -Name postgresql-x64-18 -Force
Start-Sleep -Seconds 3
$psql = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$output = & $psql -U postgres -h localhost -c "SELECT version()"
Write-Host $output
