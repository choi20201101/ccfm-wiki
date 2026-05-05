#!/usr/bin/env node
/**
 * context-bootstrap.mjs
 *
 * 사용자 prompt를 받아 메모리 인덱스(MEMORY.md)와 위키 단축표(HOTSHEET.md)를
 * 스캔해서 관련 파일 후보를 반환한다.
 *
 * 사용 (CLI):
 *   node ~/.codex/scripts/context-bootstrap.mjs "<user prompt>"
 *   echo "<user prompt>" | node ~/.codex/scripts/context-bootstrap.mjs --stdin
 *
 * 출력 (text 기본):
 *   <context_grounding>
 *   ## Memory matches
 *   - C:/.../memory/foo.md — bullet text
 *   ## Wiki matches
 *   - [[domains/bar]] — trigger row text
 *   </context_grounding>
 *
 * --json 옵션: { memory: [...], wiki: [...], keywords: [...] }
 *
 * 매칭 규칙: 사용자 prompt에서 한글 토큰 + 영문 토큰 추출 후
 * 인덱스 줄에 동일 토큰이 1개 이상 포함되면 hit. 점수=hit count.
 * 상위 N개를 반환 (기본 6).
 */

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const HOME = process.env.USERPROFILE || process.env.HOME || "C:/Users/Administrator";

// Memory index 경로: env override 우선, 없으면 Administrator 기본 경로
const MEMORY_INDEX =
  process.env.CCFM_MEMORY_INDEX ||
  path.join(HOME, ".claude/projects/C--Users-Administrator/memory/MEMORY.md");
const MEMORY_DIR = path.dirname(MEMORY_INDEX);

// 위키 루트: env override → AGENTS.local.md 의 CCFM_WIKI_ROOT → 기본값 후보 (gguy / Administrator / Desktop)
function resolveWikiRoot() {
  if (process.env.CCFM_WIKI_ROOT) return process.env.CCFM_WIKI_ROOT;
  // ~/.codex/AGENTS.local.md 에 `CCFM_WIKI_ROOT=...` 한 줄이 있으면 사용
  try {
    const localCfg = path.join(HOME, ".codex/AGENTS.local.md");
    const cfg = fs.readFileSync(localCfg, "utf8");
    const m = cfg.match(/^CCFM_WIKI_ROOT\s*=\s*(.+)$/m);
    if (m) return m[1].trim();
  } catch {
    /* ignore */
  }
  // 후보 경로: 기존 환경(gguy 프로필) → Administrator 프로필 → Desktop 폴더
  const candidates = [
    "C:/Users/gguy/ccfm-wiki",
    path.join(HOME, "ccfm-wiki"),
    path.join(HOME, "Desktop/ccfm-wiki")
  ];
  for (const c of candidates) {
    try {
      if (fs.statSync(c).isDirectory()) return c;
    } catch {
      /* keep going */
    }
  }
  return candidates[0]; // 없어도 첫 후보 반환 (헬퍼는 readSafe 로 부드럽게 처리)
}

const WIKI_ROOT_BASE = resolveWikiRoot();
const WIKI_HOTSHEET = path.join(WIKI_ROOT_BASE, "wiki/HOTSHEET.md");
const WIKI_INDEX = path.join(WIKI_ROOT_BASE, "wiki/index.md");
const WIKI_ROOT = path.join(WIKI_ROOT_BASE, "wiki");

const STOP_WORDS = new Set([
  // 한국어 일반 stop word
  "이거", "저거", "그거", "이번", "저번", "그건", "그런", "이런", "저런",
  "있어", "없어", "있음", "없음", "있다", "없다", "한번", "한 번", "좀",
  "좀더", "더", "그리고", "근데", "그런데", "또한", "또", "혹은", "또는",
  "에서", "에게", "에는", "에도", "이고", "이다", "다음", "전부",
  // 한국어 의문/명령 어미 (검색 의도 표현, 매칭 가치 X)
  "어떻게", "어떡해", "어때", "어떤", "뭐야", "뭐가", "뭐임", "뭐지",
  "해줘", "해주", "해봐", "보여줘", "알려줘", "만들어줘", "만들어",
  "시작해줘", "시작", "처리", "진행", "정리", "확인", "체크",
  // 영어 일반 stop word
  "the", "a", "an", "is", "are", "was", "were", "and", "or", "of", "to",
  "for", "in", "on", "at", "by", "with", "from", "this", "that", "these",
  "those", "it", "you", "we", "they", "be", "been", "being", "do", "does",
  "did", "have", "has", "had", "but", "not", "no", "yes", "if", "then",
  "so", "as", "than", "us", "me", "my", "your", "our", "his", "her",
  "im", "ive", "ll", "ve", "re", "him", "she", "he"
]);

