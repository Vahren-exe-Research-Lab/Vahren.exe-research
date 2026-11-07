# 迫真戦記 ver0.67｜REA 2026-10-25 02時台 P0: ArmyChipBuilder 2経路のowner引数とhelper EAX戻値
研究ID: `REA-LOCAL-20261025-0236-P0-ARMYCHIP-TWO-OWNER-RETURN-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。既存64/64 VERIFIEDは変更せず、今回の新規VERIFIEDは0。
原作EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
統合V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
基盤: MASTER/レーン規約/REA README・QUEUE・PROGRESS、最新sync 20261011T153958076Z、既存01Hの73/73監査・証拠JSON・報告、旧検索README/BUILD_MANIFEST、統合V9 read-only CLI。V9は11,950関数、SQLite quick_check=ok。QUEUE/PROGRESSの古い表示はEPERM起因であり、正式変更禁止。
## 新規確認A: 0x005B0680の2つのE8呼出元は同じowner生成ではない
V9 callers 0x005B0680 は **2件**: `0x004917B3`（関数`0x00490590`内）と`0x00491E99`（関数`0x00491870`内）。両E8の相対変位を原作PEで独立照合。
**経路1、0x004917B3**: `0x0049179F CALL 0x00597BA0`の戻りEAXが、`0x004917B1 MOV ECX,EAX`で生成関数のthis候補となる。別途`0x004917A4 MOV ECX,[ESP+0x7C]` → `0x004917AB PUSH ECX`がowner候補の**第2スタック引数**を用意する。事前に`0x004917AC LEA EDX,[ESP+0x48]` → `0x004917B0 PUSH EDX`が第1引数。caller側スタック値をrootグローバルと同一視しない。
**経路2、0x00491E99**: `0x00491DC2 CALL 0x00597BA0`の戻りEAXを`0x00491DCD MOV [ESP+0x28],EAX`へ保存。この値を`0x00491E80 MOV ECX,[ESP+0x28]` → `0x00491E8F PUSH ECX`により第2スタック引数（owner）として使用。`0x00491DC7 MOV EDI,[EBP+0x1EED1C]`の後に`0x00491DD1 CALL 0x00597BA0`、戻りEAXを`0x00491DDA MOV [ESP+0x24],EAX`に保存。2つのPUSH後に`0x00491E90 MOV ECX,[ESP+0x2C]`を実行するため、実アドレスは元の`[ESP+0x24]`を指し、この2回目の戻り値が**生成関数のECX/this候補**となる。第1・第3スタック引数はそれぞれ`0x00491E98`と`0x00491E8E`で用意。
**呼出規約上の重要点**: `0x005B06AB MOV EBX,ECX`、`0x005B06E2 MOV ESI,[ESP+0x40]`、`0x005B06EA MOV [EDI+0x24],ESI`、`0x005B06ED MOV [EDI+0x28],EBX`を照合。両callerの第2スタック引数がbuilder+0x24へ、ECXがbuilder+0x28へ格納されることを確認した。正式ABIの承認ではない。
## 新規確認B: 0x00597BA0 はGhidraのvoid疑似Cとは異なり、callerがEAXを使用する
V9疑似Cは `void FUN_00597ba0(void)` と表示するが、上記2経路のcallerは明確にその戻りEAXをECXやowner引数に使用する。実際の呼出規約/型は**VERIFY**であり、疑似Cを正しいhookプロトタイプと扱わない。
原作命令上の挙動: `0x597BD0`で`[EDI+0xB0]`を取得→`0x597BD6`で`+0x2C`、`0x597BD9`で`+0x504`を導出→`0x597BDF CALL 0x0049E490`。戻りが0なら`0x597BEC MOV EAX,[0x00AC0990]`で共有キャッシュを調べ、必要時には`0x597C6B CALL 0x005A8110`を経由して`0x597C74 MOV [0x00AC0990],EAX`。共通出口`0x597C79`から`0x597C89 RET`まで、EAXを上書きしない命令列。EAX値の厳密な論理型、キャッシュ共有・再入・失敗時の挙動は未検証。
第一回目の`0x00491DC2`はEDIが分岐によって`0x00583CF0`由来または前段値になり得る。第二回目`0x00491DD1`はEDIを`[EBP+0x1EED1C]`に明示変更する。したがって、**2回のhelperが同じ対象を解決するとは限らない**。
## 同一manager仮説の精密化
既知: builder+0x24がowner Xを保持し、builder処理`0x005B0B05/08/0B/0E`で`R=[[X+0x0C]+4]`、manager候補`M=R+0x0C`を参照する。main経路`0x00555E35 MOV ECX,0x008BE2F0`→`0x004B9930`→`0x004C24B0`の管理者はroot globalの`+0x0C`を使う（先行01H証拠）。
今回追加した点は、**Xの供給元が2経路で異なる**ため、`R=0x008BE2F0`または`M=0x008BE2FC`を全経路で証明したとは言えないこと。先行01Hが述べる「同じポインタ導出式」はbuilder登録と後処理で維持されるが、caller間のXの同一性までは含まない。所有者・キャッシュ同一性と寿命をVERIFYに維持する。
## 独立検査と非重複
新規`REA_20261025_02H_P0_OWNER_ARG_AUDIT.py`で原作PE/V9実SHA・SQLite quick_check・32個のx86命令・6つのE8相対CALL・6つのV9索引一致・関数疑似C/ABI未承認を照合し、**58/58 PASS**。保存済JSONを独立プロセスから`--readback`で再照合し**58/58・INDEPENDENT_READBACK PASS**。件数は**静的検査項目数であり関数完了数ではない**。00Hと01Hの既知命令の再照合は新規発見へ再計上しない。
REA info/pseudo/assembly/callers/calleesの正式5種完全充足0、新規VERIFIED0、正式TODO/VERIFY/BLOCKED変更0/0/0。旧Wave1～5 64/64はsyncの保存値で今回新規加算0。ゲームGolden実測0、strict MATCH0、完全複製率未測定。新規Ghidra/REA/原作ゲーム実行0。
## 安全・記録・次の検証
PCのLocal接続成功。解析開始時にdecomp_taskのactive.lockなし、Java/Ghidra/REA稼働プロセスの明確な検出なし。CPU全体の負荷・空きRAM・研究全所要時間は未測定。スクリプト実行単体は1.487秒、保存実行1.585秒、独立再実行1.822秒。既存安全拒否済み`0x004BC9C0`検索、`0x5710C0..0x571500`、Wave6・REA export等の再試行・迂回は0。
保存先はREA owner`rea_lab/decomp_task/`の新規ファイルのみ。原作、MASTER、QUEUE、PROGRESS、既存runs/証拠、A～E、T018、Git、公開先、スケジュール、Workは変更しない。証拠JSONは`--save`で新規作成のみ、既存ファイルの上書きなし。
次の**P0**: `0x0049E490`と`0x005A8110`の実際の戻り値・キャッシュ同一性、`0x00597BA0` EDI引数の分岐別値、`0x00490590`へ渡されるengine/owner pointerの由来を確認し、`R=[[X+0xC]+4]`が`0x008BE2F0`と一致する実行時条件を限定する。動的Golden設計（**DESIGNED / NOT RUN**）: 2 caller別にX/R/M/rootの値をログ採取し、共有キャッシュヒット/ミス、Builder0/1/多重登録時、manager loop exit前後を照合する。
障害IDは今回新規なし。新規静的監査PASS、後続正式VERIFIED/Golden昇格なし。
