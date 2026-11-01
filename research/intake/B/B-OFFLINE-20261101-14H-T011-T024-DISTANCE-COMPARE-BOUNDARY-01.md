# B 14H: 32bit距離比較の境界値とUnit適格条件の差
research_id: B-OFFLINE-20261101-14H-T011-T024-DISTANCE-COMPARE-BOUNDARY-01
owner: B; tasks: T011,T024; observed_at: 2026-11-01 14H JST; intake_at: 2026-11-01 23H JST
source_relative_paths: data/T011_T024_DISTANCE_COMPARATOR_BOUNDARY_CROSS_GATES_OFFLINE_20261101_14H.md
source_sha256: 2A6F516810D29B5B6E08AF683892CA8AD32300C7BDBF52C336E3D423064DAF63 (PC Get-FileHash実測23H、19H source map一致)
exe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (先行記録、14Hと本runのEXE実体再hashなし)
evidence_kind: PRIOR_CAPTURED_STATIC / INFERRED / SYNTHETIC_ONLY / VERIFY; golden_status: PASS0; strict_match: 0; dynamic: 0; ready_status: NOT_READY; intake: PUBLISHED_INTAKE/NOT_CURATED
prior_ids: 13H DISTANCE-SORT-MODE-GATE-01, 10H GROUP34-PROXIMITY-GATE-01。関数や距離ソート自体の発見を二重計上せず、境界条件・適格条件差のみ追加。
## 静的元命令と合成反例
以前採取した0x526030内のx86: 0x52607D 2B C2（SUB）、0x52607F D1 F8（SAR1）、0x526081 03 C2（ADD）。X=i32(left+SAR32(i32(right-left),1))で符号つき差をfloor方向へ割る。(left,right)=(10,7)は8。INT_MINとINT_MAXの合成例では32bit wrapで結果INT_MAXとなり、数学的中点-1とは違う。実ゲームでこの境界へ到達可能かはVERIFY。
0x52608E 0F AF C0 / 0x526091 0F AF C9 / 0x526094 03 C1 は二乗と加算を32bitで行い、dx=46341,dy=0の合成ではsigned結果 -2147479015。無限精度距離式への書換えはstrict互換ではない。0x526117 FCOMP、0x52611D TEST AH,0x41、0x526120 JNZではordered greater以外が偽側の条件付き静的モデル。負値平方根→NaN・x87例外制御とゲーム到達性はVERIFYで、原作BUG認定をしない。
0x569360の近接ratio集計はUnit+0x1867C==0かつ+0x1867E==0を要求する一方、0x526030の距離ソートanchorは+0x1867C==0だけ。flags=(0,1)は合成上取り扱い差が生じる。この2関数のフィルタをalive等の単一述語に統一しない。
CALL site 0x52AD35 -> 0x526030。先行Ghidra ZIP相対path functions/0052/00526030.c SHA256=7FEE7676046DFF1E081ED82702FBB17AEEEA2CCA92CCE64E1BB57B2F0D5745CF; 0052AD00.c SHA256=F733FD10A1DB29D30C54096EC23DFC45152BBF06805554C099F755A467ED80C8; 0056/00569360.c SHA256=309A88BD46955E9873936F91AF03731C50156A1B2476FAAA18EEE9F5696AAF1C（14H報告由来、本run擬似C再読なし）。
KB_CANDIDATE: 0x526030,0x569360,0x52AD00; Unit+0x40/+0x48/+0x4C/+0x1867C/+0x1867E。元14H検査のnative記録17件＋合成16件=33/33は旧結果であり今run再試験していない。
next_validation: 無改変原作同一DAT/MAP/SAVE/input/Unit群/tickにおけるx87状態、入力範囲、0x526030返値、0x52AD00ノード順・条件flagを観測。Golden0/READY0。
recovery: 03H UNKNOWN、07H core4 MISSING、10/25原文と54byte差OPEN、旧安全HOLD21維持。curator以外のdevelop/REF/辞書変更は禁止。
