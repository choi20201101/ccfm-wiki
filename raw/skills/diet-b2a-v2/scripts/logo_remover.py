#!/usr/bin/env python3
"""
Gemini Logo Remover v3.0
━━━━━━━━━━━━━━━━━━━━━━━━
Gemini 생성 이미지의 ✦ 워터마크를 자동 제거하는 도구

방식: 하단 좌/우 코너를 고정 마스킹 + OpenCV Inpainting
- 로고 감지 없이 고정 위치를 인페인팅하여 100% 제거율
- TELEA + NS 알고리즘 블렌딩으로 자연스러운 복원
- 가우시안 블러 마스크로 경계 없는 부드러운 처리

지원 비율: 9:16(세로), 1:1(정사각형), 16:9(가로) 등 모든 비율
지원 포맷: PNG, JPG, JPEG, WEBP (알파 채널 보존)
처리 속도: ~0.5초/장

사용법:
  단일 파일:  python remove_logo.py image.png
  폴더 일괄:  python remove_logo.py ./input_folder/
  출력 지정:  python remove_logo.py ./input_folder/ ./output_folder/

의존성: pip install opencv-python numpy Pillow
"""

import cv2
import numpy as np
from PIL import Image
import os
import sys
import glob
import time


# ══════════════════════════════════════════════════════════════
# 설정 (필요시 조정)
# ══════════════════════════════════════════════════════════════

CORNER_W_RATIO = 0.09   # 코너 마스크 가로 크기 (이미지 대비 %)
CORNER_H_RATIO = 0.07   # 코너 마스크 세로 크기 (이미지 대비 %)
INPAINT_RADIUS = 15      # 인페인팅 반경 (클수록 넓게 참조)
BLUR_KERNEL = 31         # 경계 블렌딩 커널 (홀수, 클수록 부드러움)


# ══════════════════════════════════════════════════════════════
# 핵심 함수
# ══════════════════════════════════════════════════════════════

def make_corner_masks(h, w):
    """하단 좌/우 코너에 타원형 마스크 생성"""
    mask = np.zeros((h, w), dtype=np.uint8)
    cw = max(int(w * CORNER_W_RATIO), 40)
    ch = max(int(h * CORNER_H_RATIO), 40)

    # 우측하단
    cv2.ellipse(mask, (w - cw // 2, h - ch // 2), (cw, ch), 0, 0, 360, 255, -1)
    # 좌측하단
    cv2.ellipse(mask, (cw // 2, h - ch // 2), (cw, ch), 0, 0, 360, 255, -1)

    return mask


def remove_logo(img_bgr):
    """
    양쪽 하단 코너를 인페인팅하여 로고 제거

    1. TELEA 알고리즘: 빠른 행진 기반 (텍스처에 강함)
    2. NS 알고리즘: 나비에-스토크스 기반 (색상 연속성에 강함)
    3. 두 결과를 50:50 블렌딩
    4. 가우시안 블러 마스크로 원본과 부드럽게 합성
    """
    h, w = img_bgr.shape[:2]
    mask = make_corner_masks(h, w)

    r_telea = cv2.inpaint(img_bgr, mask, INPAINT_RADIUS, cv2.INPAINT_TELEA)
    r_ns = cv2.inpaint(img_bgr, mask, INPAINT_RADIUS, cv2.INPAINT_NS)
    inpainted = cv2.addWeighted(r_telea, 0.5, r_ns, 0.5, 0)

    # 경계 블렌딩
    blur_mask = cv2.GaussianBlur(mask.astype(np.float32), (BLUR_KERNEL, BLUR_KERNEL), 0)
    if blur_mask.max() > 0:
        blur_mask /= blur_mask.max()
    blend = blur_mask[:, :, np.newaxis]

    return (inpainted * blend + img_bgr * (1 - blend)).astype(np.uint8)


# ══════════════════════════════════════════════════════════════
# 파이프라인
# ══════════════════════════════════════════════════════════════

def process_image(input_path, output_path):
    """단일 이미지 처리"""
    img_pil = Image.open(input_path)
    has_alpha = img_pil.mode == 'RGBA'
    alpha = np.array(img_pil)[:, :, 3] if has_alpha else None
    img_bgr = cv2.cvtColor(np.array(img_pil.convert('RGB')), cv2.COLOR_RGB2BGR)

    result_bgr = remove_logo(img_bgr)

    result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)
    if has_alpha and alpha is not None:
        out_pil = Image.fromarray(np.dstack([result_rgb, alpha]), 'RGBA')
    else:
        out_pil = Image.fromarray(result_rgb, 'RGB')

    out_pil.save(output_path, quality=95)
    return True


def batch_process(input_dir, output_dir):
    """폴더 내 이미지 일괄 처리"""
    os.makedirs(output_dir, exist_ok=True)

    files = []
    for ext in ('*.png', '*.jpg', '*.jpeg', '*.webp'):
        files.extend(glob.glob(os.path.join(input_dir, ext)))

    if not files:
        print("[!] no images found")
        return

    print(f"[*] {len(files)} images")
    print("-" * 40)

    t_start = time.time()
    for f in sorted(files):
        fname = os.path.basename(f)
        out = os.path.join(output_dir, fname)
        t0 = time.time()
        process_image(f, out)
        elapsed = time.time() - t0
        print(f"  [{elapsed:.1f}s] {fname}")

    total = time.time() - t_start
    print("-" * 40)
    print(f"[*] done: {len(files)} images in {total:.1f}s")
    print(f"[*] output: {output_dir}")


# ══════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gemini Logo Remover v3.0")
        print("-" * 40)
        print("Usage:")
        print("  single:  python remove_logo.py image.png")
        print("  batch:   python remove_logo.py ./input_folder/")
        print("  output:  python remove_logo.py ./input_folder/ ./output_folder/")
        print()
        print("Supported: PNG, JPG, JPEG, WEBP")
        print("Ratios:    9:16, 1:1, 16:9, etc.")
        sys.exit(0)

    target = sys.argv[1]

    if os.path.isdir(target):
        output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(target, "output")
        batch_process(target, output_dir)

    elif os.path.isfile(target):
        if len(sys.argv) > 2:
            output_path = sys.argv[2]
        else:
            base, ext = os.path.splitext(target)
            output_path = f"{base}_clean{ext}"

        print(f"[*] {os.path.basename(target)}")
        t0 = time.time()
        process_image(target, output_path)
        print(f"  [{time.time() - t0:.1f}s] saved: {output_path}")

    else:
        print(f"[!] not found: {target}")
        sys.exit(1)
