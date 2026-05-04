@echo off
setlocal
REM หลังย้าย path รายงาน — ลิงก์ปัจจุบัน: https://yk-logistics.github.io/transport-rate-calculator/reports/oatside-pg-2026/index.html
REM (ลิงก์เก่า …/reports/oatside-apr2026/… จะ 404 หลัง deploy ครั้งนี้ เพราะสคริปต์ลบโฟลเดอร์เก่า)
REM โฟลเดอร์ clone ต้องมี remote ชี้ https://github.com/yk-logistics/transport-rate-calculator.git

set "REPO_PATH=transport-rate-calculator-repo"
set "SOURCE_REPORT_DIR=ProjectYK_System\TransportRateCalculator\reports\oatside-apr2026"

cd /d "%~dp0"

echo Rebuild Oatside Excel + HTML from GPS files in Oatside\ ...
python Oatside\build_oatside_reports.py
if errorlevel 1 (
  echo Build failed.
  pause
  exit /b 1
)

echo Copy Oatside report folder into GitHub Pages repo...
echo Source: %SOURCE_REPORT_DIR%
echo Repo: %REPO_PATH%

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy_oatside_report.ps1" -RepoPath "%REPO_PATH%" -SourceReportDir "%SOURCE_REPORT_DIR%" -PagesReportSlug "oatside-pg-2026" -RemoveLegacyApr2026 -Push

pause

