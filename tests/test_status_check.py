"""Unit tests for repository status classification."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

from git import GitCommandError, Repo
import pytest

from lupaxa.github_repo_sync.git_operations import check_repository_status


def _write_config(tmp_path: Path) -> Path:
    config_path = tmp_path / "config.json5"
    config_path.write_text(
        json.dumps(
            {
                "config": {
                    "clone_path": str(tmp_path / "clones"),
                    "clone_protocol": "https",
                },
                "organisations": [
                    {
                        "name": "org",
                        "repositories": [
                            {"name": "clean-repo"},
                            {"name": "z-ahead-repo"},
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return config_path


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


def test_missing_path_is_missing(tmp_path: Path) -> None:
    result = check_repository_status(
        tmp_path / "absent",
        "org",
        "repo",
        offline=True,
    )
    assert result["status"] == "missing"
    assert result["ahead"] == 0
    assert result["behind"] == 0


def test_dirty_working_tree(tmp_path: Path) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    (work / "untracked.txt").write_text("dirty\n", encoding="utf-8")

    result = check_repository_status(work, "org", "repo", offline=True)

    assert result["status"] == "dirty"


def test_ahead_of_upstream_offline(tmp_path: Path) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    repository = Repo(work)
    try:
        (work / "local.txt").write_text("local\n", encoding="utf-8")
        repository.index.add(["local.txt"])
        repository.index.commit("local commit")
    finally:
        repository.close()

    result = check_repository_status(work, "org", "repo", offline=True)

    assert result["status"] == "ahead"
    assert result["ahead"] >= 1


def test_behind_upstream_offline(tmp_path: Path) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    repository = Repo(work)
    try:
        head_commit = repository.head.commit
        (work / "remote.txt").write_text("remote\n", encoding="utf-8")
        repository.index.add(["remote.txt"])
        remote_commit = repository.index.commit("remote commit")
        repository.git.reset("--hard", head_commit.hexsha)
        repository.git.update_ref("refs/remotes/origin/main", remote_commit.hexsha)
    finally:
        repository.close()

    result = check_repository_status(work, "org", "repo", offline=True)

    assert result["status"] == "behind"
    assert result["behind"] >= 1


def test_clean_when_equal_offline(tmp_path: Path) -> None:
    work = _seed_clone(tmp_path, "org", "repo")

    result = check_repository_status(work, "org", "repo", offline=True)

    assert result["status"] == "clean"


def test_offline_does_not_fetch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    work = _seed_clone(tmp_path, "org", "repo")

    fetch_mock = MagicMock(side_effect=AssertionError("fetch must not be called"))
    monkeypatch.setattr("git.remote.Remote.fetch", fetch_mock)

    result = check_repository_status(work, "org", "repo", offline=True)

    assert result["status"] == "clean"
    fetch_mock.assert_not_called()


def test_missing_remote_tracking_ref_is_no_upstream(tmp_path: Path) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    repository = Repo(work)
    try:
        repository.git.update_ref("-d", "refs/remotes/origin/main")
    finally:
        repository.close()

    result = check_repository_status(work, "org", "repo", offline=True)

    assert result["status"] == "no-upstream"
    assert result["ahead"] == 0
    assert result["behind"] == 0


def test_fetch_failure_uses_concise_git_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    work = _seed_clone(tmp_path, "org", "repo")
    error = GitCommandError("fetch", 128, stderr="fatal: network down")
    monkeypatch.setattr("git.remote.Remote.fetch", MagicMock(side_effect=error))
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.git_operations.time.sleep",
        lambda _seconds: None,
    )

    result = check_repository_status(work, "org", "repo")

    assert result["status"] == "fetch-failed"
    assert result["message"] == "Could not fetch from 'origin': fatal: network down"


def test_collect_repository_statuses_aggregates_configured_repositories(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from lupaxa.github_repo_sync.commands import load_and_validate_configuration
    from lupaxa.github_repo_sync.status import collect_repository_statuses

    configuration = load_and_validate_configuration(_write_config(tmp_path))
    checks = iter(
        [
            {
                "status": "clean",
                "message": "Clean.",
                "ahead": 0,
                "behind": 0,
            },
            {
                "status": "ahead",
                "message": "Ahead.",
                "ahead": 1,
                "behind": 0,
            },
        ]
    )
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.status.check_repository_status",
        lambda *args, **kwargs: next(checks),
    )

    results = collect_repository_statuses(configuration, offline=True)

    assert [result["repository"] for result in results] == [
        "clean-repo",
        "z-ahead-repo",
    ]
    assert [result["status"] for result in results] == ["clean", "ahead"]
    assert results[0]["path"] == str(tmp_path / "clones" / "org" / "clean-repo")


def test_collect_repository_statuses_contains_repository_exceptions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from lupaxa.github_repo_sync.commands import load_and_validate_configuration
    from lupaxa.github_repo_sync.status import collect_repository_statuses

    configuration = load_and_validate_configuration(_write_config(tmp_path))
    checks = iter(
        [
            RuntimeError("broken clone"),
            {
                "status": "clean",
                "message": "Clean.",
                "ahead": 0,
                "behind": 0,
            },
        ]
    )

    def check_or_raise(*args, **kwargs):
        result = next(checks)
        if isinstance(result, Exception):
            raise result
        return result

    monkeypatch.setattr(
        "lupaxa.github_repo_sync.status.check_repository_status",
        check_or_raise,
    )

    results = collect_repository_statuses(configuration, offline=True)

    assert [result["status"] for result in results] == ["inaccessible", "clean"]
    assert "broken clone" in results[0]["message"]


def test_run_status_all_clean_exits_zero(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from lupaxa.github_repo_sync.commands import run_status

    monkeypatch.setattr(
        "lupaxa.github_repo_sync.status.check_repository_status",
        lambda *args, **kwargs: {
            "status": "clean",
            "message": "Clean.",
            "ahead": 0,
            "behind": 0,
        },
    )

    assert (
        run_status(
            config_path=_write_config(tmp_path),
            offline=True,
            show_header=False,
            show_progress=False,
            show_repository_output=False,
            show_summary_table=False,
        )
        == 0
    )


def test_run_status_not_clean_exits_one(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from lupaxa.github_repo_sync.commands import run_status

    monkeypatch.setattr(
        "lupaxa.github_repo_sync.status.check_repository_status",
        lambda path, *args, **kwargs: {
            "status": "ahead" if path.name == "z-ahead-repo" else "clean",
            "message": "Checked.",
            "ahead": 1 if path.name == "z-ahead-repo" else 0,
            "behind": 0,
        },
    )

    assert (
        run_status(
            config_path=_write_config(tmp_path),
            offline=True,
            show_header=False,
            show_progress=False,
            show_repository_output=False,
            show_summary_table=False,
        )
        == 1
    )


def test_run_status_renders_output_and_tables_for_mixed_results(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from lupaxa.github_repo_sync.commands import run_status

    monkeypatch.setattr(
        "lupaxa.github_repo_sync.status.check_repository_status",
        lambda path, *args, **kwargs: {
            "status": "ahead" if path.name == "z-ahead-repo" else "clean",
            "message": "Checked.",
            "ahead": 1 if path.name == "z-ahead-repo" else 0,
            "behind": 0,
        },
    )

    code = run_status(
        config_path=_write_config(tmp_path),
        offline=True,
        show_header=False,
        show_progress=False,
        show_repository_output=True,
        show_results_table=True,
        show_summary_table=True,
    )

    assert code == 1


def test_ignore_clean_does_not_change_exit_code(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from lupaxa.github_repo_sync.commands import run_status

    monkeypatch.setattr(
        "lupaxa.github_repo_sync.status.check_repository_status",
        lambda path, *args, **kwargs: {
            "status": "ahead" if path.name == "z-ahead-repo" else "clean",
            "message": "Checked.",
            "ahead": 1 if path.name == "z-ahead-repo" else 0,
            "behind": 0,
        },
    )
    config_path = _write_config(tmp_path)
    options = {
        "config_path": config_path,
        "offline": True,
        "show_header": False,
        "show_progress": False,
        "show_repository_output": False,
        "show_summary_table": False,
    }

    code_full = run_status(ignore_clean=False, **options)
    code_filtered = run_status(ignore_clean=True, **options)

    assert code_full == code_filtered == 1


def test_status_mode_parses() -> None:
    from lupaxa.github_repo_sync.cli import create_parser

    args = create_parser().parse_args(["--status", "--ignore-clean", "--offline"])
    assert args.status is True
    assert args.ignore_clean is True
    assert args.offline is True


def test_status_mutex_with_validate() -> None:
    from lupaxa.github_repo_sync.cli import create_parser

    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--status", "--validate"])


def test_ignore_clean_requires_status() -> None:
    from lupaxa.github_repo_sync.cli import main

    code = main(["--ignore-clean"])
    assert code == 1


def test_offline_requires_status() -> None:
    from lupaxa.github_repo_sync.cli import main

    code = main(["--offline"])
    assert code == 1
