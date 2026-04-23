---
aliases: ["유튜브 수집"]
type: source
domain: content-ai-automation
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources: [C:\Users\Administrator\Desktop\market-research-package\modules\youtube]
---

# src: YouTube 대규모 수집·분석 모듈

## 위치
C:\Users\Administrator\Desktop\market-research-package\modules\youtube\

## 핵심 기능 (8단계 파이프라인)
1. 키워드 확장 (40여 종 접미사: 추천/후기/전후/팩트체크 등)
2. yt-dlp ytsearch 대량 수집 (수만~수십만 건, --flat-playlist)
3. enrich (좋아요/댓글수 보강 — flat-playlist는 빠짐)
4. 한글 비율 15%+ 필터
5. 자막 VTT 수집 (manual → auto fallback)
6. regex 분석 4종 (훅 7종 / 페인포인트 / 권위 / 통념)
7. 10만뷰+ 가중치 1~5배 (고성과 영상 우선)
8. Claude CLI 서브에이전트 4개 병렬 디스패치 → 인사이트 MD

## 수집 필드
| 분류 | 항목 | 비고 |
| --- | --- | --- |
| 메타 | title, description, view/like/comment count, channel, duration | yt-dlp 기본 |
| **자막** | manual subtitles (VTT) → auto fallback | 풀텍스트 |
| 영상 자체 | ❌ (메타·자막만) | |
| 댓글 본문 | ❌ (count만) | API 미사용 |

## 주요 파일
| 파일 | 역할 |
| --- | --- |
| run.py | 8단계 오케스트레이터 |
| core.py | 키워드 확장, 한글 필터, yt-dlp 래퍼 |
| transcript_collector.py | 자막 VTT 수집 (write-sub + write-auto-sub) |
| analyzer.py | view/like/comment 집계 + TOP10 |
| script_analyzer.py | 훅 7종 regex |
| painpoint_analyzer.py | 페인포인트(외모/대인/경제/불신) regex |
| authority_analyzer.py | 권위(의사/논문/수치/유명인) regex |
| bundle_builder.py | Claude 컨텍스트 150KB 안전 마진 번들러 |
| claude_dispatcher.py | claude.cmd 병렬 호출 (stdin 프롬프트) |
| hooks/ | pre-collect.sh, verify-output.sh |

## 의존성 / 환경
- yt-dlp 2024+
- Claude Code CLI (`claude.cmd` 로컬 설치)
- Python 3.x
- ❌ youtube-data-api (할당량 회피)

## 사용 예
```bash
py src/run.py "탈모"
```

## 알려진 제약
- 자막 없는 영상 다수 → 1000자 미만 필터로 분석 대상이 수집의 5~10%로 줄 수 있음
- yt-dlp 차단·IP 밴 가능 (rate limit 1.5~3초 필수)
- claude.cmd 의존 → 서버 자동화 어려움 (대안: Anthropic SDK)
- regex 패턴 사전이 뷰티/헬스(탈모/기미) 중심 — 타 도메인 확장 시 재튜닝
- YouTube ToS 회색지대

## 관련 도메인
- [[content-ai-automation]] (Claude 서브에이전트 병렬 디스패치 패턴)
- [[viral]] (훅/페인포인트/권위/통념 regex 사전 = 바이럴 원형)
- [[da-creative]] (퍼포먼스 광고 스크립트에 권위·증거·사회증거 삽입 기법)
