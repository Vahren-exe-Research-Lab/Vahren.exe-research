# 雇用並替えDLLの共通Core移植メモ

2026-10-25 / Work / 状態 PARTIAL（調査、未移植）

## 対象と根拠
利用者指定 dist/HakushinRecruitSort-0.1.0-preview.zip は人材雇用4分類ツール。BattleObserverは含まれない。ZIP SHA256: 27040aa51b02c497ce2824986f7f44130dc7ebee3f7748c3be97ad934a4fb9f0。
DLL SHA256: ffdc73d2f416ab29d89089bdafee487b712b85d693426c31db4539bac3e0c981。manifest照合済。対応ソースは data/recruit_sort_v4/src/hakushin_recruit_sort_v4.c、native_priority_v4.c、hire_ui_native_readonly.c、trace_v4.c、original_exe_attach.c。tools/build_v4.ps1とreports/V4_ENGINEERING_AUDIT_20261021.mdが対応を示すが、再現ビルドの証明ではない。

## 現行実装の寿命
HakushinSort_Install（src/hakushin_recruit_sort_v4.c:407）はstdcall。アンインストール/終了処理exportはない。DllMain自体はthread通知無効化のみ。
原作module baseからの8箇所（RVA D462B,D84FA,D8611,D861D,D8BDA,D8BE6,A5B28,A5B54）の5byte CALLを変更する。元targetはD4A50。導入前にPE/timestamp/image size/描画関数prefix/CALL target等を検証するがDLL単体の完全EXE SHA照合ではない。
rewrite_call（392行付近）は保護属性変更・書換え・命令cache flush・保護復元を行う。Install失敗時は途中まで戻すが、復元失敗も単純な失敗戻り値に集約される。失敗だから安全にDLL解放できるとは限らない。
SetTimer(NULL,0,16,retry_view)によるUI thread上の遅延再描画がある（280行付近）。window/surface/tagを保持。KillTimerのみで既に配送中のcallback消失を証明しない。既存attach経路は永久pinで寿命を保つ。

## 移植する順序
1. 元ABIと原作CALL ABIを維持したまま、専用query/init/shutdown adapterを追加する。既存配布物は上書きしない。
2. 共通Coreからinstance専用の予約APIを受け取り、8範囲すべてを予約してから実patchへ進む。予約はmetadataであり、patch成功の証拠ではない。
3. 導入と取消は原作UI threadで実行する。汎用Core initを呼ぶthreadだけで安全とみなさない。
4. 実patch側に直前のexpected/owned bytes照合と失敗復元の結果を保持する。未解決時はDLLと予約を残す。
5. 新規処理停止→timer取消→実行中callbackの完了確認→owned bytes検証と原状復元→予約解除→shutdown成功の契約を実装・検証する。
6. 維持中のtimer/messageや不明な復元結果があればshutdown成功を返さない。過渡版はprocess終了までpinを維持してよいが、unload可能とは表示しない。

## 制限
現在はmetadata予約管理とCoreへの接続を実装中。実hook共通化・callback drain・雇用DLL移植は未完了。既存の雇用成功/並替え実機証拠を壊さず、小さな試験から進める。原作EXE/DAT/saveファイルは変更しない。ランダムfriend cache初期化による乱数消費の既存制限は維持する。


## WORK-MANAGED-CALL-MIGRATION-PRECONDITION-20261025
Core extension3がfixtureで利用可能になったが現行雇用adapterへ直接接続しない。現行adapterはinit時に8予約を取り、UI threadでlegacy HakushinSort_Installを実行する。worker/UI callbackからCoreへは現状呼び出していない。Core APIはcaller直列化契約である。UI callbackをmanaged installへ置換すると、他pluginのstartup init中と重なり得るため、Core API全体のthread直列化または明示的なstartup完了dispatch契約を先に設計・検証する必要がある。既存8 metadata予約はmanaged installと重複するためそのまま移植不可。
移行時はlegacy installerのhost照合/GDI準備/renderer ABIを維持し、managed patchのowner handleを全8箇所で管理し、途中失敗時逆順復旧と未復旧保持を試験する。これは原作処理threadのquiescence証明とは別問題。現行DLLは永久pin/停止拒否を維持し、hot unloadを追加しない。ゲーム配置や既存ソート挙動は未変更。


### Core thread gate実装済み（2026-10-25）
WORK-CORE-THREAD-GATE-20261025にてCore内部の同時呼出し拒否を実装/fixture検証した。先の移行前提のうちCore metadata競合は対応済み。adapterはまだ移行しておらず、BUSY時にUIを停止させず次回messageへ延期すること、既存予約とmanaged installの重複、部分失敗rollbackとpin保持は残る。原作のpatch実行thread/quiescenceの保証とは別である。
