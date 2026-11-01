# B research intake — verified PC-owned evidence
research_id: B-20261101-18H-T024-DUAL-REFERENCE-COORD-AND-PC-RESTORE-01
owner: B
source_relative_path: data/T011_T024_DUAL_REFERENCE_COORD_NATIVE_20261101_18H.md
source_sha256_verified_2026-11-02_JST: 4C4C5C55D7CCB849BB93CE445B6669CE2B8BC5A0F451088EBB4E42F944658FBC
intake_status: PUBLISHED_INTAKE / NOT_CURATED / STATIC-VERIFY / NOT_READY
original_gameplay_Golden_PASS: 0
strict_MATCH: 0
source_note: The research below is the B-owned source report; its historical OFFLINE state describes its original capture. This archive was staged after source-file SHA confirmation on the authorized PC. Native ABI and game behavior remain unproven.

---

# 迫真戦記 新B T011/T024｜二系統基準座標のNative照合と未同期復旧（2026-11-01 18H JST）

研究ID: B-20261101-18H-T024-DUAL-REFERENCE-COORD-AND-PC-RESTORE-01
Owner B / Task T024主担当, T011関連 / T013 final-targetはVERIFY。
状態: STATIC_NATIVE / STATIC_V9 / INFERRED / VERIFY / NOT READY。
原作実機Golden PASS=0、strict MATCH=0、DYNAMIC=0、新規READY=0。

## 証拠源と優先復旧
Desktop Commander Local CompactでPC ONLINE。MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、B安全復旧台帳、knowledge README/SYNC_STATUSを読取。private Github Hakushin067-Research-Knowledge develop の KNOWLEDGE_CURATION_PROTOCOL、GHIDRA_V9_B_REVIEW_TOP150、GHIDRA_V9_COVERAGE_REPORTを読取専用確認。旧search_index/README.md・BUILD_MANIFEST.jsonはENOENTだが、統合V9別名SQLite/CLIは利用可能。旧標準V3昇格の拒否は迂回しない。

17Hの未回収32核心ファイルのうち08/09/10/11/12/14/15H各4件＝計28件を、会話およびChatGPT Libraryの既存保存原文からB所有dataへ復元。各時間の報告・証拠JSON・読取専用verifier・旧readback receiptを保全。PCでreceiptの期待SHA256/bytesと復元coreを独立照合：CORE_PASS=21、RECEIPT_PASS=7、ISSUES=0。旧receipt本体も元出典のSHA256と7/7一致。13H/16Hの8件は17Hに復元済みであり、本run二重反映なし。これにより17H時点の残32件は28件解決、残り07H核心4件だけ。07～16HのHANDOFF delta10件は17Hに既に原文復旧済みであり重複追記しない。

残OPEN：07H原文4件はLibrary/PC dataファイル名で未発見、03H保存失敗は実在/SHA未照合、10/25元研究文の欠落、B生資料のGitHub不完全保存、既存安全保留21件。SAFE134全件の新規ハッシュ監査は実施せず。安全拒否済み証拠/VA/コマンドを別tool/path/ZIPで迂回せず、MASTER/他lane/knowledge/Git/原作EXEには書込なし。

## 今回の新規STATIC Native：二経路の引数・グローバル記録先の独立照合
原作ゲームフォルダのVahren.exeは読取専用でSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致。PE file bytesをpefile + Capstoneで限定2窓だけデコード。ゲーム実行ゼロ。検証スクリプト data/T024_20261101_18H_TWO_REFERENCE_COORD_NATIVE_READONLY_VERIFY.py。

第1系統 0x529691（41 bytes窓SHA256=0FE94E8CD421DDE51B969600485745C329A044910D0D4D20173C7936892F8053）：
- 0x529691 89 3D 48 E0 8B 00 : mov dword ptr [0x008BE048],edi
- 0x529697 E8 E4 84 0A 00 : call 0x005D1B80
- 0x52969C push eax、0x52969D A3 4C E0 8B 00 : mov [0x008BE04C],eax
- 0x5296A2 push edi、0x5296A3 lea eax,[esp+0x64]、0x5296A7 push eax、0x5296A8 E8 13 07 00 00 : call 0x00529DC0。

第2系統 0x529851（41 bytes窓SHA256=6CB93A097F9C377A2CF07F6AC29215D6C817DCD6BFB072997B2082AEAA37C6B0）：
- 0x529851 89 35 48 E0 8B 00 : mov dword ptr [0x008BE048],esi
- 0x529857 E8 24 83 0A 00 : call 0x005D1B80
- 0x52985C push eax、0x52985D A3 4C E0 8B 00 : mov [0x008BE04C],eax
- 0x529862 push esi、0x529863 lea eax,[esp+0x70]、0x529867 push eax、0x529868 E8 53 05 00 00 : call 0x00529DC0。

相違点：座標系の入力レジスタは第1 EDI、第2 ESI。ソート対象も別スタック参照 [esp+0x64] / [esp+0x70]（**Unitフィールドではなく一時スタック位置**）。一方で記録先グローバル0x8BE048と0x8BE04Cは両系統共通、各CALL前に上書きされる。したがって二系統を同じ入力・単一ソートと機械的に統合すると危険。ただしEDIとESIの数値が常に異なるとは断言しない。共有グローバルの外部参照・並列/再入時影響はVERIFY。

## V9/KB、重複防止
統合V9 read-only CLI function 0x528DB0（3104 bytes）擬似Cには、2回の別々のD3DXVec3TransformCoordから FUN_005D1B80、共通 _DAT_008BE048/+4C更新、FUN_00529DC0(appcStack_9c,uVar8,_DAT_008be04c) が現れる。これは原作ASMの置き換えではなくSTATIC擬似C。
V9 callers 0x529DC0 = direct E8 exactly 2 sites: 0x5296A8/0x529868（上記Native bytes完全一致）。function 0x529DC0から 0x529EAE/0x529F04/0x529F74→0x52AD00 までの3 E8を確認。以前の0x52AD35→0x526030（距離比較）および13H独立ソート、17H同距離局所左側優先を再計数しない。0x529DC0はV9 ABI_UNVERIFIED。
knowledge/kb.py addr 0x529DC0 は未命名・直接言及なし、addr 0x528DB0にはB/Dの先行証拠がある。Dの所有資料は読取だけ。旧11H～17H研究IDを継承し訂正・重複を防止。
KB_CANDIDATE：owner B/T024,T011、今回ID、VA 0x529691/0x529851/0x5296A8/0x529868/0x529DC0、global 0x8BE048/+4C、0x5D1B80、source original EXE SHA + 各Native窓SHA、data/T024_20261101_18H_TWO_REFERENCE_COORD_NATIVE_READONLY_VERIFY.py、当報告。STATIC=原作bytes/E8/V9照合、INFERRED=formation reference coordinates、VERIFY=上流座標数学/ABI/グローバル副作用/最終ターゲット/Golden。正式辞書登録は知識ベース専任のみ。

## Golden・安全・次回
原作実測Golden0、strict MATCH0、READY0、DYNAMIC0。HOLD21維持。旧禁止0x5710C0..0x571500・既拒否XREF/対象には未接触。実機Goldenには原作DAT/MAP/SAVE、mode、両方のグループ一覧・参照座標・RNG/tick・同距離ノード、0x569730後続と実移動/対象との突合が必要。次回は07H残4原文と03H失敗保存を優先し、それ以外は0x5D1B80変換前の座標計算と0x569730作用をread-only調査する。すべてNOT READY。
