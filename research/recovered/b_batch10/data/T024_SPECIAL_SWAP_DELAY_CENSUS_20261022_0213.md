# B-20261022-0213-01｜T024高難度スキル交換：gun_delay参照の親不一致6件とcheck/倍率分布

時刻: 2026-10-22 02時台 JST | Owner: B / T024（T011/T012参照）| 分類: SOURCE-STATIC-FACT、native/SAVE/gameplay VERIFY | 原作Game Golden PASS0・新旧strict MATCH0・Task DONE増0。
原作識別: hakushin067_Vahren.exe manifest SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回は原作EXEの実行、直接hash再計算、製品コードの変更なし。
入力: normalized CORE script/Ai戦闘制御_入れ替え必殺技.dat （895行・SHA256 BC8EDC93A43CAB13B86429E164C17D8F9CC466AF7B643BF6EAFB91E633F3F255）および Ai戦闘制御_軍楽隊なし版.dat （3707行・SHA256 48B1A62AB5B2D80645639100447797290FBD4481AD91F8A3CCCA79A4038456E6）。両ファイルは正規化コピーをread-onlyで読み、Get-FileHashを確認。
重複除外: T024§14と既 evidence/T024_SKILL_SWAP_MATRIX.tsv は「81 triggers、158 skill宣言、bnkrg没収、majimekun/kusoのrand2択、異なる親・共通wait」の既成果。このIDではそれを再発見・新READY計数しない。新規増分は全variantのgun_delay参照元とparentを別列で比較した6不一致、共有参照グループ、全wait倍率と全com check明示度数を機械集計した点。

## SOURCE 定量調査（宣言数、実効インスタンス数ではない）
- active declaration: 158 = waitspecial 1 + wait_* 77 + com_* 80。既T024§14の件数と一致（件数自体はNEWではない）。
- wait 77件の gun_delay「skill-name*倍率」: *9 48件、*12 27件、*16 2件。*16は wait_majimekun（L178-181）/wait_kuso（L413-417）、各ランダム対抗の wait_majimekun_b（L190-193）/wait_kuso_b（L423-426）は*12。既T024§14の二択発見に、二択の具体的倍率差を新規接続。どちらも原作で実発動することはVERIFY。
- com 80件の gun_delay は全て「名前*1」の字句形。check上書き明示70件：100=3、200=16、250=4、300=26、350=3、400=9、500=1、600=8。check未明示10件: com_move, com_nyn, com_death, com_ondisk, com_tusk_act4, com_snnn, com_kasuga, com_conf, com_conf_nyn, com_flour。未明示はinherit/engine defaultの候補であり、実効check値の確定ではない。
- com parent 名とgun_delayの名前参照が不一致のものは次の6件のみ（80宣言を全文比較）：
  com_alc: parent=sp_new_alc, delayRef=sp_alc, check400 (L429以降)
  com_udk: parent=sp_masu3, delayRef=sp_masupa, check400 (L762)
  com_azs: parent=sp_masupa_azs, delayRef=sp_masupa, check400 (L767)
  com_masupa5: parent=sp_masupa5, delayRef=sp_masupa, check400 (L772)
  com_masupa5b: parent=bsp_masupa5, delayRef=sp_masupa, check400 (L777)
  com_kusari_higekuma: parent=kusari_higekuma, delayRef=kusari, check300 (L804)
- 実名参照が共有されるgroupは sp_masupa にcom_masupa/com_udk/com_azs/com_masupa5/com_masupa5bの5宣言、kusari にcom_kusari/com_kusari_higekumaの2宣言。これはgun_delay RHSの**字句上の共有**であり、runtime timer storageを同じにすることの証拠ではない。

## CONDITION / EXE static anchor
- normalized軍楽隊なし版 L949付近のsp_megabeam は「難度共通」処理であり、L954付近以降は if(sp_irekae == 1) で高難度交換に入る（旧T024§14が確定済み）。bnkrg_hokyu L1041-1044はremoveSkillのみでwait/comを追加しない（旧§14既知）。これらの条件は追加経路の可視発火には依然VERIFY。
- Ghidra STRING_INDEX の gun_delay 文字列 VA 0x00624DD0 と0x00624DE4 はともに参照関数0x00599BD0。該当関数は24,124 bytesでGhidra decompileは103,119文字、Code SHA256 94F69BED55F2E76978B831CCF1179B94987DE2C655B7B861B4E8B49A99588C64。直接CALL 0x004679BF (from 0x4678A0) と0x0046FC3E (from 0x46FB00) を既検索DBで確認。これはnativeでgun_delay字句を扱う候補への**索引リンク**であり、RHS数値化・timer共有・MP/AIの実作用は未解析、関数本体の全量復元を実施せず。

## REIMPLEMENT/ GOLDEN / LIMIT
- 宣言を「variant parent」「gun_delay参照名」「倍率」「check override有無＋値」「AIスクリプトの動的add/remove/erase」の別fieldで保持する。親とdelayRefの自動同一視や、全comでcheck一定値に正規化する設計を禁止。上記は設計上の注意であり実験済み仕様と混同しない。
- GOLDEN DESIGNED NOT RUN: (A) sp_majimekun/sp_kusoの二択(16/12)について同seedの合法sp_irekae戦闘でwait・発動時刻・MP・RNGを捕捉。(B) sp_masu3/sp_masupa5/sp_masupa_azsを合法同戦場で実動作の共有/非共有cooldown検証。(C) com_moveと明示check上書きskillの射程、原作effective parentと実距離を比較。旧EXE/DAT/SAVE/map/input/capture SHA、旧原作と新実装の同一条件が不足のためactual Golden PASS=0・strict MATCH=0。
- OPEN P0: 0x599BD0のbounded ASMでgun_delay name×multの保存先/算術/解決時相、RNG二択とcom継承のruntime効果、Skill instance lifecycle/alias、実際の発動条件、MP/status影響。必要な許可済みcaller/consumerだけ追跡。旧安全拒否VA0x5710C0..0x571500、T011 0x416870、既拒否のT011/T012/T013詳細書込やSQLは再試行・迂回しない。
- 書込所有者はB data本detailとB T024 ownerとLANE_B_HANDOFFに限定。MASTER/T018/他レーン/REA/dev_lab/原本/SAVE/Git/Work/設定/schedulesを変更しない。正式E READY取り込みは別処理。
