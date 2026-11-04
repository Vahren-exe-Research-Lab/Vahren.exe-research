# 迫真戦記 新B T012｜戦略→戦闘入口：参照元の解決、援軍分岐、別初期化による上書き境界
研究ID: B-20261021-BOUNDARY-02 / 日付: 2026-10-21 JST / owner: B T012（T011/T013/T024/T028参照）
状態: STATIC / INFERRED / VERIFY / NOT READY。実旧Gameplay Golden PASS=0、新旧strict MATCH=0、当回新B READY=0、E MASTER統合=0。
対象の原作EXE識別SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回原本の再hash・起動・変更なし。
PRECHECK: Local CompactでMASTER最終E checkpoint195、規約36行、B HANDOFF最終拒否IDとT011/T012/T013/T024/T028 owner、復旧22資料、search_index README/BUILD_MANIFEST PASSを読取。active terminal sessions 0、CPU/RAM実使用率UNKNOWN。T011前回の拒否 0x416870 と当該研究本文書込は再試行しない。
PROVENANCE: 既存Ghidra search_index の対象function/callees/search のみread-only。A既存T010とC既存T025資料はread-only参照、所有権を移さず既知READY再計上0。
CODE_SHA256: 0x48F9E0=01FA8FF96D64D2B66D8B17560E9B27FA68C6A7A5529A1A377C155E38C8A24C58。
CODE_SHA256: 0x597B00=304B70512EDD5BA69D52DB15D79C0B46193837488C0CC6C7CB9B310623773002。
CODE_SHA256: 0x583C70=7C21FE57FA64A54B8D9A5A5C4FE44C487561BBCCED3D62060CABD8AAD7B02D90。
CODE_SHA256: 0x49AF10=12C67F7C7EA415371B864D7FB4073BB7DA623B9E426F71FB6C2D0090F92803C7。
CODE_SHA256: 0x48F720=2D9CB26D2093138C72C9481C418A54BD6A6709521C2C39AB07684B53265EB821。
【静的検出された入口の受渡し】
1. 0x48F9E0への直接CALLは5 site：0x475AD0、0x47D9B6、0x4CD931、0x522322、0x5B1F57（search.py function CALL索引）。5経路の人間向け種類と実到達頻度は未確認。
2. 0x48F9E0は擬似Cで E+0x1EED18=0 を書き、E+0x1EED1C=param_1 を格納する。その後 0x48FBEA→0x597B00 の戻り値を E+0x1EED4C へ、0x48FBF7→0x583C70 の戻り値を E+0x1EED50 へ設定。以前のB-20261021-BOUNDARY-01が確認した0x4922A0の@battlefield/@battledefense/@battleattack公開とのproducer→consumer接続が新増分。
3. 0x597B00のGhidra擬似Cは in_EAX+0xB0 の参照元を取り、その+0x2E0 treeを走査する。node[10]候補の+0x68と0x415460関連結果を比較、条件が成立すれば候補のpointerを返す。該当候補が無ければ参照元+0x58というpointer式を返す。ゲーム上のPower・Spot・Unit型はASM/RTTIでVERIFY。
4. 0x583C70のGhidra擬似Cは in_EAX+0x94==0のときのみ in_EAX+0x1A4のowner候補を使い、owner+0x2F0 treeのcandidate+0x20を比較。条件成立で0x597B00の結果へ進み、それ以外はowner+0x58のpointer式を返す。無候補=単純NULLとモデル化できないが、fallback対象が中立Power等かはUNKNOWN。
5. 0x48F9E0は 0x48FA1D→0x597860 由来のcVar4候補を E+0x1EED40/+41/+42 の3byteへ複写。cVar4==0のとき0x48FA56→0x40B200由来の値で+42を上書きする候補経路。Ghidraは0x597860の戻り型をvoidと誤復元するため、正式ABI/判定値の意味は原作ASM照合要。
6. さらに 0x48F9E0 後段で *(int*)(*(int*)(E+0x1EED4C)+0x10)==0 なら E+0x1EED40 を0にする分岐がある。A既保存nativeで0x492710のlimit初期化は同+0x1EED40によって別context-keyを選ぶと判明済み。ただし同一battleで0x48F9E0→0x492710の実順が固定か、どのキーが採用されるかはVERIFY。
【援軍・外交/選択分岐：戦闘開始packet確定時点を区別】
7. 0x48F9E0 0x48FBD9→0x48F720 が実候補iStack_38を返す。0x48F720はtreeを走査しkey・payload判定でポインタを返し、見つからなければ0。map/援軍/代表者の最終型はVERIFY。
8. E+0x1EED4Cの対象+0x10==0の枝を処理した後、0x4900DA→0x597A50の結果>0、iStack_38!=0、[iStack_38+0x94]==0の3条件で、0x490122→0x4868D0の戻り値を用いる。真なら0x490149→0x52DE20、偽なら0x490151→0x490180へ。条件が不成立なら0x490180へ。0x490180側は別途決定選択（decide3等）の擬似Cを持つ。これらがUI/援軍のどの選択か・最終roster変化・ランダム呼出はVERIFY。
9. 従って戦闘開始の「操作開始時の候補」と「援軍/外交/配置後の実3side ordered roster」を分離すべき。0x48F9E0に入った瞬間の生pointerを外部EXEへ確定packetとして送信するのは根拠不足。これは提案/INFERREDであり原作が二つの公式packetを持つことの証明ではない。
【初期状態上書きの別入口】
10. 0x49AF10の保存擬似Cには E+0x1EED1C=&DAT_00B0A9D0、E+0x1EED4C=E+0xCのowner+0x58、E+0x1EED50も同じowner+0x58への明示上書きが存在する。さらにE+0x1EED18=E+0x14、E+0x1EED44=E+0x1E8634、E+0x1EED48=E+0x1E8630。直接CALLは0x49C170（fn49B5C0）と0x522B8B（fn521D90）。これは0x48F9E0による戦闘候補と異なるコンテキストを作ることの静的証拠。
11. ただし0x49AF10が通常の戦闘終了直後に必ず呼ばれるわけではなく、UIモード/scene入口別の到達条件は未確定。外部hookで開始前/中/終了後のどこをcaptureするかにより、同じfieldに異なるpointerがあり得る。
【既存成果との重複回避・実装設計・Golden】
12. 既B-20261021-BOUNDARY-01の0x4922A0の3キー登録/0x493630の3キー再公開、A/T010の0x492710 limit-key/finish/world reentry、C/T025の戦争開始票と既存apply_battle_end APIは再解析/再採番しない。今件の独立増分は新producer 0x48F9E0、二段lookup fallback、+1EED40三byte分岐、援軍側delegate、別reset producer0x49AF10の跨関数接続。
13. PROPOSED extern battle handshake: Intent(戦争指示・候補) → ResolvedEntry(最後の参加Unit instance/ordered Troop/3side・実map/hash・owner/援軍・初期HP/MP/EXP/status/Skill/RNG) → ExecResult(終了理由・delta・RNG/event) → CommitReceipt(0x493630相当とWorld reentryを一度だけ)。これは新設設計であり原作ABIではない。
14. GOLDEN DESIGNED NOT RUN: EのC-NB02通常侵攻で合法原作1runを採り、(a)侵攻指示前、(b)援軍交渉/配置の選択後、(c)Fight event実行後と戦闘first tick直前、(d)戦闘終了直前、(e)strategy result apply直後、(f)World最初の可視画面復帰後をSHAと可視Unit名簿・Power/Spot・MAP・HP/MP/EXP・結果UIで区別。選択待ちの有無・通常/簡易/イベントは各別fixture。
15. VERIFY P0: 0x597860実戻りABI、0x597B00/0x583C70のin_EAX元、0x415460比較値、candidate/owner+0x58の型、0x48F9E0実起点と援軍による名簿確定、0x492710との実順、3side初期並び、時刻/結果/dynamic Golden。実再開発コードや原本へ書込無し。
16. SAFE: 前回T011 18時の0x416870 read拒否と詳細document書込拒否、旧0x5710C0..0x571500、08時資料転送、間接SQL、既拒否payloadは再試行/別shell/tool/path/Remote/ZIP迂回0。B以外のMASTER/他lane/REA/dev_lab/原本/Git/Work/設定/スケジュール変更0。