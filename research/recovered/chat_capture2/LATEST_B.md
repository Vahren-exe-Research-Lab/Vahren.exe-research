迫真戦記・新Bの既存研究2件を整理し、非公開GitHubの既存Draft PR #18へ2コミット保存しました。GitHub読戻しは2/2一致しています。

**① `B-20261012-1719-01`：未回収キューの安全条件を訂正。** 現行developの保留台帳を確認した結果、`data/T013_AI.md`と`data/T012_BATTLE_CALC.md`は複合資料全体がレビュー保留でした。研究PCへの接続復旧だけでは読み取りを再開できないことを明記し、出典SHAの版差と、合法的な再開条件を記録しました。コミット：`e1cc37de151f727b57285444ca422b7fb30bcd66`。

**② `B-20261013-1814-01`：Codexが正本へ回収した原資料との対応を確認。** `data/T012_HEAL_ATTR_NAME_GUARD_551653_CONTRACT_20261013.md`は、developの回収照合表で`EXACT_BODY_AVAILABLE`です。記録された原資料SHA-256は`82D4B5E8…8640786`で、B担当の既存研究記録と一致します。GitHub固定版への参照を研究本文へ追加し、二重回収を防止しました。コミット：`d3e4a85c280794e28e5aa3970e581db1e3f15174`。

**保存結果：** [Draft PR #18](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/18)の最新HEADは`d3e4a85c280794e28e5aa3970e581db1e3f15174`。変更はB所有研究本文2ファイルのみ。developの確認済みHEADは`b347163cd3201b99f06ebdad0bb0882a4371f045`で、B担当から変更していません。

新規研究ID・追加PUBLISHED_INTAKE・新規CURATED・新規READY・原作Golden PASS・strict MATCHは各0件です。研究PCへの通常接続は429で失敗したため、原本SHA・MASTER・V9の再検証は未実施です。拒否済み索引書込、`B_AI_ENTRY.md`作成、PR説明変更は再試行していません。INDEX_UNSYNCEDを維持しています。

**次カーソル：** `B-20261011-0115-01`は保留中の複合原資料を再取得せず、既存メタデータと正式な保留解除条件だけを追跡します。独立した候補`B-20261012-1719-02`、`1814-01/02`は出典と既存保存先の照合を優先します。Codex側ですでに回収済みの資料は新成果として重複計上しません。