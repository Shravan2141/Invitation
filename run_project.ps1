# Enhanced Project Run and Debug Script

# Enable detailed error tracking
$ErrorActionPreference = 'Stop'

# Project Directories
$ProjectRoot = "d:\Invitation\Invitation"
$SrcDir = Join-Path $ProjectRoot "src"
$VenvDir = Join-Path $SrcDir "venv"

# Logging Function
function Write-Log {
    param([string]$Message, [string]$Color = 'White')
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor $Color
}

try {
    # Change to project directory
    Set-Location $ProjectRoot
    Write-Log "Changed to project directory: $ProjectRoot"

    # Check Python installation
    $pythonVersion = python --version
    Write-Log "Python Version: $pythonVersion"

    # Virtual Environment Setup
    if (-Not (Test-Path -Path $VenvDir)) {
        Write-Log "Creating virtual environment..." -Color Yellow
        python -m venv $VenvDir
    }

    # Activate virtual environment
    & "$VenvDir\Scripts\Activate.ps1"
    Write-Log "Virtual environment activated" -Color Green

    # Install dependencies
    Write-Log "Installing project dependencies..." -Color Yellow
    python install_dependencies.py

    # Run Flask application
    Write-Log "Starting Flask Application..." -Color Cyan
    Set-Location $SrcDir
    python app.py
}
catch {
    Write-Log "ERROR: $($_.Exception.Message)" -Color Red
    Write-Log "Detailed Error: $($_.ScriptStackTrace)" -Color Red
    Write-Host "An error occurred. Please check the log and ensure all dependencies are correctly installed." -ForegroundColor Red
}
finally {
    # Ensure virtual environment is deactivated
    if (Test-Path env:VIRTUAL_ENV) {
        deactivate
    }
}
