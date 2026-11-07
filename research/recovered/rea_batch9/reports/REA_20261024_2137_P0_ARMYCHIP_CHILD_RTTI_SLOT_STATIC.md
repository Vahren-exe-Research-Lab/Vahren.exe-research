# 迫真戦記 ver0.67｜REA P0 ArmyChip子要素の実vtable解決
ID: REA-LOCAL-20261024-2137-P0-ARMYCHIP-CHILD-RTTI-VCALL-TARGET-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY。2026-10-24 21時台 JST。新規REA VERIFIED=0、Golden NOT RUN。
原作EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
統合V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 出典・重複防止
MASTER/解析レーン規約/REA README/QUEUE/PROGRESS、既存21 runs/20261011T153958076Z sync、20261024 20H・2035報告、旧検索README/MANIFEST、V9入口を先読。
syncのWave1-5=64/64。旧QUEUE/PROGRESSはrename EPERMでstale。既存64に今回の48検査項目を加算しない。
20Hは子vptrの4 CALLIND存在と順序、2035は理論上の8分岐を解明済み。本記録は実クラスRTTI・各vtableスロットの具体的な宛先・固定戻り値を新規解決する差分。

## 新しい静的証拠
0x005B0C83 CALL 0x005B0EA0。0x005B0EA0は0x005B0EF6でChara基底vptr=0x00638164、0x005B0F42で派生vptr=0x0063AE74をオブジェクト先頭へ設定する。
0x0063AE70にRTTI CompleteObjectLocatorポインタ0x0063FFB4。COLのTypeDescriptor=0x0068DA64、decorated name=「.?AVArmyChip@ArmyChipBuilder@@」。
0x005B0C88で作成結果をESIへ、0x005B0CC3でbuilder+0x14のvector先頭、0x005B0CC9で一時格納した子ポインタのアドレスを指定、0x005B0CCD CALL 0x004C1290。callee擬似Cはポインタをvector末尾へ書いてendを+4進める。成功経路のコンテナ連結として確認。例外時の完全契約は未確定。
| 0x005B0A50 内site | 子vtable slot | 実宛先 | PE命令から分かる動作 |
|---|---|---|---|
| 0x005B0B53 | +0x34 | 0x004BBBD0 | RETのみ。直後AL分岐なし |
| 0x005B0B5C | +0x08 | 0x00431910 | MOV AL,1; RET |
| 0x005B0B77 | +0x48 | 0x0043B5A0 | XOR AL,AL; RET |
| 0x005B0B91 | +0x44 | 0x0043B5A0 | XOR AL,AL; RET |

## クラス限定で8通りを1通りへ絞る
通常正常復帰かつ実行時vptrが上記ArmyChip vtableを保持する場合、3判定の結果は +0x08/+0x48/+0x44 = 1/0/0。
そのため0x004C22B0(flag=0)は呼ばれ、0x004C3E40はスキップ、子+0x6C=0代入分岐はスキップ、0x004C2440は呼ばれる。0x004BC9C0 CALLは20H先行証拠から続くが、同calleeへの今回の再問い合わせはしない。
これは**新規生成ArmyChipの固定vtable**に限定する結論。既存配列へ別クラス/派生型が混入する可能性や生成後のvptr変更は未否定。以前の汎用8組合せを全体仕様として破棄せず、特定型の分岐を1例へ限定できた。
## 検証・5方法の充足
read-only原作PE実バイト・RTTI・vtable・V9の関数擬似C・E8とcallsite対応を別Python監査スクリプトで照合し48/48項目PASS。対象V9関数6件のverified_abi=0。info/pseudo/assembly/callers/calleesの新規完全セット=0。正式REA VERIFIED +0、TODO/VERIFY/BLOCKED書込差分0/0/0。
ゲーム実機Golden PASS=0、strict MATCH=0、完全複製率未測定。Ghidra/REA/ゲーム新規実行0。実行時間は監査単体約1.23秒、全調査時間未計測、PC総CPU/RAM負荷不明。
新規スクリプト: REA_20261024_2137_P0_ARMYCHIP_CHILD_RTTI_SLOT_AUDIT.py
新規JSON: REA_20261024_2137_P0_ARMYCHIP_CHILD_RTTI_SLOT_EVIDENCE.json
先行安全拒否 REA-LOCAL-20261024-2035-CLI-SAFETY-01 (0x004BC9C0の検索CLI) は迂回・再試行なし。先行拒否によるcallee内部未取得は継続。
## 次のP0 / Golden条件
次はこの型以外がbuilder+0x14配列に入る経路、登録時のvptr再設定・解放と配列変更による呼出順を限定調査。実機は別担当Golden条件として、ArmyChip子要素の正常経路で flag0 の0x004C22B0と0x004C2440を観測し、0x004C3E40/+0x6Cゼロ化を不実行と期待（NOT RUN）。
原本、MASTER、QUEUE、PROGRESS、既存runs/evidence、A-E、Git、Work、スケジュール無変更。REA所有フォルダの新規報告・JSON・監査スクリプトのみ。
