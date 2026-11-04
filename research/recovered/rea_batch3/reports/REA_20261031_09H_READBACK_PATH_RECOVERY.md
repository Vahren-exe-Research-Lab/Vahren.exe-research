# REA09H readback path recovery
RECOVERY-ID: `RECOVERY-REA-20261031-09H-READBACK-PATH-01`
Owner REA / task T015 / 2026-10-31 09H JST. Status RECOVERED; NOT READY.
初回の `REA_20261031_09H_P0_VORBIS_CODEBOOK_MALLOC_CLEANUP_READBACK_VERIFY.py` は、新規証拠のファイル名を `...MALLOC_CLEANUP_EVIDENCE.json` と推測し、FileNotFoundErrorとなった。
証拠は実際には `REA_20261031_09H_P0_VORBIS_CODEBOOK_ALLOC_CLEANUP_EVIDENCE.json` として48/48 PASSで既に保存済みだった。保存失敗や安全拒否ではない。
検証スクリプトの入力名のみを実在ファイルへ訂正し、再実行は `20/20 PASS`、0.2167秒。`REA_20261031_09H_P0_VORBIS_CODEBOOK_MALLOC_CLEANUP_READBACK.json` へ新規保存。
既存の監査・証拠・研究正本・他レーン/Gitは未変更。再開は `0x005D3DE0`/ `0x005D57C0` の所有権照合から。安全拒否の迂回なし。
