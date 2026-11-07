> 後続訂正：この監査票はFの追加範囲訂正前の保存状態を固定したもの。現在のFは旧保存版3182行を追加除外し、保持原行は4,123。旧SHA・4,124保持という値は当時の入力を示す。[現在の範囲訂正](../findings/REVISION_20261105.json)とSCREENINGを併読する。全体手動レビュー未完了は継続。

# Claude Code / dev_lab current Markdown identity audit

Current metadata scan completedUTC 2026-11-05T12:26:34.990921+00:00. Fixed comparison root2428; selected roots only dev_lab/docs, dev_lab/reports, dev_lab/_work and dev_lab/story. Independent dev_lab documents are included regardless of Claude/PEER_SCRIPT01 naming. The task checks concrete document omissions, not all historical semantics.

## Result

158 scoped Markdown files /3403415 bytes:131 current sources exactly equal their accepted destination bytes;25 current source versions have existing reviewed variants;1 current FINDINGS source has a known screened partial derivative;1 archive has an exact existing whole-file deferral. Zero changed-version same-path sources, zero independent new primary candidates, zero new accepted bodies.157 source identities match the ledger by exact relative path plus current SHA256, and their156 unique canonical destinations passed local SHA256 verification.

The screened partial is dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md,478107B, current SHA2569e5ceec9635f2c0306c9417bef1648722f8c354c382a3049986507fc7bbb5c34. Its existing derivative6c61b104076363710e09535c6db62daedbe0f0ee159a6ce3240aceb4f417d2d8 explicitly retains omitted paragraphs/appendix and full manual review pending. Source identity does not turn this into complete text recovery or release held content. No FINDINGS body or screening payload was reopened.

The unmatched-to-accepted archive is dev_lab/docs/archive/CHATGPT_CURRENT_HANDOFF_ARCHIVE_20261029.md,1041019B,SHA256165008ae027cfd2373a86916541a151adbf0e2bdd1ec35a16ecbdf8d356a9ba2. Published handoff_scope1/DEFERRED.tsv has the exact same source path/SHA/size and a whole-composite4C28D0-interior dependency deferral. It was not reopened through header, alternate alias or wrapper.

Root counts:docs54, reports0, _work83, story21. Reports root was examined but has no in-scope Markdown. Matching identities include earlier outside_dev1/outside_design1/outside_kb1, dev_reports/ac_tests6/remaining_md1, legacy standalone accepted documents and handoff_scope1. Existing destination groups are metadata, not new discoveries:

{"ac_tests6": 15, "ad_small": 1, "dev_reports": 16, "existing_standalone_research_body": 9, "findings": 1, "handoff_scope1": 1, "knowledge_history1": 1, "outside_design1": 42, "outside_dev1": 60, "outside_kb1": 1, "plugin_reports1": 1, "remaining_md1": 9}

## Scope and method

Only literal descendant .md paths under the4 approved roots were opened for streaming SHA256, with stat size/mtime checked before and after; all158 were stable. No decoded source body or header was displayed/reviewed in this pass because no independent new candidate remained. Hashing bytes is metadata measurement, not semantic/full-body review. Existing source-vs-derivative SHA and limits remain separate in STATUS.

Dependency/generated/source prefixes and reparse directories were not followed; EXCLUDED_DIRS records actual pruned paths. The toolchains dependency prefix was explicitly removed from the result after one preliminary README metadata row, without body review. Known dirs include .git/node_modules/.venv/venv/__pycache__/site-packages/vendor/dist/build/out/target/coverage/.next/generated/_generated/src/recovered_source. Ancestors within the approved originalROOT were checked for reparse attributes. Non-Markdown names were not content-opened.

No originals were modified. No linked/native/game/DB/archive/script/recovered_source payload was acquired or executed. Existing accepted/held status is not a new native/type/ABI/Golden/READY finding. No shared/core/Git/network/chat/automation changes. Only this folder was written. REPORT_LEDGER remains header-only pending parent selection; none was needed here.

## Practical conclusion and limits

For the currently visible authored Markdown in these4 roots, there is no newly discovered independent Claude/dev_lab report or current revision absent from existing identity records. This is narrower than saying every Claude Code result is fully integrated: the known FINDINGS partial/held archive remain, and excluded dependencies/generated outputs, other formats, other roots and unselected chat/history/Library material were not audited or declared complete.

Input metadata pins are unchanged; current canonical destination hashes verified; STATUS partitions158 unique paths exactly. Output manifest covers publication files except itself. No temporary builder/input file remains.
