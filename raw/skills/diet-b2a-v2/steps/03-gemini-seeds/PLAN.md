# step-03 · Gemini 시드 생성 (10장)

## 목적
5세트 각각 모델(model/N.png) + 배경(bg_png/bgN.png) 2장을 Gemini에 업로드해 **before(뚱뚱/방어지러움/밤)**, **after(마름/정돈/낮)** 시드 이미지를 생성.

## 입력
- `../01-styles-prompts/styles.json`
- `../../model/1..5.png`
- `../../v2/bg_png/bg1..5.png`
- `.session` (step-02 완료)

## 출력
- `../../seeds/set1..5/before.png` (뚱뚱+어지러움+밤)
- `../../seeds/set1..5/after.png`  (마름+정돈+낮)

## 실행
```bash
python gen_seeds.py --only set3     # 특정 세트만
python gen_seeds.py                 # 전체
```

## 프롬프트 템플릿
### before (뚱뚱)
```
Photo 1 is the model. Photo 2 is the reference room.
Create a realistic photo of this exact model but now looking about {kg_before} kg overweight/chubby (round face, fuller body, loose clothing), standing inside the EXACT same room from Photo 2.
The room is in a messy state: unmade bed with wrinkled blankets, clothes scattered on floor, random items, dim warm night lamp light, window dark (night time).
Full body vertical 9:16 portrait, model standing in the center of the room, looking slightly tired/self-conscious.
Do NOT change the room architecture. Keep the same walls, furniture layout, floor.
```
### after (마름)
```
Photo 1 is the original model. Photo 2 is the target reference image (the before version).
Create the same model but now transformed: slim and toned ~{kg_after} kg body (slender arms, visible abs, fitted crop top and denim shorts), standing in the SAME pose in the SAME room as Photo 2.
Now the room is perfectly tidy: neatly made bed, everything organized, bright morning sunlight coming through a clean window (day time), fresh atmosphere.
This is the DRAMATIC AFTER transformation.
Full body vertical 9:16 portrait.
Keep the same room architecture. Change only: the body shape, outfit, room tidiness, and lighting (night→day).
```

## 검증
- 10장 파일 존재, 각 > 100KB
- 해상도 ≥ 720×1280
- before/after 각각 얼굴 하나만 보여야 함
