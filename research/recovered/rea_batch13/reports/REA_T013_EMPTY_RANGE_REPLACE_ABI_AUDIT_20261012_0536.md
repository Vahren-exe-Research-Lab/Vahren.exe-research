# REA T013 — 空入力時の候補vector置換／ABI追加照合（2026-10-12 05:36 JST）
- 区分: 保存済みGhidra静的証拠の独立照合。新規REA/Ghidra取得0、VERIFIED増加0。ゲーム実機未実行。
- 証拠元: runs/20261011T153309850Z/{57CFA0_procedure_assembly.json,57CFD0_procedure_assembly.json,57CFD0_procedure_pseudo_code.json}、最新sync logs/progress_sync_20261011T153958076Z.json。
- 対象: 承認済み rea_lab/targets/hakushin067_Vahren.exe。実機Get-FileHash SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致。
## T013で追加確認した境界動作
1. 0x57CFA0では begin!=end 時、EAX=begin、ECX=EDX=end で0x5158A0を呼び、戻りEAXをvector.endへ書く（0x57CFA0..0x57CFB5）。これは既存要素の**論理的clear**。元storageのfreeや要素破棄はこの操作からは確定しない。
2. 0x57CFA0はその直後に0x57CFD0へ5値をPUSHして呼ぶ（0x57CFC2..C7）。空入力（src_begin==src_end）なら0x57CFD0の0x57CFFB..0x57D012は0レコードを算出し、JZ 0x57D15Eへ直接進む。保存assembly上、この早期分岐ではvector.begin/end/capへの書込もallocator呼出も行わない。
3. 従って「既存候補が非空／入力候補が空」で0x57CFA0を通過すると、論理end=beginのまま、0x57CFD0は0件挿入で戻る。これは空の新候補範囲に置換された状態。古い候補を維持するappend型実装は非互換になる可能性がある。
4. 既存候補も空ならclear枝をskipし、挿入0件もno-op。動的意味（容量維持、旧レコード破棄、並列状態・実ゲーム可視性）は引き続きVERIFY。
5. ABI補足: 0x57CFA0で5 PUSH、0x57CFD0でRET 0x14を再確認。今回照合した非連続2区画の保存assemblyでは[EBP+0x08..0x14]参照はあるが[EBP+0x18]参照は見えない。5番目を必須意味引数と断定せず、疑似コードの4引数形式も確定宣言とはしない。
## 根拠evidence ID（保存済み）
- 0x57CFA0/T013 assembly: ev_65ab310aa388f22a6840b91176516ae019845155a3de0f0f739d125e7ad14789。
- 0x57CFD0/T013 assembly: ev_08eb96aea33c3dbd4a1ae58fa08f3b20bfb31b8ccea4539a5bc0044cbb4887b5。
- 0x57CFD0/T013 pseudo: ev_fa33cc83cda4f064bed5262e5fa063359e2fbb86a07b22329757999821da3725。
- 0x5158A0/T013 assembly: ev_d4d1952d5b5e5da305467de47caec6d2ce02aadfbc2cd5475a12f7f41e291e80（既存監査での空range即RET根拠）。
## 進捗／制限／次回
- Wave1〜5: 64/64 静的VERIFIED、Wave5=16/16、P0=29/29・P1=35/35。今回増加0。Wave6未正式登録16候補=0/16（P0=5、P1=11、TODO16、関数VERIFY0）。MASTER最終checkpoint83: DONE9/34、旧EXE実機golden PASS0。ゲーム再実装率は測定していない。
- PC事前確認: CPU約11%、空き物理RAM約16.06GiB、Java/Ghidra先行0、active.lock=False、コピーSHA一致。新規Ghidra実行0秒／軽量照合全時間未計測。
- QUEUE.json/PROGRESS.mdは既往Windows EPERMによる古い表示。最新sync queueUpdate=STALE_RENAME_DENIED/humanReadableProgress=SKIPPED_QUEUE_STALE。既往renameを再試行・迂回せず、Wave6正式登録やrun_decompile.ps1新規起動は保留。
- 新規ファイルは本レポートのみ。原本ZIP/EXE、A〜E、MASTER、T018、研究他領域、MCP設定、Git/push/公開、automationsは無変更。
- 次回優先: 正式キュー更新が安全に復旧した場合に限り、T013 0x515750/0x515790/0x5159B0/0x57D180を最大4関数・単一MCPセッション・Ghidra 900000ms/request 960000msで検証。復旧前は既存証拠のread-only監査を継続。