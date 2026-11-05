# 迫真戦記｜追加ストーリー正本
このフォルダは原作から独立した追加シナリオの資料保管庫です。原作ゲーム・他研究レーンは読み取り専用です。
## 引継ぎの読書順
1. [ONDISK/MASTER.md](ONDISK/MASTER.md) — 採用設定・原作との区別
2. [ONDISK/HANDOFF.md](ONDISK/HANDOFF.md) — 最新状態・次作業・安全境界
3. [ONDISK/PLOT.md](ONDISK/PLOT.md) — 粗筋・伏線
4. [ONDISK/CHARACTERS.md](ONDISK/CHARACTERS.md) — 人物設定
5. [ONDISK/STAND_SPEC.md](ONDISK/STAND_SPEC.md) — 戦闘システム仕様
   - [ONDISK/STAND_DAMAGE_MATRIX_20261025.md](ONDISK/STAND_DAMAGE_MATRIX_20261025.md) — 通常物理無効とスタンド専用打撃の最新契約
   - [ONDISK/FOLLOW_AI_RESEARCH_20261025.md](ONDISK/FOLLOW_AI_RESEARCH_20261025.md) — 召喚術者追従・CPU AI DATとEXEの解析
   - [ONDISK/BATTLE_AI_ARCHITECTURE_20261025.md](ONDISK/BATTLE_AI_ARCHITECTURE_20261025.md) — **戦闘AI全体像、通常Unit AI、戦闘指揮DAT、スキル選択、スタンド利用設計**
   - [ONDISK/STAND_DISC_TRANSFER_DAT_20261025.md](ONDISK/STAND_DISC_TRANSFER_DAT_20261025.md) — 遠野によるスタンド技能奪取と他の味方への付与・開幕自動召喚の**固定技能DAT試作**
   - [ONDISK/STAND_DISC_GENERIC_TRANSFER_FEASIBILITY_20261025.md](ONDISK/STAND_DISC_GENERIC_TRANSFER_FEASIBILITY_20261025.md) — **戦闘限定・技能DAT無改変の汎用スキル転送とポケモン召喚への適用可能性**
   - [ONDISK/TNOK_CHIKORITA_RECALL_20261025.md](ONDISK/TNOK_CHIKORITA_RECALL_20261025.md) — **TNOKのチコリータ召喚・元術者だけの消滅・進化・飛行中のボール対策**
6. [ONDISK/TASKS.md](ONDISK/TASKS.md) — 開発計画
7. [ONDISK/stand_proto/README.md](ONDISK/stand_proto/README.md) — 動作試作
   - [ONDISK/SUMMON_PARENT_NATIVE_DAT_BOUNDARY_20261025.md](ONDISK/SUMMON_PARENT_NATIVE_DAT_BOUNDARY_20261025.md) — **原作にある召喚親子Unit一覧、DATだけでの消去可能性、最小DLLの必要範囲**
   - [ONDISK/SUMMON_DISC_REMOVAL_POLICY_20261026.md](ONDISK/SUMMON_DISC_REMOVAL_POLICY_20261026.md) — **固有召喚物の一括消去と、量産召喚物の安全な技能封印の区別**

   - [ONDISK/PERSISTENT_BOSS_ESCALATION_PROPOSAL_20261026.md](ONDISK/PERSISTENT_BOSS_ESCALATION_PROPOSAL_20261026.md) — **放置による永続技能獲得・ターン段階成長ボスの候補案（未確定）**
   - [ONDISK/SIMPLIFIED_CPU_BATTLE_DISC_RESEARCH_20261026.md](ONDISK/SIMPLIFIED_CPU_BATTLE_DISC_RESEARCH_20261026.md) — **CPU対CPUの簡略戦闘からDISC技能を取得しボスが成長する案・原作DAT APIの調査**
## 共通運用
- 状態分類：USER_FIXED（利用者確定）/ USER_CANDIDATE（利用者案）/ PROPOSED（AI案）/ ORIGINAL_CONFIRMED（原作データ裏付け）/ UNVERIFIED（未確認）。
- 仮案を確定設定として引用しない。変更時は日付・決定ID・理由を記録し、HANDOFFを更新する。
- 複数AIは担当所有権とGitのdirty状態を照合してから編集する。他担当ファイルを上書きしない。
- 実機未確認は PROTOTYPE / STATIC / NOT RUN を区別。単体テストをゲーム実機合格とみなさない。
- 現dev_lab Gitにはremote未設定。PCに書けてもGitHubへ共有されたとは主張しない。
