# T020｜script2→script 二段階解析とphase flagの比較条件（2026-10-21 22:50 JST）
ID: E-AUDIT-20261021-2250-SCRIPT-ROOT-PHASE-GATE-01
状態: STATIC source proof / T020 DESIGNED_NOT_RUN / NOT READY / 原作Gameplay未実施。
根拠: 既存 Ghidra search_index function 0x50C9A0 の22時台読み取り専用取得。コードSHA256 37A2E5F58FEED52FD8630083E8983FB55661858E93CE3DCE7E02750D2FBCC22B。
対象EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（BUILD_MANIFEST記録）。
STATIC: entryでDAT_008797D2=0、両枝でDAT_008797D1=0。script2成立枝では 0x50CCD4→0x50BF60→候補反復→FUN_0050B220 後、DAT_008797D1=1・FUN_00416870・list初期化→0x50CE86→0x50BF60→候補反復→FUN_0050B220。
STATIC: script2不在/非directory枝は0x50CA91→0x50BF60を使用し、二段階目を通らない。どちらも候補リスト空ならParseException候補。flagの使用先・decl優先順位・list初期化の作用はVERIFY。
CASE-PHASE-01: script2不在かつscript内同名宣言あり。単一root処理。旧UI NOT RUN。
CASE-PHASE-02: script2有効・別名DATが双方に存在。二rootの段階別取得を記録。旧UI NOT RUN。
CASE-PHASE-03: script2有効・同名定義を双方が含む。最終observable値/シナリオ別有効定義を記録。旧UI NOT RUN。
CASE-PHASE-04: script2有効・script2側空、script側非空。先行phaseの例外候補を独立記録。旧UI NOT RUN。
CASE-PHASE-05: script2側非空、後続script側空。後段の例外候補を独立記録。旧UI NOT RUN。
ケースはいずれも既存の合法原作スクリプト構成でのみ測る。原本変更・想像での結果補完禁止。合法入口がなければINELIGIBLE。
比較receipt: EXE/DAT/SAVE/source root別SHA・シナリオ・起動引数・同一run入力・ロード成功/可視エラー・同名宣言の有効結果・旧新build SHAをnullableで採取。
内部flagの実値を画面から推定しない。SCRIPT_STATICとGAMEPLAY_OBSERVEDを別ラベルにし、raw sourceとnormalizedを混同しない。
拒否履歴: E-RC-20261021-2252-T019-XREF-SEARCH-SAFETY-01。関連関数・flag crossrefの追加検索コマンドが安全拒否され、同操作再試行/別tool/path/shell/Remote/ZIPでの代行なし。flag consumerおよびFindFirstFile handle lifecycleは未解決。
READY追加0 / original DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。旧T018表境界・17:55・18:56拒否対象に変更なし。
