# T013・support候補vectorの2経路と更新前ガード（2026-10-10 23時台 JST）
状態: CONFIRMED-SAVED-ASSEMBLY（関数内の条件・CALL・書込のみ）。0x5158A0/0x57CFA0/0x57CFD0の内部効果、実機動作はVERIFY。
対象関数: 0x57B870（T013、run 20261009T225741694Z、812 byte、34 basic blocks）。
一次証拠: runs/20261009T225741694Z/57B870_procedure_assembly.json（ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c）。
照合: runs/20261009T225741694Z/57B870_procedure_pseudo_code.json（ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc）、callee一覧 ev_5f69dc42c9b24ee6e1c0cf83c2fb4da210af2dda6c4e48b70cbf9ef185ea6203。
source SHA（保存runに記録）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回の再hash・新規Ghidraなし。
## 観察できた局所分岐
- 0x57B9F4 CMP byte [Unit+0x137],0 → 0x57BA01のJZではsecondary候補経路をまるごと飛ばし0x57BA9Cへ。
- 0x57BA07..0x57BA34ではUnit+0xC8<0なら独立CRT乱数と境界比較を行い、一方の選択時だけ0x57BA3Fの0x514F10を経て0x57BA53 CALL 0x57CFA0→0x57BA58 JMP 0x57BA9C。この経路では下記0x5158A0や0x57CFD0を呼ばない。
- 他方の0x57BA5A..0x57BA67でも0x514F10を呼ぶが、後続0x57BA6C MOV ECX,[Unit+0x1E588] / 0x57BA72 MOV EAX,[Unit+0x1E584]→0x57BA7E CMP EAX,ECXで既存vector begin/end相当を比較。
- 不一致なら0x57BA82 MOV EDX,ECX→0x57BA84 CALL 0x5158A0→0x57BA89 MOV [Unit+0x1E588],EAX。一致ならこのcall/writeをskipし0x57BA8Cへ。
- 共通で0x57BA97 CALL 0x57CFD0（既存vector位置・候補範囲・local数値引数）後、0x57BA9Cへ。したがって0x57CFA0と0x57CFD0は同じ経路で無条件に連続実行されない。
## 再実装・残課題
- [CONFIRMED] secondary候補の更新には少なくとも2経路があり、通常経路だけに「begin!=endなら0x5158A0で新endを設定」という前処理がある。単一の常時vectorクリアとして実装してはいけない。
- [VERIFY] 0x5158A0の内部効果（縮小/再配置/終端整列等）は未取得。vector内容、所有権、既存要素破棄を断定しない。confusion判定と0x514F10内部の副作用も未知。
- [TEST DESIGNED/NOT RUN] full refresh、Unit+0x137={0,1}、Unit+0xC8={負,非負}、乱数比較={成否}、vector begin=end/!=endで、3 calleeの呼数・+0x1E588・可視ターゲット・乱数系列を独立trace。
- 本監査は保存済み5方法VERIFIEDの0x57B870に含まれる新しい分岐読み取りであり、新しい関数のVERIFIED昇格ではない。
- 進捗はW1=16/16、W2=10/10、W3=10/10、W4=3/12、合計39/48。新VERIFIED0。原作golden PASS0、ゲーム再実装率未計測。
- 既往安全拒否のREA batch/抽出、原本・A〜E/MASTER/T018/設定/Git/スケジュールには非接触。
