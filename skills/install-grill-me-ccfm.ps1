#requires -Version 5.1
<#
.SYNOPSIS
  ccfm-wiki/skills/grill-me-ccfm  →  ~/.claude/skills/grill-me-ccfm
  복사 또는 심볼릭 링크. Claude Code + Claude Desktop 양쪽이 동일 경로에서 자동 로드.

.DESCRIPTION
  글로벌 부트스트랩. 새 컴퓨터에서 ccfm-wiki를 git clone 한 직후 한 번만 실행:
    cd <wiki-clone>\skills
    .\install-grill-me-ccfm.ps1            # 복사 모드 (기본, 안전)
    .\install-grill-me-ccfm.ps1 -Symlink   # 심볼릭 링크 (위키 업데이트 시 자동 반영, 관리자 권한 필요)

  이미 설치돼 있으면 백업 후 덮어쓴다. -DryRun 으로 사전 확인 가능.

.PARAMETER Symlink
  심볼릭 링크 모드. git pull 시 자동으로 스킬도 업데이트됨.
  Windows 에서는 관리자 권한 또는 개발자 모드 필요.

.PARAMETER DryRun
  실제 변경 없이 계획만 출력.

.PARAMETER ClaudeHome
  ~/.claude 경로 오버라이드 (기본: $env:USERPROFILE\.claude)
#>
param(
    [switch]$Symlink,
    [switch]$DryRun,
    [string]$ClaudeHome = (Join-Path $env:USERPROFILE ".claude")
)

$ErrorActionPreference = "Stop"

# ─── 위치 자동 감지 ───────────────────────────────
$srcRoot = Split-Path -Parent $PSCommandPath              # ccfm-wiki/skills/
$srcSkill = Join-Path $srcRoot "grill-me-ccfm"
if (-not (Test-Path $srcSkill)) {
    Write-Host "ERROR: 원본 스킬 미발견: $srcSkill" -ForegroundColor Red
    Write-Host "       이 스크립트는 ccfm-wiki/skills/install-grill-me-ccfm.ps1 위치에서 실행돼야 함" -ForegroundColor Red
    exit 1
}

$dstSkillsDir = Join-Path $ClaudeHome "skills"
$dstSkill = Join-Path $dstSkillsDir "grill-me-ccfm"

Write-Host ""
Write-Host "grill-me-ccfm 글로벌 설치" -ForegroundColor Cyan
Write-Host "  원본: $srcSkill" -ForegroundColor Gray
Write-Host "  대상: $dstSkill" -ForegroundColor Gray
Write-Host "  모드: $(if($Symlink){'symlink'}else{'copy'})$(if($DryRun){' (DRY RUN)'})" -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path $ClaudeHome)) {
    Write-Host "ERROR: Claude 설정 폴더 없음: $ClaudeHome" -ForegroundColor Red
    Write-Host "       Claude Code 또는 Desktop을 먼저 한 번 실행하세요." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $dstSkillsDir)) {
    if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $dstSkillsDir | Out-Null }
    Write-Host "  + skills 폴더 생성: $dstSkillsDir" -ForegroundColor Green
}

# ─── 백업 ───────────────────────────────
if (Test-Path $dstSkill) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backup = "$dstSkill.bak-$stamp"
    if (-not $DryRun) {
        if ((Get-Item $dstSkill).LinkType) {
            Remove-Item $dstSkill -Force
            Write-Host "  - 기존 심볼릭 링크 제거" -ForegroundColor Yellow
        } else {
            Move-Item $dstSkill $backup -Force
            Write-Host "  ~ 기존 폴더 백업: $backup" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [DRY] 기존 항목 백업 예정: $backup" -ForegroundColor Magenta
    }
}

# ─── 설치 ───────────────────────────────
if ($Symlink) {
    if (-not $DryRun) {
        try {
            New-Item -ItemType SymbolicLink -Path $dstSkill -Target $srcSkill -ErrorAction Stop | Out-Null
            Write-Host "  + 심볼릭 링크 생성 완료" -ForegroundColor Green
        } catch {
            Write-Host "  ! 심볼릭 링크 실패 (관리자 권한 또는 개발자 모드 필요): $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "    복사 모드로 폴백..." -ForegroundColor Yellow
            Copy-Item $srcSkill $dstSkill -Recurse -Force
            Write-Host "  + 복사 완료" -ForegroundColor Green
        }
    } else {
        Write-Host "  [DRY] symlink 생성 예정" -ForegroundColor Magenta
    }
} else {
    if (-not $DryRun) {
        Copy-Item $srcSkill $dstSkill -Recurse -Force
        Write-Host "  + 복사 완료" -ForegroundColor Green
    } else {
        Write-Host "  [DRY] 복사 예정" -ForegroundColor Magenta
    }
}

# ─── 검증 ───────────────────────────────
Write-Host ""
if (-not $DryRun) {
    $check = @(
        (Join-Path $dstSkill "SKILL.md"),
        (Join-Path $dstSkill "scripts\ambiguity_scorer.py"),
        (Join-Path $dstSkill "schema\grill-result.schema.yaml")
    )
    $allOk = $true
    foreach ($f in $check) {
        if (Test-Path $f) {
            Write-Host "  OK $($f.Substring($dstSkill.Length+1))" -ForegroundColor Green
        } else {
            Write-Host "  MISSING $f" -ForegroundColor Red
            $allOk = $false
        }
    }
    Write-Host ""
    if ($allOk) {
        Write-Host "설치 완료. Claude Code 또는 Desktop 재시작 후 'grill해줘' 등으로 트리거." -ForegroundColor Green
    } else {
        Write-Host "일부 파일 누락. 위키 원본 상태 확인 필요." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "DRY RUN 완료. 실제 설치는 -DryRun 빼고 재실행." -ForegroundColor Magenta
}
