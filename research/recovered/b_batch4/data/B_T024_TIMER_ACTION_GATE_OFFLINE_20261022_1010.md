# 迫真戦記 新B / T024 — 時間値消費先とUnitへの候補操作配送（オフライン独立研究）

- 研究ID: `B-OFFLINE-20261022-1010-T024-TIMER-ACTION-01`
- 復旧ID: `B-RC-20261022-1010-LOCAL-SESSION-TERMINATED-01`
- 日時: 2026-10-22 10時台 JST
- 所有: B/T024（T013は既知研究の参照のみ）。状態: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。
- PC状態: Desktop Commander Local Compact の初回読取操作が `INVALID_ARGUMENT: McpServerError: Session terminated` で失敗。**安全拒否ではなく、接続セッションエラー**。PC最新MASTER/READY/owner/重複は照合不能、PCへ保存・同期なし。Work未使用。原本実行・編集なし。
- オフライン根拠: Library `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34 entries、CRC PASS。search.sqlite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、SQLite `PRAGMA quick_check` = ok。元EXE SHA256はmanifest**記録値** `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（原本EXE実測なし）。これは10/21時点の検索基盤・研究snapshotであり、10/22のPC現行V3とは別物。
- 利用手段: ZIP内の`headless_analysis/search_index/{search.py, search.sqlite, README.md, BUILD_MANIFEST.json}`。全Ghidra/REA再解析なし。以下の直接CALLは古いGhidra参照DBに基づく**STATIC**。現行V3/原作ASM照合は未実施。

## 追加の静的事実（今回の非重複増分）

1. `0x44AE70`から`0x449500`への直接CALLが少なくとも4箇所: site `0x44B081`, `0x44B12E`, `0x44B145`, `0x44B22E`。`0x44AE70`で条件を評価した後の処理が`0x449500`へ進む経路がある。`0x449500`は複数関数から共用される（`0x4498E0`, `0x44B240`, `0x44BBB0`, `0x44CD70`など）。**前回`0x44AE70`の時間比較だけでは末端の行動を結論できない。**
2. `0x449500`は、まず`context+0x78 == context+0x7C`なら早期return（候補ポインタ範囲が空の場合と整合）。状態 `context+0x98 < 11` なら、引数モードが0以外の場合に6へ切り替える経路がある。`context+0x98 >= 11` では引数モード1または7に対し、`0x46F4C0(context.game+0x1B8,500)`および`0x5D1B80`の結果を、**内部時間式** `start==0 && current==0 → 10000; start==0x80000008 → current; その他 → start-current` と比較し、`result > time` の場合はモード6に切り替える。`result <= time`の場合は元のモードを維持して先へ進む。※両関数の引数規約・resultの分布・時間の単位はVERIFY。
3. 同じ`0x449500`は、`(game+0x1EF244)!=0 && (context+0x18)==0 && mode==6`ならmodeを7に切り替える。**時間だけで最終modeを決められず、戦闘側フラグによる追加書換えがある**。
4. `0x449500`はpointer列を走査し、各Unit候補の `+0x1867C==0 && +0x1867E==0 && +0xC0>=0 && +0xD0>=0 && +0xC8>=0` のとき、`0x5D1B80` / `0x40ED80` を経て `0x577220` へ進む。直接CALL siteは`0x4496AF`, `0x4496B9`, `0x4496C4`（それぞれ上記順）。この条件が偽の候補では本経路上の`0x577220`を呼ばない。対象選択(T013)の最終命中先とは現段階で同一視しない。
5. `0x577220`の擬似Cは文字列の長さを走査して`0x402800`を呼び、条件に応じUnit候補 `+0x1E4F8` に `+0x1E518` かEBX値の大きい側を代入する形。`ESI/EBX`はGhidra未解決レジスタであり、**引数とUnitの実体・代入の意味はVERIFY**。`0x449500`の呼出先を「移動」や「攻撃」とは断定しない。
6. `0x44AE70`の文字列索引に`btl_standby` (`0x6358A8`, reference site `0x44AEDF`)を確認。この字句単体は処理のゲーム内意味を確定しない。`0x44AE70` は `0x515060` を2回呼出（sites `0x44AE78`,`0x44AE82`）し、Unit集計を参照する候補経路があるが、**Ghidraの`0x515060`が`void`と宣言される一方、`0x44AE70`側が戻り値を参照する不整合**があり、ABIと値の所在はASMを要確認。`0x515060`の`+0x88/+0x8C`集計自体は既存T013成果であり再計上しない。

## 既存研究と差分

- 前回 `B-20261022-0915-T024-T028-CLOCKARG-01` は`0x44AE70`への時間引数と`+0x94`との2比較まで。今回の増分は **`0x449500`の追加時間依存分岐／モード変換／Unitフィルタ／`0x577220`への到達**。過去の`0x565750`や`0x515060`の発見は再計上しない。
- ZIPのsnapshot（10/21）でB HANDOFF/T024/MASTERに`0x449500`、`0x44AE70`、`btl_standby`の同定記録は見つからなかったが、PC現行記録未確認のため**非重複確定ではなく暫定**。
- Ghidra DBは現行V3ではなく古いRefTypeベース。CALL siteの機械語E8独立検証は今回0件。原作Gameplay Golden PASS = 0、strict MATCH = 0、Task DONE増加 = 0、MASTER正式READY増加 = 0。

## 合法な次の検証と境界

- PC復帰後、最初にMASTER/HANDOFF/T024の最新IDと未同期回収状態を確認し、ID重複を避けて一度だけ取り込む。現行V3で`0x44AE70→0x449500`の4 CALLと`0x449500→0x577220`、`0x44AE70→0x515060`の機械語E8を限定再照合し、`0x449500`の2引数ABI・入力modeが1/7であるCALL site・時間値の実取得/型を原作ASMで確定する。
- Golden：無改変EXE/DAT/SAVE/MAPで、対象mode 1/7、カウンタ10/11、`result-time`の負/零/正、無制限modeの `current=0/499/500`、追加battleフラグ0/1、対象vector空/非空、Unit座標と状態フラグを独立に観測。RNG呼出順を含むログを取得できるまでは実挙動未確証。
- ローカル拒否扱い: 初回Desktop Commander read_multiple_filesは`Session terminated`（接続系）。安全拒否の迂回は実施せず、Libraryの正規のZIPへオフライン切替。PC正本未保存 / 一時オフライン成果のみ。

## 検索再現

```text
python search.py function 0x44AE70 --max-chars 25000 --limit 1
python search.py function 0x449500 --max-chars 12000 --limit 3
python search.py function 0x577220 --max-chars 12000 --limit 5
python search.py callers 0x449500 --limit 60
python search.py callees 0x449500 --limit 45
python search.py strings btl_standby --limit 20
```
