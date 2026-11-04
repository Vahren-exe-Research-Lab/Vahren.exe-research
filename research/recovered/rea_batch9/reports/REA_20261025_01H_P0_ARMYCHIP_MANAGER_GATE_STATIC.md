# 迫真戦記ver0.67｜REA 2026-10-25 01時台 P0：ArmyChip manager同一性条件・待機キュー移送・終了ゲート
研究ID: `REA-LOCAL-20261025-0131-P0-ARMYCHIP-MANAGER-TRANSFER-EXITGATE-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。既存成果の再認定ではなく、新たなアドレス連鎖の条件付き補強。
原作SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
先読: MASTER・規約、REA README/QUEUE/PROGRESS、既存runsと `progress_sync_20261011T153958076Z.json`、2026-10-24 22H/23H・2026-10-25 00H報告、旧索引manifest、統合V9入口。保存済みWave1～5は**64/64**（最新同期ログ、既存実績、今回増加0）。QUEUE/PROGRESSの旧表示はEPERMでstale。原本・DBのSHAは今回再計算。
## 今回追加した独立の静的連鎖
**A. Builderからmanagerへの式の再利用**
- `0x005B06EA`: `builder+0x24=ESI`（生成時のowner引数X）。
- `0x005B0843/46/4A/4D`: `EAX=[X+0x0C]` → `EAX=[EAX+4]` → `EAX+=0x0C` → `0x004C2240`。登録はmanager Mの`+0x64/+0x68` vectorへ。
- `0x005B0B42/45`: builder処理でも`EDI=[ [builder+0x24] + 0x0C]`を取得。`0x005B0B9D/A1/A4`で`EAX=[EDI+4]+0x0C`を介して`0x004C2440`に子を渡す。この呼び出しはmanager Mの`+0x44/+0x48` vectorへの追加。
- よって**builder+0x24のownerと中間ポインタが不変なら、生成時の親登録と後の子破棄予約は同じMを使用する**。この範囲のレジスタ命令列を原作PEで独立照合。途中のowner/vptr変更や別インスタンス混入は未否定。
**B. managerが待機vectorから処理vectorへ渡す境界**
- `0x004B996B/99DF/99E0`: 親ゲーム処理の`root+0x0C`を`0x004C24B0`に渡す。呼出元`0x00555E35`はrootとして`0x008BE2F0`を設定する。
- `0x004C2712/2714`: `0x004C24B0`は同じ引数をESIに移して`0x004C28D0`を呼ぶ。
- `0x004C2980/83`: `manager+0x64/+0x68`の待機vectorが非空か判定。`0x004C2996/99`: `manager+0x2C`を第1ベクタの入口として`0x004FAA60`を呼ぶ。V9擬似Cの同関数はsource範囲要素をvectorへ挿入する構造。ABI正式検証は未了。
- `0x004C29C3`: 移送処理後、待機vector終端`manager+0x68`を更新。**生成直後のbuilderは主処理vectorに直接置かれるのではなく、別の待機vectorから処理側へ取り込まれる**静的経路がある。

**C. 子キューのdestructor呼び出しは毎tickではなく、内側ループを抜けた後に配置される**
- `0x004C2780/83/86`: managerの`manager+4`が指す状態`+8`を検査し、ゼロなら`0x004C2500`へ戻る。非ゼロなら下方の遅延破棄処理に進む。
- `0x004C278C`: 条件付きキュー `manager+0x54/+0x58` の走査開始。`0x004C27C1`: vtable`+0x14`述語を確認した要素について削除フラグ1の仮想destructor。
- `0x004C27FB`: 子キュー `manager+0x44/+0x48` の走査開始。`0x004C281F/2821/2823/2825`: 非NULL要素についてvtable先頭に削除フラグ1で間接CALL。
- **この関数内では両キューの破棄は`0x004C24B0`のループ継続条件が非ゼロになった後。** したがって`0x004C28D0`の各tickで子を即時deleteする実装は原作の当該経路と異なる可能性が高い。ただし別関数からの早期解放、例外、モード遷移、ループ再入の動的実測は未了。ゲーム全体の終了時だけという意味ではない。
## なおVERIFYの条件
1. `0x005B06EA`のXを経由したroot `R=[ [X+0x0C] +4]` と、`0x00555E35`のゲーム側root `0x008BE2F0`が実行中の同一インスタンスかは**未証明**。両manager式の値が同じとは、まだ断定しない。
2. Mのポインタ寿命・vptr維持・派生型や重複登録・pending→activeの完全な転送意味（`0x004FAA60`のABI）・キューの別経路消費/再入が未解明。
3. `0x004C24B0`退出時に有効な全キューを毎回破棄するかは、異常中断や他threadを含め未実測。
## 静的監査・非重複
新規独立監査 `REA_20261025_01H_P0_ARMYCHIP_MANAGER_GATE_AUDIT.py`: **73/73 PASS**、保存後別プロセスで再実行 **73/73 PASS / INDEPENDENT_READBACK PASS**。原作・V9 SHA、PEのx86命令、E8相対CALL、V9 native_callsite、ABI未検証フラグ、SQLite quick_checkを照合。
初回は**71/73**: Ghidraの関数byte countが途中のx86命令を切っていた2件を誤って「関数全バイト一括decode」に使った検証器の想定ミス。調査し、該当2関数は**対象命令までの既知prefixのdecode確認**に変更。別の調査用Python -cの構文エラー1件もコード実行前に発生。いずれも安全拒否ではなく、先行成果の消失や原本変更なし。
前回00時台の60/60・35/35と検査が一部重複するが**新規関数数やVERIFIEDに加算しない**。今回の新たな焦点はownerポインタ式・待機→処理移送・内側ループ出口ゲート。
正式REAの新規5種一式(info/pseudo/assembly/callers/callees) **0関数**、新規VERIFIED **0件**。正式TODO/VERIFY/BLOCKED書込差分 **0/0/0**。旧Wave1～5の64/64は保存済み同期記録、今回再取得なし。ゲームGolden PASS **0件**、strict MATCH **0件**、完全複製率未測定。
## 安全・再開点
PCオンライン、REA active.lockなし、空きRAM約15.68GiB、CPUスナップショット約32%（瞬時値）。Ghidra/REA/原作ゲーム新規起動なし。監査1.816秒、独立再実行1.105秒。全調査所要時間未計測。安全拒否済み`0x004BC9C0`検索・Wave6・`0x5710C0..0x571500`・REA exportの再試行/迂回なし。
新規ファイルはREA所有decomp_taskのみ。他owner/MASTER/QUEUE/PROGRESS/既存runs・EXE/ZIP/SAVE/Git/Work/スケジュール無変更。owner/lock/既存ID衝突確認済。
**次の関数/根拠:** P0 `0x005B0680`のowner引数Xの生成元（直接CALL `0x004917B3`,`0x00491E99`）、`0x00555CD0`の`0x008BE2F0`とRの対応を実バイト・参照で追う。次点`0x004FAA60`の正確なsource/destination条件と管理vector再入の安全性。Golden条件はbuilder0/1/複数、pending→active tick、子登録後にloop継続とexit、重複child、モード再入（**DESIGNED / NOT RUN**）。
