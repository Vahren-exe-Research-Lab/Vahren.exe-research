# T012 MP不足・latch・processed を混同しないGolden受入票（設計のみ）
ID: B-AUDIT-20261019-2116-02 / T012 primary、T013 caller reference / 2026-10-19 21時台。
[PROVENANCE] 既保存exe/T013_SKILL_HANDLERS_BOUNDED_NATIVE_20261013.txt VA57ED68..57ED99、exe/T012_ALLFUNC_FLOW_PROBE.txt VA547161..54718F、exe/T013_SKILL_ALLFUNC_CONTINUATION_NATIVE_20261013.txt VA58012A..58017E を今回軽量read-only再確認。新規EXE解析なし。
[EXISTING FACT-1] kind2 normal候補の保存VA57ED68..99はSkill+278 cost>0・Unit+94 MP<costかつUnit+135==0ならUnit+B8>0をALにした早期retを持つ。AL=1と効果成功を同一視しない。
[EXISTING FACT-2] normal missile保存VA547173 call4E7ED0後、AL!=0ならUnit+1E560=2にしてAL0で局所return。AL=0の別枝は既保存証拠のlatch1/MP減算へ進む。AL!=0は効果成功でない。
[EXISTING FACT-3] allfunc保存VA580133 call580280直後のcallee return値を比較せず、VA58013Fは局所processed=1。VA580172..17Eでprocessedを見てSkill+278をMPから減らす別段階。580280本体は安全拒否済み領域に隣接するため新逆解析を行わない。
[MATRIX A] kind2 normal: cost=0 vs cost>0、MP=cost-1/cost/cost+1、Unit+135=0/非0、Unit+B8=0/正を個別receipt {preMP,cost,branchTaken,earlyAL,visibleEffect,postMP}へ。earlyALは内部不可視ならUNKNOWN。
[MATRIX B] normal missile: latch pre=0/nonzero、4E7ED0 AL=0/nonzero、Unit+18688方位、合法命中/近傍配置を {latchCandidate,chargeAttempt,visibleProjectile,actualTargetHP,postMP,nextTick} に分離。内部AL再現のみをGameplay PASSとしない。
[MATRIX C] allfunc: candidate count=0/1/2、距離下限境界、processed=0/1、MP cost前後、Unit+18688方向を {selected,candidateStage,callIssued,processedLocal,charge,visibleHP,nextTick} に分ける。callee内部失敗を勝手にsuccessful returnと置換しない。
[PROVENANCE RULE] 必須: 同一原作EXE/DAT/対象Skill/Unitの同一性、SAVE bytes+SHA256、map hash、入力時刻・capture SHA。不可視内部AL/latch/processedはINELIGIBLE/UNKNOWN、動的観測無しならGolden NOT RUN。
[SCOPE/DEDUP] 新しい原本命令・新ソース発見0。既E cp187監査とB T012/T013既READYの事実を再採番しない。T018 Golden正本はE所有、ここはB側受入条件案のみ。
[P0 BLOCKED] 0x5710C0..0x571500、0x58021E..0x580340等の拒否済み新逆解析は再試行しない。0x580280内部実作用、MP fallbackの最終攻撃効果、具体ターゲットと実HP変動は未確定。
[STATUS] DESIGN_ONLY / NONREADY_AUDIT、E統合対象外、Gameplay Golden PASS0、新旧strict MATCH0、Task DONE+0。
[NEXT] 合法旧実機GoldenがEから共有された場合に、同一Unit Skill/候補/MP前後とroute identityを照合。E実機受入なしに合成モデルだけで完了扱いしない。
