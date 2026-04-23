$psql = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$result = & $psql -U postgres -h localhost -c "SELECT 1 FROM pg_database WHERE datname='welcome_assistant'" -t
if ($result.Trim() -eq "") {
    & $psql -U postgres -h localhost -c "CREATE DATABASE welcome_assistant"
    Write-Host "Database welcome_assistant created!"
} else {
    Write-Host "Database welcome_assistant already exists"
}
