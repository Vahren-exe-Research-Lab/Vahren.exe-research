# T006 API unmatched triage
調査日: 2026-10-06

## 目的
`T006_CASE_ANALYSIS.json` の true_unmatched 8件を、target script文脈・target Vahren.exe文字列・2017 parser・Wikiで再分類する。

## 解消
- `ammo(`: APIではない。`serihu_pls.dat` のvoice/台詞データ本文に現れる文字列で、function scannerのfalse positive。
- `sFriend(`: 独立APIではない。`isFriend(` の部分一致を拾ったscanner false positive。
- `backscroll()`: 実API。target EXEは canonical string `backScroll` を保持。2017 parserにも `backscroll` 0引数case。target script 108回。
- `hideimage()`: 実API。target EXEは canonical string `hideImage` を保持。大文字小文字非依存のaliasとして扱うべき。target script 12回。
- `isNPC(...)`: 実条件API。target EXE canonical stringは `isNpc`。2017 parserは `isnpc` を1個以上のpower/unit引数として扱う。

## 未解決候補の解消（target native dispatch）
- `chat3(...)` 4回: target EXE command registryに未登録。runtime lookup missはsentinel 0x80000008となり、opcode範囲外としてcleanup/returnへ進むためno-op。2台詞×2コピーは表示されないstrict互換edge。
- `eras()` 1回: `erase()` typo。registry未登録につきno-op。
- `fafeout` 2回: bare `fadeout` typo。registry未登録につきno-op。
- target native command mapは `event/call -> opcode 0`, `routine -> opcode 1`, `msg/msg2/talk/talk2/chat/chat2 -> opcode 11` を明示する。
- lexical unmatched候補は今回0件まで縮小。全APIのsignature/副作用/timing/persistenceは引き続きT006で追う。
[EVIDENCE] `exe/T006_TARGET_DISPATCH.md`, `T006_DISPATCH_PROBE.txt`, `T006_UNKNOWN_BRANCH.txt`

## 設計反映
- API dispatchはASCII case-insensitiveに正規化するが、原綴りをsource spanと共に保持する。
- function-like scannerはtoken境界と構造文脈を認識し、free textや部分一致をAPI候補から除外する。
- target native runtimeのregistry lookupに到達した未知commandはno-op。ただしmalformed構文・未知condition/function-expressionまで同じ扱いとは限らないため、parser/condition側は別途検証する。