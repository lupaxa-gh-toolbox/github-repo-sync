"""Tests for organisation and repository clone_path overrides."""

from __future__ import annotations

from pathlib import Path

import pytest

from lupaxa.github_repo_sync.exceptions import ConfigurationError
from lupaxa.github_repo_sync.synchronisation import build_repository_path
from lupaxa.github_repo_sync.validation import validate_configuration


def _configuration(organisations: list[object]) -> dict[str, object]:
    return {
        "config": {
            "clone_path": "~/Desktop/GitMaster",
            "clone_protocol": "ssh",
        },
        "organisations": organisations,
    }


def test_organisation_clone_path_overrides_the_global_root() -> None:
    validated = validate_configuration(
        _configuration(
            [
                {
                    "name": "personal",
                    "alias": ".config",
                    "clone_path": "~",
                    "repositories": [
                        {"name": ".github-intel"},
                        {"name": "dockerhub-intel"},
                    ],
                }
            ]
        )
    )

    organisation = validated["organisations"][0]
    home = str(Path.home())

    assert organisation["repositories"][0]["clone_path"] == home
    assert organisation["repositories"][1]["clone_path"] == home
    assert (
        build_repository_path(
            organisation,
            organisation["repositories"][0],
        )
        == Path.home() / ".config" / ".github-intel"
    )
    assert (
        build_repository_path(
            organisation,
            organisation["repositories"][1],
        )
        == Path.home() / ".config" / "dockerhub-intel"
    )


def test_repository_clone_path_overrides_the_organisation_root() -> None:
    validated = validate_configuration(
        _configuration(
            [
                {
                    "name": "personal",
                    "alias": ".config",
                    "clone_path": "~",
                    "repositories": [
                        {"name": ".github-intel"},
                        {
                            "name": "dockerhub-intel",
                            "clone_path": "~/Desktop/GitMaster",
                        },
                    ],
                }
            ]
        )
    )

    organisation = validated["organisations"][0]
    gitmaster = str(Path.home() / "Desktop" / "GitMaster")

    assert organisation["repositories"][0]["clone_path"] == str(Path.home())
    assert organisation["repositories"][1]["clone_path"] == gitmaster
    assert (
        build_repository_path(
            organisation,
            organisation["repositories"][1],
        )
        == Path(gitmaster) / ".config" / "dockerhub-intel"
    )


def test_omitted_clone_path_uses_the_global_root() -> None:
    validated = validate_configuration(
        _configuration(
            [
                {
                    "name": "the-lupaxa-project",
                    "repositories": [{"name": "workflows"}],
                }
            ]
        )
    )

    organisation = validated["organisations"][0]
    root = str(Path.home() / "Desktop" / "GitMaster")

    assert organisation["repositories"][0]["clone_path"] == root


def test_same_alias_under_different_clone_paths_is_allowed() -> None:
    validated = validate_configuration(
        _configuration(
            [
                {
                    "name": "one",
                    "alias": "shared",
                    "repositories": [{"name": "alpha"}],
                },
                {
                    "name": "two",
                    "alias": "shared",
                    "clone_path": "~/other",
                    "repositories": [{"name": "beta"}],
                },
            ]
        )
    )

    assert len(validated["organisations"]) == 2


def test_dot_alias_places_repositories_directly_under_clone_path() -> None:
    validated = validate_configuration(
        _configuration(
            [
                {
                    "name": "Lupraxus",
                    "alias": ".config",
                    "clone_path": "~",
                    "repositories": [{"name": "github-intel"}],
                },
                {
                    "name": "Lupraxus",
                    "alias": ".",
                    "clone_path": "~",
                    "repositories": [{"name": "bin"}],
                },
            ]
        )
    )

    home_organisation = next(
        organisation
        for organisation in validated["organisations"]
        if organisation["destination_name"] == "."
    )

    assert (
        build_repository_path(
            home_organisation,
            home_organisation["repositories"][0],
        )
        == Path.home() / "bin"
    )


def test_duplicate_repository_for_one_organisation_is_rejected() -> None:
    with pytest.raises(ConfigurationError, match="duplicates Lupraxus/bin"):
        validate_configuration(
            _configuration(
                [
                    {
                        "name": "Lupraxus",
                        "alias": ".config",
                        "clone_path": "~",
                        "repositories": [{"name": "bin"}],
                    },
                    {
                        "name": "Lupraxus",
                        "alias": ".",
                        "clone_path": "~",
                        "repositories": [{"name": "bin"}],
                    },
                ]
            )
        )


def test_same_directory_under_the_same_clone_path_is_rejected() -> None:
    with pytest.raises(ConfigurationError, match="same local directory"):
        validate_configuration(
            _configuration(
                [
                    {
                        "name": "one",
                        "alias": "shared",
                        "repositories": [{"name": "alpha"}],
                    },
                    {
                        "name": "two",
                        "alias": "shared",
                        "repositories": [{"name": "beta"}],
                    },
                ]
            )
        )
