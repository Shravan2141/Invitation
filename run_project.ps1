# Enhanced Project Run and Debug Script

# Enable detailed error tracking
$ErrorActionPreference = 'Stop'

# Logging function
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

# Project directory setup
$ProjectRoot = "d:\Invitation\Invitation"
$SrcDir = Join-Path $ProjectRoot "src"

try {
    # Change to project directory
    Set-Location $ProjectRoot
    Write-Log "Changed to project directory: $ProjectRoot"

    # Check Python installation
    $pythonVersion = python --version
    Write-Log "Python Version: $pythonVersion"

    # Virtual Environment Setup
    $venvPath = Join-Path $SrcDir "venv"
    if (-Not (Test-Path -Path $venvPath)) {
        Write-Log "Creating virtual environment..."
        python -m venv $venvPath
    }

    # Activate virtual environment
    & "$venvPath\Scripts\Activate.ps1"
    Write-Log "Virtual environment activated"

    # Upgrade pip and setuptools
    python -m pip install --upgrade pip setuptools
    Write-Log "Upgraded pip and setuptools"

    # Install project requirements
    python -m pip install -r "$SrcDir\requirements.txt"
    Write-Log "Installed project requirements"

    # Run diagnostic script
    Write-Log "Running system diagnostic..."
    python system_diagnostic.py

    # Run Flask application
    Write-Log "Starting Flask Application..."
    Set-Location $SrcDir
    python app.py
}
catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    Write-Log "Detailed Error: $($_.ScriptStackTrace)"
    Write-Host "An error occurred. Please check the log and ensure all dependencies are correctly installed." -ForegroundColor Red
}
finally {
    # Ensure virtual environment is deactivated
    if (Test-Path env:VIRTUAL_ENV) {
        deactivate
    }
}
