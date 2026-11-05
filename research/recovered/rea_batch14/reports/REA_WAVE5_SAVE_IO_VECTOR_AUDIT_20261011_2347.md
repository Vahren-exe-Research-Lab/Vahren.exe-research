# REA Wave5 保存I/O・AI候補vector 静的監査（2026-10-11 23:47 JST）
- 対象：承認済み `rea_lab/targets/hakushin067_Vahren.exe`、SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 根拠：`runs/20261011T144115307Z/RUN_RESULT.json`（23:41:15–23:46:33 JST）。REA6.1.0/Ghidra12.1.4、completed=true、failure=null、no_game_execution=true、end SHA一致。
- 4関数すべてinfo/pseudo/assembly/callers/calleesを保存。20ファイルの存在、関数entry/size、evidence ID、source/end SHAはRUN_RESULTとsyncで照合。
## VERIFIEDと根拠（各列は evidence ID）
| 関数VA / T-ID / サイズ | info | pseudo | assembly | callers | callees |
|---|---|---|---|---|---|
| 0x4705F0 / T014 / 256B | ev_8d6b4c6b269ce0021d9fc898bb87d4fb557a70421b0ed4453ab1d6c4d161784f | ev_3851d07b1e0119564efeb2d7215b9c16ff9a63f274ce843c13ed100dfee38752 | ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d | ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87 | ev_661507e7456c44d65dd153fff0f2c6b8de0e33a9519370d794118fae0def6743 |
| 0x470700 / T014 / 99B | ev_e676039e3083db867c85605ee376898d307e4a18d8f264c9c6f5003be1deb31e | ev_fa4f2750e44895495089baaea76f6c2e6b39e1ec155c9b68af4b63bc17ac8e07 | ev_f7ed3af4df1cdf7b14d9208f3d4aa735267b9ab022ee7d6b3860c4521bbb95cf | ev_14939a8b9ce66f7858434d5f57609aca8f4d26a7781078754cfc513c5032989c | ev_3f9a89a60c30eee71f662be8ef197b9016cfe610caae887926287dcb5d131286 |
| 0x471D20 / T014 / 144B | ev_d66eb9ca2ede2dddefec4ffa0700384bde6cdbe4d00f9186cf00ff67748de6fc | ev_ab5115883f3f7287b9e69a76b95333a8ddd343252dfc9c1efdafb3f4db81d846 | ev_64adbba14e1cee99ca12f12987032aa749c2890ee33057c941c4d0b3eed1fe6f | ev_a459496a5ab977b94c768d186aefbfc6f58bb2cb97dcc009e0be9b470f192a56 | ev_8f32e24032fa7db1f4ddd3212cbf805c0509f176888721d560966984d495d307 |
| 0x5154F0 / T013 / 207B | ev_49cbc451308e458f59684fb8b64adbb92e6d0bcdd5abb08e63f08fcf044184d2 | ev_8c2e00fbbaaca29b29284ec0899df000751530685da489a4b210c6bffdad8b4d | ev_6a53e867e218f8905561e0687a0340e1dafe224e61cc7d465b0047e7b21c3d64 | ev_8ce283bf9f936114ed4749b1907814810be35fb077af15de779d65256288d320 | ev_c8e76cb2fcf962a30ce7b57a87aa46569443fdfdf23f9314b8ef66435ce3447a |
## 静的観察（疑似コードから確定できる局所処理とVERIFYを区別）
- T014/0x4705F0: 共有0x400B buffer初期化→0x470980から1文字ずつ取得→NUL終端。0x20未満の非NUL制御文字・stream errorでLoadException。ループ境界はi<0xFF。FUN_00402800へ文字列長を渡す。実際の入力エンコーディング/例外再現はVERIFY。
- T014/0x470700: 0x42E700経由で4バイト相当の値を共有領域へ読み込み、stream errorを確認して出力先へ代入。解釈型・endiannessや既存save全体の互換性はVERIFY。
- T014/0x471D20: 0x4708A0×2、0x4628F0×2、32bit幅vectorの要素数ぶん0x470830を反復し、最後に同関数を1回追加。tag / sentinelの対応、reader 0x471AF0とのbyte-by-byte対称性はVERIFY。
- T013/0x5154F0: 固定24byte候補レコードを末尾追加。コピー元が配列内なら再配置前にoffsetを保存し、0x5155C0による再配置後にsourceを再基準化する。候補のrank・重複排除はここでは処理しない。容量成長/例外処理はVERIFY。
## 次回と管理
- Wave5: 12/16 VERIFIED（今回+4）/未着手4/関数VERIFY0。残りP1=0x5158A0,0x57CFA0,0x57CFD0,0x5155C0（T013）。P0 29/29、P1 31/35。全Wave 60/64。
- 研究MASTER DONE9/34（確認時点）、旧EXE gameplay golden PASS0。ゲーム再実装率は測定していない。
- preflight CPU約10%、空きRAM15.68GB、javaなし、active.lockなし、SHA一致。実行約318秒／Ghidra 900000ms・request 960000ms・最大4関数・単一セッション。
- sync `logs/progress_sync_20261011T144633765Z.json` は60/64のRUN_RESULT照合を正常集計。ただし既存 QUEUE/PROGRESS rename=EPERMで旧表示維持。ACL/lock操作や別経路での置換はしない。
- 次回は前提負荷を確認し残りT013 4関数の正式5方法取得を優先。部分失敗はVERIFY/BLOCKEDへ区分。
- 原本・既存5レーン・MASTER/T018・Git・MCP・スケジュール変更なし。安全拒否範囲0x5710C0..0x571500/既往拒否済み抽出は非対象。