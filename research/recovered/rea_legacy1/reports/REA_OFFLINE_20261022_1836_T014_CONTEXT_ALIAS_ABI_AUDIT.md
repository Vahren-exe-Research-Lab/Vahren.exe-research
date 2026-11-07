# 迫真戦記ver0.67｜REA独立T014 P0・間接CALLのcontext別名追跡と呼出ABI補正（2026-10-22 18時台）

**研究ID:** `REA-OFFLINE-20261022-1836-T014-CONTEXT-ALIAS-ABI-STATIC-01`  
**状態:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。この報告書は正式REA VERIFIEDではなく、PC正本へ未同期。  
**所有範囲:** REA独立T014の未解決仮想CALLと関数ABI。原本EXE・ZIP・SAVE、A～E、MASTER、T018、dev_lab、Git、スケジュールは変更しない。

## 1. 環境・旧run・検索DBの扱い

最初にDesktop Commander Local CompactでPC正本のMASTER、規約、REA README/QUEUE/PROGRESS、検索DBを複数ファイル読込しようとしたが、`INVALID_ARGUMENT / McpServerError: Session terminated`により失敗した。**接続障害**であり、実際に発生していない安全拒否・Windows PC電源OFF・現行lock無し・現行run成功を主張しない。PCの電源、owner、active.lock、CPU/RAM、現行QUEUE・RUN_RESULT・V3/V4は**不明**。

認可済みLibraryの`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`と`Vahren(2).exe`を正規取得し、原本を変更・実行せず、ZIP収録の2026-10-21静的検索DBを一時コピーしてread-onlyで照合した。ZIPは34/34件CRC PASS。SQLiteの`PRAGMA integrity_check=ok`、DB SHAと同梱BUILD_MANIFESTが一致した。新規Ghidra/REA再実行は各0回。

| 入力 | 実測SHA256 |
|---|---|
| 原作EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内検索SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |
| 先行17:35 REA JSON（参照専用） | `730FEB55D8716C97C66FA9B7DA1C0328B79CFD976F951823B218C8FC586E6132` |

ZIPの旧`PROGRESS.md`は2026-10-09の初期15/16を示す。過去報告Wave1～5の64/64 VERIFIEDは**今回再検証なし**。異なる分母を加算せず、正式REA5種証拠への自動昇格もしない。

## 2. 増分A：例外的に見えた`0x4322E7`の`[EBP+0x10]`がcontext+0x10と判明

先行17:35の11件横断調査では、`0x4322DF MOV ECX,[EBP+0x10]`だけが他の`[ESI+0x10]`と違って見え、レイアウトが同一か未確定だった。今回は**同じ親関数`0x4321B0`の前方に戻り、EBPの再代入元とガードまでPE実命令で追跡した。**

```asm
0x4321EB  mov ebp,[esp+0x12C]  ; 当初は親オブジェクト側
...                               ; 当該分岐内
0x4322B2  mov ebp,[ebp+0x04]  ; EBPをcontextポインタに置換
0x4322B5  mov edi,[ebp+0x20]  ; context+0x20の事前取得
0x4322D6  call 0x416B90      ; 先行の木構造操作（既知）
0x4322DB  test edi,edi
0x4322DD  jne  0x4322E9      ; 非ゼロ時はvcallをスキップ
0x4322DF  mov ecx,[ebp+0x10] ; 実際はcontext+0x10の二次オブジェクト
0x4322E2  mov eax,[ecx]      ; vptr
0x4322E4  mov edx,[eax+0x1C]
0x4322E7  call edx
```

**局所的な結論：** `0x4322B2`を通る経路では、`0x4322E7`の受信者は`context+0x10`が指す二次オブジェクトであり、CALLのゼロガードは**同じcontextの`+0x20`**に由来する。`0x4322DF`のEBP表現は別レイアウトを示す証拠ではなかった。MSVC x86の通常ABIどおり呼出先がEBPを保持するという前提は残る。

17:35に確認済みの「11件のslot+0x1C」を**12件や新たな11件として再計上しない**。同じ静的パターンと見なせる根拠は改善したが、すべてが同一の実行時インスタンス・クラス・vptrを持つことは未証明。

## 3. 増分B：`0x543AE0→0x5433D0`の実際の呼出ABI

先行報告では`0x543428`から参照するオブジェクトが`context+0x10`由来であること、`0x5433D0`の登録副作用まで確認済み。一方、`0x543AE0`のGhidra疑似Cは`FUN_005433d0(param_2)`と表示し、数値引数だけで呼び出しているように見える。しかし原作EXEのレジスタ操作は以下のとおり。

