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
- Original 60 PRs: 45 merged and 1 closed (unmerged) are now also represented as GitHub-native PR pages using isolated historical archive base branches (all statuses and original head SHAs verified).
- Original issue/PR comments: 131 captured in total including 2 post-snapshot additions
- Comments on native-restored Issues/open PRs: 130 restored and text checked
- Historical closed PR comment was also reproduced in the destination PR page. Original comments remain archived in JSON.
- Large PR bodies retained in JSON and continued in native PR comments without truncation
- PR author/number/creation timestamp cannot be reproduced as GitHub-native identity; provenance noted in each imported item
- Original Issue/PR source remains untouched; see native_issue_mapping.json and native_pr_mapping.json
- JSON snapshot index and full PR detailed metadata stored in migration/github-meta/

## Still not identical to source GitHub UI
- Historical 45 Merged and one Closed-unmerged PRs **are now recreated as PR pages**, verified. Merge commits made specifically for reconstruction are synthetic commits on `archive/recreated-pr-base/*` branches; original FF commits, `develop` and source PRs are unchanged.
- External linked attachments, GitHub project/setting history and exact original actor timestamps are not reconstructed
- Old links and references to original private GitHub URLs remain, and need fixing before publication
- Private repository has historical author emails/local paths and unreviewed rights; **DO NOT CHANGE TO PUBLIC**
- The original research index also documents uncollected historic conversations and research data; source incompleteness is not transfer loss

## Verification
- See native_migration_verify.json: mismatches=0 for checked issues, open PRs, comments and branches
- All this metadata is intentionally on the private archive branch associated with draft PR #1; develop was not modified


## Historical closed/merged PR reconstruction — verified 2026-11-07T13:31:43.747793+00:00

- Historical 45 Merged PRs and one Closed-unmerged PR now exist as true GitHub PR pages; all checked against original title, body, head SHA, archive-only base ref, original URL and states. Mismatches: **0**.
- Original source had 45 merged, 1 closed-unmerged, 14 open. Destination now has 45 merged, 1 closed-unmerged, and 15 open (14 original open plus this archive Draft PR #1).
- Every recreated PR targets a dedicated `archive/recreated-pr-base/NNNN` branch initialized from its original pre-merge base SHA. 45 archival merges made new merge commits **only in those archive branches**. Original `develop` remains at `b0be48dd5316f0dba8cc560456e64a6a9f3c7d08`.
- Recreated PRs have **new GitHub PR numbers, authors, merge timestamps and synthetic merge commits**. Their bodies explicitly link the original PR, original author, date, head and base SHAs; these new PRs must not be represented as the original GitHub operations.
- Original PR metadata, original comments, reviewed file lists and Git commits remain archived in JSON.
- Reconstructed mapping and independent verification: `historical_pr_native_mapping.json`, `historical_pr_verification.json`.
- **Private only.** Organization/public-anonymity checks and rights review remain incomplete.
