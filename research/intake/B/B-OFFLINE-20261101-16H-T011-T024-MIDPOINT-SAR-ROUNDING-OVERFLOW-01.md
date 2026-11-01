# B research intake — verified PC-owned evidence
research_id: B-OFFLINE-20261101-16H-T011-T024-MIDPOINT-SAR-ROUNDING-OVERFLOW-01
owner: B
source_relative_path: data/T011_T024_NATIVE_MIDPOINT_SAR_ROUNDING_OVERFLOW_OFFLINE_20261101_16H.md
source_sha256_verified_2026-11-02_JST: B111C5F2EE1DBC568E18F803288542AC120DF0EA4011D7B929AEB79DC29C01C6
intake_status: PUBLISHED_INTAKE / NOT_CURATED / STATIC-VERIFY / NOT_READY
original_gameplay_Golden_PASS: 0
strict_MATCH: 0
source_note: The research below is the B-owned source report; its historical OFFLINE state describes its original capture. This archive was staged after source-file SHA confirmation on the authorized PC. Native ABI and game behavior remain unproven.

---

# 迫真戦記 新B・T011/T024｜Unit座標中央のSAR丸め・符号付き32bit差分境界（2026-11-01 16H JST）

研究ID：`B-OFFLINE-20261101-16H-T011-T024-MIDPOINT-SAR-ROUNDING-OVERFLOW-01`。owner=B、tasks=T011/T024。状態：**OFFLINE-UNSYNCED / STATIC / INFERRED / SYNTHETIC_ONLY / VERIFY / NOT READY**。原作実機Golden PASS=0、strict MATCH=0、正式READY=0。

## 証拠源・未同期回収

