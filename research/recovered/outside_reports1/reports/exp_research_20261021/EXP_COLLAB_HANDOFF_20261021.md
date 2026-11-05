# EXP-COLLAB-20261021-2112-01｜経験値・召喚と戦闘終了の独立横断研究

- 作業ID: EXP-COLLAB-20261021-2112-01。対象: 迫真戦記ver0.67／T011経験値・T012召喚・戦闘決着。
- 状態: IN PROGRESS / STATIC / VERIFY / NOT READY / ACTUAL GAMEPLAY NOT RUN。
- 保存先: 本ファイルと同じ既存 `exp_research_20261021`。MASTER/B HANDOFF/Work queue等の担当正本は今回編集しない。
- 原作識別: Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（検索基盤manifest記載、今回の再ハッシュではない）。
- 機械解析DB: `../rea_lab/headless_analysis/search_index/search.sqlite` SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（manifest記載）。
- 先読: `../MASTER_LEDGER.md`（E所有）、`../evidence/ANALYSIS_LANES_PROTOCOL.md`、`../evidence/LANE_B_HANDOFF.md`、`../dev_lab/docs/WORK_REQUEST_QUEUE.md`、本フォルダ既存 `EXP_SUMMON_OWNER_RESEARCH.md`。
- 重複参照: `../rea_lab/headless_analysis/search_index/P0_SUMMON_EXP_OWNER_REPORT_20261021.md`、同 `EXP_SUMMON_DEATH_RESEARCH_20261021.md`、`../data/T011_SUMMON_RUNTIME_UNIT_56F880_CONTRACT_20261013.md`。
- 既知: 0x54E7B0→0x577260/0x577310でUnitData相当Rを再利用・生成→0x56F880の+0x1C8に結合→0x551E50がR+0x16Cを加算（条件付き）。召喚発動XPは0x57F4E9別系列。
- 既知: 0x56F880は陣営への登録を+0x8Dで振り分け、+0x8Cは単純型の更新処理に関わる。戦闘後の永続保存と子Rの解放時刻はVERIFY。
- 未解決: child R の所有・再利用キーと消滅、陣営側+0x48/+0x58の登録/確定順、永久UnitとのXP同期・SAVE/LOAD境界。
- 既安全拒否は個別保留。Wiki草稿の未保存残部、B/REA既拒否VA・SQLを別経路で再提出しない。独立研究のみ実施。
- 使用可能な分類: STATIC_PSEUDOC、STATIC_ASM、DAT_SOURCE、INFERRED、VERIFY、GOLDEN_NOT_RUN。READY/DONE/原作Golden PASSは根拠なく昇格しない。
- 引継ぎ: 他AIは本書→証拠レコード→保存済B/REA資料→manifestの順に参照し、IDと出典を重複照合する。ファイル変更だけでは他チャットへプッシュ通知されない。
- 次: 新規の因果関係を静的参照で検査し、具体site/観測可能な条件/否定できない経路を追記。原本、製品コード、Git、MASTER、Work、他レーンは変更しない。
