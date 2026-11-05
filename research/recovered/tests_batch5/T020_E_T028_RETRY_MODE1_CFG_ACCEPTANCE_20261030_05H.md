# 研究E｜T020 二度の退却先探索と post-RET mode1 入口の局所CFG受入（2026-10-30 05H JST）
研究ID: `E-AUDIT-20261030-05H-T020-T028-RETRY-MODE1-CFG-01`
状態: STATIC / SOURCE BYTE VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作旧EXEと再実装の実行・動的比較は未実施。
## 出典・同一性
- B owner `B-20261030-0515-T028-DUAL-RETRY-POSTRET-MODE1-JUMP-01`、`data/T028_RETREAT_DUAL_ATTEMPT_POSTRET_EDGE_NATIVE_20261030_05H.md`。EのLocal readと独立Get-FileHashにより出典実SHA256=`9510EAE2532D8DFE854EFB46DBC393E5C61EF5F2AA4553E355C27A156374727A`を確認。
- B状態 VERIFY/NOT READY、B原作PE SHA `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 DB SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`はB資料・管理JSON記録値。Eの今回再hash対象はB詳細のみ。
- 旧README/BUILD_MANIFESTは現在不在。現行案内 `rea_lab/headless_analysis/00_START_HERE_ACTIVE_RESEARCH.md` と `CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json` に従い統合V9を使用対象とした。Ghidra再解析0。
## T020新規判定
- `0x495032`既存Unit+0x1B4が非NULLなら保存済Spotを使用。NULLの場合 `0x495050`が候補探索初回index0 /第三引数0、失敗時のみ二度目index1/第三引数1を試みる。二度目はUnit+0x77非0が必要、index2は無い。
- `0x5AC3AF/0x5AC3B5/0x5AC3B9`のcandidate+0x77/+0x75両0は`0x5AC5E3`に直接分岐し`0x5AC5E7`の`0x598450(mode1)` CALL siteへ到達し得る。このCFG上の明示枝は、RET直後に位置することだけを理由に到達不能扱いしない。
- ただし`0x5AC36D`までの上流caller/第三引数stack対応、候補listの生成、実ゲームで条件が成立すること、mode1 helper副作用はVERIFY。静的辺存在と正常Gameplay到達、実際の画面通知・予約数変化を別評価とする。
- `0x494F98`の[ESP+0x6F] writerと`0x495596`の[ESP+0x6F] readerは間のSUB ESPにより同一slot未証明。同名offsetだけで通知flag producerを確定しない。
## T020合成検証
- 新規E専用`tests/t020_e_t028_retry_mode1_cfg_gate_20261030_05H.py` / `tests/T020_E_T028_RETRY_MODE1_CFG_CASES_20261030_05H.json`。出典SHAと記載VAをfail-closed、全fixtureの完全再生成一致・case ID一意を検査。
- 新規探索経路16＋局所CFG4＋追加境界・型・欠落・仮想Golden検証16＝36/36 PASS。E旧21H～04Hの8検証器は独立read-only再実行し191/191 PASS、総合227/227 synthetic。実原作Gameplay=NOT RUN、DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。
- この36件はBのSTATIC研究を模した検証器自身の合成分岐であり、原作退却成功・新エンジンstrict互換・未解明のstack由来を証明しない。
## T018・T019・MASTER
- C-NB02のG0合法UI旧原作戦闘開始限定receiptは既存だが、同一戦闘G1直前未改変SAVE SHA＋操作、G2 ACTIVE実MAP/三陣営/順序付き出撃Unit/Troop、G3結果、G4World差分は未充足。観測PID/時刻違い・x20 DAT改変等の混合を認めない。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2は検索範囲差のみRESOLVED、script2順序/phase flag/TXT loader/gwrite/decide11用途はVERIFY。今回のRET後枝の静的訂正はT019のWiki矛盾確定として加算しない。
- MASTER最終正式checkpoint196、READY596=A115/B229/C136/D116。今回新規READY正式統合0件。TASK QUEUE34行はPC上で再集計 DONE9/IN_PROGRESS21/VERIFY4。MASTER実SHA=`E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3`（今回のread-only時点）。
## 安全・継続
- 旧T018表境界、E session join、T019 XREF、C T026/T032、D T030 TSV、禁止0x5710C0等はBLOCKED据置、拒否payload再投稿・別tool/path/shell/Remote/ZIPの迂回0。旧OFFLINE-UNSYNCEDのowner/重複/READY全件照合は未完了。
- 今回、E所有tests以外への書込なし、MASTER/他lane/REA/dev_lab/原本EXE/DAT/ZIP/SAVE/Git/Work/設定/automationは変更しない。新安全拒否0、接続エラー0。
- 次: Bの`0x5AC3B9`上位CFGと`0x598450(mode1)`副作用、ESP frame deltaのread-only一次照合、合法原作同一runのG0/G1/G2の真正receipt確保。未確定をREADYへ昇格させない。