最初に Desktop Commander Local Compact で研究PCの `MASTER_LEDGER.md`、PROTOCOL、B HANDOFFなどの閲覧を試みたが、`UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。**安全拒否ではなく一時的な接続制限**。最新PC正本・3H保存失敗の有無・05〜16H成果のPC取り込みは未確認。研究PCへ書き込んでいない。

今回はChatGPT Libraryから `13H` 原作機械語エビデンスJSONと13H・15H研究報告を取得し、既存ローカル保存済み14H/15H成果のmanifest SHAを**8/8**再確認して利用した。**16Hに原作EXE本体・SQLite・Ghidra擬似C原本を再取得してはいない**。13H記録に付された原作EXE SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、13H機械語記録SHA256=`1C2030F7A1D8EB12A5E97F51509C70FA1BA25ADD600C271A5DA23516939A0205`。今回の根拠は13H取得済STATIC再利用と独立合成テストである。原作EXE実行なし・禁止VAアクセスなし。

GitHub非公開 `ButaMonky/Hakushin067-Research-Knowledge` の `develop` にある `symbols.tsv`（blob SHA `3fcf2d436c21f3fc91791a91e75c9a800167ca4d`）、`structs.tsv`（`d79f03b1dbac67012882b0cb691d6af479610a01`）、`REF_BATTLE_AI_MORALE.md`（`83fb9b91a84e8190042802ed7af5666ca51f7f8c`）、`KNOWLEDGE_CURATION_PROTOCOL.md`、V9レビュー表を読取専用で参照。上記3 KBファイルでは対象 `0x526030/0x529DC0/0x52AD00/0x52607F` の文字列直接一致は0件。**PC上の最新研究まで非重複と断定しない**。

## 新しい派生結果：小さい負座標でもSARによる丸め差が出る

既存13H研究は `0x526030` 内の Unit の `+0x40` と `+0x48` から比較用のX位置を構成することを同定済み。今回、13Hの記録を読み直し、**末尾の算術命令の組合せと境界値**を別研究IDで検査した。新たに未取得のASMを読んだと主張しない。

```asm
0x526074: 8B5140      mov edx,[ecx+0x40]
0x526077: 8B4148      mov eax,[ecx+0x48]
0x52607A: 8B494C      mov ecx,[ecx+0x4C]
0x52607D: 2BC2        sub eax,edx
0x52607F: D1F8        sar eax,1
0x526081: 03C2        add eax,edx
```

記号化：`a=Unit+0x40`、`b=Unit+0x48` とすると、**X = i32(a + (i32(b-a) SAR 1))**。`Y=Unit+0x4C` は13H先行確認。ここで `i32` は32bitレジスタのwrap。差分が符号付き範囲内なら、Xは数学的な `floor((a+b)/2)` に一致する。C/C++の符号付き整数除算 `(a+b)/2`（ゼロ方向丸め）と**負かつ奇数和**で異なる。例：a=-1、b=0 → ASMモデルX=-1、ゼロ方向の平均0。a=-3、b=0 → -2対-1。

追加の合成テストでは `a,b ∈ [-256,256]` の**263,169組**を全検査。ASMモデルは数学的floorと**263,169/263,169一致**、ゼロ方向丸めの平均式とは**65,792組で不一致**。これは合成テストの合否でありゲーム内座標や原作Golden PASSを意味しない。

## 新しい派生結果：32bit差分overflowで始点終点の入替が非対称になる

境界の合成例：`a=-2147483648, b=0` では `i32(b-a)=-2147483648`、SAR後に `a` を加えると **+1073741824**。始点・終点を入れ替えた `a=0,b=-2147483648` では **-1073741824**。真の中点はいずれも -1073741824。したがって**巨大差分での2点の順序交換は原作機械語の中点結果に対して可換でない**。同様に a=INT32_MIN、b=INT32_MAX ではX=INT32_MAXにwrapし、数学的floor平均=-1と大きく食い違う。

通常ゲームでこれらの異常値が入力されるかは不明（VERIFY）。13〜15Hの距離比較が `Unit+0x40/+0x48/+0x4C` に依存するという先行観測と組み合わせ、再実装時は**非負で小さい値だけを仮定した整数平均への置換を禁止候補**として記録する。さらにC/C++では符号付きoverflowが未定義となり得るので、もし完全一致実装を行うなら明示的な32bitレジスタ演算または符号なし演算から再解釈し、原作Goldenで比較する必要がある。

## 追跡範囲・既存IDとの差分

先行13Hの `0x52AD35 -> 0x526030` は直接E8 CALLとして**過去に確認済み**。今回新たなCALL経路を発見したとは主張しない。13Hは距離式とモード別ソート、14Hは平方和overflow/NaN条件、15HはNaN比較の関係を研究した。**16Hの新規差分は中点の負奇数丸め、演算順序による非対称overflow、および合成263,169組の再現回帰テスト**。以前の研究を再計上しない。

`0x52AD00` 同距離の実際のノード移動順序、`0x529691`対`0x529851`の基準座標の意味、`0x569730`の行動結果、T011経験値・召喚、T012ダメージ・回復・状態、T013最終攻撃対象、T024 AI全体、T028士気・敗走は依然P0/VERIFY。`0x5710C0..0x571500`等の禁止範囲と拒否済XREF操作は再試行しない。安全保留21件と旧SAFE134（今回未全検証）はそのまま。

## 検証・失敗記録とGolden条件

検証スクリプト `data/B_20261101_16H_MIDPOINT_SAR_NATIVE_READONLY_VERIFY.py`、結果 `data/B_OFFLINE_20261101_16H_MIDPOINT_SAR_EVIDENCE.json`。**21/21個の限定アサーションPASS**（元の6命令bytesの既存記録と照合、境界ケース12組、グリッド全数1件＋差分存在1件、方向非対称1件）。これは**21個のASM検証ではない**。初回のアドレス表記 `0x`/`0X`正規化ミスでKeyError、続いてテストの予想値に数学的floorとゼロ方向丸めを混同したAssertionErrorを検出。検証コードと期待値を修正し、21/21 PASS。両失敗を消さず保持。

Golden要件：原作ver0.67の同じEXE/DAT/MAP/SAVE上で、負奇数和の位置、通常正座標、同距離、軸点の前後逆転、32bit境界の到達可否、`0x526030`比較結果と`0x52AD00`ノード順をログ採取し、再実装とstrict比較する。**原作実機Golden PASS=0、strict MATCH=0、READY=0**。

## KB_CANDIDATE・次の再開

`KB_CANDIDATE` owner=B tasks=T011/T024、研究ID=`B-OFFLINE-20261101-16H-T011-T024-MIDPOINT-SAR-ROUNDING-OVERFLOW-01`。VA `0x526030`、命令サイト `0x526074/77/7A/7D/7F/81`、先行CALL site `0x52AD35 -> 0x526030`。オフセット `Unit+0x40/+0x48/+0x4C`。出典：13H保存済検証JSON SHA256 `1C2030F7A1D8EB12A5E97F51509C70FA1BA25ADD600C271A5DA23516939A0205`、擬似C `functions/0052/00526030.c` SHA256 `7FEE7676046DFF1E081ED82702FBB17AEEEA2CCA92CCE64E1BB57B2F0D5745CF` は**以前の記録を引用しただけ**。STATIC=元ASM保存記録、INFERRED=中点式の導出、SYNTHETIC_ONLY=境界と回帰、VERIFY=実際の到達と最終行動。訂正注意：`(a+b)/2` のC式では一般に原作と等価でない。**知識ベースへの自動確定・共有GitHubへのpushなし**。

次の許可一手：PC復帰時にMASTER/PROTOCOL/B HANDOFF/03H回収とID・owner・HOLD競合を**先に**照合し、B許可領域へ一度だけ取り込んでreadback。オフライン継続なら過去の合成条件を再繰返しせず、`0x52AD00` の実際の同値マージ・`0x529691` と `0x529851` の座標が**別系統かどうか**を、許可済み原本または保存済静的証拠の範囲で追う。
