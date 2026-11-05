# Wave4 T014/T010 — 新規VERIFIED保存形式と時間カウンタの静的復元
- 時点: 2026-10-11。新規Ghidra成功run `20261011T113414092Z`。保存source/end SHA `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 対象は保存済み承認済みコピーの静的証拠のみ。旧ゲームEXE実行0・golden PASS0。新規関数3件とも5方法+境界がVERIFIED。
## T014: 0x427040 encrypt / 0x4270F0 decrypt
- Encrypt `0x427040`（174 bytes）：info `ev_04f97081148c5b70a34c1f70d55ef4100240002c8aade454c183f1c6c1f267be`、pseudo `ev_cc5bde730579a34289233a8406ed8b02996d9ffebd7ec12b375398fd353359f3`。
- Encrypt assembly `ev_21d9cad3ff2b047a9f34ec1a4be3a8053e3bdb9ad5acc35c0d93e42dc035b9d4`。
- `*dest=0x04030201`のlittle-endian先頭4byte、続けて28byteの鍵を生成。28回の直接CRT rand `0x5B6EAB`消費経路がある。各鍵byteはGhidraの `round(rand * (1/32768) *112)+8` 形だが、真のx87丸め契約はVERIFY。
- `i=0x20`から末尾まで、byte `dest[i]+=key[i%28]` の周期加算（8bit wrap）。鍵28byteはoffset4..31に配置。
- Decrypt `0x4270F0`（148 bytes）：info `ev_635c2e10a0dc0c5959db8b9dbe207d6add73016686659c7d69d1ebc6ebf6d861`、pseudo `ev_39248efde5737b8ffb423ef2219bf7f22a8407ba4d2fba240047fa9dc22d9e8e`。
- Decrypt assembly `ev_84ece236c68732c4d4ba932ee7067c72cac05ae979a3b9c31eb74a1564448aff`。
- Magic違いはこの関数内の該当分岐で早期return。一致時にoffset4..31の鍵を読み、`i>=32`のpayloadから`key[i%28]`を引き、先頭32byteを除去するmemcpyへ進む。
- 不正サイズ(0..31)、Magic不一致時の上位エラー伝播/stream長、rand/x87丸め、in-place overlapを含む完全実行結果はVERIFY。
## T010: 0x565700 battle timing gate
- `0x565700`（35 bytes）info `ev_38f76e7e1e556dbcfffe3e8830f53a66c5080b395e7673add73eb5a6e73ceeac`、pseudo `ev_4236ba2cb5bd0403d1f1c52ce271be5a980a0170aaca244cd2a26067d727ed38`、assembly `ev_199f778915fba3f40b5f0f5c530cd39c09ae578cfceb26396b480efca1a1a6fa`。
- グローバル `0x67B938==0x80000008` の場合 `0x67B93C`を1増やしてreturn。そうでなく `0x67B93C>0`の場合は1減算、0以下は維持。
- sentinelの人間向け意味・実戦フレーム頻度・callback側の補足処理はVERIFY。既存T010とは別の新規STATIC監査資料として記録。
