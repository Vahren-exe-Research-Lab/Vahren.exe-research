# E-AUDIT-20261028-12H-T020-T028-NULL-VECTOR-OWNER-CLEANUP-01
Owner E / T020。2026-10-28 12H JST。STATIC ORIGINAL BYTE VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY。
## 出典・継承
- Local Compactオンライン。MASTER TASK QUEUE、規約、A-D HANDOFF、REA PROGRESS、DEV実装計画、T018/T019、旧検索索引と現行V3案内をread-only参照。Ghidra・Java再解析、原作ゲーム実行なし。
- B最新 B-20261028-1217-T028-NULL-VECTOR-CANDIDATE-DESTRUCTION-01 はSTATIC/VERIFY/NOT READY。B資料 data/T028_NULL_VECTOR_CANDIDATE_DESTRUCTION_NATIVE_20261028_12H.md 実バイトSHA256 890DB7A710BA6747B9B29F7A0A6485081A062C7DCAC99D3C8747A8E05772D13B（今回Eテスト照合）。
- 前回E11テスト実バイトSHA256 A5476B07415F52CEA7BA3CBE75E7A094DAAAF37F401FE704E280A220566E1868。B11候補vectorと第2RB集合の区別は既済であり再計上しない。
- 研究用原作PE rea_lab/targets/hakushin067_Vahren.exe 2910720B、実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。本回Python read-onlyで実バイト検証、ゲーム起動なし。
## 新規T020クロスウォーク
- 0x497C0D/0x497C12のcandidate+0x77/+0x75両方zeroの時、ECX非0なら0x497C31→0x4C1290 vector append、ECX==0なら0x497C21→0x463590 cleanup経路。flag非0は別枝であり「null ECXなら常に破棄」と単純化しない。
- 0x463590系はowner+0x2FCの木を対象に0x49F410範囲計算→0x4BF820処理を呼び、0x460F10側でowner+0x330検索・照合一致時にowner+0x32C索引eraseとrecord+0x94/+0x84ゼロ化を行う局所経路がある。
- 同経路candidate非NULLなら0x4591F0資源解放様呼出と0x5B6BBB解放呼出へ進む。関数呼出の存在を索引削除成功数、Unit死亡、士気減少、外部別名ポインタの安全な寿命と同一視しない。合法ゲーム到達も未証明。
- EXE 0x463590 117Bと0x460F10 377Bの2窓SHA256をB12値と2/2一致。E8 REL32 0x497C21、0x4635A7、0x4635BA、0x4635DE、0x4635E4、0x4635EE、0x4635F4、0x460F95、0x46103E、0x46106Aの10/10一致。V3検索基盤はB側PASS報告を継承、EからV3 guardを新規実行したとは主張しない。
## 回帰テスト・受入判定
- E新規 tests/t020_t028_null_vector_candidate_cleanup_gate_20261028_12H.py SHA256 F996015AD9DB989B7CE060AB46B4F1D9970F346A4110DEE8FAB7CFC7DFF5CAA6。
- Python -B unittestで新規32/32 PASS（exit 0）、既存11H 30/30 PASS（exit 0）、今回の2ファイル合計62/62 PASS。累積全T020のPASS数ではない。32件には2入力SHA、元EXE SHA、2窓、10 CALL、flag/ECX条件、ownerとcandidateのpointer有効性、run同一性、比較一致/不一致、不明時の観測保留、Golden否認を含む。
- 合成モデルのrange_erase_callは命令経路を表すだけで実削除件数はnull。候補寿命・外部参照・忠誠/死亡/士気の値も未観測null/falseで、原作Gameplay再現成功として扱わない。
- T018原作合法G0=画面からの戦闘開始・同run操作、G1=同一戦闘直前SAVEバイトSHA+順序付き入力、G2=現物MAPバイトSHA+三陣営+配置順のUnit/Troopをまず必要とする。G3=可視終戦、G4=戦略World差分も同runで接続する。空手20倍テストDATを無改変原作DATとしない。
- 今回の新規原作DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。合成PASSをactualに昇格しない。T020作者変更5系列6条件、GameClear/loaderなどの原作比較はNOT RUN。
- T019新規確定矛盾0、確定BUG0。GameClear DAT13/TXT2の字句検索範囲差SOURCE-SCOPE RESOLVED維持。script2同名優先、phase flag、TXT実読込、gwrite復帰、候補破棄がゲーム上の敗走/死亡を表すかはVERIFY。
## MASTER・保全
- MASTER TASK QUEUEを今回独立再集計：34件／一意34、DONE9、IN_PROGRESS21、VERIFY4、ID重複0。最後に記録された正式checkpoint196/READY596=A115/B229/C136/D116は既存値を継承（READY全履歴の再集計なし）。
- B12はNOT READYなので新規正式READY統合ID0、MASTER更新0。A-D/REA/dev_lab/原本EXE・ZIP・DAT・SAVE/Git/push/Work/設定/スケジュール変更0。
- 既存のT018表境界/session-join、T019旧XREF、C T026/T032、D T030 TSV、0x5710C0および他拒否済み操作の再試行・別tool/shell/path/Remote/ZIP迂回なし。今回新安全拒否/接続障害0。10月25日OFFLINE-UNSYNCED全文と他owner完全意味重複照合は未解決。
- 初回報告書作成用JavaScriptが引用符の構文エラーで失敗（OTHER/RECOVERED、PC書込処理は呼出前）。再構成した別文書本文で初回正式書込を実施。本回のPC書込はE所有の新規テストと本報告書だけ。
## 次の優先
P0：C-NB02合法原作G0+G1+G2同run一次受入。P1：0x497BB0のnull ECX producer、owner+0x2FC/+0x32C索引と候補の参照寿命、別vector+第2RB集合の真consumerを局所callと実ゲーム効果に分けて追跡する。
## 復旧識別・保存確認
RECOVERY-ID E-RC-20261028-12H-DOC-JS-LITERAL-OTHER-01。初回JavaScript文字列構築のSyntaxErrorによりPCへのwrite_file呼出前に失敗。影響は研究報告書の未生成のみで原本・他ownerへの影響0。後続の許可されたE新規文書保存操作で復旧、報告書26行の独立readback・本Python152行の独立readback成功。元の失敗したツール呼出は拒否ではなくOTHERで、禁止済み安全拒否の迂回に該当しない。最終SHAは次回receipt/会話結果を参照。
