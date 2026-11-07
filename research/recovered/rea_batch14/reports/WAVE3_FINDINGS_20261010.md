# REA Wave3 保存済みGhidra静的証拠の独立照合（2026-10-10）

対象: ver0.67専用Vahren.exeコピー、SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。ソースは `runs/20261009T222501703Z/RUN_RESULT.json`、`runs/20261009T223622536Z/RUN_RESULT.json`。各4件はinfo/pseudo/assembly/callers/callees、source SHA、evidence IDが揃い、保存済み証拠の静的取得判定VERIFIED。原EXEを実行してのgolden結果ではない。

## Script AST/variant (T005/T006/T011)

- `0x505210` generic property parser: 3717 bytes、declared callers1/callees22。target T005で先勝ちのRB-tree insertion `0x463280`まで確認済み。field layout・重複の意味論はspecial property handlerとは別に保つ。
- `0x504400` named structure/current property table: 1485 bytes、callers1/callees23。T005の`global current structure`/property tableの根拠と接続。`if` body内にあるgeneric structural propertyのparse-time harvestはruntime条件と分離。
- `0x4693F0` variant selection helper: 108 bytes、callers22/callees3。保存Ghidra疑似コードでは`0x464290` presenceと`0x4647D0`取得が見えるが、両branchの出力が同じように見える。qualified keyとbase fallbackの実入力を疑似コードだけで断定せず、T005の保存native assemblyを優先。`@`を勝手に空文字化しない。
- `0x464290` property-existence search: 802 bytes、callers62。`current→super`の存在チェックとvariant/base選択の鍵になる。cross-kind parent選択順位はなおVERIFY。
- `0x50A5E0` if/rif parser callback: 616 bytes、callers1/callees11。`ScriptIF::vftable`の44 byte objectを生成し、rif判別boolean、conditionとthen/else要素を持つ構造。root if/rifの一度きり/反復評価は T010 の`0x4930D0`実行段階の挙動であり、parserだけから実行意味論を完成扱いしない。
- `0x50A850` while parser callback: 489 bytes、caller0/callee9 (resolved directのみ)。`ScriptWhile::vftable`24 byte objectを生成してcondition/body pointerを組み立てる。静的xrefsが0件でもregistry callbackからのcomputed dispatchの可能性があり、未使用と判定しない。

## Battle/status & save (T012/T014)

- `0x57DF90` status natural recovery: 484 bytes、callers3/callees3。poi<0かつhprec>=0ならHP正の回復をskip、sil<0かつmprec>=0ならMP回復をskip。HP減少でHP<0のvirtual death-like branch、MPだけlower 0 clamp。7種類gaugeに `unit_status_rec`を加え`unit_status_hp`でupper cap、末尾にstatus評価 helper。T012保存nativeの既知仕様と整合。呼出時刻/action cadenceはcaller実装の追加解析が必要。
- `0x58E870` Unit runtime save reader: 1861 bytes、callers2。Unit欄のscalar/string、status、inventory/skill等の繰返し部分をserializer helperへ順次委譲し、`+0x130`位置のtreeや複数のvectorを再構築するコードが見える。生メモリdumpとしてreadしてはいけない。`+0x16C/+0x170`等の経験値fieldもserialized offsetsに含まれるが、battle-only vs strategic persistent lifeはVERIFY。

## 互換性テストへの引継ぎ

Static evidence verified と REIMPLEMENT MATCH / TARGET OBSERVED を別の合格条件とする。旧EXE実ゲームgolden PASS=0。A/T005,T006,T014とB/T011,T012およびE/T018への正式統合はレーン所有者のみ実行できる。

今回のファイルは `rea_lab/decomp_task` だけへ新規保存。MASTERやA〜E資料を編集せず、過去に安全拒否された操作を別経路で実施しない。

## 最終batch: Unit runtime保存writer & 0x4E7ED0 空間/敵判定

- [EVIDENCE VERIFIED] `runs/20261009T224617297Z/RUN_RESULT.json`： `0x58EFD0` body2050 bytes / direct caller1, callees8； `0x4E7ED0` body814 bytes / callers2, callees4。両関数についてinfo/pseudo/assembly/callers/callees各5点・元EXE SHA一致、前後ハッシュ一致。両方旧EXEゲーム動作はNOT RUN。
- **T014 `0x58EFD0`:** Unit runtime serializerは単なる `memcpy` ではない。数値fieldとNUL終端string（writer `0x470830`）を順番に出力し、28byte strideのvectorを複数走査する。sourceには `arbeit`, `arbeit_user`, `item_skill`, `friend` というserialized label、Unitのstatus gauge(+0xBC,+0xC0,+0xC4,+0xD0等)、経験値関連field(+0x16C,+0x170)へ連なるエントリが見える。`0x58E870` readerとの非対称/可変長群の対応、NUL markerの位置・slot順は専用goldenで検証。
- **T012/T013 `0x4E7ED0`:** 返値0/1の判定helperには `param_1+0x3C` による2つのアルゴリズム分岐がある。一方は `param_2` の座標+0x214/+0x218を中心とする空間グリッドを走査し、候補のenable byte+0x65、除外状態+0x1AE、power/team風field+0x1D0/+0x1D4、distance対候補値(+0x228)などを照合した条件で1を返す。他方はunit+0x220/+0x224の離散セルとunit+0x18688方向/属性index風fieldで単一grid要素を参照し、同系filterの成立で1。意味としては**周囲の他勢力候補の存在・距離判定**が有力で、単純に『projectile collision=hit success』と命名しない。
- **Bへの確認依頼 / VERIFY**: `0x547161..0x547196` callerが0x4E7ED0のALを読んでUnit+0x1E560 latch=2と0->1の経路を分け、MP debit前に戻り得る。これは既存T012の静的観測と整合。ただしfilter fieldの正式論理名、全候補空間範囲、デコンパイラの座標計算（x87/整数丸め）はassembly＋Ghidra callerの照合を要し、結果1を『攻撃成功』へ短絡しない。
- Wave1 16/16、Wave2 10/10、Wave3 10/10=計36関数がSTATIC evidence VERIFIED。未観測gameplay goldenは0。Node既存`QUEUE.json`/`PROGRESS.md` rename EPERMのため表示が古くなり得る。証拠正本は固有run JSONと`logs/progress_sync_*`。
