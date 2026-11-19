"""
Configuration loading for Lupaxa GitHub Repository Sync.

This module locates and loads a YAML, JSON, or JSON5 configuration file.
Structural validation is performed separately by the validation module.
"""

from __future__ import annotations

from collections.abc import Callable
import json
from pathlib import Path
from typing import IO, Any

import json5
import yaml

from .constants import (
    DEFAULT_CONFIG_BASENAME,
    DEFAULT_CONFIG_DIRECTORY,
    DEFAULT_CONFIG_DIRECTORY_BASENAME,
    DEFAULT_CONFIG_EXTENSIONS,
    DEFAULT_CONFIG_FILENAME,
    DEFAULT_CONFIG_HOME,
)
from .exceptions import ConfigurationError
from .utils import resolve_path


def _configuration_candidates(directory: Path, basename: str) -> list[Path]:
    """
    Build the configuration filenames for one directory.

    Args:
        directory: Directory to search.
        basename: Filename without an extension.

    Returns:
        Candidates in extension order: ``.yaml``, ``.yml``, ``.json``,
        ``.json5``.

    """

    return [
        directory / f"{basename}{extension}" for extension in DEFAULT_CONFIG_EXTENSIONS
    ]


def resolve_default_configuration_path(
    search_dir: Path | None = None,
) -> Path:
    """
    Find the default configuration file.

    When no directory is given, ``~/.config/github-repo-sync`` is searched
    for ``github-repo-sync.yaml``, then ``.yml``, ``.json``, and ``.json5``.
    The home directory is searched next for the same names with a leading
    dot. A single directory is searched for the hidden names only.

    Args:
        search_dir:
            Directory to search for hidden configuration names. Defaults to
            ``~/.config/github-repo-sync`` and then the home directory.

    Returns:
        Path of the first matching configuration file.

    Raises:
        ConfigurationError:
            If none of the default configuration filenames exist.

    """

    if search_dir is None:
        candidates = [
            *_configuration_candidates(
                DEFAULT_CONFIG_DIRECTORY,
                DEFAULT_CONFIG_DIRECTORY_BASENAME,
            ),
            *_configuration_candidates(
                DEFAULT_CONFIG_HOME,
                DEFAULT_CONFIG_BASENAME,
            ),
        ]
    else:
        candidates = _configuration_candidates(
            search_dir,
            DEFAULT_CONFIG_BASENAME,
        )

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    listed = ", ".join(str(candidate) for candidate in candidates)
    raise ConfigurationError(f"Configuration file does not exist: {listed}")


def select_configuration_path(config_path: Path) -> Path:
    """
    Resolve the configuration file that should be loaded.

    An explicit file is used as given. When the default
    ``~/.config/github-repo-sync/github-repo-sync.yaml`` is missing, the
    remaining names in that directory are tried, then the hidden names in
    the home directory. Any other missing ``.github-repo-sync.yaml`` falls
    back to the other hidden extensions in that same directory.

    Args:
        config_path: Requested configuration path.

    Returns:
        Configuration file to load.

    Raises:
        ConfigurationError:
            If a default-name lookup finds no configuration file.

    """

    resolved_config_path = resolve_path(config_path)

    if resolved_config_path.is_file():
        return resolved_config_path

    if resolved_config_path == resolve_path(DEFAULT_CONFIG_FILENAME):
        return resolve_default_configuration_path()

    if resolved_config_path.name != f"{DEFAULT_CONFIG_BASENAME}.yaml":
        return resolved_config_path

    return resolve_default_configuration_path(resolved_config_path.parent)


def load_configuration(config_path: Path) -> dict[str, Any]:
    """
    Load a YAML, JSON, or JSON5 configuration file.

    The parser is selected from the filename suffix. ``.yaml`` / ``.yml`` use
    YAML, ``.json`` uses strict JSON, and ``.json5`` uses JSON5. Unknown
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
