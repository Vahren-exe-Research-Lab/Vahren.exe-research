# REA 2026-10-31 05H｜KB CLIの引数エンコード不整合（復旧記録）
RECOVERY-ID: REA-RECOVERY-20261031-05H-KB-CLI-ENCODING-OTHER-01
分類: OTHER / CLI_ENCODING, 安全拒否でも接続障害でもない。
実行時刻: 2026-10-31 05時台 JST（正確な秒は未計測）。
試行: Desktop Commander Local CompactのPowerShellで python -B knowledge/kb.py candidates --domain 音声 --limit 8。
実エラー: --domain の選択肢が文字化けし invalid choice と表示。検索候補8件は得られなかった。
最後の成功: 同じプロセスの kb.py addr 0x5D4030 / addr 0x5D1C71 / docs / research は読み取り専用で応答した。Private GitHub developのREADME・symbols.tsv・structs.tsvも読めた。
影響: KB候補の自動順位は未取得。今回のP0静的監査や保存済み56/56 PASSには影響なし。失敗結果を候補ゼロと誤解しない。
未保存差分: なし。研究上の未統合候補は05HのSTATIC報告へKB_CANDIDATEとして保存済みで、shared knowledge/MASTERは変更していない。
許された次手: 文字コード/PowerShellの表示・渡し方をまずread-onlyで検証し、必要時に専任KB統合担当が再検索。今回同一操作を無限再試行しない。
状態: RECOVERED_WITH_STATIC_CANDIDATE / NOT READY。既存のV9検索名差異は04HのINDEX_PATH_RECOVERY記録を優先し、二重記録しない。
