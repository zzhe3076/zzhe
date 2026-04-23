$pg_ctl = "C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe"
& $pg_ctl reload -D "C:\Program Files\PostgreSQL\18\data"
Start-Sleep -Seconds 2
$psql = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$output = & $psql -U postgres -h localhost -c "SELECT version()"
Write-Host $output
