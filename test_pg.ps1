$env:PGPASSWORD = "Zhang123"
$psql = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$output = & $psql -U postgres -h localhost -c "SELECT version()" 2>&1
Write-Host $output
