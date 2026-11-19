"""Tests for YAML, JSON, and JSON5 configuration loading."""

from __future__ import annotations

from pathlib import Path

import pytest

from lupaxa.github_repo_sync.exceptions import ConfigurationError
from lupaxa.github_repo_sync.loader import (
    load_configuration,
    resolve_default_configuration_path,
    select_configuration_path,
)

MINIMAL_OBJECT = {
    "config": {
        "clone_path": "~/repos",
        "clone_protocol": "ssh",
    },
    "organisations": [],
}


def test_load_configuration_json5(tmp_path: Path) -> None:
    path = tmp_path / "config.json5"
    path.write_text(
        """
        {
          // comment
          config: {
            clone_path: "~/repos",
            clone_protocol: "ssh",
          },
          organisations: [],
        }
        """,
        encoding="utf-8",
    )

    assert load_configuration(path) == MINIMAL_OBJECT


def test_load_configuration_json(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text(
        """
        {
          "config": {
            "clone_path": "~/repos",
            "clone_protocol": "ssh"
          },
          "organisations": []
        }
        """,
        encoding="utf-8",
    )

    assert load_configuration(path) == MINIMAL_OBJECT


def test_load_configuration_yaml(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(
        """
        # comment
        config:
          clone_path: ~/repos
          clone_protocol: ssh
        organisations: []
        """,
        encoding="utf-8",
    )

    assert load_configuration(path) == MINIMAL_OBJECT


def test_load_configuration_yml_suffix(tmp_path: Path) -> None:
    path = tmp_path / "config.yml"
    path.write_text(
        "config:\n  clone_path: ~/repos\n  clone_protocol: ssh\norganisations: []\n",
        encoding="utf-8",
    )

    assert load_configuration(path) == MINIMAL_OBJECT


def test_load_configuration_invalid_yaml(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text("config: [\n", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="Invalid YAML"):
        load_configuration(path)


def test_load_configuration_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="Invalid JSON"):
        load_configuration(path)


def test_resolve_default_configuration_prefers_yaml(tmp_path: Path) -> None:
    yaml_path = tmp_path / ".github-repo-sync.yaml"
    yaml_path.write_text("config: {}\n", encoding="utf-8")
    (tmp_path / ".github-repo-sync.json5").write_text("{}\n", encoding="utf-8")
    (tmp_path / ".github-repo-sync.json").write_text("{}\n", encoding="utf-8")

    assert resolve_default_configuration_path(tmp_path) == yaml_path


def test_resolve_default_configuration_falls_back_to_json(tmp_path: Path) -> None:
    json_path = tmp_path / ".github-repo-sync.json"
    json_path.write_text("{}\n", encoding="utf-8")
    (tmp_path / ".github-repo-sync.json5").write_text("{}\n", encoding="utf-8")

    assert resolve_default_configuration_path(tmp_path) == json_path


def test_resolve_default_configuration_falls_back_to_json5(tmp_path: Path) -> None:
    json5_path = tmp_path / ".github-repo-sync.json5"
    json5_path.write_text("{}\n", encoding="utf-8")

    assert resolve_default_configuration_path(tmp_path) == json5_path


def test_resolve_default_configuration_reports_missing(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError, match="does not exist"):
        resolve_default_configuration_path(tmp_path)


def _use_config_directories(
    monkeypatch: pytest.MonkeyPatch,
    config_dir: Path,
    home_dir: Path,
) -> None:
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.loader.DEFAULT_CONFIG_DIRECTORY",
        config_dir,
    )
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.loader.DEFAULT_CONFIG_HOME",
        home_dir,
    )
    monkeypatch.setattr(
        "lupaxa.github_repo_sync.loader.DEFAULT_CONFIG_FILENAME",
        config_dir / "github-repo-sync.yaml",
    )


def test_config_directory_wins_over_home(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_dir = tmp_path / ".config" / "github-repo-sync"
    config_dir.mkdir(parents=True)
    preferred = config_dir / "github-repo-sync.yml"
    preferred.write_text("{}\n", encoding="utf-8")
    (tmp_path / ".github-repo-sync.yaml").write_text("{}\n", encoding="utf-8")
    _use_config_directories(monkeypatch, config_dir, tmp_path)

    assert resolve_default_configuration_path() == preferred


def test_hidden_name_in_config_directory_is_ignored(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_dir = tmp_path / ".config" / "github-repo-sync"
    config_dir.mkdir(parents=True)
    (config_dir / ".github-repo-sync.yaml").write_text("{}\n", encoding="utf-8")
    home_file = tmp_path / ".github-repo-sync.yml"
    home_file.write_text("{}\n", encoding="utf-8")
    _use_config_directories(monkeypatch, config_dir, tmp_path)

    assert resolve_default_configuration_path() == home_file


def test_home_is_used_when_config_directory_is_empty(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_dir = tmp_path / ".config" / "github-repo-sync"
    config_dir.mkdir(parents=True)
    home_file = tmp_path / ".github-repo-sync.yml"
    home_file.write_text("{}\n", encoding="utf-8")
    _use_config_directories(monkeypatch, config_dir, tmp_path)

    assert resolve_default_configuration_path() == home_file


def test_select_configuration_uses_config_directory_before_home(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_dir = tmp_path / ".config" / "github-repo-sync"
    config_dir.mkdir(parents=True)
    preferred = config_dir / "github-repo-sync.yml"
    preferred.write_text("{}\n", encoding="utf-8")
    (tmp_path / ".github-repo-sync.yaml").write_text("{}\n", encoding="utf-8")
    _use_config_directories(monkeypatch, config_dir, tmp_path)

    assert select_configuration_path(config_dir / "github-repo-sync.yaml") == preferred


def test_select_configuration_keeps_an_explicit_directory(tmp_path: Path) -> None:
    other = tmp_path / "other"
    other.mkdir()
    chosen = other / ".github-repo-sync.yml"
    chosen.write_text("{}\n", encoding="utf-8")
    config_dir = tmp_path / ".config" / "github-repo-sync"
    config_dir.mkdir(parents=True)
    (config_dir / "github-repo-sync.yaml").write_text("{}\n", encoding="utf-8")

    assert select_configuration_path(other / ".github-repo-sync.yaml") == chosen
