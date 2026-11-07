# 非公開移行の照合記録 / Private migration status
Captured: 2026-11-07T13:04:35Z

**Private migration verified; NOT approved for Public.**
Source: ButaMonky/Hakushin067-Research-Knowledge
Target: Vahren-exe-Research-Lab/Vahren.exe-research

## Git repository content
- Source: 104 original branches and their histories, develop SHA b0be48dd5316f0dba8cc560456e64a6a9f3c7d08
- Target: same 104 branches, all original commits matched; 4,883 tracked develop files matched, git fsck PASS
- 74 original PR Git refs preserved in archive/original-pull/*; no tags, LFS files or releases in original
- Target also has the initial main branch and private migration branches; default is develop
- Both source and target remain PRIVATE, original develop is untouched

## Native GitHub issues and PRs
- Original Issues: 7, now 7 native Issues in target
- Open PRs: 14, all restored with matching branch SHA, 13 drafts + one normal open PR
- Original 60 PRs: 45 merged and 1 closed (unmerged) retained as archived JSON, not recreated as falsely merged/closed native PRs
- Original issue/PR comments: 131 captured in total including 2 post-snapshot additions
- Comments on native-restored Issues/open PRs: 130 restored and text checked
- One historical closed/merged PR comment remains in archived metadata JSON only
- Large PR bodies retained in JSON and continued in native PR comments without truncation
- PR author/number/creation timestamp cannot be reproduced as GitHub-native identity; provenance noted in each imported item
- Original Issue/PR source remains untouched; see native_issue_mapping.json and native_pr_mapping.json
- JSON snapshot index and full PR detailed metadata stored in migration/github-meta/

## Still not identical to source GitHub UI
- 45 merged / 1 closed PRs are archival JSON and Git evidence, not native PR status recreations
- External linked attachments, GitHub project/setting history and exact original actor timestamps are not reconstructed
- Old links and references to original private GitHub URLs remain, and need fixing before publication
- Private repository has historical author emails/local paths and unreviewed rights; **DO NOT CHANGE TO PUBLIC**
- The original research index also documents uncollected historic conversations and research data; source incompleteness is not transfer loss

## Verification
- See native_migration_verify.json: mismatches=0 for checked issues, open PRs, comments and branches
- All this metadata is intentionally on the private archive branch associated with draft PR #1; develop was not modified
