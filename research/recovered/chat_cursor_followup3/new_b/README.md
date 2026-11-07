# NewB固定cursorの1回確認

frozen CAPTURE_SCOPESのthread6aea0916-3ee4-83ec-b05f-2b3afe2d3f5d / cursor47a78203-d89b-40ac-9c91-368e7d10dcd2だけを、turnLimit1/includeOutputs=false/maxOutputCharsPerItem1200で一度要求した。

サービスはUnknown cursor、isError=trueを返した。turn/message/item IDs/page/hasMore/次cursorは返っていない。本文0・新受理0・新候補は判定不能。安全拒否や内容不存在と扱わず、失効/不認識cursorによる未取得のまま残す。既存frozen hasMore=trueの歴史値を今回のhasMoreに流用しない。

事前にrootの既受理URIとchat群DEFERRED metadataを照合した。このthreadへの既受理URIはあるが、今回返却itemがないため同一性/重複/研究ID/primary意味は新たに判定できない。chat*/DEFERREDのthread/NewB文字列一致なしも、保留の全不存在を証明しない。

別cursor・最新turnへの切替や再試行・wrapper迂回はしていない。原本/native/Library/linked/codeを取得/実行せず、共有/core/Git変更なし。TOOL_RECEIPTは要求と返却エラーの文字列表現を保存したもので、研究本文ではない。取得時点は2026-11-05の今回1call。元listing時点はAPPROVED_SCOPEに残る。

STATUSに現在root行数・metadata hashと未確認事項、OUTPUT_MANIFESTに自身を除く4票のhashを記録した。