// 한국어 조사: 토큰 끝에서 trim (feedback이 → feedback, 메모리에서 → 메모리)
// 길이 우선순위: 긴 조사 먼저 매칭 (에서 > 에)
const KOR_PARTICLES = /(에서|에게|에도|에는|이라고|이라|라고|이고|이며|이다|입니다|이에요|예요|로서|로써|로|으로|에|을|를|이|가|은|는|의|와|과|도|만|까지|부터|마저|조차|이나|나|랑|랑은|랑도)$/;

function readSafe(filePath) {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch {
    return null;
  }
}

function tokenize(text) {
  if (!text) return [];
  // 한글/영문/숫자 토큰만 (구두점 제거). 한글은 2글자 이상, 영문은 3글자 이상.
  const raw = text
    .toLowerCase()
    .replace(/[\r\n\t]+/g, " ")
    .split(/[^a-z0-9가-힣_-]+/u)
    .filter(Boolean);
  const seen = new Set();
  const tokens = [];
  for (let t of raw) {
    // 한글 토큰: 끝의 조사 제거 (feedback이 → feedback 의 경우는 영문+조사 조합)
    if (/[가-힣]/.test(t)) {
      t = t.replace(KOR_PARTICLES, "");
    } else if (/[a-z]/.test(t)) {
      // 영문 토큰 끝에 한글 조사가 붙은 경우도 처리 (feedback이, codex가, mllm을)
      // raw split 단계에서 이미 영문/한글 경계로 분리되지만 안전망
      t = t.replace(KOR_PARTICLES, "");
    }
    if (!t) continue;
    if (STOP_WORDS.has(t)) continue;
    // 한글 2자+, 영문/숫자 2자+ (도메인 약어 BJ, AE, UI 보존). 1자는 noise.
    if (t.length < 2) continue;
    if (seen.has(t)) continue;
    seen.add(t);
    tokens.push(t);
  }
  return tokens;
}

function scoreLine(line, tokens) {
  const lc = line.toLowerCase();
  let hits = 0;
  const matched = [];
  for (const t of tokens) {
    if (lc.includes(t)) {
      hits += 1;
      matched.push(t);
    }
  }
  return { hits, matched };
}

function parseMemoryIndex(content) {
  // MEMORY.md 의 bullet 줄: `- [Title](file.md) — description`
  // 또는 `- [Title](path/file.md) — description`
  const out = [];
  if (!content) return out;
  for (const rawLine of content.split(/\r?\n/)) {
    const m = rawLine.match(/^\s*[-*]\s*\[([^\]]+)\]\(([^)]+)\)\s*[—-]\s*(.+)$/);
    if (!m) continue;
    const [, title, file, desc] = m;
    out.push({
      title: title.trim(),
      file: path.resolve(MEMORY_DIR, file.trim()),
      relFile: file.trim(),
      desc: desc.trim(),
      raw: rawLine.trim()
    });
  }
  return out;
}

function parseWikiHotsheet(content) {
  // HOTSHEET.md 트리거 표: `| 요청 트리거 | 진입할 위치 | 비고 |`
  // 진입 위치는 [[wikilink]] 또는 스킬명.
  const out = [];
  if (!content) return out;
  for (const rawLine of content.split(/\r?\n/)) {
    if (!rawLine.startsWith("|")) continue;
    const cells = rawLine.split("|").map((s) => s.trim());
    if (cells.length < 4) continue;
    const trigger = cells[1];
    const target = cells[2];
    const note = cells[3];
    if (!trigger || trigger === "요청 트리거" || /^[-:]+$/.test(trigger)) continue;
    out.push({ trigger, target, note, raw: rawLine.trim() });
  }
  return out;
}

