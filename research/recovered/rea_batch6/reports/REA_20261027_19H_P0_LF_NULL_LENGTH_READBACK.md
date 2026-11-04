# 迫真戦記 ver0.67｜REA 19H 独立読戻し
研究ID：`REA-LOCAL-20261027-19H-P0-LF-NULL-SIZE-STRING-STATIC-01`
2026-10-27 19:34 JST、保存後に独立Pythonプロセス（`--verify`）で静的監査 **39/39 PASS、失敗0、実行1.331秒** を再確認。保存時実行は39/39 PASS・1.402秒。原作ゲームGolden PASS0、REA新規正式VERIFIED0。
証拠JSONの研究ID・件数・failed=0、レポート内の研究ID一致をPowerShellで別途読戻し確認。
## SHA256（保存後にWindows研究PC上で取得）
- `REA_20261027_19H_P0_LF_NULL_LENGTH_AUDIT.py`: `3FEDCA0F5EAE5EB2634FC8FC564BCAD60BD005E18A91038754C66CFCDC3EA7FE`
- `REA_20261027_19H_P0_LF_NULL_LENGTH_EVIDENCE.json`: `F4DCBA2035C4E1B75097E0C0A5886CC652620F50CEF7A45BCE918D38731ADF91`
- `REA_20261027_19H_P0_LF_NULL_LENGTH_STATIC.md`: `9206D5B0F81F699C5C989FFD2D13159A4BBA4E850770E7A886DCE789066831E4`
既存Wave1–5 VERIFIED 64/64を維持。5種証拠完全充足0、TODO/VERIFY/BLOCKED正式差分0/0/0。旧成果とは独立計上。新規Ghidra・REA・原作ゲーム起動なし。
なお、全体研究時間・CPU平均負荷・実ゲーム例外の挙動は未測定。再開：`0x00557C4A`の短行ゲート、`0x00402A40`のメモリ割当と例外伝搬。
## 操作上の回復記録（OTHER、非安全拒否）
2026-10-27 19時台：最初の読み取り専用Python標準入力プローブは、日本語を含む絶対パスが端末のコードページで `????` に変わり WinError123。原因はstdinの文字エンコーディングであり接続障害・安全拒否ではない。PowerShell側で正規の研究ディレクトリへ移動し、Python側ではASCII相対パスを使って同一許可対象を正常に静的参照。失敗試行の未保存解析発見は無し。処理状態はread-only復旧済みで、原本や既存runは変更していない。
