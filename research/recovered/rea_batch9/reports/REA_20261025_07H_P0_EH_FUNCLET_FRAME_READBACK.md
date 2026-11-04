# 2026-10-25 07H｜REA EH funclet frame 保存・読み戻し
ID: `REA-LOCAL-20261025-0736-P0-SPOT-EH-FUNCLET-EBP-STATIC-01`
Status: PC-SAVED / STATIC / VERIFY / NOT READY
保存場所: rea_lab/decomp_task/ （新規3証拠 + 本readback、原本/既存成果無変更）
- AUDIT.py: SHA256 `E862DB1F4D6F01B412B331FDD4EA4508266DDC802670FBC811DE5979BEE7FAE2`
- EVIDENCE.json: SHA256 `7AE4785960D8E8C0AE83CFB9ECC51FD03FBBA19FEBC2B1C55F9C579F3158105D`
- STATIC.md: SHA256 `39C78A5729AF27B521C904D0CEC6B4C3DCAC6AE304B2B42E3048E057E0B45D8D`
Python auditor: 46/46 PASS（保存後別プロセス --verify: 46/46 PASS、READBACK PASS）。
独立PowerShell: JSONをConvertFrom-Jsonで再読込、ID一致、検査46/46、原作SHA一致、報告書にも同一IDが存在することを確認。2026-10-25T07:42:16+09:00。
前回06HのEBP=S未証明→当回正規state1 unwindの機械語経路のみ静的解決。REA 5種新規完成0、正式VERIFIED新規0、旧64重複加算なし、Golden実測0。
既知の初回read-only Python stdin日本語パス文字化けはOTHER（対処済）。安全拒否操作の再試行なし。次は `0x005B6C2B` のallocator契約またはatexit失敗分岐を非重複で調査。
