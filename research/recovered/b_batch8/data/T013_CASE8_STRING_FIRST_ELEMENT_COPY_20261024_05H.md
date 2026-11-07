# B-20261024-05H-T013-STRING-FIRST-ELEMENT-COPY-01｜case8辞書値の先頭文字列コピーとNUL境界
[OWNER/STATE] B/T013主。2026-10-24 05時台 JST。STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。
[PRECHECK] Desktop Commander Local Compact成功。MASTER最終正式checkpoint196/READY596、5レーン規約、B HANDOFF・B5担当資料・22ファイル回収記録・既安全拒否を先読。PC現行V3 guard PASS_ACTIVE_V3_STATIC、入力SHA14/14、E8 CALL44889、JMP6324、errors=[]。
[INDEX] 最新pointerはV3 canonical、旧2026-10-21 search.sqliteは非正本。V3 CLIで0x49C450/0x49ECA0/0x49F390/0x402710、callers/calleesを軽量読取のみ。全面Ghidra/REA再実行なし。
[SOURCE] 原作 rea_lab/targets/hakushin067_Vahren.exe read-only実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 に一致。ゲーム実行・原本変更なし。
[NEW-1 SELECT] 0x49C54F～0x49C589原作ASM: 0x49C55Bでiteratorとmap headerを比較、不在なら0x49C563 push 0x68B3A8(empty string)。存在なら0x49C56A node+0x28(begin)をEDXへ、0x49C56D node+0x2C(end)と比較し同値ならempty。非空なら0x49C572 mov eax,edx / 0x49C574 push eax。第2要素を列挙せず先頭だけ選択。
[NEW-2 COPY CALL] 0x49C557 push -1 / 0x49C559 push 0、0x49C575で出力文字列capacity=15、0x49C57C length=0、0x49C585 first byte=0に初期化し、0x49C589 E8→0x402710へ。Ghidra+native ASMにより source stringのpos=0,count=UINT_MAX全域コピー契約と整合。
[NEW-3 SOURCE TYPE] 0x402710のnative 0x40271C source+0x10長を取得、0x402721 position範囲検査、0x40272F～0x402739でcopy長min(srcLen-pos,count)を生成。0x40276B/0x402785/0x4027B7でdest/sourceの+0x14 capacity確認、0x4027C2～0x4027C7にmemcpy(宛先,元+pos,実際長)。0x4027D3にdest+0x10 length書込、0x4027DAで末尾NULを追加。これよりnode+0x28が指す先頭要素は少なくともMSVC std::string様の長さ/容量付き文字列オブジェクトと静的に判定。
[INFERRED] node+0x28/+0x2Cは連続した文字列要素のbegin/endペアと整合し、先頭値だけ返す。vector<string>型名・要素stride・allocator/capacity(+0x30)・writerは未確定。lookupの完全な等値契約も既0415と同じVERIFY。
[NEW-4 NUL ASYMMETRY] 同系列のUnit検索入力では0x49E954 LEA EDX,[EAX+1] / 0x49E957 MOV CL,[EAX] / 0x49E95A TEST CL,CL / 0x49E95C JNEでC-style NUL終端のbyte数を測定し0x49E966→0x402800へ渡す。一方、辞書値コピー0x402710はstored source length(+0x10)を使いmemcpyする。埋込NULが存在可能なら『キーはNULで打切り・値は長さ分コピー』の非対称が生じ得る（INFERRED; ゲーム内に埋込NULが到達するか未確認）。
[PROVENANCE] 原作PE窓 VA0x49C54F len0x45 SHA256=66285BCEE6E4862428832B158901A0F74AA20CAC95DF524408A62BAE4F9574B1。
[PROVENANCE] 原作PE窓 VA0x402710 len0x30 SHA256=770B8A1B713C0D5317757210CB2C0E293DB276846188280D0F3725AFE3095EF0。
[PROVENANCE] 原作PE窓 VA0x40275C len0x8E SHA256=579814CEB7A31393CF33BE6476A50213F4A3E63B3997A2A592EC466F30F39F37。
[PROVENANCE] 原作PE窓 VA0x49E954 len0x3E SHA256=B4DDF849C23041EC7326FFA29C90BE51090B56CCD3FFB76A8F2B348E19193CEE。PE image base=0x400000、Capstone x86-32 readonly。
[DEDUP] 0415のiterator outparam/不在・空値2分岐、0317のproducer→Unit検索と空フォールバック、0217のbyte辞書順を再計上しない。今回初確認は先頭要素のstring ABI、全部コピー、キーNUL終端と値length memcpyの対照。B T013_AI/HANDOFFで0x49C572/0x49E95E/embedded NULの既出0件をread-only確認。一般的0x402710参照自体は旧研究に存在（新関数扱いしない）。
[RECOVERY] 本run軽量read-only Python旧式引用符組立でSyntaxErrorが1回（Localプロセス起動後に引数リストが途中で切断）、後続の独立許可済み文書検索で正常完了。これはOTHER/構文ミスであり接続障害や安全拒否ではない。新たな安全拒否0。拒否済み0x5710C0..0x571500／0x514C50／0x5769B0 XREF／拒否payload再試行・迂回なし。
[UNSYNCED] 10/21の19+Library3=22ファイル回収済み事実と、後発『03～12時10研究未同期』とのID単位意味照合は未了。02時後発Library訂正版2・08:10/14:14拒否本文は別未解決。過去拒否研究の復元を装わない。
[GOLDEN] 同一無改変原作EXE・X20変更前DAT・SAVE・MAP・操作・RNGで辞書キー不在/値配列空/単件/複数件（異なる文字列で先頭値選択を区別）、値内部NUL/15,16byte境界とキーNUL有無を比較すること。データで埋込NULを合法構成可能かはVERIFY。DESIGNED NOT RUN、旧Gameplay PASS0、strict MATCH0。
[NEXT] B/T013: node+0x28/+0x2Cの実writerと要素stride、同キー複数値の挿入順・空配列境界、0x49E8B0への検索キー生成前のNUL可否を合法な既存SQLite/原作ASMだけで追跡。T011/T012/T024/T028のP0は未解明継続。
[BOUNDARY] B新規READY0、E MASTER統合0、Task DONE0。PCへ書くのはB所有detail/T013_AI/B HANDOFFのみ。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/スケジュール変更禁止。
