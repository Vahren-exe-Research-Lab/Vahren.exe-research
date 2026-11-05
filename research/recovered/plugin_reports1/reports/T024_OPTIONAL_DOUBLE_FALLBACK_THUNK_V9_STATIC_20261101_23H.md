# 新B T024｜0x542280 二経路入力: +0x50 double優先と+0x40/+0x38 fallback（2026-11-01 23H JST）
research_id: B-20261101-23H-T024-542280-OPTIONAL-DOUBLE-FALLBACK-01
owner: B; tasks: T024（T013は最終対象への連結未確証）; status: STATIC_V9 / INFERRED / VERIFY / NOT READY; Golden PASS 0, strict MATCH 0, DYNAMIC 0.
## 出典・既存研究との非重複
Desktop Commander Local Compact ONLINE。PC MASTER cp196/READY596はEの旧checkpoint値（本run再集計なし）。B規約/HANDOFF、PRIVATE GitHub developのKNOWLEDGE_CURATION_PROTOCOLとRESEARCH_INTAKE_PROTOCOL、B 10〜22HとV9を読取専用照合。
新研究は先行 B-20261101-22H-T024-DUAL-CALLER-FACTOR-PROVENANCE-CROSSJOIN-01 の2 caller対照を継承し、未解明だった0x542280の内部fallback条件を追跡したもの。10/25の+0x45D経路、20/21H mode0ゲート、13〜18H距離ソートは二重発見として計上しない。
V9相対資料: rea_lab/headless_analysis/search_index/00_START_HERE_UNIFIED_V9_20261023.md / HAKUSHIN067_UNIFIED_V9_20261023.sqlite / UNIFIED_V9_INTEGRITY_20261023.json。
V9 DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（保存済manifestで検証・今回全141MB再hash無し）。original EXE SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（manifest、今回PE再hash無し）。Ghidra擬似C個別SHA/行番号は本run未採取でUNVERIFIED_SOURCE。
## 新規静的結果
V9 function 0x542280 body [0x542280,0x5422BC] 61B（pseudoc帰属）。Ghidra表示: if (global double [0x63B0B8] != *(double *)(obj+0x50)) return *(double *)(obj+0x50); else return FUN_005E743A(*(int *)(obj+0x40)-*(int *)(obj+0x38)) + global [0x62A190]。
すなわち0x542280は+0x50を無条件に使用する関数でも、常に+0x40/+0x38差分で計算する関数でもない。比較定数0x63B0B8の実値・比較順序とx87 NaN/例外はVERIFY。+0x50が未指定時sentinelに一致するという意味付けはINFERREDであり確定しない。
V9 native direct CALL: 0x5422B0 E8 85 51 0A 00 -> 0x5E743A。0x5E743A entry 10B, 0x5E743F E9 CC DA FF FF -> 0x5E4F10 は **JMP（CALLではない）**。V9擬似Cは __cintrindisp2() と出すがABI/変換・時間/RNG等の実意味はVERIFY。
先行0x5271A0は0x52722F/0x527258/0x52728B/0x52729C/0x5273BAで0x542280を直接呼び、その返値を0x5272AB -> 0x528DB0や0x52727A -> 0x569730へ渡す経路を持つ（E8および擬似C）。先行0x528870の0x528919/0x5289EF -> 0x5E743Aは0x542280を呼ばず、global 0x62A190を加える別producer。2 callerの第3浮動引数を同一算出式に正規化しない。
## 補正・検証条件
22Hの「0x542280戻値由来」は維持し、今回は**戻値は+0x50 doubleの条件付き優先／別の場合は2つの整数offset差の変換＋定数**まで進めた。旧「0x5E743A＝RNG/時間」という未証明ラベルは採用しない。vtable、関数のnative prototype、実戦闘副作用、+0x50書込者、sentinel実数値、変換関数0x5E4F10の意味、最終ターゲットをVERIFYとする。
KB_CANDIDATE: 0x542280 / E8 0x5422B0 -> 0x5E743A / E9 0x5E743F -> 0x5E4F10; object +0x50(double)/+0x40/+0x38; globals 0x63B0B8/0x62A190; caller 0x52722F/258/28B/29C/3BAと0x528919/5289EF。Curatorのみ正式辞書・REF採録。
Golden: 正規原作ver0.67同一EXE/DAT/SAVE/MAP/入力/乱数/tickで+0x50とsentinelの前後、整数2値、double実引数、選択先0x528DB0/0x569730、Unit最終行動を同一実機runで観測するまでPASS0/strict0/READY0。
Recovery: 03H保存UNKNOWN、07H核心4未回収、10/25原文および54byte差OPEN。HOLD21旧安全拒否維持。禁止0x5710C0..0x571500と拒否0x5769B0 XREFの再試行・迂回なし。原本実行・全Ghidra再解析・共有KB/MASTER/他lane/生成DB/既存Git作業ツリー変更なし。次は0x63B0B8実値と0x542280のnative比較命令、+0x50 writerを既許可静的資料で限定照合し、T011/T012/T013/T024/T028未解明P0を継続。
