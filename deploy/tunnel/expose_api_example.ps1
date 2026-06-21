<#
.SYNOPSIS
    Expose AgentFlow-Launcher to the public internet via tunnel tools.

.DESCRIPTION
    This script demonstrates how to create a public URL for your local
    AgentFlow-Launcher server using Cloudflare Tunnel, Ngrok, or LocalTunnel.

.PARAMETER Method
    The tunnel tool to use: cloudflare (default), ngrok, or localtunnel.

.PARAMETER Port
    Local port number (default: 8000).

.EXAMPLE
    powershell -File expose_api_example.ps1 cloudflare
    powershell -File expose_api_example.ps1 ngrok 8000
#>

param(
    [ValidateSet("cloudflare", "ngrok", "localtunnel")]
    [string]$Method = "cloudflare",
    [int]$Port = 8000
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  AgentFlow-Launcher — Public Tunnel" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Method    : $Method"
Write-Host "  Local Port: $Port"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Ensure server is running or start it
try {
    $null = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/health" -UseBasicParsing -TimeoutSec 2
} catch {
    Write-Host "[INFO] Starting AgentFlow-Launcher server..." -ForegroundColor Yellow
    $ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
    Set-Location $ProjectRoot
    Start-Process python -ArgumentList "scripts/run_server.py" -WindowStyle Minimized
    Start-Sleep -Seconds 4
}

switch ($Method) {
    "cloudflare" {
        Write-Host "[INFO] Starting Cloudflare Tunnel..." -ForegroundColor Green
        Write-Host "  Public URL will be a *.trycloudflare.com address" -ForegroundColor Gray
        Write-Host ""
        cloudflared tunnel --url "http://127.0.0.1:$Port"
    }
    "ngrok" {
        Write-Host "[INFO] Starting Ngrok Tunnel..." -ForegroundColor Green
        Write-Host "  Public URL will be a *.ngrok-free.app address" -ForegroundColor Gray
        Write-Host "  Local inspector: http://127.0.0.1:4040" -ForegroundColor Gray
        Write-Host ""
        ngrok http $Port
    }
    "localtunnel" {
        Write-Host "[INFO] Starting LocalTunnel..." -ForegroundColor Green
        Write-Host "  Public URL will be a *.loca.lt address" -ForegroundColor Gray
        Write-Host ""
        lt --port $Port
    }
}
