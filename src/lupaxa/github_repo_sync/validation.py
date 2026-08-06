"""
Application-specific configuration validation.

This module validates and normalises repository and organisation structures
after the JSON5 configuration has been loaded.
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


def validate_repository(
    repository: object,
    organisation_index: int,
    repository_index: int,
    global_protocol: CloneProtocol,
) -> RepositoryConfiguration:
    """
    Validate and normalise one repository configuration.

    Args:
        repository: Raw repository configuration.
        organisation_index: Parent organisation list index.
        repository_index: Repository list index.
        global_protocol: Default clone protocol.

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

    return {
        "name": name,
        "alias": alias,
        "destination_name": alias or name,
        "clone_protocol": clone_protocol,
    }


def validate_organisation(
    organisation: object,
    organisation_index: int,
    global_protocol: CloneProtocol,
) -> OrganisationConfiguration:
    """
    Validate and normalise one organisation configuration.

    Args:
        organisation: Raw organisation configuration.
        organisation_index: Organisation list index.
        global_protocol: Default clone protocol.

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

    alias = validate_optional_alias(
        organisation_object.get("alias"),
        f"{location}.alias",
    )

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

    for repository_index, raw_repository in enumerate(raw_repositories):
        repository = validate_repository(
            repository=raw_repository,
            organisation_index=organisation_index,
            repository_index=repository_index,
            global_protocol=global_protocol,
        )

        repository_name_key = repository["name"].casefold()
        repository_destination_key = repository["destination_name"].casefold()

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
                f"{repository['destination_name']!r}."
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

    organisation_names: dict[str, int] = {}
    organisation_destinations: dict[str, int] = {}
    organisations: list[OrganisationConfiguration] = []

    for organisation_index, raw_organisation in enumerate(raw_organisations):
        organisation = validate_organisation(
            organisation=raw_organisation,
            organisation_index=organisation_index,
            global_protocol=clone_protocol,
        )

        organisation_name_key = organisation["name"].casefold()
        organisation_destination_key = organisation["destination_name"].casefold()

        if organisation_name_key in organisation_names:
            previous_index = organisation_names[organisation_name_key]

            raise ConfigurationError(
                f"organisations[{organisation_index}].name duplicates "
                f"organisations[{previous_index}].name: "
                f"{organisation['name']!r}."
            )

        if organisation_destination_key in organisation_destinations:
            previous_index = organisation_destinations[organisation_destination_key]

            raise ConfigurationError(
                f"organisations[{organisation_index}] resolves to the same "
                f"local directory as organisations[{previous_index}]: "
                f"{organisation['destination_name']!r}."
            )

        organisation_names[organisation_name_key] = organisation_index

        organisation_destinations[organisation_destination_key] = organisation_index

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
