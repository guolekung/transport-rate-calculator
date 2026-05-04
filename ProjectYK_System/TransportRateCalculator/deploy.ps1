param(
  [string]$RepoPath = "..\..",
  [string]$SourceHtml = ".\transport_rate_calculator.html",
  [string]$TargetIndex = "index.html",
  [string]$CommitMessage = "",
  # Safe default: commit locally only. Use -Push to publish to origin (GitHub Pages).
  [switch]$Push,
  [switch]$NoPush
)

$ErrorActionPreference = "Stop"

function Assert-LastExitCode([string]$stepName) {
  if ($LASTEXITCODE -ne 0) {
    throw "$stepName failed (exit code: $LASTEXITCODE)"
  }
}

function Resolve-AbsolutePath([string]$basePath, [string]$pathValue) {
  if ([System.IO.Path]::IsPathRooted($pathValue)) {
    return [System.IO.Path]::GetFullPath($pathValue)
  }
  return [System.IO.Path]::GetFullPath((Join-Path $basePath $pathValue))
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoAbs = Resolve-AbsolutePath $scriptDir $RepoPath
$sourceAbs = Resolve-AbsolutePath $scriptDir $SourceHtml
$targetAbs = Resolve-AbsolutePath $repoAbs $TargetIndex

if (-not (Test-Path $sourceAbs)) {
  throw "Source HTML not found: $sourceAbs"
}

if (-not (Test-Path $repoAbs)) {
  throw "Repo path not found: $repoAbs"
}

$targetDir = Split-Path -Parent $targetAbs
if (-not (Test-Path $targetDir)) {
  New-Item -ItemType Directory -Path $targetDir | Out-Null
}

Copy-Item -Path $sourceAbs -Destination $targetAbs -Force
Write-Host "Copied:`n  $sourceAbs`n-> $targetAbs" -ForegroundColor Green

Push-Location $repoAbs
try {
  $isGitRepo = $false
  try {
    git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -eq 0) { $isGitRepo = $true }
  } catch {}

  if (-not $isGitRepo) {
    Write-Host "Not a git repo at $repoAbs. Copy complete (no commit/push)." -ForegroundColor Yellow
    return
  }

  git add -- $TargetIndex
  Assert-LastExitCode "git add"

  $hasChanges = $false
  git diff --cached --quiet
  if ($LASTEXITCODE -ne 0) { $hasChanges = $true }

  if (-not $hasChanges) {
    Write-Host "No staged changes to commit." -ForegroundColor Yellow
    return
  }

  if (-not $CommitMessage) {
    $CommitMessage = "Update calculator deploy " + (Get-Date -Format "yyyy-MM-dd HH:mm")
  }

  git commit -m $CommitMessage
  Assert-LastExitCode "git commit"

  if ($NoPush) {
    Write-Host "Committed (push skipped due to -NoPush)." -ForegroundColor Yellow
  }
  elseif ($Push) {
    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    git push -u origin $branch
    Assert-LastExitCode "git push"
    Write-Host "Push complete." -ForegroundColor Green
  }
  else {
    Write-Host "Committed locally only (safe default). To publish to GitHub: run again with -Push, or use deploy_one_click.bat" -ForegroundColor Yellow
  }
}
finally {
  Pop-Location
}
