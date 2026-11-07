# REA 08H lightweight read-only probe recovery
RECOVERY-ID: REA-RECOVERY-20261031-08H-PYTHON-C-QUOTING-OTHER-01
Owner: REA / T015。発生時刻: 2026-10-31 08時台 JST。区分: OTHER（コマンド文字列の構文失敗）。CONNECTIONでもSAFETY_REFUSALでもない。
対象: PowerShell の `python -B -c '...'` を用いたread-only逆アセンブル印字（0x005E6CD0 / 0x005DA550）。
実結果: Shell側で引用符が脱落しPython SyntaxError。元EXE、Ghidra DB、MASTER、QUEUE、PROGRESS、Gitに書込なし。未保存の独立発見なし。
安全な代替ではなく通常の操作修正として、同じ許可済みPEのread-only検査を自担当の新規 `REA_20261031_08H_VORBIS_CODEBOOK_PROBE.py` に移し印字成功（拒否操作の迂回ではない）。
最終成功: 08H監査64/64 PASS、保存済みEVIDENCE.json、読戻し成功のREADBACK.json。新規正式VERIFIED 0、Golden実測0。
再開: 同一ワンライナーの繰返し不要。次回は保存済みEVIDENCE/STATICと08Hプローブを読み、0x005DA6D6/0x005DA811のallocator周りへ進む。