```asm
0x543AE2  mov edi,[esp+0x0C]  ; wrapperのスタック上の数値引数
0x543AE6  push edi            ; 補助関数へ引数を積む
0x543AE7  mov esi,ecx        ; ECXはこの間そのまま
0x543AE9  call 0x5433D0

0x5433D5  mov esi,ecx        ; 登録対象this = ECX
0x5433D7  mov eax,[esi+0x04] ; context = [this+4]
...
0x5433F3  mov esi,[esi+0x04] ; ESI = context
0x5433F6  mov ebx,[esi+0x20] ; 事前取得ゼロガード
...
0x543420  mov ecx,[esi+0x10] ; contextの二次オブジェクト
0x543425  mov eax,[edx+0x1C]
0x543428  call eax
...
0x543430  ret 4              ; 追加のスタックDWORDを回収
```

**局所的な結論：** `0x5433D0`の実際の対象は**ECX内のオブジェクトポインタ**。スタックの1 DWORDは関数終了時`RET 4`で回収されるが、今回検査した関数全体の命令でその値が処理に使われる形跡はない。Ghidra疑似Cに現れる`param_2`を「登録対象ポインタ」と誤って解釈してフックの宣言・再実装をしてはいけない。

独立した別caller `0x543440`も`0x543441 PUSH 0`→`0x543443 MOV ESI,ECX`→`0x543445 CALL 0x5433D0`の経路を持ち、`0x5433D0`のECX受信と`RET 4`を裏付けた。`0x543AE0`自身も`RET 4`（`0x543B00`と`0x543B08`）を使い、別フレームの引数をそれぞれ回収する。

## 4. 増分C：contextの伝播と未確定の動的vptr

`0x543A30`のコンストラクタでは`0x543A63 MOV [ESI+4],EAX`により、FadeSheet側`this+4`へ受領したcontextが保存され、`0x543A66 ADD EAX,0x88`で別ポインタを算出する。`0x5433D0`の`0x5433F3`はこのcontextを取得し、`[context+0x20]`のガードと`[context+0x10]`の仮想受信者へアクセスする。

この経路は**`0x4321B0`のevent枝と同じ`context+0x10/+0x20`オフセット解釈**と整合する。ただしcontext生成時に`+0x10`へどのポインタが代入され、その実体のvptrがどこで設定されたかは未解決。したがって間接CALL `0x543428` / `0x4322E7`の実装先VA・クラスの同一性・描画更新かどうかは**VERIFY**のまま。

`0x43400E→FadeOutSheet vtable+0x18→0x543AE0`の先行条件付き特定、`0x5433D0`での登録順序、11件の同形CALLはいずれも**過去成果**であり今回の新規カウントに含めない。`0x5AA6E0`ジャンプテーブル警告も未解決のまま、勝手に12件目に加えない。

## 5. 検証結果と正式進捗

| 検証/指標 | 今回の結果 |
|---|---|
| 実PE命令バイトの固定位置照合 | **39/39 PASS** |
| `E8 rel32`直接CALL先照合 | **6/6 PASS** |
| SQLite関数本文SHA再計算 | **5/5 PASS** |
| SQLite直接CALL索引 | **4/4 PASS** |
| SQLite間接CALL索引 | **2/2 PASS** |
| オフラインDB整合性 | PASS |
| 新規REA正式5種セット | **0** |
| 新規REA VERIFIED | **0** |
| 正式TODO/VERIFY/BLOCKED差分 | **0/0/0**（PC正本未変更） |
| 原作実機Golden PASS / strict MATCH | **0 / 0** |
| REA・Ghidra・ゲーム起動 | **0 / 0 / 0** |
| 静的検証器のみの経過 | **1.162秒** |
| 調査全体の時間 / 研究PC CPU・RAM | 未計測 / 不明 |

5種区分：`info`=旧Ghidraメタデータのみ、`pseudo`=旧Ghidra擬似Cのみ、`assembly`=原作PE固定バイトの独立検証（REA実run出力ではない）、`callers/callees`=旧SQLite索引のみ。**正式REA五種証拠の新規完成はゼロ。**

## 6. 保存と再開位置

再検証用Python：`verify_rea_t014_context_alias_abi_20261022.py`。機械可読JSON：`REA_OFFLINE_20261022_1836_T014_CONTEXT_ALIAS_ABI_EVIDENCE.json`。この文書：`REA_OFFLINE_20261022_1836_T014_CONTEXT_ALIAS_ABI_AUDIT.md`。

今後のP0：**`context+0x10`の代入元**を特定し、指されるオブジェクトのコンストラクタ／vptr設定を原作ASMで照合する。`0x543428`の静的呼出先候補を得た場合も、動的な型の分岐と安全なABIを再検証する。`0x5AA6E0`は別件VERIFYとして扱う。

PC復旧時は**最新**MASTER・QUEUE・PROGRESS・REA run/evidence・owner・lock・入力ハッシュ・既存ID・V3/V4競合を読んでから、一度だけ許可されたREA担当範囲へ統合する。接続障害記録ID：`REA-RC-20261022-1836-LOCAL-SESSION-TERMINATED-01`。安全拒否済み0x5710C0..0x571500/Wave6/REA exportは経路を変えて再試行しない。

**保存状態:** 作成直後はコンテナのみ。Library保存と独立readbackは別途実施し、その成否を実測結果として報告する。PC正本未同期。
