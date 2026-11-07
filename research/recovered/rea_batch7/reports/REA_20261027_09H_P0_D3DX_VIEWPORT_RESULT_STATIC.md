# 迫真戦記 ver0.67 REA｜P0 Viewport取得→逆投影→交差計算→2D変換の未検査結果伝播
研究ID: `REA-LOCAL-20261027-09H-P0-D3DX-VIEWPORT-RETURN-FLOW-STATIC-01`
日時: 2026-10-27 09時台 JST。状態: PC-SAVED / STATIC / VERIFY / NOT READY。原作Golden: NOT RUN。
原作EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 新規静的証拠と先行研究との区別
07Hは0x00559990のFPUループの終了条件、08Hはz=0平面/理想幾何/通常約42反復の合成モデルを記録した。本回ではこれらの成果は破棄・二重計上せず、**vtable +0xC0の戻り値検査有無、スタック出力の実引渡し、失敗出力を消費する後段の新関数**を対象限定で原作PE機械語から調べた。原作実行・REA/Ghidra再実行はゼロ。
関数0x00559990は保存Ghidra索引で915バイト、直親0x00559690の直接CALL siteは0x00559830（旧/V9 DB双方）。新規後段0x004C3C20は264バイト、旧/V9 DB双方に7直接CALL siteを確認した。

## NEW STATIC: vcall+0xC0結果を検査しない
0x005599E4 `LEA EDX,[ESP+0xF0]` → 0x005599EF `PUSH EDX`、対象グローバル0x0087980Cのvtable +0xC0を0x00559A22で取得して0x00559A28 `CALL EAX`。このスロットはDirect3DDevice9 GetViewport相当の候補。戻り値EAX/HRESULTを0x00559A2A以降で判定せず、次の平面・行列計算へ進む。
`S`=各stdcall呼出し前の安定ESPとすると、0x005599E4の出力バッファ候補は`S+0xF0`。D3DXVec3Unproject呼出し0x00559BCF/0x00559BFEの第3引数用`LEA [ESP+0xFC]`（その時点で12バイトPUSH済み）も同じ`S+0xF0`に対応する。したがってViewport出力がそのまま逆投影に入力されることをABI上確認。
GetViewportが常に成功するか、失敗時にAPIが出力バッファをどう変更するかは未実測。vptr実行時の型同定もVERIFYで、失敗や未初期化値の実害は断定しない。

## NEW STATIC: 2回のUnprojectと交差点は戻り値判定なしで連結
0x00559BCF, 0x00559BFEはPE IAT 0x006092DC=`D3DXVec3Unproject`をESIから呼ぶ。第1出力は`S+0xE4`、第2出力は`S+0xD8`。両方とも戻り値を条件分岐に使用せず、0x00559C1DのEBX（PE IAT 0x006092E4=`D3DXPlaneIntersectLine`）へ入力される。
交差点出力は`S+0xCC`。0x00559C1D `CALL EBX`の**直後**0x00559C1F `FLD [ESP+0xCC]`、0x00559C42 `FLD [ESP+0xD0]`でx/yを読む。NULL相当の失敗返却や交点出力未更新の場合でも原作側に明示的な直後ガードはない。交点不成立の実際の到達性、FPU例外/NaNの挙動はVERIFY。
## NEW STATIC: 結果の後段consumerで寸法割算
初期化ループ終了時0x00559D11はfloat走査値を`DAT_00879838`へ格納する。旧検索FTSで別関数0x004C3C20がこの値を参照し、限定逆アセンブルで0x004C3C4F `FLD [0x00879838]`を確認。
0x004C3C20は`[ESI+0x54]`、`[ESI+0x58]`を整数寸法として用い、0x004C3C93、0x004C3CBB、0x004C3CD9で`FIDIV`する。関数全体0x004C3C20..0x004C3D27にはCMP/TEST/条件分岐がなく、内部にゼロ寸法ガードは見えない。
同関数はPE IAT経由で`D3DXMatrixScaling`(0x006092D8)、`D3DXMatrixTranslation`(0x006092F0)、`D3DXMatrixMultiply`(0x006092D4)を呼ぶ。直接CALL sites: 0x0048B2E6, 0x0048BBBA, 0x0048BEAF, 0x004C2D28, 0x00520546, 0x00520758, 0x005208BC（双方の検索DBで一致）。
幅・高さが0なら数値異常となり得るが、**呼出元から0を渡せるか/実機でどう動くかは未調査**。FPU制御ワードやAPIの入力保証を未確認のままバグ確定としない。

## 再実装・Goldenの実験設計（まだ未実行）
GetViewport失敗、Viewport幅/高さゼロ、Unproject戻り値失敗、平面と線の平行条件、NaN/Infを含む交点について、原作と新実装で関数の返却/出力値・ループ終了回数・計算された`DAT_00879838`・後段2D変換を別々に観測する。実行中ゲームへ介入せず、別の許可済み実験環境を確保してから検証する。
原作互換のため失敗時処理を勝手に追加するのではなく、まず再現条件と観測結果を区分し、strict原作互換と安全性改善案を別管理する。

## 監査・安全・差分
`REA_20261027_09H_P0_D3DX_VIEWPORT_RESULT_AUDIT.py`で原作PE・旧/統合V9 DB SHA、read-only SQLite quick_check、旧RUN64/64、08H=74/74、限定ASM・IAT・両DB CALLを照合。最初51/52は**監査スクリプトの1命令指定ミス**（0x004C3C65と0x004C3C67の混同）であり、当該新規監査スクリプトのみ訂正して52/52 PASS。原作解析に失敗したものではなく、安全拒否でもない。
5種証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。新規正式VERIFIED=0（既存64保持）、正式TODO/VERIFY/BLOCKED更新差分=0/0/0。原作Golden PASS=0。strict MATCH・完全複製率=未測定。
旧QUEUE/PROGRESSには既知EPERM由来の表示不整合あり。正本は従来の保存RUNと`logs/progress_sync_20261011T153958076Z.json`（64/64、QUEUE STALE_RENAME_DENIED）を優先し既存ファイル更新なし。
事前PC接続成功、active.lockなし、空き物理メモリ約16.65GiB（WindowsのKiB表示から換算）、CPU負荷は未測定、監査単発約1.88秒、作業総所要時間は未計測。REA/Ghidra/ゲーム/Work新規起動0。原本・MASTER・A～E・QUEUE/PROGRESS・既存runs・Git・スケジュール変更0。

## 次回P0
0x004C3C20の7親のうち、幅/高さを+0x54/+0x58へ設定する経路を限定追跡し、ゼロ値到達性を判定。0x00559690のdevice設定からvtable +0xC0の実装同定・異常Viewportの発生条件、交差API失敗時のpOut契約を追加検証。後段の危険性は実測までVERIFY/NOT READY。
