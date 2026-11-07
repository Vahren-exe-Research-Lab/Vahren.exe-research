# 迫真戦記 REA｜2026-10-30 11H P0 追加検証：Vorbisのフレーム消費commitガード
研究ID：`REA-LOCAL-20261030-11H-P0-VORBIS-FRAMECOMMIT-UNHANDLED-VERIFY-02`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。先行11Hモデルの正式な補足であり、既存知見を二重計上しない。
## 新しい独立静的証拠
既存V9の`0x005D5790`（37bytes）と原本同一SHAの研究専用PEを直接照合。`0x005D5799 TEST ECX,ECX` の後、countが非0なら `0x005D57A0 ADD EDX,ECX`、`0x005D57A2 CMP EDX,[EAX+0x14]`、`0x005D57A5 JLE`で上限内を許容する。
上限を超えると `0x005D57A7 MOV EAX,0xFFFFFF7D`（-131）からreturnし、`[EAX+0x18]`の消費カーソルを増やさない。成功側 `0x005D57AE ADD [EAX+0x18],ECX` はframe数を進め、`0x005D57B1 XOR EAX,EAX`で0を返す。
呼出元 `0x005D0FB0` の `0x005D128D CALL 0x005D5790`直後は`0x005D1292 MOV ECX,[ESI+0x48]`、`0x005D1296 CALL 0x005D48E0`へ直行し、**commit helperの-131を判定しない**。その後 `0x005D12B7/BA` でframeBytes×frameCountの正の復号バイト数を返し得る。
## 11H先行モデルへの限定修正
先行 `REA_20261030_11H_P0_ODDRATE_EXTRA_PCM_ADVANCE_STATIC.md` の「11,025Hz・1〜4chで半周あたり+131×Cバイト多くPCMを復号」は、すべての成功出力に対し今回の**commit helperも0を返して消費状態を更新できた場合の条件付き結果**。返却バイト数が正という理由だけでは内部カーソル進行を証明できない。
直前の`0x005D5730`が返すframesが利用可能frames上限内なら通常はcommit guardに収まると考えられるが、その不変条件は未検証。異常状態・競合・入力破損での到達は不明。音声欠落・同じPCMの再読込・原作バグを確定したものではない。
## 検証と継続
`REA_20261030_11H_P0_FRAMECOMMIT_GUARD_AUDIT.py`のPE命令/V9/CALL静的検査 **23/23 PASS**。11H先行60/60を保持。新規正式REA 5種完備0・VERIFIED0、既存静的64/64、正式TODO/VERIFY/BLOCKED差分0/0/0。原作Golden0、完全複製率未測定。実ゲーム・Ghidra・REA再起動なし。
出典SHA256 EXE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。保存先はREA所有ディレクトリのみ。他レーン・原本・Git・スケジュール・共有正本無変更。
**次の最優先：** `0x005D5730`が与えるフレーム数と`0x005D5790`の残量ガードを直接照合し、消費失敗が実経路から到達可能かどうかをVERIFYする。
