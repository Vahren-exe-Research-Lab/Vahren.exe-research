# B-20261019-2321-01｜T024 編隊AI二重gateの時点差／砲兵除外（原文限定）
[DATE/SOURCE] 2026-10-19 23時台 JST。迫真戦記ver0.67 CORE正規化済み原作 data/normalized/hakushin067_core/a_default/script/Ai戦闘制御_軍楽隊なし版.dat（3707行）をLocal Compactでread-only直読。MASTER最終確認cp191、公式588=A115/B221/C136/D116。原本ZIP/EXE実行・変更・再解析0。
[TASK/DELTA] T024主・T011分類参照。既B-20261019-2213-01の編隊slot29→30誤割当とは別の、二つのAI作動gateの配置順と砲兵groupの欠落をsource-onlyで追加確認。新EXE VA/xrefは無し（script原文行位置を根拠）。
[FACT-CLASSIFICATION] 原文L781..812: isTalent時、騎兵kiheidayo==1→@form_cav、歩兵hoheidayo==1→@form_inf、支援砲兵分類→@form_art、残り後衛→@form_general0.. を別枝へ格納。砲兵を@form_general0と同じpoolとして扱う根拠はこの部分に無い。
[FACT-EARLY] L1708の「一般部隊へ軽い待機skillを付与する」gateは bosugairu==0 && sp_irekae==1 && (count(@form_general0)>0 || count(@form_generalcav0)>0 || count(@form_generalinf0)>0)。L1710以降の一般非Talentリーダーへ a_wait1000_0 をadd/eraseする処理を条件で囲う。
[FACT-LATE] L2093は battleEvent(form_inbattle) 対 battleEvent(form_inbattle_kanni) の選択に、同じ3group gateを再利用する。両gateに count(@form_generalart0)>0 は書かれていない。falseならL2103で簡易版へ。
[FACT-WRITER-ORDER] このsourceで後衛0のaddvはL812、騎兵0はL1754、歩兵0はL1869、砲兵0はL1985。したがってL1708より後に現invocation内の騎兵/歩兵/砲兵の0-slot構築がある。L2093より前には3兵科の0-slotが構築され得る。
[CONDITIONAL MODEL] 前戦のarray残存がなく、0-slotが空から始まり、分類とcounter/whileが意図どおり動く場合、L1708 gateのgroup部分は後衛有無Rのみ、L2093はR||騎兵C||歩兵I。砲兵のみ（A=1,R=C=I=0）なら両gate false、騎兵のみ/歩兵のみ（R=0,C=1またはI=1）なら前段false・後段true。これはsource上の条件付き論理帰結で原作実機観測ではない。
[VERIFY] @form_general*の戦闘間初期化はL12のif(count(@enemy_army)>0)以下で条件付き。実環境で前戦array残存有無、count/countVar・分類/配列先頭の実作用、battleEvent scheduling、実「砲兵のみ」構築可能性、ユーザー視認効果は全未確認。砲兵だけ必ず低AIとなる・必ずバグ発生とは認定しない。
[REIMPLEMENT] 厳密互換モデルでは EARLY_WAIT_ELIGIBLE と LATE_FULL_FORM_ELIGIBLE を別ステージとして保持し、@form_generalart0を親切に追加して原作と同一視しない。前段のpool可視性・残存値・フラグをnullable provenanceにして、推測による正常return/攻撃成功/AI動作を偽装しない。
[SYNTHETIC] 保存sourceのanchor gate2件、rear writer L812、cav L1754、inf L1869、art L1985、両gate artillery欠落とwriter時点差をLocal側読取データ上でASSERT済み。R/C/I/Aの16組の局所boolean合成行列は16/16整合。旧原作実機GoldenのPASSではない。
[GOLDEN-DESIGNED-NOT-RUN] bosugairu=0/sp_irekae=1を合法旧ゲーム経路で得て、敵の有効リーダー群を後衛のみ・騎兵のみ・歩兵のみ・砲兵のみ・砲兵＋他兵科で分類。初回/連戦を分け、待機技能・full/kanniイベント、可視移動・時刻・戦闘結果を旧新同EXE/DAT/SAVE/map/input/capture SHA及びseed可否付きで採取。C-NB02 G0/G1/G2未実行ならfixture INELIGIBLE / NOT RUN。原作Gameplay PASS0・新旧strict MATCH0。
[DEDUP] 先行B-20261019-2213-01はslot29/30欠落、既T024速度skill・AI間隔・一般待機skillの出自は再READY加算しない。今回の増分は同一式の二箇所の「評価時点」と砲兵非参照の組合せに限定。新確定原作BUG0、新EXE解析結果0。
[SAFETY/NEXT] 禁止済みVA0x5710C0..0x571500等と旧B/T024 safety拒否payloadの迂回0。再開は前戦array寿命・legitimate artillery-only/cavalry-only inputを既許可の原作ソース/保存済ASM範囲で照合。原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/設定/automation変更禁止。
[STATE] DETAIL INITIAL SAVED PENDING independent readback／B owner索引・HANDOFF同ID保存/独立readback／dedup後のみB限定SOURCE STATIC READY、E正式MASTER統合別。実Gameplay Golden PASS0・strict MATCH0。
