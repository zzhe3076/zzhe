$pg_ctl = "C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe"
$output = & $pg_ctl stop -D "C:\Program Files\PostgreSQL\18\data" -m fast -w
Write-Host "Stop result: $output"
Start-Sleep -Seconds 3
$output2 = & $pg_ctl start -D "C:\Program Files\PostgreSQL\18\data" -w
Write-Host "Start result: $output2"
Start-Sleep -Seconds 3
$psql = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$version = & $psql -U postgres -h localhost -c "SELECT version()"
Write-Host $version
