"""
Configuration loading for Lupaxa GitHub Repository Sync.

This module locates and loads a JSON5, JSON, or YAML configuration file.
Structural validation is performed separately by the validation module.
"""

from __future__ import annotations

from collections.abc import Callable
import json
from pathlib import Path
from typing import IO, Any

import json5
import yaml

from .constants import DEFAULT_CONFIG_BASENAME, DEFAULT_CONFIG_EXTENSIONS
from .exceptions import ConfigurationError


def resolve_default_configuration_path(
    search_dir: Path | None = None,
) -> Path:
    """
    Find the default configuration file in a directory.

    Candidates are tried in this order: ``.yaml``, ``.yml``, ``.json``,
    ``.json5``.

    Args:
        search_dir:
            Directory to search. Defaults to the user's home directory.

    Returns:
        Path of the first matching configuration file.

    Raises:
        ConfigurationError:
            If none of the default configuration filenames exist.

    """

    directory = Path.home() if search_dir is None else search_dir
    candidates = [
        directory / f"{DEFAULT_CONFIG_BASENAME}{extension}"
        for extension in DEFAULT_CONFIG_EXTENSIONS
    ]

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    listed = ", ".join(str(candidate) for candidate in candidates)
    raise ConfigurationError(f"Configuration file does not exist: {listed}")


def load_configuration(config_path: Path) -> dict[str, Any]:
    """
    Load a JSON5, JSON, or YAML configuration file.

    The parser is selected from the filename suffix. ``.json5`` uses JSON5,
    ``.json`` uses strict JSON, and ``.yaml`` / ``.yml`` use YAML. Unknown
    suffixes are parsed as JSON5.

    Args:
        config_path: Path to the configuration file.

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

    suffix = config_path.suffix.casefold()
    format_name, parser = _parser_for_suffix(suffix)

    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            configuration = parser(config_file)
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
    except (ValueError, yaml.YAMLError) as exc:
        raise ConfigurationError(
            f"Invalid {format_name} syntax in '{config_path}': {exc}"
        ) from exc

    if not isinstance(configuration, dict):
        raise ConfigurationError("The top-level configuration value must be an object.")

    return configuration


def _parser_for_suffix(
    suffix: str,
) -> tuple[str, Callable[[IO[str]], Any]]:
    """
    Return the format name and parser for a configuration suffix.

    Args:
        suffix: Filename suffix including the leading dot.

    Returns:
        Format name and a callable that parses an open text file.

    """

    if suffix in {".yaml", ".yml"}:
        return "YAML", yaml.safe_load

    if suffix == ".json":
        return "JSON", json.load

    return "JSON5", json5.load
