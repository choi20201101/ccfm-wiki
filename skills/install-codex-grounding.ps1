#requires -Version 5.1
<#
.SYNOPSIS
  ccfm-wiki/skills/codex-grounding -> 3-CLI dotfile 통합 설치
  Codex/Claude/Gemini 가 호출될 때 개인 메모리·위키 인덱스를 자동 grounding 하도록
  PRE-WORK PROTOCOL 을 dotfile 에 주입하고 헬퍼 스크립트를 배포.

.DESCRIPTION
  새 컴퓨터에서 ccfm-wiki 를 git clone 한 직후 한 번만 실행:
    cd <wiki-clone>\skills
    .\install-codex-grounding.ps1            # 기본: marker 사이만 갱신, idempotent
    .\install-codex-grounding.ps1 -DryRun    # 실제 변경 없이 계획만 출력
    .\install-codex-grounding.ps1 -Uninstall # marker 사이를 제거 (헬퍼는 유지)
#>
param(
    [switch]$DryRun,
    [switch]$Uninstall,
    [string]$ClaudeHome = (Join-Path $env:USERPROFILE ".claude"),
    [string]$CodexHome  = (Join-Path $env:USERPROFILE ".codex"),
    [string]$GeminiHome = (Join-Path $env:USERPROFILE ".gemini"),
    [string]$WikiRoot   = $null
)

$ErrorActionPreference = "Stop"
$BeginMarker = "<!-- BEGIN: codex-grounding-protocol v1 -->"
$EndMarker   = "<!-- END: codex-grounding-protocol v1 -->"

# Source detection
$srcRoot = Split-Path -Parent $PSCommandPath
if (-not $WikiRoot) {
    $WikiRoot = Split-Path -Parent $srcRoot
}
$srcSkill  = Join-Path $srcRoot "codex-grounding"
$srcHelper = Join-Path $srcSkill "context-bootstrap.mjs"
$srcAgents = Join-Path $srcSkill "AGENTS-protocol.md"
$srcClaude = Join-Path $srcSkill "CLAUDE-protocol.md"
$srcGemini = Join-Path $srcSkill "GEMINI-protocol.md"

foreach ($f in @($srcHelper, $srcAgents, $srcClaude, $srcGemini)) {
    if (-not (Test-Path $f)) {
        Write-Host ("ERROR: source missing: {0}" -f $f) -ForegroundColor Red
        exit 1
    }
}

$dstHelper = Join-Path $CodexHome "scripts\context-bootstrap.mjs"
$dstAgents = Join-Path $CodexHome "AGENTS.md"
$dstClaude = Join-Path $ClaudeHome "CLAUDE.md"
$dstGemini = Join-Path $GeminiHome "GEMINI.md"

Write-Host ""
Write-Host "codex-grounding install" -ForegroundColor Cyan
Write-Host ("  WikiRoot   : {0}" -f $WikiRoot) -ForegroundColor Gray
Write-Host ("  ClaudeHome : {0}" -f $ClaudeHome) -ForegroundColor Gray
Write-Host ("  CodexHome  : {0}" -f $CodexHome) -ForegroundColor Gray
Write-Host ("  GeminiHome : {0}" -f $GeminiHome) -ForegroundColor Gray
$mode = "INSTALL"
if ($Uninstall) { $mode = "UNINSTALL" }
if ($DryRun)    { $mode = $mode + " (DRY RUN)" }
Write-Host ("  Mode       : {0}" -f $mode) -ForegroundColor Yellow
Write-Host ""

function Ensure-Dir($p) {
    if (-not (Test-Path $p)) {
        if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $p | Out-Null }
        Write-Host ("  + dir: {0}" -f $p) -ForegroundColor Green
    }
}

function Backup-File($p) {
    if (Test-Path $p) {
        $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $bak = ($p + ".bak-" + $stamp)
        if (-not $DryRun) { Copy-Item $p $bak -Force }
        Write-Host ("  ~ backup: {0}" -f $bak) -ForegroundColor DarkGray
    }
}

function Save-Utf8($path, $text) {
    Ensure-Dir (Split-Path -Parent $path)
    $utf8WithBom = New-Object System.Text.UTF8Encoding($true)
    [System.IO.File]::WriteAllText($path, $text, $utf8WithBom)
}

