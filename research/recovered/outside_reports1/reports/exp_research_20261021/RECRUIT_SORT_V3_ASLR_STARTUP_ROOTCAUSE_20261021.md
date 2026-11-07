# 人材雇用・雇用可能順 V2 起動失敗の原因と V3 修正実証
- ID: `WRQ-RECRUIT-SORT-ASLR-V3-20261021`
- Date: 2026-10-21
- Status: `STARTUP_HOOK_INSTALL_VERIFIED` / `GAMEPLAY_NOT_TESTED` / `NO_MASTER_MODIFICATION`
- 試験: ユーザーPCの32bit Windowsネイティブプロセス。原本ゲームは起動していない。
- 対象: 迫真戦記0.67 / `Vahren.exe` + `新約迫真戦記ーほのぼの神話ー.exe`、両派生EXE。

## 症状と切り分け
- V2起動時の表示: 「HakushinRecruitSortV2.dll failed to install; starting original game.」
- ゲームフォルダ内の原本・V2派生EXE・V2 DLLのSHA256を検証。想定した版と一致。
- 32bit PowerShellによる `LoadLibraryW` は成功。`GetProcAddress('HakushinSort_Install')` も成功。
- 本体ゲームを起動しないステージ診断EXEでは、V2の `HakushinSort_Install` がFALSEを返した（終了コード30）。
- 条件ジャンプを1つずつ調査した結果、最初の失敗点はDLL `0x1000106F`。
- 直前の機械語 `0x10001067: cmp dword ptr [eax+ecx+0x34],0x00400000` は、ゲームの実際のロード時に一致しない。
- これはPEヘッダー内のImageBaseを固定アドレスと比較した不適切な実行時版検査であり、DLLの配置・破損やWindowsがDLLフックを禁止したことではない。

## 修正
- V3ソースの検査: `if(hrs_u32(nt+24+28)!=(U32)g_base)return 0;`
- 修正後の実機DLL命令: `cmp dword ptr [eax+ecx+0x34],eax`。
- 検査全体は残したまま比較対象だけを実行中のモジュール先頭アドレスへ変更。
- 比較命令だけを変更したテスト用V2 DLLでもステージ診断は終了コード0へ改善。
- V3ソースから独立再ビルドしたDLLも、Windowsに転送してステージ診断に成功。
## Windows上で確かめた成果
| 組合せ | 導入ステージ結果 |
| --- | --- |
| 原本に対応したVahren V2 EXE＋未修正V2 DLL | 30（Install失敗） |
| Vahren V2 EXE＋比較条件のみ修正DLL | 0（Install成功） |
| Vahren V3 EXE＋ソースから新規ビルドV3 DLL | 0（Install成功） |
| 新約迫真戦記 V3 EXE＋新規ビルドV3 DLL | 0（Install成功） |
| Vahren V3 EXE＋ゲームフォルダの既存V3 DLL | 0（Install成功） |
| 新約迫真戦記 V3 EXE＋ゲームフォルダの既存V3 DLL | 0（Install成功） |

## 既存ファイルの保全・競合
- 既存V3 DLLはゲームフォルダ内に既に存在したため、SHA相違検出により書込みを中断して上書きしなかった。
- 既存 `HakushinRecruitSortV3.dll` SHA256:
  `C9879BA31F75B7DE74A3B8948A80117D533BCB6D3D1CBF39E23A80438B0903C2`
- 比較検査用に独立再コンパイルしたV3 DLL SHA256:
  `0B375E0043B6E59666736DF024DA3DF72D5E756FD0061D818EB9AB426D8D5A9F`
- 既存のV3 DLLでも上記2種類のインストールテストが成功したため、現段階で置換不要。
- V3対応EXEも両方既存、想定SHA256と一致:
  - Vahren V3: `1BE236967FB306C6774141DCE6A2AE404CD1D594E37C57D03EAF9BDFDB6FD1D1`
  - 新約迫真戦記 V3: `107D522358FFEFCDA581B41C40864B0E2ECB84103DA2CB500A93BB2BB17C308A`
- 元の実行ファイル、DAT、セーブデータ、MASTER、他レーンのソースは変更していない。
- 一時テストはユーザーPCの `%TEMP%/HakushinInstallProbe_20261021`。診断EXEはゲーム本体の処理を実行せず、開始前のDLL導入処理で終了させる。

## 未確認と次の再開
- **未確認:** 実ゲームの起動完了、画面レイアウト、雇用可能人材の順序、スクロール、ホバー、選択時の費用と人物ID、雇用決済、セーブ・ロード。
- **制限:** 候補列の先頭100件内の並び替え。101件目以降を引き上げる機能は未実装。
- 次はゲームフォルダの既存 `*_修正版V3.exe` と `HakushinRecruitSortV3.dll` を使用し、コピーしたテストセーブで混在ケースを検証する。
- V2は以前の誤検出があるため使用しない。V3でも画面異常・誤雇用があれば即中止し原本EXEへ戻す。
- 調査・修正の主体は本チャット。Workは未使用。ファイル調査や診断に障害が生じた場合は、このIDを起点に未完了範囲と再開位置を記録する。
