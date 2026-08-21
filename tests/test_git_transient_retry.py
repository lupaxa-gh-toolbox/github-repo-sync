"""Tests for transient Git/SSH retry and single-connection updates."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from git import GitCommandError, Repo
import pytest

from lupaxa.github_repo_sync.exceptions import RepositorySyncError
from lupaxa.github_repo_sync.git_operations import (
    check_repository_status,
    clone_repository,
    format_git_error,
    is_transient_git_error,
    update_repository,
)

TRANSIENT_STDERR = (
    "kex_exchange_identification: Connection closed by remote host\n"
    "Connection closed by 140.82.112.4 port 22\n"
    "fatal: Could not read from remote repository.\n"
    "\n"
    "Please make sure you have the correct access rights\n"
    "and the repository exists.\n"
)

PERMANENT_FF_STDERR = "fatal: Not possible to fast-forward, aborting.\n"
PERMANENT_AUTH_STDERR = "Permission denied (publickey).\n"


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


def test_is_transient_git_error_detects_ssh_handshake_drop() -> None:
    error = GitCommandError("fetch", 128, stderr=TRANSIENT_STDERR)

    assert is_transient_git_error(error) is True


def test_is_transient_git_error_rejects_fast_forward_and_auth_failures() -> None:
    ff_error = GitCommandError("pull", 128, stderr=PERMANENT_FF_STDERR)
    auth_error = GitCommandError("fetch", 128, stderr=PERMANENT_AUTH_STDERR)

    assert is_transient_git_error(ff_error) is False
    assert is_transient_git_error(auth_error) is False


def test_format_git_error_keeps_ssh_handshake_lines() -> None:
    error = GitCommandError("fetch", 128, stderr=TRANSIENT_STDERR)
    message = format_git_error(error)

    assert "kex_exchange_identification" in message
    assert "Could not read from remote repository" in message
    assert "stderr:" not in message


def test_update_repository_fetches_then_merges_locally(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    fetch_mock = MagicMock(return_value=[])
    pull_mock = MagicMock()
    monkeypatch.setattr("git.remote.Remote.fetch", fetch_mock)
    monkeypatch.setattr("git.remote.Remote.pull", pull_mock)

    outcome = update_repository(work, "org", "repo")

    assert outcome == "fast-forwarded"
    fetch_mock.assert_called_once()
    _, kwargs = fetch_mock.call_args
    assert kwargs.get("prune") is True
    pull_mock.assert_not_called()


def test_update_repository_retries_transient_fetch_then_succeeds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    attempts = {"count": 0}
    sleeps: list[float] = []

    def fetch(*args, **kwargs):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise GitCommandError("fetch", 128, stderr=TRANSIENT_STDERR)
        return []

    monkeypatch.setattr("git.remote.Remote.fetch", fetch)
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.git_operations.time.sleep",
        sleeps.append,
    )

    outcome = update_repository(work, "org", "repo")

    assert outcome == "fast-forwarded"
    assert attempts["count"] == 3
    assert sleeps == [0.5, 1.5]


def test_update_repository_does_not_retry_fast_forward_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
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

    fetch_mock = MagicMock(return_value=[])
    monkeypatch.setattr("git.remote.Remote.fetch", fetch_mock)
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.git_operations.time.sleep",
        lambda _seconds: None,
    )

    with pytest.raises(RepositorySyncError, match="fast-forward"):
        update_repository(work, "org", "repo")

    assert fetch_mock.call_count == 1


def test_check_repository_status_retries_transient_fetch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    attempts = {"count": 0}

    def fetch(*args, **kwargs):
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise GitCommandError("fetch", 128, stderr=TRANSIENT_STDERR)
        return []

    monkeypatch.setattr("git.remote.Remote.fetch", fetch)
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.git_operations.time.sleep",
        lambda _seconds: None,
    )

    result = check_repository_status(work, "org", "repo")

    assert result["status"] == "clean"
    assert attempts["count"] == 2


def test_clone_repository_retries_transient_clone(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "org" / "repo"
    attempts = {"count": 0}

    def clone_from(*, url: str, to_path: Path):
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise GitCommandError("clone", 128, stderr=TRANSIENT_STDERR)
        destination.mkdir(parents=True)
        Repo.init(destination)

    monkeypatch.setattr(
        "lupaxa.github_repo_sync.git_operations.Repo.clone_from",
        clone_from,
    )
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.git_operations.time.sleep",
        lambda _seconds: None,
    )

    clone_repository("https://github.com/org/repo.git", destination)

    assert attempts["count"] == 2
    assert destination.is_dir()
