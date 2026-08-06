"""
Project-wide constants for Lupaxa GitHub Repository Sync.

This module contains stable values shared across the application. Runtime
configuration, command-line arguments, and Rich presentation styles belong in
their respective modules.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

__all__ = [
    "CLONE_PROTOCOL_HTTPS",
    "CLONE_PROTOCOL_SSH",
    "DEFAULT_CONFIG_FILENAME",
    "DEFAULT_CONSOLE_WIDTH",
    "DEFAULT_REMOTE_NAME",
    "EXIT_CANCELLED",
    "EXIT_CONFIGURATION_ERROR",
    "EXIT_FAILURE",
    "EXIT_REPOSITORY_ERROR",
    "EXIT_SUCCESS",
    "EXIT_SYNC_INCOMPLETE",
    "GITHUB_HOSTNAME",
    "GITHUB_HTTPS_BASE_URL",
    "GITHUB_SSH_USER",
    "MAX_CONSOLE_WIDTH",
    "MIN_CONSOLE_WIDTH",
    "PROGRAM_ALIAS",
    "PROGRAM_NAME",
    "PROGRAM_VERSION",
    "PROGRAM_VERSION_STRING",
    "PROJECT_NAME",
    "SUPPORTED_CLONE_PROTOCOLS",
]

PROGRAM_NAME: Final[str] = "github-repo-sync"
PROGRAM_ALIAS: Final[str] = "grs"
PROJECT_NAME: Final[str] = "lupaxa-github-repo-sync"
PROGRAM_VERSION: Final[str] = "v0.1.0"
PROGRAM_VERSION_STRING: Final[str] = f"{PROGRAM_NAME} {PROGRAM_VERSION}"

DEFAULT_CONFIG_FILENAME: Final[Path] = Path.home() / ".github-repo-sync.json5"

DEFAULT_CONSOLE_WIDTH: Final[int] = 180
MIN_CONSOLE_WIDTH: Final[int] = 80
MAX_CONSOLE_WIDTH: Final[int] = 300

GITHUB_HOSTNAME: Final[str] = "github.com"
GITHUB_HTTPS_BASE_URL: Final[str] = f"https://{GITHUB_HOSTNAME}"
GITHUB_SSH_USER: Final[str] = "git"

DEFAULT_REMOTE_NAME: Final[str] = "origin"

CLONE_PROTOCOL_HTTPS: Final[str] = "https"
CLONE_PROTOCOL_SSH: Final[str] = "ssh"

SUPPORTED_CLONE_PROTOCOLS: Final[frozenset[str]] = frozenset(
    {
        CLONE_PROTOCOL_HTTPS,
        CLONE_PROTOCOL_SSH,
    }
)

EXIT_SUCCESS: Final[int] = 0
EXIT_FAILURE: Final[int] = 1
EXIT_SYNC_INCOMPLETE: Final[int] = 2
EXIT_CONFIGURATION_ERROR: Final[int] = 3
EXIT_REPOSITORY_ERROR: Final[int] = 4
EXIT_CANCELLED: Final[int] = 130