function rankAndPick(entries, tokens, n = 6) {
  const scored = entries
    .map((e) => {
      const { hits, matched } = scoreLine(e.raw, tokens);
      return { ...e, hits, matched };
    })
    .filter((e) => e.hits > 0)
    .sort((a, b) => b.hits - a.hits);
  return scored.slice(0, n);
}

function formatText({ keywords, memHits, wikiHits, mode }) {
  const lines = [];
  lines.push("<context_grounding>");
  lines.push(`<!-- auto-generated by ~/.codex/scripts/context-bootstrap.mjs -->`);
  lines.push(`<!-- mode=${mode} keywords=${keywords.slice(0, 12).join(", ")} -->`);
  lines.push("");
  lines.push("## Memory matches (개인 메모리 인덱스)");
  if (memHits.length === 0) {
    lines.push("(없음 — 인덱스 스캔 완료, 키워드 매칭 0건)");
  } else {
    for (const h of memHits) {
      lines.push(`- **${h.title}** \`${h.relFile}\` (hits=${h.hits}: ${h.matched.join(",")})`);
      lines.push(`  - ${h.desc}`);
    }
  }
  lines.push("");
  lines.push("## Wiki matches (CCFM HOTSHEET)");
  if (wikiHits.length === 0) {
    lines.push("(없음 — HOTSHEET 스캔 완료, 매칭 0건)");
  } else {
    for (const h of wikiHits) {
      lines.push(`- **trigger**: ${h.trigger}`);
      lines.push(`  - target: ${h.target}`);
      if (h.note) lines.push(`  - note: ${h.note}`);
    }
  }
  lines.push("");
  lines.push("## 처리 지침");
  lines.push("- 위에 매칭된 메모리/위키 파일을 **답변·코드 작성 전에 직접 읽는다**.");
  lines.push("- 응답 첫 줄에 `📚 참조: <읽은 파일 목록>` 명시 (0건이면 `참조: 없음`).");
  lines.push("- feedback_*.md 매칭은 과거 사용자가 거른 함정. 같은 실수 반복 금지.");
  lines.push("- 매칭 정확도 의심되면 인덱스 전체를 한 번 더 scan 해도 됨 (cat MEMORY.md).");
  lines.push("</context_grounding>");
  return lines.join("\n");
}

function readPrompt(args) {
  const stdinFlag = args.includes("--stdin");
  if (stdinFlag) {
    let buf = "";
    try {
      buf = fs.readFileSync(0, "utf8");
    } catch {
      buf = "";
    }
    return buf.trim();
  }
  // 첫 번째 비-flag 인자
  const positional = args.filter((a) => !a.startsWith("--"));
  return positional.join(" ").trim();
}

function main() {
  const args = process.argv.slice(2);
  const jsonOut = args.includes("--json");
  const verbose = args.includes("--verbose");

  const prompt = readPrompt(args);
  if (!prompt) {
    process.stderr.write(
      "usage: context-bootstrap.mjs \"<user prompt>\" [--json] [--stdin]\n"
    );
    process.exit(2);
  }

  const tokens = tokenize(prompt);
  if (verbose) {
    process.stderr.write(`[ctx] tokens=${tokens.join(",")}\n`);
  }

  const memContent = readSafe(MEMORY_INDEX);
  const memEntries = parseMemoryIndex(memContent);
  const memHits = rankAndPick(memEntries, tokens, 6);

  const wikiContent = readSafe(WIKI_HOTSHEET);
  const wikiEntries = parseWikiHotsheet(wikiContent);
  const wikiHits = rankAndPick(wikiEntries, tokens, 6);

  const mode = !memContent
    ? "memory-missing"
    : !wikiContent
      ? "wiki-missing"
      : "ok";

  if (jsonOut) {
    process.stdout.write(
      JSON.stringify(
        {
          mode,
          keywords: tokens,
          memoryIndex: MEMORY_INDEX,
          wikiHotsheet: WIKI_HOTSHEET,
          memory: memHits,
          wiki: wikiHits
        },
        null,
        2
      )
    );
    process.stdout.write("\n");
  } else {
    process.stdout.write(
      formatText({ keywords: tokens, memHits, wikiHits, mode }) + "\n"
    );
  }
}

main();
