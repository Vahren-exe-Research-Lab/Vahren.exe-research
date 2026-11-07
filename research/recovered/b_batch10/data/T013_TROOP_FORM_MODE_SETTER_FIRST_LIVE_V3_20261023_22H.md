# T013｜Troop+0x30モード設定と先頭生存Unit起点の配置再配送（22時台）
ID: B-20261023-22H-T013-TROOP-FORM-MODE-SETTER-01 / owner B:T013 / 2026-10-23 22時台 JST / STATIC-EXE-ASM + STATIC-GHIDRA / VERIFY / NOT READY。
【SOURCE】PC Local Compact成功。E MASTER最終公式checkpoint196/READY596、規約・B HANDOFF・B5資料・未同期/拒否索引をread-only確認。V3 guard=PASS_ACTIVE_V3_STATIC、SHA14/14、E8=44889、JMP=6324、errors=[]。原作EXE現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
【DEDUP】既B-20261023-18H/1915/20H/21Hは目標指定/生成/sort/2-index配布を既報として再計数0。HANDOFF/T013/T011への`0x569530`既記録検索では一致なし。範囲0x567000..0x56BFFFのcached擬似C43関数を+0x30/+0x38 writerで軽量走査。原本/他lane/MASTERに書込なし。
【NEW 1 / WRITER】Troop候補のモードsetter 0x00569530（113bytes）。原作ASM 0x569531 `mov dword ptr [edi+0x30],eax`。これが+0x30書込みの一つの直接根拠。V3 cached Ghidraと原作PE小窓一致。+0x30=0の初期化は既0x00568080、他範囲writerの全網羅はVERIFY。
【NEW 2 / PRECONDITION】0x569534～0x569547でTroop+0x0C/+0x10のメンバvector要素数を算出。0要素でも+0x30書込後にRETし、後続配置関数はCALLしない。
【NEW 3 / FIRST LIVE】0x56954F～0x56957Dで登録順にUnit参照をたどり、Unit+0x1867C==0の最初の候補に限って、0x56957D→0x569730 E8直接CALLで配置処理を呼ぶ。呼出位置はUnit+0x214/+0x218を整数2つとしてPUSH、Troop+0x28のdoubleを渡す。局所検証範囲では2人目以後を同callで反復しない。ABI/座標の名称はVERIFY。
【NEW 4 / THREE CALLERS】V3 callers(0x569530)はE8実証3件、jump-callers 0件。0x004B5A00（owner 0x004B4710）/ 0x004F9837 と 0x004FA043（owner 0x004F9510）。native bytes各E8で相対着地をV3照合。
【NEW 5 / INPUT MODE】0x4F9831 `xor eax,eax`→0x4F9837でmode=0を与える経路。0x4FA03A `mov eax,[esp+0x28]`→0x4FA03E `mov eax,[eax+0x28]`→0x4FA041 `mov edi,ebx`→0x4FA043 CALLで、別構造の+0x28由来値を与える。0x4B59FD `mov eax,[ebp-0x80]`→0x4B5A00 CALLでローカル値を与える。後者2値の到達時実値はVERIFY。
【NEW 6 / SECOND CONSUMER】0x0056A790 cached GhidraもTroop+0x30==1 / ==2 / otherwiseで別配置経路を分岐し、mode1では+0x38を構成員数上限に使用。既0x5699C0の3分岐と別のconsumerを確認。+0x28角度更新とD3DX回転があるがFPU/ABI/実行時用途はVERIFY。
【+0x38 / PRIOR】既0x568080が+0x38を`FUN_0046F4C0(owner+0x1B8,15)`で初期化、既0x568710はTroop+0x1D==0かつ最初の構成員追加の枝で`breast_width`を設定し、0なら同ヘルパーへfallbackする。既15H/19H研究との照合で、+0x38のゲーム上の厳密意味・0/負数境界は固定しない。
【EVIDENCE WINDOW SHA】原作PE read-only VA0x569530長113 SHA256=DE665FEE046108A0068F516BD61D2B8F7DC88E5B6B87B45D064DDFA0A1168663。VA0x4B59E8長34 SHA=607E206E4E8B5AB7560172F0D6BE26F592D53F9FE7AAFDBA79C9FB752895BA53。
【EVIDENCE WINDOW SHA】VA0x4F982D長20 SHA=23DC86B95DACF47CDB64E10C7D30269F03F39FCD97AD733DF7ACA1A3FC2E6924。VA0x4FA03A長14 SHA=7D2840BA587AC8B1F6B4624F58F15B0C0CE9506E3ADF6628FCCF1179DEEC428C。
【IMPLEMENTATION BOUNDARY】「モード更新」と「最初の生存Unitの現在座標を基準にした再配置要求」は1関数の独立段階。モード値はゼロ構成員でも保存され得る。1度のCALLだけで全Unitに配送済みとはいわず、0x569730/0x5699C0の後続で行われる処理と分離する。
【VERIFY】0x4B5A00のEAXローカル値producer、0x4FA043の参照先+0x28の実型/値、0x569530呼出規約・Troop pointer同一性、0x56A790のFPU・mode2丸め、mode再設定時に実unit移動が起きるか、後続RNG・隊列座標が未解明。0x5769B0既拒否XREF等には照会しない。
【GOLDEN DESIGNED/NOT RUN】無改変同一原作EXE/DAT/SAVE/MAP/input/seed/captureでmode=0/1/2/その他、構成員数0/1/3、先頭死亡・2番目生存、+0x38上限0/1/3、角度0/非0、初回命令と再設定命令を直交比較し、+0x30保存・0x569730 CALL回数・pairs数・実移動・RNG位置を観測。
【RECOVERY】旧03～12時オフライン10件、02時Library訂正版2件、14:14拒否されたdetailは未同期/未保存据置。既拒否された書込payload、0x5710C0..571500、0x514C50、0x5769B0 XREF等の別tool/path迂回0。今回Pythonコマンドの初回read-only SQL 1件は引用符崩れでSyntaxError、後続の独立した正常読取で回復しPC変更なし。
【STATE】B新READY0、E MASTER統合0、Task DONE0、原作Gameplay Golden PASS0、strict MATCH0。今回B-owner文書とHANDOFFの保存/readback可否は別途確認。次のB/T013検索: 0x4B5A00 EAX local producer・0x4FA043 +0x28 source・0x56A790と0x5699C0のmode別実座標式。原本EXE実行・改変・Git/Work/スケジュール変更なし。
