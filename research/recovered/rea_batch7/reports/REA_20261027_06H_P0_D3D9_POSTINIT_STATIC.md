# 迫真戦記 ver0.67 REA｜P0 DirectX9初期化後段の戻り値無検査CALLと補助初期化
研究ID: REA-LOCAL-20261027-06H-P0-D3D9-POSTGATE-UNCHECKED-VTABLE-STATIC-01
日時: 2026-10-27 06時台 JST。状態: PC-SAVED / STATIC / VERIFY / NOT READY。原作Golden: NOT RUN。
対象EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## NEW STATIC: 3 HRESULTゲート後に18件の間接CALLを戻り値分岐なしで実行
関数 0x00559690 は前回05Hに0x005596B0(vptr+0x20)、0x00559774(+0x40)、0x005597CA(+0x68)の3失敗ゲートと0/1のAL returnを確認済み。今回はそこから後段 0x005597F7～0x00559975 の原作機械語を独立で解析した。
- 間接CALL18件: 0x00559804, 0x00559811, 0x0055982E, 0x00559848, 0x0055985C, 0x00559873, 0x00559887, 0x0055989B, 0x005598AF, 0x005598C3, 0x005598D9, 0x005598EF, 0x00559905, 0x0055991B, 0x00559931, 0x00559947, 0x0055995D, 0x00559973。旧Ghidra検索DBのindirect_callsと18件一致。
- 直接CALL: 0x00559830 → 0x00559990。旧DBと統合V9の双方で同じdirect CALLを確認。
- 上記後段には条件付きJMP・TEST・CMPが0件。従って後段の仮想CALLが正常復帰する範囲では、その戻り値で以後の初期化を中止する判定は存在しない。
- 終点は0x0055997B MOV AL,1 → 0x0055997D __security_check_cookie → 0x00559985 RET。05Hの3つの失敗ゲートのみでAL=0経路を明示確認。後段のCALL成功までAL=1が保証するわけではない。
- +0xE4(vtable) 6回、+0x10C 6回、+0x114 2回、+0x164 1回、+0x190 1回、別オブジェクト+0x1C/+0x24各1回の計18回。API名対応は一部未確定なのでvtable offsetを一次証拠とする。

## NEW STATIC: 0x00559990の補助初期化
関数0x00559990の原作線形逆アセンブル範囲は0x00559990～0x00559D22(RET1箇所)。
仮想CALL4件: 0x005599BC, 0x005599D3 (両者+0xB4), 0x00559A28 (+0xC0), 0x00559B05 (+0xB4)。旧DBのindirect_callsと一致。
そのほか0x00559A73/0x00559B43/0x00559BA0/0x00559BCF/0x00559BFE/0x00559C1Dの6件の動的API/関数ポインタCALLを保存済み擬似Cと原作機械語で照合。PEインポート表の独立読出しでIAT 0x006092CC=D3DXPlaneFromPoints、0x006092D0=D3DXMatrixPerspectiveFovLH、0x006092F4=D3DXMatrixLookAtLH、0x006092DC=D3DXVec3Unproject を確認した。仮想CALL先の実体・戻り値型はまだ未確定。
0x00559990は戻り値として初期化成否を親へ渡さず、途中に浮動小数点を使う反復処理がある。収束条件・NaN/ゼロ増分・API失敗による挙動はVERIFY。

## 認証・差分・互換試験
今回の監査は43/43 PASS。原作EXE SHA、旧DB/V9 SHA、両DB quick_check、親・子の命令境界とCALL site、保存済み05Hの53 PASS、2026-10-11同期64/64を確認。43は静的検査条件数であり、解析完了関数数ではない。
5種類: info=INDEX_ONLY, pseudo=INDEX_ONLY, assembly=TARGETED_PE_NATIVE, callers=INDEX_ONLY, callees=INDEX_ONLY。新規正式VERIFIED=0、5種新規完全取得0。正式TODO/VERIFY/BLOCKEDの書込差分は各0。旧64件を二重加算しない。
Golden 実ゲームPASS=0、strict MATCH/完全複製率=未測定。合成監査は原作実行試験ではない。
VERIFY: 仮想CALLの戻り値型と各D3D9メソッドの失敗条件。戻り値未検査というSTATICと実ゲームの不具合発生は別。成功後のAL=1をすべての後段API成功とみなさない。
次回は0x00559990の浮動小数点反復条件(0x00559C1F～0x00559CF0)、入力定数のゼロ・NaN・非有限値の到達性を限定追跡。または0x00556790と第二BGMベースパスDAT_0068B38Cの生成元を調査。
資料は本ownerフォルダ内の06Hプローブ、06H監査、06H証拠JSONに独立保存。保存後に再監査・SHA256・独立readbackを実施する。REA/Ghidra/ゲーム/Workは起動しない。
禁止VA、拒否済みWave6、REA exportを試行しない。原本・MASTER・QUEUE・PROGRESS・旧RUN・他レーン・Git・公開先・スケジュールは変更しない。