# [규칙] After Effects .aep 자동 빌드 기본 버전 = 25.0

**소속 도메인 후보**: `wiki/tacit/coding-lessons.md` 새 § 또는 `wiki/domains/performance-ad.md` 또는 `wiki/domains/ai-automation.md`
**confidence**: high (사용자 직접 명시 + 검증된 빌드 패턴)
**source**: 2026-05-03 율이 EP02 광고 직원 인계 패키지 빌드 (Administrator PC)
**triggered by**: 사용자 명시 — "환경에 따라 차이가 있어서 25.0 버전을 기본으로 만들도록"

---

## 규칙 한 줄

광고/영상 자동화 산출물 중 **`.aep` 파일을 자동 생성할 때 AE 25.0을 기본 버전으로 사용**한다. 현장 직원 PC 호환성이 가장 넓다.

## Why

Adobe After Effects는 **상위 버전에서 만든 `.aep`를 하위 버전에서 열지 못한다** (binary format이 버전마다 변경). 즉:

- 26.0(2026)으로 빌드 → 25.0/24.0 직원 PC: ❌ "지원하지 않는 프로젝트 버전"
- 25.0(2025)으로 빌드 → 25.0 PC: ✅, 26.0 PC: ✅ (상위 호환은 보통 됨)

직원마다 PC AE 버전이 제각각이므로 **가장 넓은 호환성**을 갖는 25.0 (현재 안정 LTS) 으로 통일하는 게 인계 마찰 0.

## 빌드 명령

```bash
# Windows (Administrator PC 기준)
"/c/Program Files/Adobe/Adobe After Effects 2025/Support Files/AfterFX.exe" \
    -r "C:/path/to/build_aep.jsx"
```

- `-r <jsx>`: 시작 시 스크립트 자동 실행. AE GUI는 뜨지만 jsx에서 `app.quit()` 호출하면 자동 종료
- 시작~파일 생성: 15-30초

## 검증된 jsx 빌드 템플릿

```jsx
(function() {
    try {
        // 빈 프로젝트로 시작
        if (app.project) {
            try { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (e) {}
        }
        app.newProject();

        // 컴포지션
        var comp = app.project.items.addComp("name", 1080, 1920, 1.0, 50.0, 30);
        comp.bgColor = [0, 0, 0];

        // footage import + layer 배치
        var imported = app.project.importFile(new ImportOptions(new File(absolutePath)));
        var layer = comp.layers.add(imported);
        layer.startTime = 0;
        layer.outPoint = 5.0;
        layer.transform.position.setValue([1080/2, 656 + 608/2]);
        layer.transform.scale.setValue([84.375, 84.375]);

        // 텍스트 레이어 (한국어 = MalgunGothic-Bold)
        var t = comp.layers.addText("내용");
        var src = t.property("Source Text").value;
        src.font = "MalgunGothic-Bold";
        src.fontSize = 54;
        src.fillColor = [1, 0.831, 0];      // #FFD400 yellow
        src.justification = ParagraphJustification.CENTER_JUSTIFY;
        src.applyStroke = true;
        src.strokeColor = [0, 0, 0];
        src.strokeWidth = 3;
        t.property("Source Text").setValue(src);

        // 저장 + 종료
        app.project.save(new File("path/file_AE25.aep"));
        app.quit();
    } catch (e) {
        // GUI alert 쓰지 말 것 — 자동 종료 막힘
        var logF = new File("path/error.log");
        logF.open("w"); logF.write("Error: " + e.toString()); logF.close();
        app.quit();
    }
})();
```

## 함정 4선 (모두 율이 EP02 빌드에서 직접 검증)

| # | 함정 | 회피 |
|---|---|---|
| 1 | `alert()` → GUI 다이얼로그 → 자동 종료 막힘 | try/catch로 감싸고 에러는 .log 파일로 기록 |
| 2 | footage 절대 경로 박힘 → 다른 PC에서 missing | 패키지 폴더 그대로 옮기게 README에 명시. 같은 path면 OK |
| 3 | AE가 footage 파일 lock → zip 압축 실패 | 빌드 후 `Stop-Process -Name 'AfterFX*' -Force` 후 zip |
| 4 | 컴포지션 자동 open 안 됨 → 직원이 "비어 보임" 오해 | README에 "Project 패널 컴포지션 더블클릭" 명시 |

## 진단 jsx 패턴

빌드 후 검증용. 컴포지션·layer·footage 상태를 텍스트 dump:

```jsx
app.open(new File(aepPath));
var log = "Items: " + app.project.numItems + "\n";
for (var i = 1; i <= app.project.numItems; i++) {
    var item = app.project.item(i);
    if (item instanceof CompItem) {
        log += "comp: " + item.numLayers + " layers, "
            + item.duration + "s @ " + item.frameRate + "fps\n";
    } else if (item instanceof FootageItem) {
        var src = item.mainSource;
        log += "footage: " + (src.file ? src.file.fsName : "?")
            + " (missing=" + item.footageMissing + ")\n";
    }
}
var f = new File(logPath); f.open("w"); f.write(log); f.close();
app.quit();
```

## 검증 사례

**2026-05-03 율이 EP02 50초 광고 직원 인계 패키지**:
- `Desktop/율이_레이저전_50s_v08_directorpkg.zip` (106MB)
- 내부 `07_project/yuri_ep02_v08_AE25.aep` (542KB)
- 컴포지션: 1080×1920, 50초, 30fps, 28 layers (영상 7 + 텍스트 21)
- footage missing=0건
- 직원 AE 25.0/26.0 어느 쪽에서도 호환

## 연계 규칙

- `feedback_image_gen_backend_priority.md` — 이미지 백엔드 우선순위
- `feedback_lipsync_multi_face_trap.md` — lipsync PIP 함정
- `yuri-ep02-8iter-success-case-2026-05-03.md` — 8회 iteration 성공 사례 종합

## ingest 작업 (gguy PC)

```bash
cp Desktop/wiki_pending/ae-aep-default-v25-2026-05-03.md \
   ccfm-wiki/wiki/tacit/coding-lessons.md  # §AE-25-기본 append
git -C ccfm-wiki add . && git commit -m "tacit: AE .aep 자동 빌드 기본 25.0 + jsx 패턴"
```
