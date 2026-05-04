@echo off
setlocal

REM One-click deploy for Transport Rate Calculator
REM Git root = Project YK (โฟลเดอร์แม่ของ ProjectYK_System — ขึ้นไป 2 ระดับจาก TransportRateCalculator)
REM → copy index.html เข้า repo เดียวกันแล้ว commit + push ไป GitHub Pages (ต้องใส่ -Push)
set "REPO_PATH=..\.."

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy.ps1" -RepoPath "%REPO_PATH%" -Push
if errorlevel 1 (
  echo.
  echo Deploy failed. Check message above.
  pause
  exit /b 1
)

echo.
echo Deploy completed successfully.
pause
