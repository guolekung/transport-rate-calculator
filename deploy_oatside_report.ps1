param(
  [string]$RepoPath = "transport-rate-calculator-repo",
  [string]$SourceReportDir = "ProjectYK_System\TransportRateCalculator\reports\oatside-apr2026",
  # Folder name under reports/ on the Pages repo → public URL …/reports/<slug>/index.html
  [string]$PagesReportSlug = "oatside-pg-2026",
  # If set: git rm reports/oatside-apr2026 (old shared links 404). deploy_oatside_report_one_click.bat passes this.
  [switch]$RemoveLegacyApr2026,
  [string]$CommitMessage = "",
  # Safe default: commit in clone only. Use -Push to run pull --rebase + push.
  [switch]$Push,
  [switch]$NoPush
)

$ErrorActionPreference = "Stop"

# Clone ของ GitHub Pages (หลังย้ายไป org): https://github.com/yk-logistics/transport-rate-calculator
# ถ้าเคย clone ตอนเป็น user เดิม ให้รันในโฟลเดอร์ repo: git remote set-url origin https://github.com/yk-logistics/transport-rate-calculator.git

function Resolve-AbsolutePath([string]$basePath, [string]$pathValue) {
  if ([System.IO.Path]::IsPathRooted($pathValue)) {
    return [System.IO.Path]::GetFullPath($pathValue)
  }
  return [System.IO.Path]::GetFullPath((Join-Path $basePath $pathValue))
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoAbs = Resolve-AbsolutePath $scriptDir $RepoPath

if (-not (Test-Path $repoAbs)) {
  throw "Repo path not found: $repoAbs"
}

# Pick the newest built report among known locations (build may write under Oatside/ or ProjectYK_System/).
$candidateDirs = @(
  (Resolve-AbsolutePath $scriptDir "Oatside\TransportRateCalculator\reports\oatside-apr2026"),
  (Resolve-AbsolutePath $scriptDir "ProjectYK_System\TransportRateCalculator\reports\oatside-apr2026"),
  (Resolve-AbsolutePath $scriptDir "TransportRateCalculator\reports\oatside-apr2026"),
  (Resolve-AbsolutePath $scriptDir $SourceReportDir)
)
$best = $null
$bestTicks = [long]0
foreach ($c in $candidateDirs) {
  if (-not (Test-Path -LiteralPath $c)) { continue }
  $idx = Join-Path $c "index.html"
  if (Test-Path -LiteralPath $idx) {
    $t = (Get-Item -LiteralPath $idx).LastWriteTimeUtc
  }
  else {
    $t = (Get-Item -LiteralPath $c).LastWriteTimeUtc
  }
  $ticks = $t.Ticks
  if ($ticks -gt $bestTicks) {
    $bestTicks = $ticks
    $best = $c
  }
}
if (-not $best) {
  throw "Source report dir not found (tried Oatside, ProjectYK_System, TransportRateCalculator, and -SourceReportDir)."
}
$srcAbs = $best
Write-Host "Using report dir: $srcAbs" -ForegroundColor Cyan

$slug = $PagesReportSlug.Trim().Trim('/').Replace('\', '')
if (-not $slug) { throw "PagesReportSlug is empty." }
if ($slug -match '[\./\\]') { throw "PagesReportSlug must be a single folder name (no slashes)." }

$destAbs = Join-Path $repoAbs "reports/$slug"
$destParent = Split-Path -Parent $destAbs
if (-not (Test-Path $destParent)) {
  New-Item -ItemType Directory -Path $destParent | Out-Null
}

# Replace report folder in the publish repo (does not touch $repoAbs/index.html).
if (Test-Path $destAbs) {
  Remove-Item -Recurse -Force $destAbs
}
Copy-Item -Path $srcAbs -Destination $destAbs -Recurse -Force
Write-Host "Copied: `n  $srcAbs`n-> $destAbs" -ForegroundColor Green
Write-Host "Public report URL (after push): https://yk-logistics.github.io/transport-rate-calculator/reports/$slug/index.html" -ForegroundColor Cyan

Push-Location $repoAbs
try {
  $isGitRepo = $false
  try {
    git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -eq 0) { $isGitRepo = $true }
  } catch { }

  if (-not $isGitRepo) {
    Write-Host "Not a git repo. Copy complete (no commit/push)."
    return
  }

  if ($RemoveLegacyApr2026.IsPresent) {
    $legacy = Join-Path $repoAbs "reports/oatside-apr2026"
    if (Test-Path -LiteralPath $legacy) {
      Write-Host "Removing legacy folder reports/oatside-apr2026 (old URLs will 404 after push)..." -ForegroundColor Yellow
      git rm -r --ignore-unmatch "reports/oatside-apr2026"
    }
  }

  # Stage new report folder (does not touch repo root index.html)
  git add -- "reports/$slug"

  $hasChanges = $false
  git diff --cached --quiet
  if ($LASTEXITCODE -ne 0) { $hasChanges = $true }

  if (-not $hasChanges) {
    Write-Host "No staged changes to commit." -ForegroundColor Yellow
    return
  }

  if (-not $CommitMessage) {
    $suffix = if ($RemoveLegacyApr2026.IsPresent) { ' (remove legacy oatside-apr2026)' } else { '' }
    $CommitMessage = "Oatside report: publish reports/$slug$suffix " + (Get-Date -Format "yyyy-MM-dd HH:mm")
  }

  git commit -m $CommitMessage
  if ($NoPush) {
    Write-Host "Push skipped due to -NoPush."
  }
  elseif ($Push) {
    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    if ($branch -eq "HEAD") {
      throw "Detached HEAD - checkout main (or your publish branch) in the repo, then retry."
    }
    Write-Host "Syncing with origin before push (fetch + pull --rebase origin $branch)..." -ForegroundColor Cyan
    git fetch origin
    git pull --rebase origin $branch
    if ($LASTEXITCODE -ne 0) {
      $msg = "git pull --rebase failed. Fix in: $repoAbs then git rebase --continue or git rebase --abort; then git push origin $branch"
      throw $msg
    }
    git push origin $branch
    if ($LASTEXITCODE -ne 0) {
      throw "git push origin $branch failed after rebase."
    }
  }
  else {
    Write-Host "Committed in clone only (safe default). To publish: re-run script with -Push from repo root." -ForegroundColor Yellow
  }
}
finally {
  Pop-Location
}

Write-Host "Done."

