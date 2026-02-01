@echo off
REM ═══════════════════════════════════════════════════════════
REM   UNFOLD v3.0 ULTRA - Windows Setup Script
REM ═══════════════════════════════════════════════════════════

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  UNFOLD v3.0 ULTRA - Windows Setup                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Starting UNFOLD v3.0 ULTRA deployment...
echo.

REM Create directories
echo [1/6] Creating directories...
if not exist "scans" mkdir scans
if not exist "report-template" mkdir report-template
if not exist "reports" mkdir reports
if not exist "logs" mkdir logs
echo       ✓ Done
echo.

REM Install profiles
echo [2/6] Installing profiles...
if exist "unified_scan_profiles.json" copy /Y unified_scan_profiles.json scans\ >nul
if exist "disk_scan_profiles.json" copy /Y disk_scan_profiles.json scans\ >nul
if exist "scans\unified_scan_profiles.json" copy /Y scans\unified_scan_profiles.json scans\windows_scan.json >nul
echo       ✓ Done
echo.

REM Install template
echo [3/6] Installing template...
if exist "report_template_FIXED.html" copy /Y report_template_FIXED.html report-template\report.html >nul
echo       ✓ Done
echo.

REM Create config
echo [4/6] Configuration...
if not exist "config.json" (
    echo {"API_KEYS":{"OPENROUTER":"","DEEPSEEK":""}}> config.json
)
echo       ✓ Done
echo.

REM Check dependencies
echo [5/6] Checking dependencies...
python -c "import pytsk3" >nul 2>&1 && echo       ✓ pytsk3 || echo       ⚠ pytsk3 missing
echo.

REM Verify
echo [6/6] Verification...
if exist "unfoldV3.py" (echo       ✓ Main script) else (echo       ✗ Main script missing)
if exist "scans\unified_scan_profiles.json" (echo       ✓ Memory profiles) else (echo       ✗ Profiles missing)
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✅ INSTALLATION COMPLETE!
echo.
echo 🚀 Quick Start:
echo    python unfoldV3.py memory.dmp --scan triage --html -o report.html
echo    python unfoldV3.py disk.dd --scan-disk ctf --html -o disk.html
echo.
echo 📚 Documentation: README.md ^| Documentation.md
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
