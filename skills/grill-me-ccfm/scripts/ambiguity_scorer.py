#!/usr/bin/env python3
"""
ambiguity_scorer.py
사용자 입력의 모호도를 자동 측정하여 grill-me-ccfm 발동 여부 결정.

사용법:
    python ambiguity_scorer.py "자동화 만들어줘"
    → {"score": 8, "trigger_grill": true, "mode_hint": "coding", ...}

    또는 bob 스킬 내부에서 import:
    from ambiguity_scorer import score_input
    result = score_input(user_text)
"""

import sys
import json
import re
from typing import Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ─────────────────────────────────────────────────────
# 점수 측정 규칙
# ─────────────────────────────────────────────────────

VAGUE_TERMS = [
    "대충", "알아서", "비슷하게", "그냥", "좀", "어떻게든",
    "적당히", "보통", "일반적인", "그런 느낌",
]

FORCE_TRIGGERS = [
    "grill", "캐물어", "꼼꼼하게", "확실히 정리",
    "방향성 잡아줘", "하지 말아야 할 거",
    "컨셉 잡기 전", "본격적으로 만들기 전",
]

# 강제 발동 키워드 (점수 무시, 무조건 grill)
HARD_TRIGGERS = [
    # 전략 - 되돌리기 어려움
    "M&A", "매각", "인수", "클로징", "스마일게이트",
    "조직개편", "인사이동", "해고", "감원",
    
    # 신규 진출
    "신제품 출시", "신규 시장", "신규 브랜드",
    "대만 진출", "동남아 진출", "해외 진출",
    
    # 개인 - 되돌리기 어려움
    "출산", "산후", "육아", "신생아",
]

CCFM_DOMAIN_KEYWORDS = {
    "brand": ["메라블", "merable", "루솔브", "rusolve", "부위부위"],
    "channel": ["네이버", "쿠팡", "메타", "인스타", "릴스", "쇼츠", "유튜브", "틱톡"],
    "market": ["한국", "대만", "동남아", "인도네시아", "베트남", "태국"],
    "tool": ["claude code", "bob", "dd", "harness", "eval", "ffmpeg", "kling", "fal.ai", "gemini"],
}

# 콘텐츠 모드 시그널
CONTENT_SIGNALS = [
    "영상", "이미지", "릴스", "쇼츠", "광고", "DA", "콘텐츠",
    "카피", "스크립트", "콘티", "썸네일", "포스터", "배너",
    "레퍼런스", "씬", "컷", "자막",
]

CODING_SIGNALS = [
    "코드", "스크립트", "자동화", "스킬", "function", "API",
    "파이프라인", "크롤링", "파싱", "DB", "서버",
]

STRATEGY_SIGNALS = [
    "전략", "결정", "선택", "방향", "비교", "옵션",
    "계약", "협상", "리스크", "ROI", "예산",
]

PERSONAL_SIGNALS = [
    "출산", "임신", "아이", "와이프", "산후", "육아",
    "러닝", "운동", "건강", "약", "병원",
]


def detect_mode(text: str) -> str:
    """입력 텍스트에서 모드 추정"""
    text_lower = text.lower()
    
    scores = {
        "content": sum(1 for s in CONTENT_SIGNALS if s in text_lower),
        "coding": sum(1 for s in CODING_SIGNALS if s in text_lower),
        "strategy": sum(1 for s in STRATEGY_SIGNALS if s in text_lower),
        "personal": sum(1 for s in PERSONAL_SIGNALS if s in text_lower),
    }
    
    if max(scores.values()) == 0:
        return "unknown"
    
    return max(scores, key=scores.get)


def count_decision_branches(text: str) -> int:
    """결정 트리 분기 개수 추정 (단순 휴리스틱)"""
    branches = 0
    # "또는", "vs", "혹은", "/" 같은 선택 표현
    branches += len(re.findall(r"\b(또는|혹은|vs|VS)\b", text))
    branches += text.count(" / ")
    # 의문형 표현
    branches += len(re.findall(r"\?", text))
    # 미정 표현
    branches += sum(1 for w in ["고민", "선택", "어떤", "어느", "뭘"] if w in text)
    return branches


def check_ccfm_context(text: str) -> Dict[str, bool]:
    """CCFM 핵심 도메인 키워드가 명시됐는지 체크"""
    text_lower = text.lower()
    return {
        category: any(kw.lower() in text_lower for kw in keywords)
        for category, keywords in CCFM_DOMAIN_KEYWORDS.items()
    }


def score_input(text: str) -> Dict:
    """
    사용자 입력 모호도 점수 측정.
    
    Returns:
        {
            "score": int,
            "trigger_grill": bool,
            "mode_hint": str,
            "reasons": List[str],
            "hard_triggered": bool
        }
    """
    score = 0
    reasons = []
    
    # 1. 강제 발동 키워드 체크 (최우선)
    hard_triggered = any(t.lower() in text.lower() for t in HARD_TRIGGERS)
    if hard_triggered:
        return {
            "score": 999,
            "trigger_grill": True,
            "mode_hint": detect_mode(text),
            "reasons": ["⭐ 강제 발동 키워드 감지 (M&A/출산/신규시장 등 되돌리기 어려운 결정)"],
            "hard_triggered": True,
        }
    
    # 2. 명시적 grill 요청 (5점)
    if any(t in text.lower() for t in FORCE_TRIGGERS):
        score += 5
        reasons.append("명시적 grill 요청 키워드 (+5)")
    
    # 3. 입력 길이 (단계별 가중치)
    text_len = len(text.strip())
    if text_len < 20:
        score += 5
        reasons.append(f"매우 짧은 입력 {text_len}자 < 20 (+5)")
    elif text_len < 50:
        score += 3
        reasons.append(f"짧은 입력 {text_len}자 < 50 (+3)")
    
    # 4. 모호한 표현 (+3)
    vague_count = sum(1 for v in VAGUE_TERMS if v in text)
    if vague_count > 0:
        score += 3
        reasons.append(f"모호한 표현 {vague_count}개 ({', '.join(v for v in VAGUE_TERMS if v in text)}) (+3)")
    
    # 5. 결정 트리 분기 (≥5개 시 +2)
    branches = count_decision_branches(text)
    if branches >= 5:
        score += 2
        reasons.append(f"결정 분기 {branches}개 ≥ 5 (+2)")
    
    # 6. CCFM 컨텍스트 누락 (+2)
    context = check_ccfm_context(text)
    missing = [k for k, v in context.items() if not v]
    mode = detect_mode(text)
    
    # 콘텐츠/전략 모드인데 brand/channel/market 누락
    if mode in ("content", "strategy"):
        critical_missing = [k for k in ["brand", "channel", "market"] if k in missing]
        if len(critical_missing) >= 2:
            score += 2
            reasons.append(f"CCFM 핵심 컨텍스트 누락: {critical_missing} (+2)")
    
    # 7. 콘텐츠 모드는 Don't List 합의가 필수 → 기본 가중치 +2
    if mode == "content":
        # Don't List 관련 키워드가 명시적으로 있으면 면제
        dont_keywords = ["하지 말", "금지", "피하", "제외", "안 되는", "안되는", "regulation", "규제"]
        if not any(k in text.lower() for k in dont_keywords):
            score += 2
            reasons.append("콘텐츠 모드인데 Don't List/규제 언급 없음 (+2)")
    
    return {
        "score": score,
        "trigger_grill": score >= 5,
        "mode_hint": mode,
        "reasons": reasons,
        "hard_triggered": False,
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "사용법: python ambiguity_scorer.py \"사용자 입력 텍스트\""
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    result = score_input(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
