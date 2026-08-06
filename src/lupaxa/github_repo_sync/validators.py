"""
Reusable configuration validators for Lupaxa GitHub Repository Sync.

This module contains small validation helpers used to validate primitive
configuration values. Application-specific configuration assembly is handled
by the validation module.
"""

from __future__ import annotations

from typing import Any, cast

from .constants import SUPPORTED_CLONE_PROTOCOLS
from .exceptions import ConfigurationError
from .models import CloneProtocol


def require_object(
    value: Any,
    location: str,
) -> dict[str, Any]:
    """
    Require a configuration value to be an object.

    Args:
        value: Value to validate.
        location: Configuration location used in error messages.

    Returns:
        Validated object.

    Raises:
        ConfigurationError: If the value is not an object.

    """

    if not isinstance(value, dict):
        raise ConfigurationError(f"{location} must be an object.")

    return value


def require_list(
    value: Any,
    location: str,
) -> list[Any]:
    """
    Require a configuration value to be a list.

    Args:
        value: Value to validate.
        location: Configuration location used in error messages.

    Returns:
        Validated list.

    Raises:
        ConfigurationError: If the value is not a list.

    """

    if not isinstance(value, list):
        raise ConfigurationError(f"{location} must be a list.")

    return value


def require_non_empty_string(
    value: Any,
    location: str,
) -> str:
    """
    Require a configuration value to be a non-empty string.

    Leading and trailing whitespace is removed before the value is returned.

    Args:
        value: Value to validate.
        location: Configuration location used in error messages.

    Returns:
        Trimmed string.

    Raises:
        ConfigurationError: If the value is not a non-empty string.

    """

    if not isinstance(value, str):
        raise ConfigurationError(f"{location} must be a string.")

    normalized_value = value.strip()

    if not normalized_value:
        raise ConfigurationError(f"{location} must not be empty.")

    return normalized_value


def reject_unknown_keys(
    mapping: dict[str, Any],
    allowed_keys: set[str],
    location: str,
) -> None:
    """
    Reject unrecognised configuration keys.

    Args:
        mapping: Configuration object to inspect.
        allowed_keys: Permitted key names.
        location: Configuration location used in error messages.

    Raises:
        ConfigurationError: If unknown keys are present.

    """

    unknown_keys = set(mapping) - allowed_keys

    if not unknown_keys:
        return

    formatted_keys = ", ".join(repr(key) for key in sorted(unknown_keys))

    key_word = "key" if len(unknown_keys) == 1 else "keys"

    raise ConfigurationError(
        f"{location} contains unknown {key_word}: {formatted_keys}."
    )


def validate_local_directory_name(
    value: str,
    location: str,
) -> None:
    """
    Validate one local directory name.

    Args:
        value: Directory name to validate.
        location: Configuration location used in error messages.

    Raises:
        ConfigurationError: If the value is not a safe directory name.

    """

    if value in {".", ".."}:
        raise ConfigurationError(f"{location} must not be '.' or '..'.")

    if "/" in value or "\\" in value:
        raise ConfigurationError(f"{location} must be a directory name, not a path.")

    if "\x00" in value:
        raise ConfigurationError(f"{location} must not contain a null character.")


def validate_github_name(
    value: Any,
    location: str,
) -> str:
    """
    Validate a GitHub organisation or repository name.

    Args:
        value: Name to validate.
        location: Configuration location used in error messages.

    Returns:
        Validated GitHub name.

    Raises:
        ConfigurationError:
            If the value is not a valid standalone GitHub name.

    """

    name = require_non_empty_string(
        value,
        location,
    )

    if name in {".", ".."}:
        raise ConfigurationError(f"{location} must not be '.' or '..'.")

    if "/" in name or "\\" in name:
        raise ConfigurationError(
            f"{location} must contain only the GitHub name, not a path."
        )

    if "\x00" in name:
        raise ConfigurationError(f"{location} must not contain a null character.")

    return name


def validate_optional_alias(
    value: Any,
    location: str,
) -> str | None:
    """
    Validate an optional local directory alias.

    Args:
        value: Alias value.
        location: Configuration location used in error messages.

    Returns:
        Validated alias, or None when no alias was supplied.

    Raises:
        ConfigurationError: If the alias is invalid.

    """

    if value is None:
        return None

    alias = require_non_empty_string(
        value,
        location,
    )

    validate_local_directory_name(
        alias,
        location,
    )

    return alias


def validate_clone_protocol(
    value: Any,
    location: str,
) -> CloneProtocol:
    """
    Validate a repository clone protocol.

    Args:
        value: Protocol value.
        location: Configuration location used in error messages.

    Returns:
        Validated clone protocol.

    Raises:
        ConfigurationError: If the protocol is unsupported.

    """

    protocol = require_non_empty_string(
        value,
        location,
    ).lower()

    if protocol not in SUPPORTED_CLONE_PROTOCOLS:
        supported_protocols = ", ".join(sorted(SUPPORTED_CLONE_PROTOCOLS))

        raise ConfigurationError(f"{location} must be one of: {supported_protocols}.")

    return cast(CloneProtocol, protocol)
