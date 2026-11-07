# 迫真戦記同梱2 EXEの関係

調査日: 2026-10-05

対象:
- `Vahren.exe` — 2,910,720 bytes / SHA-256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- `新約迫真戦記ーほのぼの神話ー.exe` — 3,108,352 bytes / SHA-256 `10BEC554C717ACBB1F6289EE7E46A83EF75936C2F2D14B37D3DC62FDCA426A5F`

## 結論
両EXEは launcher/wrapper と本体の関係ではない。
実行コードと主要データsectionは同一で、タイトル名EXEは主としてWindows resource sectionだけを差し替え・追加した同一engine buildである。

根拠:
- PE timestamp: 両方 `1476792537`
- EntryPoint RVA: 両方 `0x1B8644`
- `.text`: raw size 2,129,920 / SHA-256先頭16 `7c701dd0629f6645` — 完全一致
- `.rdata`: raw size 329,728 / `2958a42dde8d0129` — 完全一致
- `.data`: raw size 211,968 / `e7560dec4d03ef1a` — 完全一致
- `.reloc`: raw size 148,992 / `62c3c30d879a6c36` — 完全一致
- `.rsrc` のみ異なる:
  - Vahren.exe: 89,088 bytes / `26fdf9547af20b41`
  - タイトル名EXE: 286,720 bytes / `d8df2660b9ff376d`
- `a_default`, `a_system`, `debug_paper`, `encode` 等のengine文字列は両EXEで同じfile offsetに存在。
- `CreateProcess`, `ShellExecute`, `Vahren.exe` 文字列は両方で検出されず、launcher仮説を支持しない。
- 迫真戦記Wiki FAQも「タイトル名EXEを起動。Vahren.exeでも構わない」と説明しており、静的結果と整合する。

再実装上の意味:
- engine挙動解析では両者を別実装として扱う必要はない。
- 迫真戦記CORE同梱 `Vahren.exe` をcode-analysis正本にし、タイトル名EXEの差はresource/UI brandingとして別管理できる。
- Vahren701の旧 `Vahren.exe` とはハッシュ・サイズが異なるため、version/build差分はT004で別途解析する。
