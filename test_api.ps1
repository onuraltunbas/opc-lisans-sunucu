# Test script for API endpoints (PowerShell)
$ErrorActionPreference = 'Stop'
Set-Location 'c:\Users\onnur\Desktop\opc-lisans-sunucu'
param([int]$waitSeconds=2)
Start-Sleep -Seconds $waitSeconds
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$email = "testuser-{0}@example.com" -f ([guid]::NewGuid().ToString())
$body = @{ ad_soyad = "Test User"; email = $email; sifre = "TestPass123" } | ConvertTo-Json
Write-Output "Registering user: $email"
try {
  $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/kayit' -Method Post -Body $body -ContentType 'application/json' -WebSession $session -UseBasicParsing -ErrorAction Stop
  Write-Output "REGISTER RESPONSE: $($r.Content)"
} catch {
  Write-Output "REGISTER ERROR: $($_.Exception.Message)"
  exit 1
}
Start-Sleep -Seconds 1
$loginBody = @{ email = $email; sifre = "TestPass123" } | ConvertTo-Json
Write-Output "Logging in..."
try {
  $login = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/giris' -Method Post -Body $loginBody -ContentType 'application/json' -WebSession $session -UseBasicParsing -ErrorAction Stop
  Write-Output "LOGIN RESPONSE: $($login.Content)"
} catch {
  Write-Output "LOGIN ERROR: $($_.Exception.Message)"
  exit 1
}
Write-Output "COOKIES:"
$session.Cookies.GetCookies('http://127.0.0.1') | ForEach-Object { Write-Output ('{0}={1}' -f $_.Name, $_.Value) }
Start-Sleep -Seconds 1
Write-Output "Calling /api/profil..."
try {
  $profil = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/profil' -Method Get -WebSession $session -UseBasicParsing -ErrorAction Stop
  Write-Output "PROFILE RESPONSE: $($profil.Content)"
  exit 0
} catch {
  Write-Output "PROFILE ERROR: $($_.Exception.Message)"
  exit 1
}
