# T018/T020｜跨プロセス固定VAとpreflightをGolden G2に誤結合しない受入条件
研究ID: E-AUDIT-20261023-1445-T020-MULTIPROCESS-PREFLIGHT-IDENTITY-01
状態: SOURCE-STATIC / E所有 / VERIFY / DESIGNED_NOT_RUN / NOT READY。新規原作Gameplay・DLL実行なし。
照合対象: 2026-10-21 LIVE_ORIGINAL_READONLY の2セッション（PID28432とPID32468）、Stage17保存研究、E既存同一PID別戦闘窓研究。
EXE識別SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（source資料記載、今回EXE原本再hash無し）。
資料現物SHA再計算: RAW-28432=7C0A7BD05FFAB908A90BBBEC0863FCE040A99A33A17E75520C9CC19094565332。
資料現物SHA再計算: RAW-32468=9DE328DA5FBFF98151ED2A26133FC123EABE6972DF1C6588F0DC4AB26098A034。
資料現物SHA再計算: BATTLE_STAGE17_ACTIVATION_BOUNDARY_20261022.json=18165D01E2A87F3188EA44AB5C890AFDBF6E822B14D07839E6416C45313F8F7A。
3 SHAともStage17のarchive/source記載値に一致（Local read-only Get-FileHash）。
## 今回の独立クロスソース差分
RAW-01二件は同じgame_manager_base=0x0072E2F0、game_event_base=0x0072E7F4、module_load_base=0x00270000を記録する。
しかしREADY.jsonのPIDは28432/32468、task_active_start_ptrは0x16DC7028/0x1E60E020と異なり、別実プロセスの採取である。
同一固定VAや共通EXE SHAだけを根拠に二記録の動的ポインタ・Unit/Troop・SAVEを同一戦闘として結合することは無効。
両READYのpreflight initialはmode=1、active=0、attack_count=0、battlefield_ptr=0。これは戦闘前の採取器準備状態であり、戦闘中G2のMAP不在や三side空を示す資料ではない。
RAW-01はUTC 16:31:11.100428 / 16:46:32.953122、recorder_provenance.atomic=false。Stage17はfirst_native_pass_observed=falseと確認。
一方、G0限定旧Watch PID23272はUTC 14:31:37 / 15:14:40に別2窓。上記PID28432/32468のRAWをこのG0のG1/G2として採録できない。
## T020追加負例fixture（DESIGNED_NOT_RUN）
MP-01: EXE SHAと固定game_manager_base一致のみでPID別RAWを同一runに結合 => REJECT_CROSS_PROCESS_JOIN。
MP-02: 共通game_event_baseを根拠にUnit/TroopまたはTask slotの同一オブジェクト性を主張 => REJECT_POINTER_IDENTITY。
MP-03: READY preflight(mode1/active0/attack0/map0)を戦闘G2観測として提出 => VERIFY_PREFLIGHT_ONLY。
MP-04: 非atomic RAWを戦闘開始直後の初回tick/初期名簿として提出 => VERIFY_UNPROVEN_TIMING。
MP-05: PID23272の合法G0限定証拠とPID28432/32468のRAWを同戦闘G1/G2へ接合 => REJECT_CROSS_PROCESS_JOIN。
## Golden・統合境界
正受入には同一プロセス世代＋戦闘時間窓＋操作/直前SAVEのbytes SHA＋MAP・三陣営・ordered deployed Unit/Troopとpost-callbackの安定性証拠が必要。static Stage17 active=1のみでは不可。
E新DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0、新規READY正式統合=0。T019新確定矛盾0。
MASTER最終正式checkpoint196/READY596(A115/B229/C136/D116)、34Task DONE9/IN_PROGRESS21/VERIFY4は旧値。OFFLINE-UNSYNCED暫定26は未照合。原本/他owner/Git/Work/設定/automation無変更。