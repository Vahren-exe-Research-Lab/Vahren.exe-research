# B-20261024-0015-T013-TROOP-MODE-EXPR-DEDUP-01｜case8 mode式のRTTI分岐とTroop重複適用抑制
[TASK/OWNER] T013主・T011/024参照のみ。2026-10-24 00:15 JST。STATIC-ORIGINAL-PE/STATIC-GHIDRA/INFERRED/VERIFY、NOT READY。
[BASELINE] MASTER cp196/既公式READY596、B HANDOFF/T011,T012,T013,T024,T028/未同期・拒否索引をLocalで先読。旧OFFLINE10/Library訂正版2/14:14拒否文書は未同期/未保存で変更なし。
[SOURCE] 原作ver0.67 rea_lab/targets/hakushin067_Vahren.exe 実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回Get-FileHash一致）。現行V3 verify PASS_ACTIVE_V3_STATIC SHA14/14、native E8 44889/JMP6324/errors[]。
[INPUT SITE] 0x4B5973 mov esi,[eax] → 0x4B5975 push ebx → 0x4B5976 E8 call 0x49CCA0 → 0x4B597B [ebp-80]=eax → 0x4B597E cmp eax,2; 0x4B5981 JG skip。signed >2だけを局所除外し、負値の実入力到達性はVERIFY。
[RTTI DIRECT] 元ASM 0x49CCA7/CCB6, 0x49CCC2/CCD1は esi Expression pointer から _RTDynamicCast(0x5E72E5)でtype 0x68C4F0を検査。PE RTTI TypeDescriptor 0x68C4F0='.?AUExpresNum@@'、0x68C144='.?AUExpresElement@@'。
[NUMERIC BRANCH] 成功時 0x49CCFA mov eax,[eax+4]／0x49CD00 ret 4: ExpresNumオブジェクトの+4 32-bit値を結果として返す。Ghidraの型宣言/ABIは未検証、式の適格性・外側parserは別扱い。
[STRING BRANCH] ESI=0又はExpresNum cast不成立で、0x49CD12 _RTDynamicCast(target 0x68C128='.?AUExpresString@@')。cast失敗時は0x49CD1E..36の例外経路。数値でない場合を単純0として扱わない。
[STRING LOOKUP] 0x49CD3B: cast-result+4をstringとして取り、+0x14>=0x10のときheap pointerへ解決。0x49CD46/4Aで実行文脈ポインタの+0x0CをEDX、文字列をECXにし、0x49CD4F→0x463CA0 E8。0x49CD54 mov eax,[eax+0x1c]でscript map entry値を返す。変数名・名前空間/返却ABIはVERIFY。
[MAP CAVEAT] 既Ghidra 0x463CA0はengine+0x30C/0x310 treeをlookupし、miss時0x20-byte entry+0x1c=0を生成して挿入する擬似Cを示す。missing variableの実副作用/例外/複数scopeはASM・実戦で要検証、現時点では0戻りの厳密仕様にしない。
[TREE INIT] case8 0x4B59AA call 0x476240は、[ebp-0x9c]から始まるtreeの+4=[ebp-0x98]に新規header/sentinelを設定し構成員数=0。0x476240 native+Ghidraで確認。
[DEDUPE KEY] 候補 0x4B59C9 Unit pointer → 0x4B59CC [Unit+0x1D0] をEDIに読み、NULLならskip。EDIを[ebp-0x88]に保持し、0x4B59E2/0x4B59E8にてeax=&output,ecx=&tree、ebx=&keyのまま0x4B59EE→0x44D070。
[TREE LOOKUP] 0x44D070 nativeでは node+0x0Cのunsigned値と[*EBX]を比較しlower_bound/equalityを求める。見つからないとtree headerをoutputへ、等値候補があればnodeをoutputへ書く。0x4B59F3 mov edx,[eax] / 0x4B59F5 cmp edx,[ebp-0x98] / 0x4B59FB JNE skip。
[DEDUP CONCLUSION] この比較は前回23Hの抽象的な『対象とのidentity一致』より具体的で、[ebp-0x98]はtree sentinel。JNE skipは既処理Troop-keyを除外し、まだ登録されていないTroopだけ0x4B59FD mode reload→0x4B5A00 E8 0x569530へ進む、とSTATIC-DERIVED。
[INSERT AFTER APPLY] 0x4B5A0E→0x565780（+0x14 tree node,keyを格納する候補）、0x4B5A20→0x5158E0（ordered-set insert/重複検査候補）。0x5158E0の既Ghidraは node+0x0C key比較・挿入/既存要素返却を示す。したがって1回のcase8候補走査中、同じTroopへのmode再設定を抑制する設計と整合。
[ORDER] 0x476240 init → Unit候補vector走査 → +1D0 NULL判定 → pointer-key tree lookup → 未登録時だけmode setter → set登録 → 次Unit。最初の有効候補が共有Troopに対するsetter入力を決める。ループ内対象の正確な順序は0x49E8B0とoriginal input未照合でVERIFY。
[DEDUP B] 23H B-20261023-2317-T013-TROOP-MODE-SOURCE-CASE8-01のproducer呼出・JG・NULL・CMP・setter siteは既成果として再READY採番なし。今回の増分はRTTI ExpresNum/ExpresString source選択と内部map値経路、0x44D070のheader/equality意味、適用後tree挿入での同一Troop抑制。
[NATIVE SEGMENT SHA] VA0x49CCA0/189 bytes=910AC6E0FBBF4B66014297CB5181900C54453EF5BA8777D11E5C659B2A15F3D3; VA0x44D070/90=FF21FFD6CFB210AAD1A2F95CB94B45917E1746A33E702BAA03B447E5379F7144。
[NATIVE SEGMENT SHA2] VA0x4B5957/247=A129B159255D9C4FC85167AFE745B27E6FE2D4CB2068620634012C625897D0BD; VA0x476240/105=45945E4A5F2613C29C41C22978D0D4D8F6EC79B2C1DE3905493E0F036A1D1373。
[GOLDEN REQUIRED] 原作無改変EXE/DAT/SAVE/MAP/入力/RNG同一条件でExpresNum直値(-1,0,1,2,3)、ExpresString同じ値の既存/未定義変数、同Troopに複数Unit/別Troop、NULL+0x1D0・同一key順序・setter発火回数/可視配置を採取。DESIGNED_NOT_RUN。
[VERIFY] ExpresStringからmap entryの実数値、欠損名追加時の副作用、0x49CCA0の例外とESI引数保証、Unit+0x1D0の所有/共有、候補順、+0x5158E0例外時状態、DAT命令名と実ゲーム行動、RNG。
[BOUNDARY] 原作起動・改変0、新Ghidra/REA0。MASTER/E/他レーン/rea_lab/dev_lab/Git/設定/Work/scheduleに書込なし。既安全拒否0x5710C0..571500、0x514C50、0x5769B0 XREF、拒否済payloadを再試行・迂回なし。
[STATUS] 新正式READY0／E MASTER統合0／DONE0／原作Gameplay Golden PASS0／strict MATCH0。PC保存と独立readbackは作成後に確認してHANDOFFへ登録する。
