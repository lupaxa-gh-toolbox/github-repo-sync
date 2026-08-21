"""
Repository synchronisation orchestration.

This module coordinates repository inspection, cloning, and updating. It
contains no command-line parsing and only limited presentation logic, allowing
the synchronisation behaviour to be reused by the CLI and future tests.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

from .exceptions import RepositorySyncError
from .git_operations import (
    build_clone_url,
    clone_repository,
    ensure_directory,
    ensure_git_available,
    inspect_repository,
    update_repository,
)
from .models import (
    CloneProtocol,
    OrganisationConfiguration,
    RepositoryAction,
    RepositoryConfiguration,
    RepositoryInspection,
    RepositoryResult,
    RepositoryResultStatus,
    ValidatedConfiguration,
)
from .progress import (
    advance_overall_repository,
    finish_overall_progress,
    repository_progress,
    set_overall_repository,
)
from .utils import count_repositories

ResultCallback = Callable[[RepositoryResult], None]

InspectionCallback = Callable[
    [
        str,
        str,
        Path,
        RepositoryInspection,
    ],
    None,
]


def build_repository_path(
    clone_path: Path,
    organisation: OrganisationConfiguration,
    repository: RepositoryConfiguration,
) -> Path:
    """
    Build the local destination for a configured repository.

    Args:
        clone_path: Root clone directory.
        organisation: Organisation configuration.
        repository: Repository configuration.

    Returns:
        Repository destination path.

    """

    return (
        clone_path / organisation["destination_name"] / repository["destination_name"]
    )


def build_result(
    *,
    organisation_name: str,
    repository_name: str,
    local_name: str,
    repository_path: Path,
    clone_protocol: CloneProtocol,
    action: RepositoryAction,
    result_status: RepositoryResultStatus,
    message: str,
) -> RepositoryResult:
    """
    Construct a repository result.

    Args:
        organisation_name: GitHub organisation name.
        repository_name: GitHub repository name.
        local_name: Local repository directory name.
        repository_path: Local repository destination.
        clone_protocol: Clone protocol used for the repository.
        action: Action performed by the synchroniser.
        result_status: Outcome of the synchronisation attempt.
        message: Result explanation.

    Returns:
        Repository result.

    """

    return {
        "organisation": organisation_name,
        "repository": repository_name,
        "local_name": local_name,
        "path": str(repository_path),
        "clone_protocol": clone_protocol,
        "action": action,
        "result": result_status,
        "message": message,
    }


def synchronise_repository(
    *,
    organisation: OrganisationConfiguration,
    repository: RepositoryConfiguration,
    clone_path: Path,
    recover_rewritten_history: bool = False,
    inspection_callback: InspectionCallback | None = None,
) -> RepositoryResult:
    """
    Synchronise one configured repository.

    A missing destination is cloned. An existing valid repository is fetched
    and fast-forwarded. Repositories with local changes, rewritten remote
    history, invalid remotes, or other unsafe states are skipped and reported
    without modification unless rewritten history recovery is enabled.

    Args:
        organisation: Parent organisation configuration.
        repository: Repository configuration.
        clone_path: Root clone directory.
        recover_rewritten_history:
            Reset a clean local branch onto rewritten remote history.
        inspection_callback:
            Optional callback invoked after repository inspection.

    Returns:
        Repository result.

    """

    organisation_name = organisation["name"]
    repository_name = repository["name"]
    local_name = repository["destination_name"]
    clone_protocol = repository["clone_protocol"]

    repository_path = build_repository_path(
        clone_path=clone_path,
        organisation=organisation,
        repository=repository,
    )

    inspection = inspect_repository(
        repository_path=repository_path,
        expected_organisation=organisation_name,
        expected_repository=repository_name,
    )

    if inspection_callback is not None:
        inspection_callback(
            organisation_name,
            repository_name,
            repository_path,
            inspection,
        )

    inspection_status = inspection["status"]

    if inspection_status == "clone":
        clone_url = build_clone_url(
            organisation_name=organisation_name,
            repository_name=repository_name,
            clone_protocol=clone_protocol,
        )

        try:
            clone_repository(
                clone_url=clone_url,
                repository_path=repository_path,
            )
        except RepositorySyncError as exc:
            return build_result(
                organisation_name=organisation_name,
                repository_name=repository_name,
                local_name=local_name,
                repository_path=repository_path,
                clone_protocol=clone_protocol,
                action="skipped",
                result_status=exc.result,
                message=str(exc),
            )

        return build_result(
            organisation_name=organisation_name,
            repository_name=repository_name,
            local_name=local_name,
            repository_path=repository_path,
            clone_protocol=clone_protocol,
            action="cloned",
            result_status="success",
            message=f"Cloned using {clone_protocol.upper()}.",
        )

    if inspection_status == "update":
        try:
            outcome = update_repository(
                repository_path=repository_path,
                expected_organisation=organisation_name,
                expected_repository=repository_name,
                recover_rewritten_history=recover_rewritten_history,
            )
        except RepositorySyncError as exc:
            return build_result(
                organisation_name=organisation_name,
                repository_name=repository_name,
                local_name=local_name,
                repository_path=repository_path,
                clone_protocol=clone_protocol,
                action="skipped",
                result_status=exc.result,
                message=str(exc),
            )

        if outcome == "reset-rewritten":
            message = "Reset local branch to rewritten upstream history."
        else:
            message = "Fetched and fast-forwarded from the upstream branch."

        return build_result(
            organisation_name=organisation_name,
            repository_name=repository_name,
            local_name=local_name,
            repository_path=repository_path,
            clone_protocol=clone_protocol,
            action="updated",
            result_status="success",
            message=message,
        )

    return build_result(
        organisation_name=organisation_name,
        repository_name=repository_name,
        local_name=local_name,
        repository_path=repository_path,
        clone_protocol=clone_protocol,
        action="skipped",
        result_status=inspection_status,
        message=inspection["message"],
    )


def synchronise_organisation(
    *,
    organisation: OrganisationConfiguration,
    clone_path: Path,
    recover_rewritten_history: bool = False,
    inspection_callback: InspectionCallback | None = None,
    result_callback: ResultCallback | None = None,
) -> list[RepositoryResult]:
    """
    Synchronise every configured repository in one organisation.

    Args:
        organisation: Organisation configuration.
        clone_path: Root clone directory.
        recover_rewritten_history:
            Reset a clean local branch onto rewritten remote history.
        inspection_callback:
            Optional callback invoked after each inspection.
        result_callback:
            Optional callback invoked after each final result.

    Returns:
        Repository results.

    """

    organisation_path = clone_path / organisation["destination_name"]

    try:
        ensure_directory(
            organisation_path,
            "Organisation directory",
        )
    except RepositorySyncError as exc:
        skipped_results: list[RepositoryResult] = []

        for repository in organisation["repositories"]:
            repository_path = build_repository_path(
                clone_path=clone_path,
                organisation=organisation,
                repository=repository,
            )

            result = build_result(
                organisation_name=organisation["name"],
                repository_name=repository["name"],
                local_name=repository["destination_name"],
                repository_path=repository_path,
                clone_protocol=repository["clone_protocol"],
                action="skipped",
                result_status=exc.result,
                message=str(exc),
            )

            skipped_results.append(result)

            if result_callback is not None:
                result_callback(result)

        return skipped_results

    results: list[RepositoryResult] = []

    for repository in organisation["repositories"]:
        result = synchronise_repository(
            organisation=organisation,
            repository=repository,
            clone_path=clone_path,
            recover_rewritten_history=recover_rewritten_history,
            inspection_callback=inspection_callback,
        )

        results.append(result)

        if result_callback is not None:
            result_callback(result)

    return results


def synchronise_repositories(
    *,
    configuration: ValidatedConfiguration,
    recover_rewritten_history: bool = False,
    show_progress: bool = True,
    inspection_callback: InspectionCallback | None = None,
    result_callback: ResultCallback | None = None,
) -> list[RepositoryResult]:
    """
    Synchronise all repositories in a validated configuration.

    Args:
        configuration: Validated application configuration.
        recover_rewritten_history:
            Reset a clean local branch onto rewritten remote history.
        show_progress: Display the Rich overall progress bar.
        inspection_callback:
            Optional callback invoked after each inspection.
        result_callback:
            Optional callback invoked after each final result.

    Returns:
        Repository results.

    Raises:
        RepositorySyncError:
            If Git is unavailable or the root clone directory cannot be
            prepared.

    """

    ensure_git_available()

    clone_path = Path(configuration["config"]["clone_path"])

    ensure_directory(
        clone_path,
        "Clone directory",
    )

    total_repositories = count_repositories(configuration)
    results: list[RepositoryResult] = []

    with repository_progress(
        total=total_repositories,
        action="SYNC",
        detail="Preparing repositories.",
        disable=not show_progress,
    ) as (progress, progress_task):
        for organisation in configuration["organisations"]:
            organisation_path = clone_path / organisation["destination_name"]

            try:
                ensure_directory(
                    organisation_path,
                    "Organisation directory",
                )
            except RepositorySyncError as exc:
                for repository in organisation["repositories"]:
                    repository_path = build_repository_path(
                        clone_path=clone_path,
                        organisation=organisation,
                        repository=repository,
                    )

                    set_overall_repository(
                        progress,
                        progress_task,
                        action="FAILED",
                        organisation_name=organisation["name"],
                        repository_name=repository["name"],
                        detail=str(exc),
                    )

                    result = build_result(
                        organisation_name=organisation["name"],
                        repository_name=repository["name"],
                        local_name=repository["destination_name"],
                        repository_path=repository_path,
                        clone_protocol=repository["clone_protocol"],
                        action="skipped",
                        result_status=exc.result,
                        message=str(exc),
                    )

                    results.append(result)

                    if result_callback is not None:
                        result_callback(result)

                    advance_overall_repository(
                        progress,
                        progress_task,
                        detail="Organisation directory unavailable.",
                    )

                continue

            for repository in organisation["repositories"]:
                set_overall_repository(
                    progress,
                    progress_task,
                    action="INSPECT",
                    organisation_name=organisation["name"],
                    repository_name=repository["name"],
                    detail="Inspecting local destination.",
                )

                result = synchronise_repository(
                    organisation=organisation,
                    repository=repository,
                    clone_path=clone_path,
                    recover_rewritten_history=recover_rewritten_history,
                    inspection_callback=inspection_callback,
                )

                results.append(result)

                if result_callback is not None:
                    result_callback(result)

                if result["result"] == "failed":
                    final_action = "FAILED"
                else:
                    final_action = {
                        "cloned": "CLONED",
                        "updated": "UPDATED",
                        "skipped": "SKIPPED",
                    }[result["action"]]

                set_overall_repository(
                    progress,
                    progress_task,
                    action=final_action,
                    organisation_name=organisation["name"],
                    repository_name=repository["name"],
                    detail=result["message"],
                )

                advance_overall_repository(
                    progress,
                    progress_task,
                    detail=result["message"],
                )

        finish_overall_progress(
            progress,
            progress_task,
            detail=_build_progress_completion_message(results),
        )

    return results


def _build_progress_completion_message(
    results: Sequence[RepositoryResult],
) -> str:
    """
    Build the final overall progress message.

    Args:
        results: Repository results.

    Returns:
        Compact completion summary.

    """

    cloned = sum(
        result["action"] == "cloned" and result["result"] == "success"
        for result in results
    )

    updated = sum(
        result["action"] == "updated" and result["result"] == "success"
        for result in results
    )

    skipped = sum(
        result["action"] == "skipped" and result["result"] != "failed"
        for result in results
    )

    failed = sum(result["result"] == "failed" for result in results)

    return f"{cloned} cloned, {updated} updated, {skipped} skipped, {failed} failed."


def synchronisation_succeeded(
    results: Sequence[RepositoryResult],
) -> bool:
    """
    Determine whether synchronisation completed without failures.

    Skipped repositories are not treated as application failures because they
    represent repositories intentionally left unchanged for safety.

    Args:
        results: Repository results.

    Returns:
        True when no repository failed.

    """

    return not any(result["result"] == "failed" for result in results)


def count_results(
    results: Sequence[RepositoryResult],
) -> dict[str, int]:
    """
    Count repository results by final action and outcome.

    Args:
        results: Repository results.

    Returns:
        Dictionary containing total, cloned, updated, skipped, and failed
        counts.

    """

    return {
        "total": len(results),
        "cloned": sum(
            result["action"] == "cloned" and result["result"] == "success"
            for result in results
        ),
        "updated": sum(
            result["action"] == "updated" and result["result"] == "success"
            for result in results
        ),
        "skipped": sum(
            result["action"] == "skipped" and result["result"] != "failed"
            for result in results
        ),
        "failed": sum(result["result"] == "failed" for result in results),
    }
