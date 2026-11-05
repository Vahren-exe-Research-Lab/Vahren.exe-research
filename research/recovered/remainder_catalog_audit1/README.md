# 旧目録の未照合・部分・版差の監査

旧目録1937行のうち未照合441行を、基準 `525b37e43f26c7a95c2b3818f83ed9507a33d452` のroot台帳2384行と既存metadataに対応付けた。[全441行の状態](STATUS.tsv)は本文を受理する台帳ではない。新本文保存・core採録・実行0。未測定/保留をresolved/body acceptedに数えない。

| 対応根拠 | 行数 | 現状 |
|---|---:|---|
| 既存票のsource/current SHAが目録SHAと一致 | 373 | 既存snapshotのmetadata保留。現在の原本bytes未測定 |
| historical catalog SHAだけ一致 | 3 | E09/10/11 paired-study選択除外。現行本文scope証明ではない |
| パスだけ一致 | 29 | 3件は別SHA、26件はSHAなし。目録版への理由適用は未解決 |
| 固定31literalの今回identity/header確認 | 31 | buffer/record/value未展開・本文未保存 |
| 選択起点の関連scope lead | 5 | source-byte未取得、関連scope照合が必要 |

405=373+3+29であり、405全件がexact現行原本に対する確定holdではない。全441のcurrentroot exact/path受理衝突は0。明示LEGACY_SCOPE_CORRECTIONとCURRENT_NATIVE_STATUSを旧票より優先し、全対応先とSHA欄名を各行に残した。古い別版のreasonを目録本文の確定holdへコピーしない。既存metadata自身の検証範囲を超える拒否・保留解除は主張しない。

31件の先頭最大800 Unicode文字はschema keyと許可されたid/status/origin等のheader labelだけを確認。19件はmemory_regions/base/hexのdetached buffer集合、2件はnode byte診断、3件はdecoded pointer集合でmetadataのみ。残7件はcompact scalar/count summary2件とfailure/traceback receipt5件で、raw memory全体とfilenameだけで断定せず全文未review/後続scope判断要とした。originが実機かsyntheticかの全体帰属も今回確定しない。31全件のsourceSHA/sizeは既存pinと一致・literal containment/no-reparse、identity読取前後size/mtimeと最終hash安定を確認。全JSON parse・buffer値・pointer配列・全records・linked traceback/脚本を展開せず、短いschema-only確認がEOFへ届く1件も意味全文reviewや本文受理にはしない。

5JSONは親指定の既存private選定metadataから5行だけ可搬化した。元metadata hash/行を[選択除外票](SELECTION_EXCLUSIONS.tsv)に固定。E10/11はsame-study研究依存、他3件はHOLD関連metadata/Library関連/dual-result scopeleadまで。exact catalog pinであっても原本を再取得せず、内容の完全scope確認/安全拒否成立とは扱わない。

[部分1・版差9の別表](PARTIAL_AND_REVISION_GAPS.tsv)もmetadataのみ。T009 schema-onlyは原文全体未回収、9件は目録版と保存版が異なり歴史的版の同一性/回収が未証明。保存Fにはpartial stateもあり、別版の存在を全文同一へ昇格しない。既存受理/別版は保存済みの限定範囲で有効だが、catalog版の残差とは分ける。

APPROVED_INPUTSは未照合441+部分/版差10の451行のmetadata監査範囲で、原本読取許可は固定31literalのidentity/headerだけ。他のoriginal/保留本文を再取得していない。INPUT_RECEIPTSは読んだmetadataのhash/size、OUTPUT_MANIFESTは自身以外の出力hash/size。原本・共有root/core/code・Git・network変更なし、native/game/log/code/DB/asset/archive/リンク先取得実行なし。この監査で古い441ラベルの理由は具体化したが、保留/未review本文の取得や研究全体完了を意味しない。
