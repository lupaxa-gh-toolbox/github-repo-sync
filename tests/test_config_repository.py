"""Tests for refreshing the configuration repository before a sync."""

from __future__ import annotations

from pathlib import Path

from git import Repo
import pytest

from lupaxa.github_repo_sync.git_operations import (
    configuration_repository_status,
    fast_forward_configuration_repository,
)
from lupaxa.github_repo_sync.loader import (
    refresh_default_configuration_repository,
)


def _identity(repository: Repo) -> None:
    with repository.config_writer() as config:
        config.set_value("user", "name", "Test User")
        config.set_value("user", "email", "test@example.com")


def test_other_config_path_is_not_refreshed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_dir = tmp_path / ".config" / "github-repo-sync"
    config_dir.mkdir(parents=True)
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.loader.DEFAULT_CONFIG_DIRECTORY",
        config_dir,
    )
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.loader.DEFAULT_CONFIG_FILENAME",
        config_dir / "github-repo-sync.yaml",
    )

    assert refresh_default_configuration_repository(tmp_path / "other.yaml") is None


def test_missing_git_directory_is_not_refreshed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_dir = tmp_path / ".config" / "github-repo-sync"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "github-repo-sync.yaml"
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.loader.DEFAULT_CONFIG_DIRECTORY",
        config_dir,
    )
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.loader.DEFAULT_CONFIG_FILENAME",
        config_file,
    )

    assert refresh_default_configuration_repository(config_file) is None


def test_configuration_repository_is_fast_forwarded(tmp_path: Path) -> None:
    origin_path = tmp_path / "origin.git"
    Repo.init(origin_path, bare=True)
    seed_path = tmp_path / "seed"
    seed = Repo.init(seed_path)
    _identity(seed)
    config_name = "github-repo-sync.yml"
    (seed_path / config_name).write_text("one\n", encoding="utf-8")
    seed.index.add([config_name])
    seed.index.commit("one")
    seed.create_remote("origin", origin_path.as_uri())
    seed.git.push("--set-upstream", "origin", "HEAD")

    checkout = tmp_path / "config"
    cloned = Repo.clone_from(origin_path.as_uri(), checkout)
    cloned.close()

    (seed_path / config_name).write_text("two\n", encoding="utf-8")
    seed.index.add([config_name])
    seed.index.commit("two")
    seed.git.push()
    seed.close()

    result = fast_forward_configuration_repository(checkout)

    assert result is not None
    assert result["result"] == "success"
    assert (checkout / config_name).read_text(encoding="utf-8") == "two\n"


def test_dirty_configuration_repository_is_left_unchanged(tmp_path: Path) -> None:
    origin_path = tmp_path / "origin.git"
    Repo.init(origin_path, bare=True)
    seed_path = tmp_path / "seed"
    seed = Repo.init(seed_path)
    _identity(seed)
    (seed_path / "github-repo-sync.yml").write_text("one\n", encoding="utf-8")
    seed.index.add(["github-repo-sync.yml"])
    seed.index.commit("one")
    seed.create_remote("origin", origin_path.as_uri())
    seed.git.push("--set-upstream", "origin", "HEAD")
    seed.close()

    checkout = tmp_path / "config"
    cloned = Repo.clone_from(origin_path.as_uri(), checkout)
    cloned.close()
    (checkout / "github-repo-sync.yml").write_text("local\n", encoding="utf-8")

    result = fast_forward_configuration_repository(checkout)

    assert result is not None
    assert result["result"] == "dirty"
    assert "submodule changes" in result["message"]
    assert (checkout / "github-repo-sync.yml").read_text(encoding="utf-8") == "local\n"


def test_configuration_repository_reports_when_behind(tmp_path: Path) -> None:
    origin_path = tmp_path / "origin.git"
    Repo.init(origin_path, bare=True)
    seed_path = tmp_path / "seed"
    seed = Repo.init(seed_path)
    _identity(seed)
    (seed_path / "github-repo-sync.yml").write_text("one\n", encoding="utf-8")
    seed.index.add(["github-repo-sync.yml"])
    seed.index.commit("one")
    seed.create_remote("origin", origin_path.as_uri())
    seed.git.push("--set-upstream", "origin", "HEAD")

    checkout = tmp_path / "config"
    cloned = Repo.clone_from(origin_path.as_uri(), checkout)
    cloned.close()

    (seed_path / "github-repo-sync.yml").write_text("two\n", encoding="utf-8")
    seed.index.add(["github-repo-sync.yml"])
    seed.index.commit("two")
    seed.git.push()
    seed.close()

    status = configuration_repository_status(checkout, offline=False)

    assert status is not None
    assert status["status"] == "behind"
    assert status["behind"] == 1
    assert (checkout / "github-repo-sync.yml").read_text(encoding="utf-8") == "one\n"