function Update-MarkerSection {
    param(
        [string]$Target,
        [string]$Body,
        [string]$Label,
        [switch]$RemoveOnly
    )
    $existing = ""
    if (Test-Path $Target) {
        $existing = Get-Content -Raw -LiteralPath $Target -Encoding UTF8
        if ($null -eq $existing) { $existing = "" }
    }

    $beginIdx = $existing.IndexOf($BeginMarker)
    $endIdx   = $existing.IndexOf($EndMarker)
    $hasBlock = ($beginIdx -ge 0 -and $endIdx -gt $beginIdx)

    if ($RemoveOnly) {
        if (-not $hasBlock) {
            Write-Host ("  - {0}: marker not found, skip" -f $Label) -ForegroundColor DarkGray
            return
        }
        $afterEnd = $endIdx + $EndMarker.Length
        # eat optional trailing newline
        if ($afterEnd -lt $existing.Length -and $existing[$afterEnd] -eq "`n") { $afterEnd++ }
        elseif ($afterEnd + 1 -lt $existing.Length -and $existing.Substring($afterEnd, 2) -eq "`r`n") { $afterEnd += 2 }
        $head = $existing.Substring(0, $beginIdx)
        $tail = $existing.Substring($afterEnd)
        $updated = $head + $tail
        if (-not $DryRun) {
            Backup-File $Target
            Save-Utf8 $Target $updated
        }
        Write-Host ("  - {0}: marker block removed" -f $Label) -ForegroundColor Yellow
        return
    }

    if ($hasBlock) {
        $afterEnd = $endIdx + $EndMarker.Length
        $head = $existing.Substring(0, $beginIdx)
        $tail = $existing.Substring($afterEnd)
        $updated = $head + $Body.TrimEnd() + $tail
    }
    elseif ($existing.Length -gt 0) {
        # Insert near the top, preserving any first-line H1 header.
        $nlIdx = $existing.IndexOf("`n")
        $firstLine = ""
        $rest = $existing
        if ($nlIdx -ge 0) {
            $firstLine = $existing.Substring(0, $nlIdx + 1)
            $rest = $existing.Substring($nlIdx + 1)
        }
        if ($firstLine -match "^#\s+\S") {
            $updated = $firstLine + "`r`n" + $Body.TrimEnd() + "`r`n`r`n" + $rest
        } else {
            $updated = $Body.TrimEnd() + "`r`n`r`n" + $existing
        }
    }
    else {
        $updated = $Body.TrimEnd() + "`r`n"
    }

    if (-not $DryRun) {
        Backup-File $Target
        Save-Utf8 $Target $updated
    }
    Write-Host ("  + {0}: marker block written ({1})" -f $Label, $Target) -ForegroundColor Green
}

# Run
Ensure-Dir $CodexHome
Ensure-Dir (Join-Path $CodexHome "scripts")
Ensure-Dir $ClaudeHome
Ensure-Dir $GeminiHome

if ($Uninstall) {
    Update-MarkerSection -Target $dstAgents -Body "" -Label "AGENTS.md" -RemoveOnly
    Update-MarkerSection -Target $dstClaude -Body "" -Label "CLAUDE.md" -RemoveOnly
    Update-MarkerSection -Target $dstGemini -Body "" -Label "GEMINI.md" -RemoveOnly
    Write-Host ""
    Write-Host ("Uninstall done. Helper kept at: {0}" -f $dstHelper) -ForegroundColor Yellow
    Write-Host ("  remove helper: Remove-Item '{0}'" -f $dstHelper) -ForegroundColor DarkGray
    exit 0
}

# Copy helper script
if (-not $DryRun) { Copy-Item $srcHelper $dstHelper -Force }
Write-Host ("  + helper: {0}" -f $dstHelper) -ForegroundColor Green

# Inject protocol markers
$agentsBody = Get-Content -Raw -LiteralPath $srcAgents -Encoding UTF8
$claudeBody = Get-Content -Raw -LiteralPath $srcClaude -Encoding UTF8
$geminiBody = Get-Content -Raw -LiteralPath $srcGemini -Encoding UTF8

Update-MarkerSection -Target $dstAgents -Body $agentsBody -Label "AGENTS.md"
Update-MarkerSection -Target $dstClaude -Body $claudeBody -Label "CLAUDE.md"
Update-MarkerSection -Target $dstGemini -Body $geminiBody -Label "GEMINI.md"

Write-Host ""
if (-not $DryRun) {
    $allOk = $true
    $checks = @(
        @{Path = $dstHelper; Label = "helper script"},
        @{Path = $dstAgents; Label = "AGENTS.md"},
        @{Path = $dstClaude; Label = "CLAUDE.md"},
        @{Path = $dstGemini; Label = "GEMINI.md"}
    )
    foreach ($c in $checks) {
        if (Test-Path $c.Path) {
            Write-Host ("  OK {0}: {1}" -f $c.Label, $c.Path) -ForegroundColor Green
        } else {
            Write-Host ("  MISSING {0}: {1}" -f $c.Label, $c.Path) -ForegroundColor Red
            $allOk = $false
        }
    }
    Write-Host ""
    if ($allOk) {
        Write-Host "install completed." -ForegroundColor Green
        Write-Host ""
        Write-Host "Verify helper:" -ForegroundColor Cyan
        Write-Host ("  node `"{0}`" `"test prompt`" --verbose" -f $dstHelper) -ForegroundColor Gray
        Write-Host ""
        Write-Host "If wiki/memory paths differ on this PC, add to ~/.codex/AGENTS.local.md:" -ForegroundColor Cyan
        Write-Host ("  CCFM_WIKI_ROOT={0}" -f $WikiRoot) -ForegroundColor Gray
    } else {
        Write-Host "Some files missing. Check wiki source state." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "DRY RUN done. Re-run without -DryRun to apply." -ForegroundColor Magenta
}
