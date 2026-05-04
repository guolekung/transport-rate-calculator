# ก่อน deploy — ตรวจสอบ Git สั้น ๆ
# ตัวอย่าง (จาก repo root): powershell -File ProjectYK_System\TransportRateCalculator\preflight_deploy.ps1

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Resolve-Path (Join-Path $scriptDir "..\..") # TransportRateCalculator -> ProjectYK_System -> Project YK

Push-Location $root
try {
  if (-not (Test-Path ".git")) {
    Write-Host "Not a git repo: $root" -ForegroundColor Red
    exit 1
  }
  Write-Host "Preflight (repo: $root)" -ForegroundColor Cyan
  git status -sb
  $porcelain = (git status --porcelain 2>$null)
  if ($porcelain) {
    $lines = @($porcelain -split "`r?`n" | Where-Object { $_ })
    Write-Host "`nThere are $($lines.Count) status line(s). Consider: git stash -u -m 'before deploy' or commit first." -ForegroundColor Yellow
  } else {
    Write-Host "`nWorking tree clean." -ForegroundColor Green
  }
  Write-Host "`nTips: deploy.ps1 default = commit only; use deploy_one_click.bat to push. Avoid git reset --hard unless you know the risk." -ForegroundColor Cyan
}
finally {
  Pop-Location
}
