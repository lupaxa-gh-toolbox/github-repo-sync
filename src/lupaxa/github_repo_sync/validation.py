"""
Application-specific configuration validation.

This module validates and normalises repository and organisation structures
after the YAML, JSON, or JSON5 configuration has been loaded.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .exceptions import ConfigurationError
from .models import (
    CloneProtocol,
    OrganisationConfiguration,
    RepositoryConfiguration,
    ValidatedConfiguration,
)
from .validators import (
    reject_unknown_keys,
    require_list,
    require_non_empty_string,
    require_object,
    validate_clone_protocol,
    validate_github_name,
    validate_optional_alias,
    validate_optional_organisation_alias,
)


def resolve_configured_path(path: Path) -> Path:
    """
    Expand environment variables and the user's home directory in a path.

    Args:
        path: Path to expand.

    Returns:
        Expanded path.

    """

    expanded_path = os.path.expandvars(str(path))
    return Path(expanded_path).expanduser()


def resolve_clone_path_setting(
    value: object,
    location: str,
) -> Path:
    """
    Resolve a clone path override.

    Args:
        value: Raw override.
        location: Configuration location used in error messages.

    Returns:
        Expanded path.

    Raises:
        ConfigurationError: If the override is not a non-empty path.

    """

    raw_clone_path = require_non_empty_string(
        value,
        location,
    )

    return resolve_configured_path(Path(raw_clone_path))


def validate_repository(
    repository: object,
    organisation_index: int,
    repository_index: int,
    global_protocol: CloneProtocol,
    clone_path: Path,
) -> RepositoryConfiguration:
    """
    Validate and normalise one repository configuration.

    Args:
        repository: Raw repository configuration.
        organisation_index: Parent organisation list index.
        repository_index: Repository list index.
        global_protocol: Default clone protocol.
        clone_path: Effective clone path before a repository override.

    Returns:
        Validated repository configuration.

    Raises:
        ConfigurationError: If the repository configuration is invalid.

    """

    location = f"organisations[{organisation_index}].repositories[{repository_index}]"

    repository_object = require_object(
        repository,
        location,
    )

    reject_unknown_keys(
        repository_object,
        {
            "name",
            "alias",
            "clone_path",
            "clone_protocol",
        },
        location,
    )

    if "name" not in repository_object:
        raise ConfigurationError(f"{location}.name is required.")

    name = validate_github_name(
        repository_object["name"],
        f"{location}.name",
    )

    alias = validate_optional_alias(
        repository_object.get("alias"),
        f"{location}.alias",
    )

    if "clone_protocol" in repository_object:
        clone_protocol = validate_clone_protocol(
            repository_object["clone_protocol"],
            f"{location}.clone_protocol",
        )
    else:
        clone_protocol = global_protocol

    if "clone_path" in repository_object:
        repository_clone_path = resolve_clone_path_setting(
            repository_object["clone_path"],
            f"{location}.clone_path",
        )
    else:
        repository_clone_path = clone_path

    return {
        "name": name,
        "alias": alias,
        "destination_name": alias or name,
        "clone_path": str(repository_clone_path),
        "clone_protocol": clone_protocol,
    }


def validate_organisation(
    organisation: object,
    organisation_index: int,
    global_protocol: CloneProtocol,
    global_clone_path: Path,
) -> OrganisationConfiguration:
    """
    Validate and normalise one organisation configuration.

    Args:
        organisation: Raw organisation configuration.
        organisation_index: Organisation list index.
        global_protocol: Default clone protocol.
        global_clone_path: Default clone path.

    Returns:
        Validated organisation configuration.

    Raises:
        ConfigurationError: If the organisation configuration is invalid.

    """

    location = f"organisations[{organisation_index}]"

    organisation_object = require_object(
        organisation,
        location,
    )

    reject_unknown_keys(
        organisation_object,
        {
            "name",
            "alias",
            "clone_path",
            "repositories",
        },
        location,
    )

    if "name" not in organisation_object:
        raise ConfigurationError(f"{location}.name is required.")

    if "repositories" not in organisation_object:
        raise ConfigurationError(f"{location}.repositories is required.")

    name = validate_github_name(
        organisation_object["name"],
        f"{location}.name",
    )

    alias = validate_optional_organisation_alias(
        organisation_object.get("alias"),
        f"{location}.alias",
    )

    if "clone_path" in organisation_object:
        organisation_clone_path = resolve_clone_path_setting(
            organisation_object["clone_path"],
            f"{location}.clone_path",
        )
    else:
        organisation_clone_path = global_clone_path

    raw_repositories = require_list(
        organisation_object["repositories"],
        f"{location}.repositories",
    )

    if not raw_repositories:
        raise ConfigurationError(
            f"{location}.repositories must contain at least one repository."
        )

    repository_names: dict[str, int] = {}
    repository_destinations: dict[str, int] = {}
    repositories: list[RepositoryConfiguration] = []
    organisation_destination = alias or name

    for repository_index, raw_repository in enumerate(raw_repositories):
        repository = validate_repository(
            repository=raw_repository,
            organisation_index=organisation_index,
            repository_index=repository_index,
            global_protocol=global_protocol,
            clone_path=organisation_clone_path,
        )

        repository_name_key = repository["name"].casefold()
        repository_destination_key = str(
            Path(repository["clone_path"])
            / organisation_destination
            / repository["destination_name"]
        ).casefold()

        if repository_name_key in repository_names:
            previous_index = repository_names[repository_name_key]

            raise ConfigurationError(
                f"{location}.repositories[{repository_index}].name "
                f"duplicates repositories[{previous_index}].name: "
                f"{repository['name']!r}."
            )

        if repository_destination_key in repository_destinations:
            previous_index = repository_destinations[repository_destination_key]

            raise ConfigurationError(
                f"{location}.repositories[{repository_index}] resolves to "
                f"the same local directory as repositories[{previous_index}]: "
                f"{repository_destination_key!r}."
            )

        repository_names[repository_name_key] = repository_index

        repository_destinations[repository_destination_key] = repository_index

        repositories.append(repository)

    return {
        "name": name,
        "alias": alias,
        "destination_name": alias or name,
        "repositories": repositories,
    }


def validate_configuration(
    configuration: dict[str, Any],
) -> ValidatedConfiguration:
    """
    Validate and normalise the complete application configuration.

    Organisations and repositories are sorted case-insensitively by their
    real GitHub names after validation.

    Args:
        configuration: Raw top-level configuration.

    Returns:
        Validated and normalised configuration.

    Raises:
        ConfigurationError: If any configuration value is invalid.

    """

    reject_unknown_keys(
        configuration,
        {
            "config",
            "organisations",
        },
        "configuration",
    )

    if "config" not in configuration:
        raise ConfigurationError("configuration.config is required.")

    if "organisations" not in configuration:
        raise ConfigurationError("configuration.organisations is required.")

    global_config = require_object(
        configuration["config"],
        "config",
    )

    reject_unknown_keys(
        global_config,
        {
            "clone_path",
            "clone_protocol",
        },
        "config",
    )

    if "clone_path" not in global_config:
        raise ConfigurationError("config.clone_path is required.")

    if "clone_protocol" not in global_config:
        raise ConfigurationError("config.clone_protocol is required.")

    raw_clone_path = require_non_empty_string(
        global_config["clone_path"],
        "config.clone_path",
    )

    clone_path = resolve_configured_path(Path(raw_clone_path))

    clone_protocol = validate_clone_protocol(
        global_config["clone_protocol"],
        "config.clone_protocol",
    )

    raw_organisations = require_list(
        configuration["organisations"],
        "organisations",
    )

    if not raw_organisations:
        raise ConfigurationError(
            "organisations must contain at least one organisation."
        )

    organisation_destinations: dict[str, int] = {}
    repository_identities: dict[str, int] = {}
    organisations: list[OrganisationConfiguration] = []

    for organisation_index, raw_organisation in enumerate(raw_organisations):
        organisation = validate_organisation(
            organisation=raw_organisation,
            organisation_index=organisation_index,
            global_protocol=clone_protocol,
            global_clone_path=clone_path,
        )

        for repository in organisation["repositories"]:
            repository_identity = (
                f"{organisation['name']}/{repository['name']}".casefold()
            )

            if repository_identity in repository_identities:
                previous_index = repository_identities[repository_identity]

                raise ConfigurationError(
                    f"organisations[{organisation_index}] duplicates "
                    f"{organisation['name']}/{repository['name']} already "
                    f"listed on organisations[{previous_index}]."
                )

            repository_identities[repository_identity] = organisation_index

            organisation_directory_key = str(
                Path(repository["clone_path"]) / organisation["destination_name"]
            ).casefold()

            if organisation_directory_key not in organisation_destinations:
                organisation_destinations[organisation_directory_key] = (
                    organisation_index
                )
                continue

            previous_index = organisation_destinations[organisation_directory_key]

            if previous_index == organisation_index:
                continue

            raise ConfigurationError(
                f"organisations[{organisation_index}] resolves to the same "
                f"local directory as organisations[{previous_index}]: "
                f"{organisation['destination_name']!r} under "
                f"{repository['clone_path']!r}."
            )

        organisations.append(organisation)

    organisations.sort(key=lambda item: item["name"].casefold())

    for organisation in organisations:
        organisation["repositories"].sort(key=lambda item: item["name"].casefold())

    return {
        "config": {
            "clone_path": str(clone_path),
            "clone_protocol": clone_protocol,
        },
        "organisations": organisations,
    }
