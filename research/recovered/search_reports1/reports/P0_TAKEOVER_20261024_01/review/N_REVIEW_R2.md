# N 修正版再レビュー（R2）
研究ID P0_TAKEOVER_20261024_01 / 2026-10-24 / 静的read-only。
EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
V9 DB SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
observe.js SHA 43045A89DF54207540C869203214CB7A8420025AC2398FAB0F6B5DF4DEC0AE9E。
run_observer.py SHA 204A9C99DE2F8A51355148078C2460ABAF3C8779F7C991814893F0178C2EC3D3。
固定コピー reviewed_r2_observe.js.txt / reviewed_r2_run_observer.py.txt。初版レポート・初版コピーを保存し修正版と混同しない。

## 解消をソースで確認
- N01: HP+90 / MP+94 / HPmax+DC / MPmax+E0へ修正。
- N02部分: dispatcher入口でtaskPass加算、GameEvent depth、VM caller stack、sceneDepth、Start時origin保存とUnit57AA00短命監視を追加。
- N03部分: task_slot_gateへ改名。EBX==E、GameEvent depth0、sceneDepth0、originがGameEvent由来・Scene外・VM return433620を追加。
- N04: observer_ready待機最大5秒、script error検出、ia32およびPEに対応する8byte guard（HIGHLOW relocation領域除外）。source_identityとinjected.jsをrunごと保存。
- N05部分: attach/load失敗時、spawnから返された所有childのkillと失敗記録を追加。既存原本PIDへattachするコードはない。

## 残る制約と誤PASS防止
1. gate eligibleにunitSinceStart===0がない。Start後Unit updateが先に観測されてもeligible:trueになり得る。現在は観測のみだが、これをhold許可として流用しない。
2. Start時のowner/passをtokenへ固定してC1で照合していない。global ownerは代入のみ。tokenにowner、taskPass、current Task/frame ID、per-thread連番を保持して同一passを確認するまでC1安全性未証明。
3. Unit監視はStart enterから最初の57AA00呼出まで。カウンタは0か1で、全Unit更新件数ではない。最初の呼出有無を観測するものとして解釈する。別update実装/別thread writerの不在を証明しない。
4. GameEvent/VM depthとvmCallersはglobal。複数threadや再入/例外で誤相関する可能性を残す。今回の通常単一threadの観測でもtidを必須照合し、連戦対応を宣言しない。
5. pefile import、guard生成、source読取はstartup try外。ここが例外になる場合は所有childがpausedで残る余地あり。稼働成功時の記録とは別問題。
6. module pathはreadyで記録されるがexpected pathとの比較はない。copyファイルSHA、spawn戻りPID、ia32、byte guardで相当範囲を限定しているが、agent側path校正未完を記す。
7. vector/型/重複検査と完全名簿statusは初版のまま。safe unavailableを含むsnapshotをG1として受理しない。
8. snapshotとgate hook設置の間でロギング/metadata処理が入る。Frida自体のnative介入とrelocationの実動作は静的確認493/493と区別する。

結論: 初版の直接的な値誤りと準備未完起動は修正済み。観測専用の限定traceで取得可否を評価する段階。C1 safe hold、全Unit更新停止、完全G1/G2、NOOP往復、復帰のPASSは本レビューから付与しない。
再開地点: 親のrun receipt/injected.jsとtraceを同一SHA・PIDで照合。Start→GameEvent復帰→C1→次slotの順とUnit0/owner/pass条件を確認してからhold試験を別途審査する。
