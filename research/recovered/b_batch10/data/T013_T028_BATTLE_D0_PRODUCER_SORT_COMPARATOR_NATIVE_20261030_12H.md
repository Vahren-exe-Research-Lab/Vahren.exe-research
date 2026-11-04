# B-20261030-12H-T013-T028-D0-CALLER-SORT-CLAMP-01｜管理値+0xD0の実引数同一性・直後の独立Unit並べ替え・x87下限判定
Owner B / T013（T028関連） / 2026-10-30 12時台 JST。STATIC / INFERRED / VERIFY / NOT READY。新規正式READY0、旧原作Gameplay Golden PASS0、strict MATCH0。
## PRECHECK / CONTINUITY
Desktop Commander Local CompactでPC実接続。MASTER最新 cp196/READY596（E旧正式値）、ANALYSIS_LANES_PROTOCOL、B HANDOFF、B5件owner、11Hの保存済詳細とRECOVERY-ID B-RC-20261030-1115-T028-T013-APPEND-SAFETY-01を先読。拒否された11H要約追記は再試行・別経路実行していない。
11H詳細 data/T028_T013_SELECTOR_D0_SENTINEL_RNG_GATE_NATIVE_20261030_11H.md は実SHA256 6A6AE20A74A4CB05E8139CDD285CEECA7C61F2364AD8844CE0660D8923AB3385 で存在を再確認。旧SAFE134/HOLD21、Library byte差54件、10/25未回収原文、他owner意味重複はOPEN。
## PE / INDEX
原作解析copy rea_lab/targets/hakushin067_Vahren.exe 実SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、V9 DB 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、SQLite immutable quick_check=ok。active.lockなし、Java/Ghidra稼働無し。既存V9 CLI function/callersと原作PE Capstone限定逆ASMを使用。
元PE window SHA：0x51EF80+64B=7D8940F552E10B91ECEBAB4A0310E3AFEA8E8C0D38115E342351FBC503AF17DC；0x5146F0+67B=66C3916B01E26F9F3D0836F5EB6772BBADC508539F871A13360B16B4BBCA4407；0x447D52+319B=09D7C23D0018426D64155D10F695AD8A6C736CE086A762B97F2A341F3B66B222。
## NEW：+0xD0 producer のcaller / pointer identity
統合V9直接CALL検索で 0x447810 のE8 callerは 0x51EF8F（関数入口0x51EF80）の1件。原作ASM 0x51EF8D MOV EDI,ECX → 0x51EF8F CALL0x447810、ECXはこの2命令間で変更されない。
callee 0x447850 MOV ESI,ECX → 0x44785A MOV [ESP+0x24],ESI、後続0x447D54 MOV EBX,[ESP+0x24]。従って当該合法制御フロー内の 0x447E41/0x447E56/0x447E88 の [EBX+0xD0] writerは、0x51EF80入口のECX管理オブジェクト自身へ書く（別proxy objectではない）。11Hの+0xD0条件/定数そのものは既知として再計上0。
## NEW：同じ caller で直後に独立のUnit配列ソート
0x447810 復帰直後の 0x51EF94 MOV EAX,[EDI+0x3C] / 0x51EF97 MOV ECX,[EDI+0x38] / 0x51EF9E PUSH0x5146F0 / 0x51EFA9 CALL0x47BB50 は、同じ管理オブジェクトの+0x38..+0x3Cの4-byte要素配列をソートする。0x47BB50擬似Cは境界差>>2・小区間0x44D6A0・分割0x47BCC0・再帰を持つ汎用ソートに一致（STATIC）。
PE native callback 0x5146F0（V9 function検索では独立登録NOT_FOUND）: Aの+0x0C/+0x10内側配列から先頭Unit候補を選び、Unit+0x1C8の参照先の+0xE4を取得。Bも同様。0x514728 CMP EAX,[EDX+0xE4]→0x51472E SETL AL→0x514731 RET。比較はsigned less-than。
このソートcallbackの0x5146F0..0x514731には+0xD0アクセスが無い。**+0xD0の計算が直前にあるからといって、この並べ替えの比較キーが+0xD0とは言えない**。+0xE4のゲーム上の名称、同値順、要素NULLの合法性・UIへの影響はVERIFY。
## NEW：x87の下限2.0はordered (<) のときだけ適用
前回11Hの0x447E41 FST [EBX+0xD0]の直後、0x447D9Aに由来する [ESP+0x64]=2.0 を0x447E47 FLD、0x447E4B FCOM ST(1)で score と比較。0x447E4D FNSTSW AX、0x447E51 TEST AH,0x41、0x447E54 JNE0x447E6A、テスト0のみ0x447E56 FSTP [EBX+0xD0]。通常のordered有限値では score<2.0 の場合だけ2.0に置換し、score>=2.0は維持する。unordered（NaN等）は条件により置換回避の静的予測だが、実FPU例外/状態はVERIFY。
0x447D64参照先+0x10=0または0x447D6E localFlag=0では0x447E82→0x447E88で1,000,000.0を直接格納（11H既知）。計算枝限定RNG 0x447E1A と共通 0x447C6E の消費差も旧11H既知・再計数0。
## DEDUP / PROVENANCE
B所有対象名に絞った data/*.md + B HANDOFF 計426ファイルをreadonly文字列照合。0x51EF8F/0x5146F0/0x51472E/0x447D54/0x447E4B/0x447E51 の各先行literal一致0。既知の0x447E41/56/88のwriter・sentinel・11H RNG gateは新発見として再計上しない。10/25原文と他ownerの意味的dedupは未完了。
## GOLDEN / NEXT / BOUNDARY
原作無改変EXE、2026-10-22能力20倍前のDAT、同SAVE/MAP/input/RNGで 0x51EF8F callerのECX/EDI、callee+0xD0（生値/下限/1e6）、ソート前後+0x38配列と各Unit+0x1C8先+0xE4、同値・空内側配列、次tickで比較。DESIGNED_NOT_RUN、DYNAMIC observed0、Golden PASS0、strict MATCH0。
次回：T013 4箇所の +0xD0 consumerと0x447810 producerの同一管理object/run時相、+0xE4 field producer、T011召喚EXP・T012 damage・T024 AI・T028 morale未解明P0。
本研究はread-only探索の増分をB所有ファイルだけへ保存する試み。原本EXE/DAT/SAVE、MASTER、他lane、REA/dev_lab/Git/Work/設定/automationを変更しない。
