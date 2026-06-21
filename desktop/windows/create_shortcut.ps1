<#
.SYNOPSIS
    Creates an "AgentFlow Launcher" shortcut on the Windows desktop.

.DESCRIPTION
    This script creates a desktop shortcut that points to start_agentflow.bat.
    Double-click the shortcut to launch the AgentFlow-Launcher server and
    open the web console in your browser.

.NOTES
    Run this script AFTER running scripts\setup_windows.ps1.
    The shortcut icon can be customized by placing a .ico file in the
    project root and updating $IconPath below.
#>

$ErrorActionPreference = "Stop"

# Paths
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$BatPath = Join-Path $PSScriptRoot "start_agentflow.bat"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "AgentFlow Launcher.lnk"
$IconPath = Join-Path $ProjectRoot "docs\images\icon.ico"

# Verify batch file exists
if (-not (Test-Path $BatPath)) {
    Write-Error "Batch file not found: $BatPath"
    exit 1
}

Write-Host "Creating desktop shortcut..."
Write-Host "  Target : $BatPath"
Write-Host "  Desktop: $ShortcutPath"

# Create the shortcut
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $BatPath
$Shortcut.WorkingDirectory = $ProjectRoot
$Shortcut.Description = "AgentFlow-Launcher — Agent / Workflow / Skill 一体化平台"
$Shortcut.WindowStyle = 7  # Minimized

# Set icon if available
if (Test-Path $IconPath) {
    $Shortcut.IconLocation = $IconPath
}

$Shortcut.Save()

Write-Host ""
Write-Host "============================================"
Write-Host "  Shortcut created successfully!"
Write-Host "  Look for 'AgentFlow Launcher' on your desktop."
Write-Host "============================================"
Write-Host ""
Write-Host "Double-click the shortcut to start the server."
Write-Host "The web console will open automatically at:"
Write-Host "  http://127.0.0.1:8000/console"
