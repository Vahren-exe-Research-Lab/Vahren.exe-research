# 共通引継ぎ・契約案の独立review
研究ID P0_TAKEOVER_20261024_01。EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、V9 DB SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
対象 HANDOFF.md / BRIDGE_CONTRACT_DRAFT.md。root文書は変更せず、review専有snapshotへ保存。監査範囲は実測・局所ABI・ID・scopeと既存成果との整合。native recovery run20261024T010904_4487298eの成功はこのreviewの前提に含めない。
判定: G3限定NOOP PASS、G4 NO-GO、全G2未達という結論に矛盾なし。入口ABI、Unit/Side/Troop/MAP offsets、EXE/DB hash、nominalアドレスとASLR換算、名簿alias数は担当証拠と一致。以下は表現/契約境界の修正推奨であり新たな実機PASSではない。

## 修正推奨
1. HANDOFF line23「delaying interception until the next frame」はframe境界を測ったと読める。実測は同Task pass内のUnit57AA00→次passのBattleTick492D80なので「until the next battle tick / Task pass」へ限定する。根拠初回固定21eventの行8/16/17、NOOP固定27eventの行9/21/22。
2. CONTRACT line17のAND条件と「Unknown route ... continues original execution」は設計上正しいが、現probeがこの拒否動作を実装済みに読める。実行済NOOPのeligibleはUnit0/owner/pass/EBX/E/深度/VM433620を照合する一方、routeの明示assertやrequest世代との対応確認は未実装。今回route0はreceipt実測である。『proposed production acceptance; current probe does not enforce explicit request-generation/route checks』を補記する。
3. HANDOFFが参照するexit/H_I_J_EXIT_RESULT_CONTRACT.md line39はACK=commitを設計語として用い、現NOOP transportはnoop_ack=echo_only。統合CONTRACT line43のIPC ACK!=COMMITTEDが正しい。旧文書のACKは将来の専用commit receiptでありtransport noop_ackを指さないことを明記すると用語衝突を解消できる。IPCの1ACKを結果反映一回と解釈しない。

## 軽微な追記候補
- HANDOFF read-first item4へreview/N_NOOP_NATIVE_RECEIPT.mdとN_NOOP_NATIVE_VERIFICATION.jsonを追加する。独立30条件照合は既に完了済み、summaryから推定したものではない。
- HANDOFF source hashのNOOP「should hash byte-exactly」は検証済みsource69489CA1...71118E1とreceiptが一致した事実に更新可能。
- CONTRACT line21のcaller stackは『differs from native4C2719; instrumentation contamination suspected, cause unproven』が最も正確。caller不一致自体は確定、trampolineという原因は未確定。原作EFLAGS/SEH未証明という結論は適切。

## 確認済み事項と再開地点
request4922A0 RET8、activation492890 ESI/stack/RET4、BattleWnd40D0A0 EAX/ECX/DL/stack/RET4、C1のlive traversal stack、finish493630の呼出元依存・SEH、433E5DのVM epilogue候補を既存native evidenceと照合。VM APIや提案callbackを既実装DLL exportへ昇格していない点は適切。
G3は206Unit診断packetの1往復と98ms wait/原作続行だけ。世代付きID・全MAP/VM/RNG・他writer停止・結果apply・save/load Goldenは未達として維持されている。1400tick/worldmode1を新結果commitと呼んでいない。
証拠: entry/ENTRY_FINDINGS.md、entry/native_entry_evidence.json、scheduler/DE_SCHEDULER_FINDINGS.md、exit/H_I_J_EXIT_RESULT_CONTRACT.md、review/N_NATIVE_RECEIPT_VERIFICATION.json、review/N_NOOP_NATIVE_VERIFICATION.json、実行source固定コピー。
再開: rootが文書を修正後、上記3点の文言と独立NOOP監査リンクを確認。recovery runは新しい固定receiptとして別途監査し、この契約reviewから成功を推定しない。
