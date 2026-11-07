# T004 静的構造地図

状態: DONE（構造地図完成。個別仕様の深掘りは T005 以降へ分離）
更新: 2026-10-05 継続監査9

## PE基礎比較
- Vahren701: SHA-256 7813d61efd3be03cb838c54098b5dd7b162e0ec8e4375bc9e6b07c8a0236ce4f
- Vahren701: 2,957,824 bytes / x86 / ImageBase 0x400000 / Entry RVA 0x1c627b
- Vahren701 PE timestamp: 2018-05-01 06:45:42 UTC
- 迫真戦記同梱Vahren: SHA-256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187
- 迫真戦記同梱Vahren: 2,910,720 bytes / x86 / ImageBase 0x400000 / Entry RVA 0x1b8644
- 迫真戦記同梱Vahren PE timestamp: 2016-10-18 12:08:57 UTC
- 両者は .text/.rdata/.data/.rsrc/.reloc の全section hashが異なる別build。

## 共通外部サブシステム
- d3d9.dll / Direct3DCreate9
- d3dx9_35.dll / 画像読込・image info・matrix/vector系
- DINPUT8.dll / DirectInput8Create
- DSOUND.dll / ordinal #11
- WINMM.dll / timeGetTime・mmio系
- USER32.dll / window・message loop・cursor
- GDI32.dll + MSIMG32.dll / text・bitmap・AlphaBlend・TransparentBlt
- ole32.dll / COM
- KERNEL32.dll / file・thread・process・文字コード等

[CONFIRMED] import table上はWinSock/WinINet等のnetwork DLLを持たない。
[VERIFY] 動的ロードの可能性は残るため、network機能なしの最終確定は別途必要。

## Vahren701 data/script loader の静的アンカー
.rdataの連続領域に以下を確認:
- 0x6318f8 a_default
- 0x631924 /script
- 0x63192c /script2
- 0x6319dc script2
- 0x6319e4 script2/
- 0x6319f0 *.dat
- 0x631a18 script/
- 0x631a34 debug_paper.txt
- 0x631a58 a_system/debug_paper.txt
- 0x631a80 encode
- 0x631a88 testmap
- 0x631a90 musicoff
- 0x631b24 a_system/load.png

.text内の直接参照:
- /script -> 0x51932a
- a_default -> 0x519656
- script/ -> 0x519ed8
- *.dat -> 0x51a12a
- debug_paper.txt -> 0x51afb8
- encode -> 0x51b29c
- a_system/load.png -> 0x51c2cc
- .map代表文字列 -> 0x432f8f

0x519300付近では /script と /script2 を組み立てた後、IAT経由で FindFirstFileA / FindClose / FindNextFileA を呼ぶ。
IAT対応: 0x6081e0=FindFirstFileA, 0x6081b4=FindClose, 0x6081b8=FindNextFileA。
0x519ed8以降では script/ と script2/ の探索・列挙処理を確認。

[CONFIRMED] Vahren701のstartup/data-loading主要クラスタは概ね0x5193xx〜0x51c2xxに集中し、script/script2探索、*.dat列挙、debug_paper、encode設定、load画像初期化が近接配置される。
[VERIFY] 個々の関数境界、正確な呼出順、parser入口は未確定。

## 迫真戦記同梱 build の追加アンカー
- [CONFIRMED] PDB path: `C:\Users\...\Visual Studio 2010\Projects\Vahren\Release\Vahren.pdb`。Vahren701 は Visual Studio 2017 系 PDB path。
- [CONFIRMED] RTTI から `ScriptBattle / ScriptBlock / ScriptData / ScriptElement / ScriptFunc / ScriptIF / ScriptSet / ScriptWhile` を確認。native script object model が存在する。
- [CONFIRMED] script high-level loader: /script=0x556A18, /script2=0x556A45, a_default=0x556C4C, script/=0x557332, script2/=0x5573BC, *.dat=0x5574B7, debug_paper=0x557A90/0x558070, encode=0x558349。
- [CONFIRMED] 別の script/parser cluster: *.dat=0x50C1DC, unicode.txt=0x50C71E, script/=0x50CA71/0x50CE66, script2/=0x50CCB7。
- [CONFIRMED] global.sav 参照: 0x428113 / 0x4287C7 / 0x428D14。近傍に CreateFileA / ReadFile / WriteFile が集中し、global 永続化経路の静的アンカーとなる。
- [CONFIRMED] map 参照: 0x4F0DF7 と 0x50020F。双方の直後に CreateFileA/ReadFile 呼出があり、map 読込系が少なくとも2経路ある。

- [CONFIRMED] audio: `sound/` xref=0x4C09E6。OggDecoder vtable=0x006395CC（methods 0x501DF0,0x501F10,0x502000,0x502020,0x501EB0）、PCMDecoder vtable=0x006395E4。WINMM mmioOpen/mmioRead code=0x4C0E8D..0x4C109F、DirectSound 初期化=0x4BFA34。
- [CONFIRMED] input: DirectInput8Create xref=0x4BCE3B。GameMouse vtable=0x00638E58（0x4BCF20,0x4BCF70,0x4BCDC0）、NewGameMouse vtable=0x006394A0。
- [CONFIRMED] rendering/window: Direct3DCreate9 xref=0x555563。GameWindow vtable=0x00638E78（0x4C5A80）。
- [CONFIRMED] timing anchors: timeGetTime xrefs=0x4BA0D5 / 0x4C2611 / 0x555F97。意味付けは T010/T015 で行う。
- [CONFIRMED] save/load UI: SaveWnd vtable=0x00639D4C（21 methods）、LoadWnd=0x00639064（21 methods）、ScenarioSelectWnd=0x0063A01C（21 methods）。
- [EVIDENCE] `T004_RTTI_MAP.md/json`, `T004_ANCHOR_XREFS.txt`, `T004_PE_SURVEY.md/json`。
- [REIMPLEMENT] T004 は subsystem の境界・入口を絞るための地図として完了。parser grammar/API は T005/T006、map は T007、save は T014、UI/audio/input は T015 に引き継ぐ。
