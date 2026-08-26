"""Validate the CGF public-base tree using only the Python standard library."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
STATUS = re.compile(r"^Status:\s+`[^`]+`\s*$", re.MULTILINE)
REVIEW_RECORD = re.compile(r"reviewed command|reviewed date|^command:", re.IGNORECASE | re.MULTILINE)
CLAIM_BOUNDARY = re.compile(r"claim boundary", re.IGNORECASE)
ARCHITECTURE_ONLY = re.compile(
    r"\b(runtime spine|execution graph|graph brain(?:/spine)?|graph runtime memory|"
    r"proposal / verifier / commit)\b",
    re.IGNORECASE,
)
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    "assigned credential": re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|password)\s*[:=]"
        r"\s*['\"][^'\"\s]{8,}"
    ),
    "private absolute path": re.compile(
        r"(?i)(?:[A-Z]:\\" + "Users" + r"\\|/" + "Users" + r"/[^/\s]+/|/" + "home" + r"/[^/\s]+/)"
    ),
}
FORBIDDEN_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "runtime",
    "runs",
    "datasets",
    "checkpoints",
}
FORBIDDEN_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".stackdump",
    ".wbproj",
    ".pt",
    ".pkl",
    ".sqlite",
    ".db",
}
TOP_LEVEL_PACKAGE_FILES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "poetry.lock",
    "pyproject.toml",
    "requirements.txt",
    "setup.cfg",
    "setup.py",
    "uv.lock",
    "yarn.lock",
}


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def git_context() -> tuple[Path | None, list[Path]]:
    root_result = run_git("rev-parse", "--show-toplevel")
    if root_result.returncode != 0:
        return None, []
    git_root = Path(root_result.stdout.strip()).resolve()
    files_result = run_git(
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
        "--full-name",
        "--",
        ".",
    )
    if files_result.returncode != 0:
        return git_root, []
    tracked = []
    for value in files_result.stdout.splitlines():
        candidate = (git_root / value).resolve()
        if candidate.is_relative_to(ROOT):
            tracked.append(candidate)
    return git_root, tracked


def markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = re.split(r"\s+(?=['\"])", target, maxsplit=1)[0]
    return unquote(target.split("#", 1)[0])


def check_markdown(errors: list[str]) -> int:
    local_links = 0
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if text.count("```") % 2:
            errors.append(f"unclosed code fence: {path.relative_to(ROOT)}")
        for match in MARKDOWN_LINK.finditer(text):
            raw_target = match.group(1).strip()
            if not raw_target or raw_target.startswith("#"):
                continue
            if re.match(r"^(?:https?://|mailto:)", raw_target, re.IGNORECASE):
                continue
            local_links += 1
            target = markdown_target(raw_target)
            if target and not (path.parent / target).exists():
                errors.append(f"broken local link: {path.relative_to(ROOT)} -> {raw_target}")
    return local_links


def check_eval_records(errors: list[str]) -> int:
    eval_root = ROOT / "labs" / "evals"
    index = (eval_root / "README.md").read_text(encoding="utf-8")
    connection_map = (ROOT / "research" / "connection-map.md").read_text(encoding="utf-8")
    suites = sorted(path for path in eval_root.iterdir() if path.is_dir())
    for suite in suites:
        relative = suite.relative_to(ROOT)
        for required in ("README.md", "eval.py", "test_eval.py", "results.md"):
            if not (suite / required).exists():
                errors.append(f"missing eval file: {relative / required}")
        fixture_dir = suite / "fixtures"
        if fixture_dir.exists() and not (fixture_dir / "README.md").exists():
            errors.append(f"fixture directory is not documented: {relative / 'fixtures/README.md'}")
        result_path = suite / "results.md"
        if result_path.exists():
            result = result_path.read_text(encoding="utf-8")
            if not STATUS.search(result):
                errors.append(f"missing direct status: {result_path.relative_to(ROOT)}")
            if not REVIEW_RECORD.search(result):
                errors.append(f"missing reviewed command or date: {result_path.relative_to(ROOT)}")
            if not CLAIM_BOUNDARY.search(result):
                errors.append(f"missing claim boundary: {result_path.relative_to(ROOT)}")
        if f"({suite.name}/README.md)" not in index:
            errors.append(f"eval is not indexed: {suite.name}")
        if f"(../labs/evals/{suite.name}/results.md)" not in connection_map:
            errors.append(f"eval is absent from research connection map: {suite.name}")
    return len(suites)


def check_release_counts(errors: list[str]) -> None:
    notes = (ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")
    manifest = (ROOT / "RELEASE_MANIFEST.md").read_text(encoding="utf-8")
    note_match = re.search(
        r"(\d+) Python tests pass: (\d+) Architecture/application tests and (\d+) Labs tests",
        notes,
    )
    labs_match = re.search(r"\| Labs eval tests \| Passed: (\d+) tests", manifest)
    total_match = re.search(r"\| Total Python tests \| Passed: (\d+) tests", manifest)
    if not note_match or not labs_match or not total_match:
        errors.append("release test totals are missing or use an unrecognized format")
        return
    note_total, note_application, note_labs = map(int, note_match.groups())
    manifest_labs = int(labs_match.group(1))
    manifest_total = int(total_match.group(1))
    if note_total != note_application + note_labs:
        errors.append("RELEASE_NOTES.md test total does not equal its component counts")
    if (note_total, note_labs) != (manifest_total, manifest_labs):
        errors.append("release notes and manifest test counts disagree")


def check_boundaries_and_history_wording(errors: list[str]) -> None:
    stale_terms = ("Path" + "ConditionedGraph", "research/" + "vms")
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for term in stale_terms:
            if term.casefold() in text.casefold():
                errors.append(f"stale project-history wording in {path.relative_to(ROOT)}: {term}")
    for path in sorted((ROOT / "substrate").rglob("*.md")):
        if ARCHITECTURE_ONLY.search(path.read_text(encoding="utf-8")):
            errors.append(f"Architecture-only operation term in Substrate: {path.relative_to(ROOT)}")


def check_tracked_tree(tracked: list[Path], errors: list[str]) -> None:
    if not tracked:
        errors.append("could not obtain the tracked publication file list")
        return
    for path in tracked:
        relative = path.relative_to(ROOT)
        folded_parts = {part.casefold() for part in relative.parts}
        if folded_parts & FORBIDDEN_PARTS or path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            errors.append(f"tracked generated artifact: {relative}")
        if path.exists() and path.stat().st_size > 1_000_000:
            errors.append(f"tracked file exceeds 1 MB and needs review: {relative}")
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {label}: {relative}")
    for name in TOP_LEVEL_PACKAGE_FILES:
        if (ROOT / name).exists():
            errors.append(f"unexpected top-level package scaffold: {name}")


def check_publication_candidate(git_root: Path | None, errors: list[str]) -> None:
    if git_root is None:
        errors.append("publication candidate is not in a Git repository")
        return
    if git_root != ROOT:
        errors.append(f"CGF is not the Git publication root (current root: {git_root})")
        return
    status = run_git("status", "--porcelain")
    if status.returncode != 0 or status.stdout.strip():
        errors.append("publication candidate working tree is not clean")
    history = run_git("rev-list", "--objects", "--all")
    if history.returncode != 0:
        errors.append("could not inspect publication history")
        return
    for line in history.stdout.splitlines():
        _, _, name = line.partition(" ")
        if not name:
            continue
        path = Path(name)
        folded_parts = {part.casefold() for part in path.parts}
        if folded_parts & FORBIDDEN_PARTS or path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            errors.append(f"generated artifact remains reachable in publication history: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--publication-candidate",
        action="store_true",
        help="also require CGF to be the clean Git root with clean reachable history",
    )
    args = parser.parse_args()
    errors: list[str] = []
    git_root, tracked = git_context()
    local_links = check_markdown(errors)
    eval_count = check_eval_records(errors)
    check_release_counts(errors)
    check_boundaries_and_history_wording(errors)
    check_tracked_tree(tracked, errors)
    if args.publication_candidate:
        check_publication_candidate(git_root, errors)
    if errors:
        print("CGF public-base validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    mode = "publication candidate" if args.publication_candidate else "working tree"
    print(f"CGF {mode} validation passed: {local_links} local links, {eval_count} eval suites.")
    if not args.publication_candidate and git_root != ROOT:
        print("Note: run with --publication-candidate after exporting CGF as the dedicated Git root.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
