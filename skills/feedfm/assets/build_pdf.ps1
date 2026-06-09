#requires -Version 5.1
<#
.SYNOPSIS
  feedfm HTML → PDF 변환 + 1페이지 자동 핏.
  Edge headless 로 인쇄, PDF 페이지 수가 1이 될 때까지 .sheet zoom 을 0.02씩 낮춰 재시도.

.USAGE
  .\build_pdf.ps1 -Html "C:\...\OOO_퍼포먼스캔버스_피드백.html"
  결과: 같은 폴더에 동일 이름 .pdf 생성, 콘솔에 최종 zoom·페이지 수 출력.

.NOTE
  - Python + pymupdf(fitz) 있으면 페이지 수 검증, 없으면 검증 생략(1회 변환만).
  - zoom 하한 0.60 (그 아래는 가독성 저하 → 내용 줄이라고 경고).
#>
param(
    [Parameter(Mandatory=$true)][string]$Html,
    [double]$StartZoom = 0.71,
    [double]$MinZoom   = 0.60
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path $Html)) { Write-Host "ERROR: HTML 없음: $Html" -ForegroundColor Red; exit 1 }
$Html = (Resolve-Path $Html).Path
$Pdf  = [IO.Path]::ChangeExtension($Html, ".pdf")

$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edge)) { $edge = "C:\Program Files\Microsoft\Edge\Application\msedge.exe" }
if (-not (Test-Path $edge)) { Write-Host "ERROR: Edge 미발견" -ForegroundColor Red; exit 1 }

$py = (Get-Command python -ErrorAction SilentlyContinue)
$canCheck = $false
if ($py) { try { python -c "import fitz" 2>$null; if ($LASTEXITCODE -eq 0) { $canCheck = $true } } catch {} }

function Set-Zoom([double]$z) {
    $raw = Get-Content -Raw -Encoding UTF8 $Html
    $new = [regex]::Replace($raw, 'zoom:\.?\d+(\.\d+)?;', ("zoom:{0};" -f $z))
    Set-Content -Encoding UTF8 -NoNewline -Path $Html -Value $new
}
function Convert-Once {
    if (Test-Path $Pdf) { Remove-Item $Pdf -Force }
    $uri = "file:///" + ($Html -replace '\\','/')
    # Start-Process: native exe stderr 가 5.1 에서 종료성 에러로 승격되는 것을 회피
    $args = @("--headless","--disable-gpu","--no-pdf-header-footer","--print-to-pdf=$Pdf",$uri)
    Start-Process -FilePath $edge -ArgumentList $args -Wait -WindowStyle Hidden
    Start-Sleep -Seconds 2
}
function Get-Pages {
    if (-not $canCheck) { return 1 }
    $n = python -c "import fitz,sys; print(len(fitz.open(sys.argv[1])))" "$Pdf" 2>$null
    return [int]$n
}

$z = $StartZoom
while ($true) {
    Set-Zoom $z
    Convert-Once
    $pages = Get-Pages
    Write-Host ("  zoom={0:N2}  pages={1}" -f $z, $pages) -ForegroundColor Gray
    if ($pages -le 1 -or -not $canCheck) {
        Write-Host ("OK → {0}  (zoom {1:N2}, {2}p)" -f $Pdf, $z, $pages) -ForegroundColor Green
        break
    }
    $z = [math]::Round($z - 0.02, 2)
    if ($z -lt $MinZoom) {
        Write-Host ("WARN: zoom {0:N2}에서도 1페이지 초과. 내용을 줄이거나 2페이지 허용 권장." -f $MinZoom) -ForegroundColor Yellow
        break
    }
}
