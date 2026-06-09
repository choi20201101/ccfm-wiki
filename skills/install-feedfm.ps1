#requires -Version 5.1
<#
.SYNOPSIS
  ccfm-wiki/skills/feedfm  →  ~/.claude/skills/feedfm
  복사 또는 심볼릭 링크. Claude Code + Claude Desktop 양쪽이 동일 경로에서 자동 로드.

.DESCRIPTION
  글로벌 부트스트랩. 새 컴퓨터에서 ccfm-wiki 를 git clone 한 직후 한 번만 실행:
    cd <wiki-clone>\skills
    .\install-feedfm.ps1            # 복사 모드 (기본, 안전)
    .\install-feedfm.ps1 -Symlink   # 심볼릭 링크 (위키 pull 시 자동 반영, 관리자/개발자 모드 필요)
  이미 설치돼 있으면 백업 후 덮어쓴다. -DryRun 으로 사전 확인 가능.
#>
param(
    [switch]$Symlink,
    [switch]$DryRun,
    [string]$ClaudeHome = (Join-Path $env:USERPROFILE ".claude")
)
$ErrorActionPreference = "Stop"

$srcRoot  = Split-Path -Parent $PSCommandPath          # ccfm-wiki/skills/
$srcSkill = Join-Path $srcRoot "feedfm"
if (-not (Test-Path $srcSkill)) {
    Write-Host "ERROR: 원본 스킬 미발견: $srcSkill" -ForegroundColor Red
    Write-Host "       ccfm-wiki/skills/install-feedfm.ps1 위치에서 실행하세요." -ForegroundColor Red
    exit 1
}
$dstSkillsDir = Join-Path $ClaudeHome "skills"
$dstSkill     = Join-Path $dstSkillsDir "feedfm"

Write-Host ""
Write-Host "feedfm 글로벌 설치" -ForegroundColor Cyan
Write-Host "  원본: $srcSkill" -ForegroundColor Gray
Write-Host "  대상: $dstSkill" -ForegroundColor Gray
Write-Host "  모드: $(if($Symlink){'symlink'}else{'copy'})$(if($DryRun){' (DRY RUN)'})" -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path $ClaudeHome)) {
    Write-Host "ERROR: Claude 설정 폴더 없음: $ClaudeHome" -ForegroundColor Red
    Write-Host "       Claude Code 또는 Desktop 을 먼저 한 번 실행하세요." -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $dstSkillsDir)) {
    if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $dstSkillsDir | Out-Null }
    Write-Host "  + skills 폴더 생성: $dstSkillsDir" -ForegroundColor Green
}
if (Test-Path $dstSkill) {
    $backup = "$dstSkill.bak"
    Write-Host "  ! 기존 설치 발견 → 백업: $backup" -ForegroundColor Yellow
    if (-not $DryRun) {
        if (Test-Path $backup) { Remove-Item -Recurse -Force $backup }
        Move-Item $dstSkill $backup
    }
}
if ($DryRun) { Write-Host "DRY RUN 종료 (실제 변경 없음)" -ForegroundColor Cyan; exit 0 }

if ($Symlink) {
    try {
        New-Item -ItemType SymbolicLink -Path $dstSkill -Target $srcSkill -Force | Out-Null
        Write-Host "  + 심볼릭 링크 생성 완료" -ForegroundColor Green
    } catch {
        Write-Host "  ! symlink 실패(권한?) → 복사 모드로 대체" -ForegroundColor Yellow
        Copy-Item -Recurse -Force $srcSkill $dstSkill
    }
} else {
    Copy-Item -Recurse -Force $srcSkill $dstSkill
    Write-Host "  + 복사 완료" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ feedfm 설치 완료 → /feedfm 으로 사용" -ForegroundColor Green
Write-Host "   사용: 진단 결과 텍스트 붙여넣고 '/feedfm'" -ForegroundColor Gray
Write-Host ""
