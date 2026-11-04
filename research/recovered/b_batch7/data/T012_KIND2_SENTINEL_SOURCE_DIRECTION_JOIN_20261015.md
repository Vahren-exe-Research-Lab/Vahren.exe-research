# B-20261015-1611-01｜通常kind2方向入力と三段factory sentinelの同一stack slot（T012/T013）
[OWNER/DATE] 2026-10-15 16時台JST、T012 primary/T013 cross-reference。STATIC SAVED-X86 DATAFLOW候補。Task DONE+0、原作Gameplay actual PASS0、新旧strict MATCH0。
[EXE] 迫真0.67 bundled Vahren.exe相当 SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。B既保存 exe/T013_SKILL_HANDLERS_BOUNDED_NATIVE_20261013.txt VA57EB79..57F170をread-only照合。原本/REA/Ghidra新実行・逆解析なし。
[UPSTREAM] 57EB79はUnit+1E574をstack+38に保持し、null側の57EB8Dは別output buffer stack+28を576E80へ渡す初期検査。57EC4C..57EC7CはUnit/選択pointer座標を積み、57EC76でEAX=&[ESP+18],57EC7AでECX=Unit,57EC80で576E80をcallする。両callのbuffer+28と+18を混同しない。
[CONSUMER1] 57ECEEは[ESP+18]を0x80000008と比較、57ED9Cも[ESP+18]を同値と比較。57ED9C一致→57EDC6..57EDDC、非一致→57EDA6..57EDC4の異なる座標差分生成経路へ進み、57EDE0 call5E743Aと方向状態Unit+18688 writer 57EE0Bへ接続し得る。
[CONSUMER2 ROOT] 57EF44でSkill+74によりcalleeを選び、57EF48のPUSH0後57EF4C/57EF82が[ESP+1C]を同sentinelと比較。通常のESP釣合いならこの+1Cはpush前+18と同一stackアドレス。B-20261015-1518-01で確定したECX/EAX null-versus-local pointer選択をそのbufferの後段consumerとして接続。
[CONSUMER3 CHILD] 57F011のSkill+74判定後57F015 PUSH0→57F019/57F04F [ESP+1C]比較。57F077..57F09Eで子vector再読しても、この親frame bufferの別producerは本保存窓で確認できない。子resolver 4678A0は既B-20261015-1011-01。
[CONSUMER4 EXTRA] 57F0F0 PUSH0と57F0F2 PUSH ESIの2回stack push後57F0F7/57F14Bが[ESP+20]比較。通常stack釣合いなら2push前+18の同一slot。root/child/extraの引数切替は既B-1518の再計上ではなく、上流buffer・方向分岐との同一参照先の接続が本件増分。
[FACT/VERIFY] saved caller命令のbuffer引数と同stack slot再読/比較はCONFIRMED（正常return/ESP保存の局所条件下）。576E80がそこへ書く具体的bit pattern、選択pointerとの同一性、全下位calleeのstack/exception/return、0x80000008の高水準意味、5E743A、0x580280/0x54F720の実作用はVERIFY。意味未確定のsentinelを「標的無し」「不発」と命名しない。
[DEDUP] B-20261015-0110-01はselected cache→geometry input、B-1518は三stage argument shape、B-0611はpost-debit処理順、B-0709はchild配列再取得。今回の独立範囲は57EC80/57ED9Cと三stage比較のsame-frame aliasのみ。過去拒否B-1410/1322/1210等を再提出・READY化しない。
[REIMPLEMENT] target cache(+1E574)、576E80の別々の一時buffer、角度候補、Unit+18688、root/child/extra caller frameのsentinel・渡したpointer、MP debit・latch+1E560・各factory returnPC/RNGを独立receipt。未知calleeの正常return・発射・HP変化を偽装しない。
[GOLDEN] 原作合法mode0 kind2でcache null/nonnull、sentinel成立可否（合法入力を確認できた場合のみ）、子0/1/2/extra有無、MP=cost-1/cost/cost+1をold/new同SAVE SHA・seed・入力・時刻で可視向き/弾/標的/HP/MP・次tick比較。DESIGNED_NOT_RUN。不可視stack値だけはINELIGIBLE。原作Gameplay PASS0、strict MATCH0。
[NEXT] 576E80保存JSONとB所有caller根拠から出力slot writer/returnの正常条件、合法DAT Skill route、T013+A18/A1C最終targetを調査。禁止VAや0x580280内部の拒否済新解析は行わない。
[STATUS] OWNER DETAIL SAVED CANDIDATE / T012 + T013 + B-HANDOFF READBACK REQUIRED / E FORMAL INTEGRATION PENDING / RUNTIME VERIFY。