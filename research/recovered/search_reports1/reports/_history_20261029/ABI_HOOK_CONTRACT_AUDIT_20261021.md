# 迫真戦記 ver0.67｜DLLフック関数ABIの独立監査（2026-10-21）
- 作業ID: `REDEV-ABI-THREE-HOOK-20261021`、状態: `STATIC VERIFIED / GAME NOT RUN / NO PATCH`。
- 調査対象の原EXE `hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 原研究SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、変更なし。
- 証拠はPC上の元EXEバイト列・Capstone逆アセンブル・Ghidra10,268擬似C・CALL索引。ゲーム起動なし、EXE/Ghidraプロジェクト/研究正本/DLL等の製品コード変更なし。

## 関数の実際の引数・復帰
| 関数 | 擬似C | 実機械語の入出力 | 関数単位フック上の注意 |
| --- | --- | --- | --- |
| `0x00595170` | `void FUN_00595170(int)` | 1引数はスタック、`ret 4`。呼出後EAXを利用。 | `void`で置換しEAXを破壊すると原作結果を変える |
| `0x00595320` | `void FUN_00595320(int)` | 1引数はスタック、`ret 4`。呼出後EAXを利用。 | 32bit結果（EAX）の引継ぎが必要 |
| `0x00551E50` | `void FUN_00551e50(int,int,int)` | EAXに隠れた処理コンテキスト、スタックに3引数、`ret 12`。 | 標準3引数stdcall関数として呼ぶとEAXが渡らず危険。Ghidraのvoid戻り値は未否定 |
| `0x004D4A50` | 雇用画面Renderer | `ret 4` | V2の__thiscall 1スタック引数と一致 |
| `0x00453C20` | 表示更新 | 各出口が`ret 12` | V2の__thiscall 3スタック引数と一致 |

## 元EXEの具体的なCALL証拠
- `0x004D2D87`: `push eax; call 0x00595170` → `0x004D2D93 mov esi,eax`。計算結果を呼び出し元が保持。
- `0x004D2D95`: `push ecx; call 0x00595320` → `0x004D2DA6 mov ebx,eax`。
- `0x00551167`: `push ecx; push edi; push ebx; mov eax,ebp; call 0x00551e50`。関数入口`0x00551E53 mov esi,eax`。戻り先ではEAXを使わない。
- 関数への直接CALL索引件数：`0x595170` 3件、`0x595320` 2件、`0x551E50` 4件。直接CALLだけの件数であり間接CALLの不在証明ではない。

## 現在の雇用画面V2への影響
- V2配布ZIPの`src/hakushin_recruit_sort_v2.c`が直接フックするのは`0x004D4A50`（6箇所のCALL差し替え）。3つの問題関数をフックしていない。
- V2ではRendererを`void (__thiscall*)(void*,U8)`、トランポリン相当のラッパを`void __fastcall hooked_renderer(void*,void*,U8)`で呼ぶ。戻り`ret 4`と引数数は一致する。
- 再表示`0x00453C20`も`void (__thiscall*)(void*,U8,I32,U32)`、原作は各出口で`ret 12`。
- よって今回の3関数のABI問題がV2に直撃するという証拠はない。ただし、V2には以前確認した6/8呼び出し箇所対応問題（reloadMenuの2箇所欠落）や実機未検証が残る。全体の安全保証ではない。

## 今後のフック実装で必須のゲート
- ①関数先頭で読む入力レジスタ（EAX/ECX/EDXなど）の読み取り前書込み・各callerのレジスタ設定を照合。
- ②全RET命令と即値（`ret 4`/`ret 12`等）・全呼び出し側のpush/add espの釣り合いを照合。
- ③復帰直後にEAX/EDX、x87 ST0、フラグなどを呼び出し元が利用するか確認。
- ④Preservedレジスタと必要なスタック・FPU/SSE状態・例外経路を保持する。原型不明ならフック実行を禁止してASM境界だけに限定。
- ⑤EAXに隠れた引数を持つ`0x551E50`は標準C関数ポインタでの安全な呼び出しを推奨しない。x86用の明示的なレジスタ引渡しブリッジと実機テストが必要。
- ⑥`void`擬似Cのまま直接関数ポインタ化しない。実機Golden比較・例外検出を別途実施。
- 修復済み検索DBの完全性と呼出規約の完全性は別。今回の確認は5関数限定であり残りの全関数ABIは未点検。
- 保存証拠: `verify_abi_three_hooks_20261021.py`, `ABI_THREE_FUNCTIONS_VERIFIED_20261021.json`。

