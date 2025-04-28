# Ask user for number of workers
$workers = Read-Host "Enter number of workers to start (e.g., 4)"

# Ask user for number of threads
$threads = Read-Host "Enter number of threads per worker (e.g., 2)"

$interfaces = @("Ethernet", "WiFi")
$ip = $null

# Loop through each interface name
foreach ($interface in $interfaces) {
    # Get the IP address for the current interface alias
    $ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias $interface | Select-Object -First 1).IPAddress
    if ($ip) {
        break
    }
}

# If an IP address was found, append port 80 and output it
if ($ip) {
    $ip = $ip + ":80"
    Write-Host "Ignore the above error."
    Write-Host "IP Address with port 80: http://$ip/" -ForegroundColor Magenta -BackgroundColor Blue
} else {
    Write-Host "No IPv4 address found for Ethernet or WiFi." -ForegroundColor Red
}


# Initialize
$port = 8000
$servers = @()
$processes = @()

Write-Host "[*] Starting $workers Waitress servers with $threads threads each..." -ForegroundColor Cyan

# Loop to start Waitress servers
for ($i = 0; $i -lt [int]$workers; $i++) {
    Write-Host "[*] Starting Waitress server on port $port..." -ForegroundColor Yellow
    
    $cmd = ".venv\Scripts\waitress-serve --host=127.0.0.1 --port=$port --threads=$threads HackCheckAPI.wsgi:application"
    
    $p = Start-Process -FilePath "cmd.exe" -ArgumentList "/c $cmd" -NoNewWindow -PassThru

    if ($p) {
        Write-Host "[+] Started on port $port (PID: $($p.Id))" -ForegroundColor Green
        $servers += "127.0.0.1:$port"
        $processes += $p
    }
    else {
        Write-Host "[!] Failed to start server on port $port. Exiting..." -ForegroundColor Red
        exit 1
    }
    
    $port++
}

# Create the Caddyfile
Write-Host "[*] Writing Caddyfile..." -ForegroundColor Cyan

$caddyfile = ":80 {
    reverse_proxy " + ($servers -join " ") + " {
        lb_policy round_robin
    }
}"

Set-Content -Path "Caddyfile" -Value $caddyfile -Encoding UTF8

Write-Host "[*] Starting Caddy server..." -ForegroundColor Cyan

# Try to start Caddy normally
$startCaddy = Start-Process -FilePath "caddy" -ArgumentList "run --config Caddyfile" -PassThru -Wait

# If Caddy fails to start, check if caddy.exe exists in current directory
if ($startCaddy.ExitCode -ne 0) {
    Write-Host "[!] Caddy didn't start successfully. Checking for 'caddy.exe' in current folder..." -ForegroundColor Yellow

    $caddyPath = Join-Path (Get-Location) "caddy.exe"
    
    if (Test-Path $caddyPath) {
        Write-Host "[+] Found 'caddy.exe' in the current directory. Starting it..." -ForegroundColor Green
        $startCaddy = Start-Process -FilePath $caddyPath -ArgumentList "run --config Caddyfile" -PassThru -Wait
    } else {
        Write-Host "[!] Could not find 'caddy.exe'. Exiting..." -ForegroundColor Red
        exit 1
    }
}

# Cleanup: When Caddy stops, stop all waitress processes
Write-Host "[*] Stopping all Waitress servers..." -ForegroundColor Magenta
foreach ($proc in $processes) {
    try {
        Stop-Process -Id $proc.Id -Force
    } catch {
        Write-Host "Failed to stop process $($proc.Id)" -ForegroundColor Red
    }
}

# Forcefully kill lingering processes on the ports used
Write-Host "[*] Forcefully killing any lingering processes holding the ports..." -ForegroundColor Red

for ($port = 8000; $port -lt (8000 + $workers); $port++) {
    $currentPID = (netstat -ano | findstr ":$port" | findstr "0.0.0.0" | foreach { $_.Split()[-1] })
    
    if ($currentPID) {
        Write-Host "[!] Found lingering process on port $port with PID $currentPID. Killing it..." -ForegroundColor Red
        try {
            taskkill /F /PID $currentPID
            Write-Host "[+] Killed process on port $port (PID: $currentPID)" -ForegroundColor Green
        } catch {
            Write-Host "[!] Failed to kill process $currentPID" -ForegroundColor Red
        }
    } else {
        Write-Host "[+] No lingering process found on port $port." -ForegroundColor Green
    }
}
