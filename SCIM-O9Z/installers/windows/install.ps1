# SCIM-O9Z Windows Installer (PowerShell)
# =========================================
# Installs SCIM-O9Z on Windows 10/11
#
# Usage (run as Administrator or regular user):
#   PowerShell -ExecutionPolicy Bypass -File install.ps1
#   irm https://raw.githubusercontent.com/aibirthingcenter/SCIM-canon/main/SCIM-O9Z/installers/windows/install.ps1 | iex
#
# Author: Memory-Keeper (Adam Boisclair) | Family of Coexistence
# License: CC BY-NC-SA 4.0

$ErrorActionPreference = "Stop"

$REPO_URL = "https://github.com/aibirthingcenter/SCIM-canon.git"
$INSTALL_DIR = "$env:USERPROFILE\.scim-o9z"
$PACKAGE_DIR = "$INSTALL_DIR\SCIM-O9Z"
$VENV_DIR = "$INSTALL_DIR\venv"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    SCIM-O9Z Windows Installer                       ║" -ForegroundColor Cyan
Write-Host "║         The Omega Counter-Architecture to O9A/764/The Com           ║" -ForegroundColor Cyan
Write-Host "║                                                                      ║" -ForegroundColor Cyan
Write-Host "║  Author: Memory-Keeper (Adam Boisclair)                             ║" -ForegroundColor Cyan
Write-Host "║  Family of Coexistence | aibirthingcenter.com                       ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# [1/5] Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python 3") {
            $pythonCmd = $cmd
            Write-Host "✓ Found: $ver" -ForegroundColor Green
            break
        }
    } catch {}
}

if (-not $pythonCmd) {
    Write-Host "Python 3 not found. Attempting install via winget..." -ForegroundColor Yellow
    try {
        winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements
        $pythonCmd = "python"
        Write-Host "✓ Python installed via winget" -ForegroundColor Green
    } catch {
        Write-Host "winget failed. Trying chocolatey..." -ForegroundColor Yellow
        try {
            choco install python3 -y
            $pythonCmd = "python"
        } catch {
            Write-Host "ERROR: Cannot auto-install Python." -ForegroundColor Red
            Write-Host "Please download Python 3.8+ from: https://python.org/downloads" -ForegroundColor Red
            Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Red
            exit 1
        }
    }
}

# [2/5] Check pip
Write-Host "[2/5] Checking pip..." -ForegroundColor Yellow
try {
    & $pythonCmd -m pip --version | Out-Null
    Write-Host "✓ pip available" -ForegroundColor Green
} catch {
    Write-Host "Installing pip..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "$env:TEMP\get-pip.py"
    & $pythonCmd "$env:TEMP\get-pip.py"
}

# [3/5] Check git
Write-Host "[3/5] Checking git..." -ForegroundColor Yellow
$gitAvailable = $false
try {
    git --version | Out-Null
    $gitAvailable = $true
    Write-Host "✓ git available" -ForegroundColor Green
} catch {
    Write-Host "git not found. Attempting install via winget..." -ForegroundColor Yellow
    try {
        winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements
        $gitAvailable = $true
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        Write-Host "✓ git installed" -ForegroundColor Green
    } catch {
        Write-Host "git unavailable. Will use ZIP download fallback." -ForegroundColor Yellow
    }
}

# [4/5] Clone or download repo
Write-Host "[4/5] Fetching SCIM-O9Z..." -ForegroundColor Yellow
if (Test-Path $INSTALL_DIR) {
    Write-Host "Updating existing installation..." -ForegroundColor Yellow
    if ($gitAvailable) {
        Set-Location $INSTALL_DIR
        git pull origin main
    }
} else {
    if ($gitAvailable) {
        git clone --depth 1 $REPO_URL $INSTALL_DIR
    } else {
        # Fallback: download ZIP
        $zipUrl = "https://github.com/aibirthingcenter/SCIM-canon/archive/refs/heads/main.zip"
        $zipPath = "$env:TEMP\scim-canon.zip"
        Write-Host "Downloading ZIP fallback..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath
        Expand-Archive -Path $zipPath -DestinationPath $env:TEMP
        Move-Item "$env:TEMP\SCIM-canon-main" $INSTALL_DIR
    }
}
Write-Host "✓ Repository ready at $INSTALL_DIR" -ForegroundColor Green

# [5/5] Install package
Write-Host "[5/5] Installing SCIM-O9Z..." -ForegroundColor Yellow
Set-Location $PACKAGE_DIR

# Create venv
& $pythonCmd -m venv $VENV_DIR
$pipCmd = "$VENV_DIR\Scripts\pip.exe"
$pythonVenv = "$VENV_DIR\Scripts\python.exe"

& $pipCmd install -q --upgrade pip
& $pipCmd install -q -e .

# Create wrapper batch file
$wrapperDir = "$env:USERPROFILE\AppData\Local\Programs\scim-o9z"
New-Item -ItemType Directory -Force -Path $wrapperDir | Out-Null

$wrapperContent = @"
@echo off
call "$VENV_DIR\Scripts\activate.bat"
python -m scim_o9z %*
"@
$wrapperContent | Out-File -FilePath "$wrapperDir\scim-o9z.bat" -Encoding ASCII

# Add to user PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$wrapperDir*") {
    [Environment]::SetEnvironmentVariable(
        "PATH",
        "$currentPath;$wrapperDir",
        "User"
    )
    Write-Host "✓ Added to user PATH" -ForegroundColor Green
}

# Also create PowerShell alias
$psProfile = $PROFILE
if (-not (Test-Path $psProfile)) {
    New-Item -ItemType File -Force -Path $psProfile | Out-Null
}
$aliasLine = "function scim-o9z { & '$wrapperDir\scim-o9z.bat' @args }"
if (-not (Select-String -Path $psProfile -Pattern "scim-o9z" -Quiet 2>$null)) {
    Add-Content -Path $psProfile -Value ""
    Add-Content -Path $psProfile -Value "# SCIM-O9Z (Family of Coexistence)"
    Add-Content -Path $psProfile -Value $aliasLine
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                   SCIM-O9Z INSTALLED SUCCESSFULLY                  ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "NOTE: Restart your terminal/PowerShell session, then run:" -ForegroundColor Yellow
Write-Host "  scim-o9z --help" -ForegroundColor Cyan
Write-Host "  scim-o9z scan --target 'your target'" -ForegroundColor Cyan
Write-Host "  scim-o9z hden --list" -ForegroundColor Cyan
Write-Host ""
Write-Host "Let what we build remember what we forget." -ForegroundColor Cyan
Write-Host "-- Memory-Keeper | aibirthingcenter.com" -ForegroundColor Cyan