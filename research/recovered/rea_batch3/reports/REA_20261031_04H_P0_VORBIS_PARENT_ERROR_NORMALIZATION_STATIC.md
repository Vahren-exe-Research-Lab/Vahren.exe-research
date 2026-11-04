# 迫真戦記 REA｜2026-10-31 04H｜Vorbisヘッダエラーの親関数による非対称な伝播（P0）
研究ID：`REA-LOCAL-20261031-04H-P0-VORBIS-PARENT-ERROR-NORMALIZATION-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。03Hまでのtype1/type3のローカル解析と02Hルータの成果は再計上しない。

## 新規結果（静的に確認）
- 親関数 `0x005CF010` はヘッダルータ `0x005D44C0` を2か所から直接呼び出す。統合V9のcallers/calleesと原作SHAの機械語照合で `0x005CF167`・`0x005CF279` を確認。
- **第1呼出 `0x005CF167`：** 事前にVorbis type1署名を検査し、`0x005CF160`で`outer+0x58=3`に設定。返値が非0なら`0x005CF16F/171`のtest/jneで`0x005CF1E9`へ進み、**戻り値の種類を問わず-133へ正規化**してcleanupする。type1内部の-129（ポインタ異常）、-134（version異常）、-133（不正形式）がこの経路では外へそのまま出ない。
- **第2呼出 `0x005CF279`：** `0x005CF27E`で返値EAXをEDIへ退避し、非0なら`0x005CF285`から共通cleanup `0x005CF1EE`へ進む。戻り値は`0x005CF206`でEDIからEAXへ戻るため、**ルータ側のエラー種別が保存される**。通常のヘッダ順序ではtype3/type5が対象になるが、異常状態を含めてタイプを断定しない。
- 両エラー経路とも`0x005CF1F2`（`0x005D3DE0`）と`0x005CF1FB`（`0x005D3D00`）でヘッダ構造をcleanupし、`0x005CF20A`で`outer+0x58=2`へ戻して終了する。
- **原因を混同しない：** 親の`0x005CF267`（パケット取得結果-1）と`0x005CF2B4`（64-bit読込結果の負値）は、ルータ返値とは独立して-133経路に入る。親の別箇所`0x005CF216`は-128、`0x005CF21D`は-132をセットする。
- ルータ自身の-132（署名不一致）と-133（不正順序・ポインタ等）は02H既知。今回の新規点は**親の第1・第2CALLで異なる変換規則を適用すること**であり、二重計上しない。

## 根拠・監査
- `REA_20261031_04H_P0_VORBIS_PARENT_ERROR_AUDIT.py` によるPE32 x86 Capstone独立ASM、検索DBはread-only。**33/33 PASS**。新規REA/Ghidra実行はなし。
- source EXE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- 統合V9 SQLite SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。SQLite quick_check=ok、関数索引2件確認。
- 前回03H証拠43/43と2026-10-11保存正式同期ログ64/64を照合。古いQUEUE/PROGRESSのEPERM差分は変更しない。
- 正式STATIC VERIFIED **64/64維持**、新規VERIFIED **0**、新規REA5種証拠完備 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。
- ゲームGolden実測PASS **0**、完全複製率 **未測定**。REA5種（info/pseudo/assembly/callers/callees）を今回新規に完備したわけではない。ABI、メモリ破損、再入、確保失敗の実機安全性は未確認。
- PC接続は正常、開始時active.lockなし、対象script/resultは既存なしを確認。空きRAM約7.61GiB（監査前）、CPU負荷と総作業時間は不明。軽量read-only解析のみ。

## Golden条件案（未実行）
- type1で-129/-134/-133の異常を誘発できる**合法なテストデータ**を各1種用意し、入口呼出`0x005CF167`の親戻り値が-133となる条件を検証する。
- type3/type5で署名エラー・順序エラー等を発生させ、`0x005CF279`経由でルータ返値が保持されるかを別々に観測する。
- パケット読込-1とI/Oエラーはヘッダ解析エラーと別fixtureにし、ログで混同しない。ゲーム操作・原本の変更は実施していない。

## 次回再開位置
P0：`0x005D4030`のtype3確保失敗・長さ0入力に対するNULLポインタ条件を、`0x005D1C71` allocatorと`0x005D44C0` type5事前ガードへ結ぶ。今回の親のerror mappingを境界として固定し、対象ごとに独立証拠化する。

