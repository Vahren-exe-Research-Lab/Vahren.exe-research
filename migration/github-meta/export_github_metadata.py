#!/usr/bin/env python3
"""Archive GitHub issue/PR metadata to a PRIVATE repository branch. Credentials never written."""
from __future__ import annotations
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys

REPO = "ButaMonky/Hakushin067-Research-Knowledge"
HERE = Path(__file__).resolve().parent
FILES = {
    "repository.json": "",
    "issues_all.json": "issues?state=all&per_page=100",
    "issue_comments.json": "issues/comments?per_page=100",
    "issue_events.json": "issues/events?per_page=100",
    "pull_requests.json": "pulls?state=all&per_page=100",
    "pull_review_comments.json": "pulls/comments?per_page=100",
    "labels.json": "labels?per_page=100",
    "milestones.json": "milestones?state=all&per_page=100",
    "releases.json": "releases?per_page=100",
}

def api(suffix: str):
    target = f"repos/{REPO}" + (f"/{suffix}" if suffix else "")
    result = subprocess.run(["gh", "api", "--paginate", "--slurp", target],
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=180)
    if result.returncode:
        raise RuntimeError(f"gh api failure ({result.returncode}) for {suffix}: {result.stderr[:300]}")
    pages = json.loads(result.stdout)
    if isinstance(pages, list) and all(isinstance(p, list) for p in pages):
        return [item for page in pages for item in page]
    if isinstance(pages, list) and len(pages) == 1 and isinstance(pages[0], dict):
        return pages[0]
    return pages

def save(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def one_pr(number: int):
    info = {"number": number}
    errors = []
    for key, suffix in [("reviews", "reviews"), ("changed_files", "files"), ("commits", "commits")]:
        try:
            info[key] = api(f"pulls/{number}/{suffix}?per_page=100")
        except Exception as exc:
            errors.append(str(exc))
    save(HERE / "pr-details" / f"{number:04d}.json", info)
    return errors

def main():
    results, errors = {}, []
    for filename, suffix in FILES.items():
        try:
            data = api(suffix)
            save(HERE / filename, data)
            results[filename] = len(data) if isinstance(data, list) else 1
            print(f"ARCHIVED {filename}: {results[filename]}", flush=True)
        except Exception as exc:
            errors.append(str(exc))
            print(f"ERROR {filename}: {exc}", flush=True)
    pulls = json.loads((HERE / "pull_requests.json").read_text(encoding="utf-8"))
    issue_wrappers = json.loads((HERE / "issues_all.json").read_text(encoding="utf-8"))
    results["issues_excluding_prs"] = sum("pull_request" not in i for i in issue_wrappers)
    results["prs"] = len(pulls)
    nums = sorted(int(pr["number"]) for pr in pulls)
    with cf.ThreadPoolExecutor(max_workers=5) as pool:
        jobs = {pool.submit(one_pr, n): n for n in nums}
        completed = 0
        for future in cf.as_completed(jobs):
            completed += 1
            try:
                errors += [f"PR #{jobs[future]}: {e}" for e in future.result()]
            except Exception as exc:
                errors.append(f"PR #{jobs[future]}: {exc}")
            if completed % 10 == 0 or completed == len(nums):
                print(f"PR_DETAILS {completed}/{len(nums)}", flush=True)
    hashes = {}
    for f in HERE.rglob("*.json"):
        if f.name != "manifest.json":
            b = f.read_bytes()
            hashes[f.relative_to(HERE).as_posix()] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    report = {
        "source": REPO,
        "captured_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "privacy": "PRIVATE ARCHIVE ONLY. DO NOT PUBLISH UNTIL ALL FILES, REF HEADS, COMMIT HISTORY, AND METADATA AUDITED.",
        "counts": results, "file_hashes": hashes, "errors": errors,
        "note": "GitHub Issues and PRs are preserved as JSON, not recreated as interactive issues or PRs.",
    }
    save(HERE / "manifest.json", report)
    (HERE / "README.md").write_text(
        "# GitHub metadata migration snapshot (PRIVATE)\n\n"
        "Contains raw metadata for the original research repository, including issue/PR bodies, comments, "
        "reviews, changed-file listings, commits, events and repository settings. It may contain identifying "
        "information. DO NOT MAKE THIS REPOSITORY PUBLIC without auditing every branch and Git history.\n\n"
        "This branch archives metadata as files; it does not recreate original GitHub issues, PR discussions, "
        "author identities, timestamps, or attachments in GitHub's interactive system.\n", encoding="utf-8")
    print("SUMMARY " + json.dumps({"counts": results, "errors": len(errors), "files": len(hashes)}, ensure_ascii=False), flush=True)
    return 0 if not errors else 7

if __name__ == "__main__":
    sys.exit(main())
