# 迫真戦記ver0.67 研究B T012｜mode4候補空→生成試行枠消費の跨関数条件（2026-10-21 11時台）

- 研究候補ID：`B-OFFLINE-20261021-1110-01`、B/T012主（T011生成・T013対象選択参照）。復旧ID：`B-RC-20261021-1110-LOCAL-SESSION-01`。
- 判定：`STATIC-GHIDRA + PRIOR-SAVED-ASM-CROSSCHECK / INFERRED-CROSS-FUNCTION / VERIFY / OFFLINE-UNSYNCED / NOT READY`。今回B限定READY 0、E MASTER統合0、原作Gameplay Golden PASS0、新旧strict MATCH0。
- 証拠源：添付 `HAKUSHIN067_AI_OFFLINE_PACK_20261021(1).zip` 34 entries、CRC全件正常。`BUILD_MANIFEST.json` PASS、対象原作EXEの記録SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回は原本実体再ハッシュなし）。
- オフラインSQLite `search.sqlite` 53,927,936 B、実測SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` がマニフェストと一致。`search.py`のSHA256 `DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0` 一致。
- 検索：`function 0x5501A0`、`related 0x5501A0 --depth 2`、`function 0x54E7B0`、`function 0x57F190`、`function 0x54DCA0`、研究snapshotの既B HANDOFF/T012資料。全てオフラインread-only。PC検索DBは本回未読。
- 擬似C識別：`0x5501A0` 621 bytes・code SHA256 `1687A2EB67E5D43881EE8E1BCA397AB1089B23168D02AA5D7E86E13DA932CB31`、`0x54E7B0` 3241 bytes・code SHA256 `B66F05D87C7E4880B668E637FEF275F24EFA80A6DC1948BA6B13BB42702B50F0`。

## 増分1：候補なしでも上位の生成試行上限に進む経路（異なる関数の条件合成）

- `0x5501A0`：`manager+0x1F4`を先に+1し、`def=*(manager+0x1D4)` の `def+0x78` 以下なら初期化して生成loopへ。`def+0x40 == 4` のとき **site `0x550219 → 0x54E7B0`**、それ以外は `0x55037F → 0x580280`（STATIC-PSEUDOC/CALLGRAPH）。
- 下位`0x54E7B0`：Skill `+0x14C == 0` **かつ** `Skill+0x158 == Skill+0x15C`（28B候補配列のbegin/end一致）で、生成effectへ入らず `LAB_0054F435` cleanup/正常returnへ分岐する。擬似Cで独立確認。B先行 `B-20261013-1134-01` の保存済みASM研究にも `0x54E82A`の候補空→cleanup と明記（今回は当時のASM全文を再取得していない）。
- calleeから正常復帰した上位`0x5501A0`は、戻り値/生成個体確認の分岐を挟まずに `manager+0x1F0` を+1し、`def+0x74` 上限と比較する。**calleeが上記の空候補短絡でeffect生成を行わなくても、上位が試行枠を消費する条件付き経路と整合**する（STATIC-PSEUDOCの制御フロー合成／実到達はVERIFY）。
- 新カウンタが上限に達すれば **site `0x5503F9 → 0x4C22B0(manager,0)`** の後 `manager+0x1D0` byteを0へ。上限未達なら `def+0x78 != 0` で今回return、`==0` なら同一呼出内でもう1回loopに進む（STATIC-PSEUDOC）。
- 召喚成功数を試行回数と同一視すると、候補なし→生成なし→上限消費という場合に原作再現がずれ得る。ゲーム上の「召喚失敗」表現/表示/HP/EXP/解除の実効は未証明であり、原作バグ認定しない。
- RNG：下位の直接CRT rand候補site `0x54E886` は候補選択の後にあるため、上記空候補早期returnではそこを通らない。ただし他callee/上位の総RNG消費0という意味ではない。

## 増分2：mode4の座標ソースと第1表示引数は常に同じとは限らない

- `0x5501A0`擬似C内で `origin = *(manager+0x1D8)` から始まる局所条件。`origin+0x65 != 0` なら `iVar1=iVar2=origin`。
- `origin+0x65 == 0` かつ `manager+0x6D != 0` なら `iVar1=iVar2=manager+8`。
- `origin+0x65 == 0` かつ `manager+0x6D == 0` なら **`iVar1=manager+8`だが`iVar2=*(manager+0x80)`**。`iVar1`から座標の`+0x40/+0x48`中点と`+0x4C`を取る一方、`iVar2`を `0x550219`の表示引数として渡す（STATIC-PSEUDOC）。
- 中点式は `(high-low >> 1)+low` として復元。signed shift・境界丸め・overflowは許可済み原作ASMの呼出窓で確認するまではVERIFY。`manager+0x80`のNULL妥当性や`+0x65/+0x6D`のゲーム上の意味もVERIFY。
- B先行 `B-20261013-1134-01` の保存済みASM研究には `0x54E7B0`入口 **ECX=placement・EDX=Skill・stack4 args** とある。`0x5501A0` Ghidraのcall表記は4引数、callee署名は`__fastcall`6引数で一致しないように見えるが、**4スタック引数＋レジスタ2引数の復元差で説明可能**。ただしこのcallerサイトのECX/EDX保持は未取得のため、どの表示引数がどのネイティブ引数か最終確定しない。`iVar2`を「確定Unit owner」とするのは禁止。

## 既存研究との差分、正本境界、次回

- 重複排除：B既存 `B-20261013-1134-01` は下位のempty candidate early return、`B-20261013-1239-01` は`0x4C22B0`解除の下位仕様。2026-10-21 `B-20261021-0910-01` は上位dispatcher/周期/上限、`B-OFFLINE-20261021-1015-01` はmode4とnon4の戻り値捕捉/NULLリンク。**今回のみの差分は、空候補による実effect非生成経路と試行上限消費の跨関数照合、およびmode4の3条件入力切替・ABI曖昧性境界。**既存READYを再計上しない。
- PC最新MASTER・B HANDOFF、02〜08時台研究本文のPC保存状況、09時台HANDOFF/08時台同期の安全拒否、重複/予約は本回更新確認できない。最後のPC checkpoint195は過去値。旧拒否操作/本文/禁止VAを別tool/ZIP/Remote等で再試行・迂回しない。
- Golden必要：同一合法旧EXE/DAT/SAVE/map/input/seed（取れなければUNKNOWN）と新build SHAを区別。合法mode4発火・空/非空の候補、`Skill+14C`優先、`def+74`上限1/複数、`def+78` 0/正値、`origin+65`と`manager+6D`分岐が実際に作れるか確認。単回/連続tickの可視生成数、実登録、解除、HP/MP/EXP、RNG、選択座標を比較。合法再現不能の内部境界はSTATIC-ONLYとしてPASSにしない。Game Golden PASS0、strict MATCH0。
- 次回：先にLocal復帰時のPC最新正本・未同期と安全拒否台帳の存在・重複をread-only確認。本件の保存済みASMにおける`0x550219`呼出直前のECX/EDX/stack引数、`0x54E82A→0x54F435`分岐、`0x5503F9`上位終了順を確認。0x5501A0の間接callerも依然VERIFY。T011 EXP所有者、T012最終ダメージ、T013最終対象、T024 AI時間、T028士気寿命のP0維持。
- 今回のLocal初回 `MASTER_LEDGER.md` 読取エラー：`INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。分類 CONNECTION（一時障害、安全拒否ではない）。PC CPU/RAM負荷未取得。Work/Remote使用0、原作EXE/ZIP/SAVE実行・変更0、PC/MASTER/他owner/REA/dev_lab/Git/設定/automation変更0。
