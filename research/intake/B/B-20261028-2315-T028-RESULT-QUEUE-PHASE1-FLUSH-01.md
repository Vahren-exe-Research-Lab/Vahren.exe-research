# T028 結果vector consumerとphase1排出経路（旧B研究の回収・G4戦後副作用候補）

- research_id: `B-20261028-2315-T028-RESULT-QUEUE-PHASE1-FLUSH-01`
- owner / tasks: `B` / `T028`（G4 postbattle consultation only、P0 takeover ownerは変更しない）。
- observed_at: `2026-10-28 23H JST`。PC source/PE SHA再hash時点 `2026-11-02 03H JST`。新規原作動的解析やnative CALL検査の再実行はしない。
- source_relative_paths: `_REDEV_RESEARCH/data/T028_RESULT_QUEUE_PHASE1_FLUSH_NATIVE_20261028_23H.md`（24行）。
- source_sha256: `A95FC92FFF9E6C3766CF3737C65A20667106C65D5CFFD5988D5320BFD97F3654`（本run実測）。
- original_PE_source: `_REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe` / SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（本run実測）。
- V9_provenance: 旧owner reportが統合V9を静的照合したと記録。旧報告内V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`（**本run V9 DB全体は再hashせず**）。
- evidence_kind: `STATIC`（owner保存のnative original-PE ASM/E8, V9）/ `INFERRED`（owner identity、record意味）/ `VERIFY`（動的効果）; actual native game `DYNAMIC=0`, `Golden PASS=0`, `strict MATCH=0`, 新規 `READY=0`。Github本文件数・全文readbackが一致した場合のみ`PUBLISHED_INTAKE / NOT_CURATED`。

## 根拠行と静的意味（新しい確定挙動を実証したのではなく旧成果を保全）
- 元報告L7–9: `0x48C880`がmanager候補`+0x1EEC74`のconsumer候補。`0x4B99C0 -> 0x48C880`はphase selector=1のジャンプ表(`0x4B997B`, index1=`0x4B99B9`)からのCALL。関数内`0x48C8BE`は`+0x1EEC3C=1`のwriter。15H–22Hのflag参照と同一objectかはVERIFY。
- 元報告L11–12: `0x48CBD3` end`+0x1EEC78`と`0x48CBD9` begin`+0x1EEC74`を差し引き、0x1C-byte stride相当の長さを使用。`0x48CF20`で走査位置に`0x8C`（5×0x1C）を加え、`0x48CF34`でelement counterを5進める。**5要素単位の反復**はSTATIC、各5項目が完全な意味レコードかは未証明。
- 元報告L13–14: 分岐した結果文経路は`0x48CE5C -> 0x52CF50`と`0x48CF0B -> 0x52CCF0`。`0x48D2AC..0x48D30C`で要素の一時解放・SSO初期化とend戻しがあるため**処理後vectorの排出/再利用候補**。永続save書込み・破棄後のUI表示を断定しない。
- 元報告L16: native E8 5/5、jump-table index1の元PE実バイト検査は旧runの記録。旧関数先頭3608B historical SHA256 `441795CC17AE77C73508DC3EB7940A8E28CE7FCFF706FF0742E9425E9B0CDB66`。本run元report+EXEファイル単位hash以外の再検証はしていない。

## 先行・訂正・G4候補・残事項
- prior_ids: `B-OFFLINE-20261028-21H-T028-WANDER-MERCENARY-DUAL-RESULT-SINK-01`, `B-OFFLINE-20261028-22H-T028-ALTERNATE-RESULT-VECTOR-PAIR-01`（同一B Draft PR #18）。本IDは22Hの未知consumer/clearを精緻化する**追加証拠**であり、22Hの`0x434B10` append呼出を再発見と数えない。`supersedes: null`; role refinement only。
- VERIFY: `0x434B10`が追加する2要素のほかのproducer 3要素、phase1/flag manager identity、endのlifetime、UI/セーブ/Unit所属変更との結線、元ゲームでの自然到達。vector排出は**settlement COMMITの証明ではない**。
- G4_takeover: native後処理で通知候補が排出されるなら結果返却前後に候補が存在する時相に影響し得るが、HP/death/EXP/召喚/Spotの副作用を同一とする証拠は無い。原作の自然finish/Task/VM継続が別途必要（`REF_BATTLE_TAKEOVER.md`）。
- next_validation: 0x434B10の残3要素producer、`0x48C880` phase1入口と同manager証明、両文面出力経路の差、World/Unit/saveへの実結果波及を、安全な未改変原作同run G0–G2で調べる。原作Golden0、G4 NO-GOを維持。
- reproduction: source MD L7–17とsource/PE SHAを照合し、専任curatorが現行V9 E8/offsetとREFに対して再評価。原作EXEを起動せず、他ownerや保護VAの操作なし。過去HOLD21・欠落10/25・03H/07H・拒否は全て維持。
