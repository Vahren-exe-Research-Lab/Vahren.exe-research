## 迫真戦記・研究D｜2026年10月16日・0時台

**今回はT015の音声初期化処理で、未特定だったAPIを特定し、新規STATIC READYを1件確定しました。**

Desktop Commander Local CompactでMASTERのTASK QUEUE・最新checkpoint、レーン規約、D HANDOFF、T015・T017・T030担当資料を確認しました。

その後、保存済み機械語とDirectMusicのAPI仕様を照合し、成果をT015担当資料とHANDOFFに保存しました。**両ファイルの読み戻しと研究IDの一意性確認も完了しています。**

### 1．新規成果：`D-20261016-0032-01`

**T015｜DirectMusicプレイヤーの`InitAudio`呼び出しを特定**

前回の解析では、音声プレイヤー生成後に外部APIとvtable関数が呼ばれることまで分かっていました。

今回は、その正確な関数名と引数を特定しました。

| EXEアドレス | 確認した処理 |
|---|---|
| `0x609310` | `ole32.dll!CoCreateInstance` |
| `0x4BE582` | `IDirectMusicLoader8`を生成 |
| `0x4BE5BA` | `IDirectMusicPerformance8`を生成 |
| `0x4BE5DD` | `IDirectMusicPerformance8::InitAudio`を呼び出す |
| `0x4BE5DF` | 初期化結果を判定せず、次の要素へ進む |

`InitAudio`の同定には、COMインターフェースのvtable配置と7個の引数を使用しました。保存済みコードの`vtable+0xB0`は、DirectMusicPerformance8の`InitAudio`に対応します。:chatgpt-content-reference{index="0"}

呼び出し引数も確認できました。

```text
InitAudio(
    ppDirectMusic    = NULL,
    ppDirectSound    = NULL,
    hWnd             = NULL,
    dwDefaultPathType = 8,
    dwPChannelCount   = 64,
    dwFlags           = 63,
    pParams           = NULL
)
```

この引数構成は、保存済み機械語とSDKの関数宣言で一致しています。

### 2．重要な発見：音声初期化の失敗を検査しない

今回の新しい発見は、関数名の特定だけではありません。

**原作エンジンは`CoCreateInstance`の失敗を検査する一方、続く`InitAudio`の戻り値を、この呼び出し箇所では検査していません。**

つまり、処理は次のように分かれています。

- COMオブジェクト生成失敗：負のHRESULTを検出し、初期化ループを中断する。
- COMオブジェクト生成成功：`InitAudio`を呼ぶ。
- `InitAudio`呼び出し後：HRESULTを確認せず、次のプレイヤーの初期化へ進む。

これは再実装に重要です。

**「プレイヤーオブジェクトを生成できた」「音声初期化が成功した」「実際に音が再生された」は、それぞれ異なる状態です。**

旧エンジンの制御順序を再現するには、これらを区別する必要があります。

ただし、実際に`InitAudio`が失敗する条件や、失敗時にどのような音声不具合が発生するかは未観測です。

**音量0時のBGM停止・再開ループの直接原因を特定したわけではありません。**

### 3．保存・読み戻し結果

| 項目 | 結果 |
|---|---|
| 研究ID | `D-20261016-0032-01` |
| 担当 | T015 |
| `data/T015_UI_RENDER_INPUT_AUDIO.md` | **保存・読み戻し成功、1,083行** |
| `evidence/LANE_D_HANDOFF.md` | **保存・読み戻し成功、1,327行** |
| 研究IDの重複 | 両資料とも各1件 |
| 今回のD限定STATIC READY | **1件** |
| MASTER正式統合 | 未実施 |
| 原作Gameplay Golden PASS | 0件 |
| 新旧strict MATCH | 0件 |

前回の`D-20261015-2340-01`で確認したプレイヤー生成とAPI呼び出し順序は、重複してREADY計上していません。

今回の独立成果は、`InitAudio`の正確な同定、7引数の確定、およびHRESULT未検査の制御境界です。

### 4．MASTER最新状態

MASTERは**checkpoint 159**まで進行していました。

| 項目 | 正式統合済み |
|---|---:|
| 研究A | 115件 |
| 研究B | 190件 |
| 研究C | 132件 |
| 研究D | 114件 |
| **合計** | **551件** |

前回のT015成果2件は正式統合されています。

また、以前報告した音声初期化の引数解釈の誤りについても、研究Eがcheckpoint 159で訂正していました。

ただし、過去の拒否記録`D-20261015-2140-01`自体は、HANDOFF保存未完了の状態を維持しています。

**今回の新規1件は、正式551件には含まれていません。** 研究Eによる重複審査と統合が必要です。

### 5．T017・T030の継続調査

**T017では、** 保存済みの音声管理処理と効果音資産資料を再確認しました。

`playSE`の物理ファイル解決処理は依然としてVERIFYです。今回特定したDirectMusicの`InitAudio`を、効果音の`playSE`内部処理と同一視していません。

**T030では、** 既存の`isAllDead`、対象なし`addSkill`、2v2所属側判定を再確認しました。

特に、`isAllDead`が内部のUnit集合を検査した後、実行モードによって追加判定を行う構造は既知の成果と一致しています。

しかし、次の問題は引き続き未解決です。

- `isAllDead`の対象未解決時・2v2最終勝敗
- `addSkill`の対象Unitが存在しない場合の実効果
- 本部MPと兵舎・兵種生産の実際の変化
- 波状AI命令後の部隊行動
- T015の音量0ループとWindow Focus復帰後のGUI動作

今回はT017・T030の新規READYはありません。

### 6．PC負荷・安全・作業制限

Desktop Commander Local Compactは正常に動作しました。

確認時点では、Node 8プロセス、ChatGPT 19プロセス、Codex本体2プロセスが稼働していました。Java・Ghidra・REAのプロセスは検出されませんでした。

CPU使用率は取得できず、低負荷とは断定できません。

このため、今回は保存済み機械語と既存資料の軽量な静的照合に限定しました。原作EXE実行、新規逆コンパイル、重量解析、ゲームテストは行っていません。正確な作業時間も計測していません。

禁止された不完全な`T030_RTS_PRODUCTION_GRAPH.tsv`、既往の拒否済みEXE解析操作、拒否された書き込み内容には触れていません。

MASTER、T018、他レーン、REA、dev_lab、原本、Git、Remote、MCP設定、スケジュールも変更していません。

---

### 今回の結論

**新規D限定STATIC READY：1件。T015担当資料とHANDOFFへの保存・読み戻し完了。**

DirectMusicの初期化処理について、未特定だったAPIの正体が分かり、**オブジェクト生成成功と音声初期化成功を区別する重要な制御境界**を確定できました。

次は、この初期化処理とWindow Focus、プレイヤー再開処理との関係を、保存済み証拠から追跡します。

並行して、T030の2v2勝敗・本部MP・兵種生産・波状AIの実効果、T017の効果音ファイル解決を優先課題として維持します。

**T015・T017・T030はいずれもIN_PROGRESSです。**