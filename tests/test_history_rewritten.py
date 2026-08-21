"""Tests for rewritten-history detection and optional recovery."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from git import Repo
import pytest

from lupaxa.github_repo_sync.exceptions import RepositorySyncError
from lupaxa.github_repo_sync.git_operations import (
    check_repository_status,
    update_repository,
)


def _seed_clone(tmp_path: Path, org: str, repo_name: str) -> Path:
    work = tmp_path / "work"
    repository = Repo.init(work)

    with repository.config_writer() as config:
        config.set_value("user", "name", "Test User")
        config.set_value("user", "email", "test@example.com")

    (work / "README").write_text("x\n", encoding="utf-8")
    repository.index.add(["README"])
    repository.index.commit("init")
    main = repository.create_head("main")
    main.checkout()

    origin_url = f"https://github.com/{org}/{repo_name}.git"
    origin = repository.create_remote("origin", origin_url)
    repository.git.update_ref(
        "refs/remotes/origin/main",
        repository.head.commit.hexsha,
    )
    repository.heads.main.set_tracking_branch(origin.refs.main)
    repository.close()

    return work


def _point_origin_at_orphan_commit(work: Path) -> str:
    repository = Repo(work)
    try:
        (work / "RESET").write_text("reset-history\n", encoding="utf-8")
        repository.index.add(["RESET"])
        tree = repository.index.write_tree()
        orphan_sha = repository.git.commit_tree(
            str(tree),
            "-m",
            "The initial commit",
        )
        repository.git.update_ref("refs/remotes/origin/main", orphan_sha)
        repository.git.reset("--hard", "HEAD")
        return orphan_sha
    finally:
        repository.close()


def test_status_classifies_unrelated_histories_as_history_rewritten(
    tmp_path: Path,
) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    _point_origin_at_orphan_commit(work)

    result = check_repository_status(work, "org", "repo", offline=True)

    assert result["status"] == "history-rewritten"
    assert result["ahead"] >= 1
    assert result["behind"] >= 1
    assert "shared ancestor" in result["message"].lower()


def test_status_keeps_diverged_when_histories_share_an_ancestor(
    tmp_path: Path,
) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    repository = Repo(work)
    try:
        shared = repository.head.commit
        (work / "local.txt").write_text("local\n", encoding="utf-8")
        repository.index.add(["local.txt"])
        local_commit = repository.index.commit("local commit")

        repository.git.reset("--hard", shared.hexsha)
        (work / "remote.txt").write_text("remote\n", encoding="utf-8")
        repository.index.add(["remote.txt"])
        remote_commit = repository.index.commit("remote commit")
        repository.git.update_ref("refs/remotes/origin/main", remote_commit.hexsha)
        repository.git.reset("--hard", local_commit.hexsha)
    finally:
        repository.close()

    result = check_repository_status(work, "org", "repo", offline=True)

    assert result["status"] == "diverged"
    assert result["ahead"] >= 1
    assert result["behind"] >= 1


def test_update_skips_rewritten_history_by_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    _point_origin_at_orphan_commit(work)
    original_head = Repo(work).head.commit.hexsha
    monkeypatch.setattr("git.remote.Remote.fetch", MagicMock(return_value=[]))

    with pytest.raises(RepositorySyncError) as exc_info:
        update_repository(work, "org", "repo")

    assert exc_info.value.result == "history-rewritten"
    assert "--recover-rewritten-history" in str(exc_info.value)
    assert Repo(work).head.commit.hexsha == original_head


def test_update_resets_rewritten_history_when_requested(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    orphan_sha = _point_origin_at_orphan_commit(work)
    monkeypatch.setattr("git.remote.Remote.fetch", MagicMock(return_value=[]))

    outcome = update_repository(
        work,
        "org",
        "repo",
        recover_rewritten_history=True,
    )

    assert outcome == "reset-rewritten"
    assert Repo(work).head.commit.hexsha == orphan_sha
    assert (work / "RESET").read_text(encoding="utf-8") == "reset-history\n"


def test_recover_flag_does_not_override_dirty_working_tree(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    orphan_sha = _point_origin_at_orphan_commit(work)
    original_head = Repo(work).head.commit.hexsha
    (work / "untracked.txt").write_text("keep\n", encoding="utf-8")
    monkeypatch.setattr("git.remote.Remote.fetch", MagicMock(return_value=[]))

    with pytest.raises(RepositorySyncError) as exc_info:
        update_repository(
            work,
            "org",
            "repo",
            recover_rewritten_history=True,
        )

    assert exc_info.value.result == "dirty"
    assert Repo(work).head.commit.hexsha == original_head
    assert Repo(work).commit(orphan_sha).hexsha == orphan_sha


def test_recover_rewritten_history_parses() -> None:
    from lupaxa.github_repo_sync.cli import create_parser

    args = create_parser().parse_args(["--recover-rewritten-history"])

    assert args.recover_rewritten_history is True


def test_recover_rewritten_history_rejected_with_status() -> None:
    from lupaxa.github_repo_sync.cli import main

    assert main(["--status", "--recover-rewritten-history"]) == 1


def test_main_passes_recover_flag_to_run_sync(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from lupaxa.github_repo_sync.cli import main

    seen: dict[str, object] = {}

    def fake_run_sync(**kwargs: object) -> int:
        seen.update(kwargs)
        return 0

    monkeypatch.setattr("lupaxa.github_repo_sync.cli.run_sync", fake_run_sync)

    assert main(["--recover-rewritten-history"]) == 0
    assert seen["recover_rewritten_history"] is True
