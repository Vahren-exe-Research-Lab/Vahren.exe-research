# REA 15H｜検証スクリプトの初回失敗と修復記録
RECOVERY-ID: REA-RECOVERY-20261030-15H-READBACK-TEXT-CHECK-OTHER-01
種別: OTHER / VALIDATION_ASSERTION（安全拒否・接続断・原本変更ではない）。
対象: 独立読み戻し `REA_20261030_15H_P0_VORBIS_PAGE_STATUS_READBACK.py` の報告書文字列検査。
初回: 報告書に実際のCALL site `0x005D0FFA` を短縮表記 `0x005D0FF2..FA` としていたため、文字列一致assertに失敗。ハッシュ・静的監査の失敗ではない。
対応: 自担当の新規15H日本語報告書のみ `0x005D0FF2..0x005D0FFA` へ修正。検証条件を緩めずに再実行。
最終: 監査50/50 PASS、独立読み戻し12/12 PASS、4ファイルのSHA256を専用readback JSONへ保存。未保存差分なし。
再開位置: `0x005CEB90` のページ取得戻り値/EOF分離。REA正式VERIFIED・Goldenは増加0。
書込範囲: `rea_lab/decomp_task/` 以外無変更。前回14H成果は無変更。
