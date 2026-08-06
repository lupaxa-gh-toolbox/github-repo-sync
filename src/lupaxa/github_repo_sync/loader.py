"""
Configuration loading for Lupaxa GitHub Repository Sync.

This module is responsible only for locating and loading a JSON5
configuration file. Structural validation is performed separately by
the validation module.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import json5

from .exceptions import ConfigurationError


def load_configuration(config_path: Path) -> dict[str, Any]:
    """
    Load a JSON5 configuration file.

    Args:
        config_path: Path to the JSON5 configuration file.

    Returns:
        Parsed configuration object.

    Raises:
        ConfigurationError:
            If the configuration cannot be read or parsed.

    """

    try:
        config_path_status = config_path.stat()
    except FileNotFoundError as exc:
        raise ConfigurationError(
            f"Configuration file does not exist: {config_path}"
        ) from exc
    except PermissionError as exc:
        raise ConfigurationError(
            f"Permission denied while accessing configuration: {config_path}"
        ) from exc
    except OSError as exc:
        raise ConfigurationError(
            f"Could not inspect configuration path '{config_path}': {exc}"
        ) from exc

    if not config_path_status:
        raise ConfigurationError(f"Could not inspect configuration path: {config_path}")

    if not config_path.is_file():
        raise ConfigurationError(
            f"Configuration path is not a regular file: {config_path}"
        )

    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            configuration = json5.load(config_file)
    except PermissionError as exc:
        raise ConfigurationError(
            f"Permission denied while reading configuration: {config_path}"
        ) from exc
    except UnicodeDecodeError as exc:
        raise ConfigurationError(
            f"Configuration file is not valid UTF-8: {config_path}"
        ) from exc
    except OSError as exc:
        raise ConfigurationError(
            f"Could not read configuration file '{config_path}': {exc}"
        ) from exc
    except ValueError as exc:
        raise ConfigurationError(
            f"Invalid JSON5 syntax in '{config_path}': {exc}"
        ) from exc

    if not isinstance(configuration, dict):
        raise ConfigurationError("The top-level configuration value must be an object.")

    return configuration
