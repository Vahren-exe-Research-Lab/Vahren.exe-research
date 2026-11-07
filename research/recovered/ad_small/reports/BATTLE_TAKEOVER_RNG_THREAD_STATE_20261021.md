# 外部戦闘EXEへ移行するための原作CRT乱数の境界研究
ID: BRIDGE-20261021-RESEARCH-02-RNG
状態: 原作PE機械語検証済みSTATIC / runtime未観測 / 外部EXE未接続
EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
既存A/T031で中央reseedingやrand式が研究済み。今回の新増分は戦闘場面構築前後と外部プロセス引渡し境界への横断照合であり、T031の成果を新規発見として二重計上しない。

## 1. 戦闘場面構築でのseed更新
- 元PEの0x48D810で0x4C1FC0 CALLを確認。同時に0x48D6A0ではこの処理より後に0x4F6540などのUnit/Troop構築処理が見える。
- 0x4C20B0でcall dword ptr [0x609164]、戻りEAXをpush→0x4C20B7でcall 0x5B6E99。戻り値をCRT seedとして受け渡す。関数ポインタ実装・seed数値・時刻単位を推測で固定しない。
- 0x5B6E99は0x5BC6A9(__getptd)を呼び、戻ったスレッドデータ+0x14へseedを書き込む機械語を確認。
- 0x5B6EABも同じ0x5BC6A9を呼び、_holdrand(state)+0x14を読んで新しい状態を同じ+0x14へ保存する。

## 2. 正確に確認できたMSVC CRT rand()の更新則
- state_next = (state * 0x343FD + 0x269EC3) modulo 2^32
- rand_value = (state_next >> 16) & 0x7FFF
- 元PE 0x5B6EB5 IMUL, 0x5B6EBB ADD, 0x5B6EC0 store, 0x5B6EC3 SHR, 0x5B6EC6 ANDから直接一致。
- 参考: seed=1の最初の8回出力は 41,18467,6334,26500,19169,15724,11478,29358。元ゲームを実行した出力ではなく、機械語式を模した合成演算の結果。
## 3. 外部戦闘EXE bridgeへの影響
- 原作戦略から戦闘へ入る前のseedだけを渡すのは不十分。初期化から最終開戦までに再seedとdrawが存在し得る。
- CRTの_holdrandはスレッド固有。worker threadや別プロセス側CRTへ単にsrand(seed)するだけでは、原作スレッドのcontinuationを再現できない。
- 将来のread-only snapshotで必要なのは同一GameEvent/Unit処理スレッドの渡す瞬間のstate32と、実際の生成draw列/時相。実際の保護されたCRT thread dataを読めるかはVERIFY。
- 外部EXEがdrawを消費しても旧EXE側_holdrandは更新されない。戻す時はnative sideに正しく現在の状態を一回だけ復元するか、対応するnative RNG処理を一回だけ実行する契約が必要。ただし安全な実書込方法は未研究で、今回は何も変更していない。
- 死亡・レベルアップ・戦略結果反映でもdrawが起こり得るため、終了時の現在値、commit後のcontinuation stateを同戦闘で比較する。
- CRT以外のrand系、外部ライブラリ、VM独自乱数、OSタイミングや他スレッドとの混合は別途確認が必要。全ゲーム乱数をCRT一種で再現したと断定しない。

## 4. 証拠・進捗
- BATTLE_HANDOFF_RNG_OWNER_STATIC_20261021.json: 0x48D810 call、0x4C20B0/+B7、Unit+1C8/+1D0/+1CC静的書込源とcall orderingを保存。
- BATTLE_NATIVE_CRT_RNG_20261021.json: 元PE seed/draw disassemblyと合成出力列を保存。
- BATTLE_TAKEOVER_RESEARCH_STAGE2_20261021.md: 本体Stage2と同じresearch IDに属する増分。
- 現在の主観進捗47.5%据置。実際の原作Gameplay Golden0件、外部EXE往復0件。静的にできる研究は前進したが、実機handoffはまだ未証明。
- 原作EXE/ZIP/DAT/SAVE、既存DB/MASTER/他lane/製品コード、Work、Git/pushへの書込は行わず。
