"""
General utility functions for Lupaxa GitHub Repository Sync.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TypeGuard

from .models import (
    RepositoryInspectionStatus,
    RepositoryProblemStatus,
    ValidatedConfiguration,
)


def is_repository_problem_status(
    status: RepositoryInspectionStatus,
) -> TypeGuard[RepositoryProblemStatus]:
    """
    Check whether an inspection status represents a repository problem.

    Args:
        status: Repository inspection status.

    Returns:
        True when the status can be used as a repository failure category.

    """

    return status not in {
        "clone",
        "update",
    }


def resolve_path(path: Path) -> Path:
    """
    Expand environment variables and the user's home directory.

    Args:
        path: Path to expand.

    Returns:
        Expanded path.

    """

    expanded_path = os.path.expandvars(str(path))
    return Path(expanded_path).expanduser()


def abbreviate_home_path(path: Path) -> str:
    """
    Replace the user's home directory with ~ for display purposes.

    Args:
        path: Path to format.

    Returns:
        Shortened display path where possible.

    """

    expanded_path = path.expanduser()
    home_path = Path.home()

    try:
        relative_path = expanded_path.relative_to(home_path)
    except ValueError:
        return str(expanded_path)

    if relative_path == Path("."):
        return "~"

    return str(Path("~") / relative_path)


def count_repositories(
    configuration: ValidatedConfiguration,
) -> int:
    """
    Count all configured repositories.

    Args:
        configuration: Validated configuration.

    Returns:
        Total repository count.

    """

    return sum(
        len(organisation["repositories"])
        for organisation in configuration["organisations"]
    )
