# REA独立監査：文字列writerの使用範囲（2026-10-10 17時台 JST）

対象はver0.67承認済みコピーの保存済みGhidra証拠のみ。新EXE/新REA/Ghidra/原作実行なし。
source SHAはRUN_RESULT記録 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回再計算なし）。
## 確認：0x470830のdirect xrefはUnit writer以外にも広がる
- T014: 0x470830 procedure_callers（run 20261009T220712454Z、evidence ev_8fd58bea9f3f6285fa73f9136ed4579d386ca9d352795c38d35e05fede16f880）はresolved direct callerを10関数報告。
- 全10入口: 0x428710,0x435C10,0x460000,0x4708D0,0x471D20,0x58EFD0,0x596AA0,0x598CE0,0x5A93F0,0x5B0600。
- 0x428710は未取得Wave4 global.sav upsert/writer候補、0x460000は取得済み通常save writer、0x58EFD0は取得済みUnit serializer。残りのcallee所属や到達性はこのxref単独では確定しない。
- writer 0x470830の保存assembly（ev_1ffa032ec901cde47d6811b2e2941ff163adbcd1a68d9573bed5f6efe6b58d02）は文字列全byteを符号付き比較し、0x20..0x7Fだけ許可。不適格byteが1つあれば元の文字列を全出力せずNULのみを出す。これは既存監査の確認済み仕様であり今回の新発見数には含めない。
- 今回追加したのは、この変換helperのresolved caller集合がUnit・通常save・global.sav候補など複数serialization入口へ跨ることのxrefs照合。
## 実装・互換テストへ渡す制約
- 単一ファイルのUnit codecに限らず、各callerが実際にこのhelperへ入力を渡す分岐と、上位save formatでの使用位置を確認する。0x428710は関数5点証拠がまだ無く、global.sav内での実レコード仕様と到達性はVERIFY。
- 合成試験候補：ASCII正常、0x7F境界、0x80以上混入、途中の0x00、複数IDが空文字化した場合のreader停止。これらはDESIGNED/NOT RUN、実ゲーム破損は未観測。
- Ghidra resolved direct xrefsだけを対象とし、computed/indirect callerは未集計。この10件を全呼出の網羅性とは解釈しない。
## 進捗と安全
- Wave1 16/16・Wave2 10/10・Wave3 10/10・Wave4 3/12、合計39/48 VERIFIED。新規VERIFIED0、P0 20/21、P1 19/27、TODO8、VERIFY1。
- MASTER最終checkpoint69：研究DONE9/34。旧EXE実機golden PASS0。ゲーム再実装率未測定。
- 新規逆解析の既往SAFETY_REFUSAL、0x5710C0..0x571500と抽出拒否は迂回・再試行なし。QUEUE/PROGRESS stale EPERMは変更せず。原本・A〜E・MASTER・T018・Git/公開・MCP設定・スケジュール不変更。
- 次回優先：0x4930C0（T010 P0）、0x514D60/0x514F10（T013 P1）、0x428010/0x428710（T014 P1）の保存証拠取得（安全実行許可時のみ）。