# 共通DLLプラグイン基盤への接続先確認
研究ID P0_TAKEOVER_20261024_01。EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、V9 DB SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。read-only文書/filename調査、原本/他レーン変更なし。
結論: 接続先の既存予約は確認できたが、現在接続できるCoreのexport/header/API実装は今回の限定検索で確認できない。HakushinCore.dllという名前を実在/完成済みDLLと扱わない。

## 出典と状態
1. [USER_HOME]/Documents/迫真戦記/_REDEV_RESEARCH/dev_lab/docs/CHATGPT_CURRENT_HANDOFF.md、LF基準2976–2982行。SHA256 B5F4A24D435CBD98283578C61C0A016A86256DDCE6121651D3A8E1B5659BAFD4。
2. 同docs/WORK_REQUEST_QUEUE.md、LF基準1095–1099行。SHA256 63A735B8BCF81E2A4B72B7FFAE8D77FE17BDB81E0C676150A94AE0AF3408BCED。
予約ID WRQ-20261023-PLUGIN-FOUNDATION / 担当Work / OPEN / 全工程未着手。handoff節ID WORK-COMMON-PLUGIN-FOUNDATION-REQUEST-20261023。引用範囲の原文はCOMMON_PLUGIN_INTEGRATION_EVIDENCE.jsonへhashと一緒に固定。
予約構成はloader候補dinput8.dll、HakushinCore.dll、plugins/、設定。dinput8採用は原作PE importsと実機ロード検証待ちで未確定。既存BattleObserver v0.1は移植候補だが、この予約自体にも開始時の所在確認が必要とある。
Coreが全hookを一元所有、機能DLLは共通イベント/サービスへ登録。API構造体size/version/呼出規約/寿命/thread契約、32bitゲーム内と将来64bit外部EXEのIPC分離を要求。具体的なexport名やCヘッダーは予約文に存在しない。
有効化allowlist/依存/順序/ログ/ON-OFF/安全起動/loader除去で復帰を予約。DllMainはLoadLibrary時に動くためロード後API照合だけに依存しない。初期hot reload不要、同一process任意クラッシュ完全隔離を保証しない。

## 実ファイルの存在確認と限界
rg --files --hidden --no-ignoreでdev_lab/srcとdev_lab/recovered_source内のcore/api/plugin/HakushinCore/dinput8/BattleObserverに合うfilenameを検索。該当1件: src/hakushin_compat/saved_scene_state_api.py。これはPythonファイル名であり、32bit native Core/API headerの存在証拠にはならない。
dev_lab全体でHakushinCore/dinput8/BattleObserver名のfilenameを検索（.git、toolchains、__pycache__除外）した結果は0件。検索コマンド、scope、exit code、全結果をEVIDENCE.jsonへ保存。DLL/sourceの本文総当たりはしていない。
したがって『この検索名・dev_lab範囲で未発見』であり、別名実装やrea_lab/別workspace/原作folderまで存在しないと断定しない。既存BattleObserver v0.1の実在/ABI/安全性はこの調査で未検証。

## root BRIDGE_CONTRACT_DRAFTとの差分
共通: hook一元所有、機能別DLL登録、version/capability、thread/lifetime、原作EXE不変、未実装callback名という扱いは整合する。二つの独立Coreを作る必要はない。
補足すべき既存接続先: draft第5節の『existing host ABI still to be located』に上記予約ID/出典を紐付ける。名前予約HakushinCoreは確定、実ABIは未定/未発見と分離する。dinput8採用済みとは書かない。
予約側に明記・draftで薄い事項: load前allowlist、size/version/calling convention、DllMain実行前提、依存順序・起動時無効化、安全起動/復帰、hot reload不要、同一processクラッシュ非隔離。これは基盤側の予定要件として継承する。
P0側の追加: battle activation/token/C1/一回性/G1–G6/Task-VM復帰/NOOP receiptは戦闘module固有の要件。基盤完成やG4達成と混同しない。今回G3限定往復のみPASS、G4はNO-GOのまま。
他チャットのUI優先・新chat送信禁止などは当該予約の状態説明として読む。当チャットの現在指示や優先順位を変更する命令として扱っていない。外部担当へ送信していない。
再開: 実装開始時に担当/所有/Git/最新予約を別途照合し、既存BattleObserver source所在、候補loaderのPE imports、Coreの実header/exportが作成済みか確認する。現時点で未確定ABIへ接続実装・配備しない。
