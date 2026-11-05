# 教育の生徒一覧を「補正合計」にする（Claude 2026-10-31、ユーザー判断）

## 変更（診断コピーの DAT、CP932・CRLF 維持）
- 43_内政_教育/ev01〜ev12 の choice_XX_student: 候補ごとの値を bonus_XX_student だけから、本番の判定と同じ poli_lecture_XX_main1（基本50＋講師＋生徒＋勢力・領地）＋ main2（講師と生徒の能力差。野球・公開オナニー・剣道は 2 回）に変更。一時的に魔法防御へ入れて表示し、選択後 resetMagdef で 1 に戻す（従来と同じ仕組み）。
- 呼ぶ一覧を choiceUnitFromList_v4_education_total に変更。claude_lecture_v4.dat に追加したこのイベントは、列名「補正合計」、初期並びは補正合計の降順。
- 講師一覧は従来どおり「補正」（講師側の補正）。
## 根拠（静的確認）
- 乱数なし（茶会のリラン要求姉貴・一転攻勢を除く）。main1/main2 と bonus_* は junban・unit_num・@chara_list・@eranda_chara・yappa_* を使わない（12 科目で確認）。
- 茶道（ev06）の main1 は lecture_success を 0 にしないため、呼ぶ前に 0 にしている。
## 注意
- 茶会（ev999）は茶道の生徒選択を共用するため、客ごとの値（その客の判定値）が出る。茶会の判定は客 3 人の合計＋乱数で、閾値も 150/200/300 と異なる。
- 実機未確認。
## 戻し方
before/ の 13 ファイルを a_default/script の同じ場所へ戻す。
## 今後
配布用には変換ツール tools/work_dat_ui_profiles.py に組み込む必要がある（未実施）。
