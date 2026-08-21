"""Repository status collection orchestration."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import TypedDict

from .git_operations import check_repository_status, ensure_git_available
from .models import RepositoryStatusCheckStatus, ValidatedConfiguration
from .synchronisation import build_repository_path


class RepositoryStatusResult(TypedDict):
    """Status check result for one configured repository."""

    organisation: str
    repository: str
    path: str
    status: RepositoryStatusCheckStatus
    message: str
    ahead: int
    behind: int


def collect_repository_statuses(
    configuration: ValidatedConfiguration,
    *,
    offline: bool = False,
    result_callback: Callable[[RepositoryStatusResult], None] | None = None,
) -> list[RepositoryStatusResult]:
    """Collect status checks for all repositories in a configuration."""

    ensure_git_available()
    results: list[RepositoryStatusResult] = []
    clone_path = Path(configuration["config"]["clone_path"])

    for organisation in configuration["organisations"]:
        for repository in organisation["repositories"]:
            path = build_repository_path(clone_path, organisation, repository)
            try:
                check = check_repository_status(
                    path,
                    organisation["name"],
                    repository["name"],
                    offline=offline,
                )
            except Exception as exc:
                check = {
                    "status": "inaccessible",
                    "message": (
                        f"Repository status check failed: {type(exc).__name__}: {exc}"
                    ),
                    "ahead": 0,
                    "behind": 0,
                }
            item: RepositoryStatusResult = {
                "organisation": organisation["name"],
                "repository": repository["name"],
                "path": str(path),
                "status": check["status"],
                "message": check["message"],
                "ahead": check["ahead"],
                "behind": check["behind"],
            }
            results.append(item)

            if result_callback is not None:
                result_callback(item)

    return results
