# REA P0｜DirectSound8 Unlock戻り値と二段階cleanupの独立静的監査（02時台）
研究ID：REA-LOCAL-20261026-0238-P0-DS8-UNLOCK-RETURN-IDEMPOTENCE-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY。担当REA専用証拠、原作Golden実測0、新規正式REA VERIFIED0。
元EXE SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
検索DB SHA256：0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
前回ID：REA-LOCAL-20261026-0136-P0-DS8-SHUTDOWN-REFILL-DOUBLE-CLEANUP-STATIC-01
出典：既存Ghidra12.1.4検索DB（疑似C、直接・間接CALL索引）＋上記SHAの原作コピーをCapstone独立逆アセンブル。

## 新規P0発見1：Lock成功後のUnlockエラーが成功扱いになる
- 0x00502387: CALL EAX＝buffer8 vtable+0x2C（IDirectSoundBuffer8::Lock想定）。
- 0x00502389 TEST EAX,EAX / 0x0050238B JS 0x005023C9：Lock失敗時は0x005023CB cleanup→AL=0で復帰。
- 0x005023A0：decoder側vtable+0x04間接CALL（返値の成否判定なし）。
- 0x005023BF：buffer8 vtable+0x4Cの間接CALL（IDirectSoundBuffer8::Unlock想定）。戻り値の検査・分岐なし。
- 0x005023C2 MOV AL,1：UnlockのHRESULT値にかかわらず、正常経路はAL=1を返す。
- 上位0x005022E9が0x00502330を呼び、0x005022EEでTEST AL,AL。1なら0x00502300で__beginthreadまで進み得る。
結論：Lock非失敗という条件下で、Unlock失敗を初期化成功として扱う制御経路を静的確定。Unlockが実ゲームで失敗する実測、クラッシュ、音声破損は未確認。COM対象同定は通常のIDirectSoundBuffer8 vtable構成に依存。

## 新規P0発見2：2回cleanup経路でのポインタ解放抑止
- 0x004BF31C→0x00502330、Lock失敗で0x005023CB→0x00502160を1回実行。
- 0x00502160は+0x08がNULLでなければ0x005021A5からRelease、+0x00がNULLでなければ0x005021B2/0x005021C0からcleanup/destructorを呼ぶ。
- 正常復帰時0x005021C2でstream+0x08=0、0x005021C5でstream+0x00=0、0x005021C7でstream+0x44=0とする。
- 呼出元0x004BF321で同一所有ポインタを取り直し、0x004BF327で2度目の0x00502160を呼ぶ。
- 通常の直列実行で+0x00/+0x08の再設定がない限り、2度目のRelease/decoder destructor呼出はNULLガードで省略される。
注意：例外・異スレッド並行動作・外部仮想メソッド副作用まで二重解放防止を証明したわけではない。前回の『2回cleanup経路』とは独立の追加状態追跡。

## 監査範囲・新旧カウント
- 新専用監査：52/52 PASS（原作・DB各SHA256、PE ImageBase、原作機械語の厳密一致、関数サイズ・直接/間接CALL、SQLite quick_check、Unlock戻り値未分岐）。
- 初回約0.6834秒、保存実行約0.575秒（監査単体）。研究全体時間・CPU負荷は未測定。
- 旧Wave1〜5：2026-10-11のprogress_sync_20261011T153958076Z.jsonで64/64保存済み。QUEUE/PROGRESSはEPERMによる古い表示なので更新しない。
- 今回の5種証拠：info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_SOURCE、callers=INDEX_ONLY、callees=INDEX_ONLY。新規5種完備=0、新規正式VERIFIED=0。
- 正式TODO/VERIFY/BLOCKED書込差分0/0/0。独立VERIFY候補は2点、正式キュー未変更。ゲームGolden PASS0、strict MATCH/複製率未測定。
- 旧23時台FLS検索・監査の安全拒否、Wave6、禁止VA 0x5710C0..0x571500、REA exportを再実行していない。
- 今回は新REA/Ghidra/ゲーム実行0回。変更範囲はrea_lab/decomp_task/内の新規固有名ファイルのみ。MASTER・他レーン・QUEUE・PROGRESS・Git・スケジュール無変更。

## 実機Goldenの試験設計（実施0）
A. 正常：Lock/decoder fill/Unlockが成功し、AL=1でワーカー生成へ到達。
B. Lock HRESULT<0：内部cleanup、AL=0、上位で再度cleanupしてもNULLガードを満たす。
C. Lock成功・Unlock失敗：実機障害注入環境で原作はAL=1を返すか、音声/リソース状態がどう遷移するか（未実施）。
D. Lock成功・decoder fillが異常を返す場合：返値が無視される条件、長さ/データ整合性（未実施）。
E. 解放処理とワーカースレッドの並行終了：レース・例外経路は実機未検証。

## 再開位置
次回P0：0x005023A0 decoder vslot+0x04の引数・戻り値型とバッファ書込サイズ。0x005023BF Unlock 4引数と二領域Lockの整合を確認。初期化0x00502220とshutdown 0x004BF2B0で同じ戻値をどう扱うか比較する。
オフライン13/14時台のLibrary成果は未同期という前回状態を維持し、今runで新たに同期済みとは主張しない。
