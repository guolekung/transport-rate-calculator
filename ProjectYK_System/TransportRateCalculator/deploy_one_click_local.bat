@echo off
setlocal
REM Copy calculator HTML + commit เท่านั้น (ไม่ push) — ค่าเริ่มต้นปลอดภัย
set "REPO_PATH=..\.."
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy.ps1" -RepoPath "%REPO_PATH%"
if errorlevel 1 (
  echo.
  echo Local deploy failed. Check message above.
  pause
  exit /b 1
)
echo.
echo Local commit OK. เปิด deploy_one_click.bat ถ้าต้องการ push ขึ้น GitHub
pause
