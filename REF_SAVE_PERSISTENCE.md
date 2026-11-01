# Persistence and save-file contracts — curated A/T014

Status: original ver0.67 x86 STATIC; synthetic codec test is not original gameplay. Golden PASS=0, strict MATCH=0, READY not upgraded.
Owner: A/T014. Main report data/T014_GLOBAL_SAVE.md; native evidence exe/T014_GLOBAL_DISASM.txt, exe/T014_NORMAL_SAVE_CORE.txt, exe/T014_NORMAL_SAVE_TAIL.txt. Original PE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187.

## 1. Global key/value store is separate from normal save
- Script commands gread opcode 0x4C and gwrite opcode 0x4D; V9 native E8 sites 0x4A5FAB→0x428010 and 0x4A61BD→0x428710 are verified. gread decodes global.sav into a logical map; it is not a fresh disk lookup per read.
- Logical records: key string, aux string, signed int32 value; mapped value offset +0x1C. gwrite performs UPSERT, not append and not key deletion; setting zero keeps a key. Optional third argument can set aux data such as a mark-image name.
- Writer serializes key-ordered records (key NUL + aux NUL + int32LE), terminator and envelope. CreateFileA OPEN_ALWAYS followed by WriteFile without established SetEndOfFile/truncate: shorter serialization may leave a physical stale tail. Actual original loader consequences are VERIFY.
- Owner source data/T014_GLOBAL_SAVE.md sections global.sav load model, gwrite logical semantics and file rewrite.

## 2. Shared encrypted envelope, distinct plaintext formats
- Native writer 0x427040 and reader 0x4270F0 use magic bytes 01 02 03 04 followed by 28-byte key, with additive/subtractive byte transform using key[fileOffset % 28] for fileOffset>=32.
- Approved V9 direct E8: 0x428F59→0x427040 global write, 0x46065C→0x427040 normal save, 0x4282B0→0x4270F0 global read. DAT and normal .sav use the same envelope, not the same payload schema.
- A clean-room codec synthetic roundtrip exists; do not count that as a true original-file or gameplay Golden test.

## 3. Normal save state groups (not automatically global.sav)
- Normal writer entry 0x460000 follows command save handler 0x4A17C8 / state builder 0x45F960. It serializes script persistent state at engine+0x310 and separate runtime groups +0x300 (Unit), +0x2F0 (Spot), +0x2E0 (Power) via distinct per-object writers, each with group delimiters.
- Normal save also writes scene/event state; the loader reads its own encoded stream and metadata. Do not assume that a raw save byte diff directly identifies changed gameplay objects or that save4/save5 came from an external result.
- Engine+0x310 script map includes @evtend_<event> execution markers. yet(name) tests the marker; common event invocation 0x4321B0 can mark it. event/call and routine differ in flags, and battle-context routine may take a marker-bypassing path. The blanket rule “routine never records completion” is false.
- **2026-11-01 訂正・追補（Claude、出典 S1101 = REF_SAVE_FORMAT.md）**: 各群の区切りは空文字ではなく `----------`+NUL（11 バイト）。+0x300/+0x2F0/+0x2E0 は map の先頭ノードで、表本体は ctx+0x2FC/+0x2EC/+0x2DC。Power 群の後にターン進行オブジェクト（G+0x1EF4B4、0x471D20/0x471AF0。T014 では「外交状態」と誤って呼んでいた）と世界地図グラフ（0x435C10/0x435550）が続く。数値変数の前の見出しは @gamemode・シナリオ名・プレイヤー勢力名・経過ターン・保存日時。実セーブ 4 件で本体を 1 バイトまで再構成して一致。save3・auto では本体の後ろに古いセーブ（auto は少なくとも 7 世代）が残り、読込は世界地図グラフの後で戻る（静的確認）。ゲームでのロード結果は未確認。
- Source: data/T014_GLOBAL_SAVE.md sections normal save writer/group serialization, event marker and battle-specific routing; exe/T014_SAVE_FUNCTION_SUMMARY.txt and exe/T014_NORMAL_SAVE_CORE.txt.

## 4. Critical unresolved gates for AI or implementation
- Type/name inference must stay separate from exact native offsets, command flags and source order. Reconstruct encrypted file payload schemas using evidence, not a guessed generic dictionary.
- Verify actual original global.sav and normal .sav fixtures, shortened rewrite tail handling (normal .sav: physical stale tail confirmed on real files 2026-11-01, REF_SAVE_FORMAT.md §3; in-game load result still VERIFY), RNG seed during fresh encryption, save-load event marker persistence, and reader/writer boundary conditions. No strict MATCH until same unmodified original fixture is observed.
- T014 as a whole is IN_PROGRESS. T003/T022 encrypted DAT roundtrips and synthetic global codec successes are distinct from game-play/save Golden.
