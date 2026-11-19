"""
Command implementations for Lupaxa GitHub Repository Sync.

This module contains the application behaviour invoked by the command-line
interface. Argument parsing remains in cli.py, allowing command functions to
be called directly from tests or other Python code.
"""

from __future__ import annotations

from pathlib import Path
from typing import cast

from .constants import (
    DEFAULT_WORKER_COUNT,
    EXIT_CONFIGURATION_ERROR,
    EXIT_FAILURE,
    EXIT_SUCCESS,
)
from .display import (
    print_completion_summary,
    print_configuration_summary,
    print_error,
    print_info,
    print_program_header,
    print_repository_failure,
    print_repository_result,
    print_section,
    print_status_check,
    print_success,
    print_system,
    print_warning,
)
from .exceptions import (
    ConfigurationError,
    RepositorySyncError,
)
from .loader import (
    configuration_repository_status_message,
    load_configuration,
    refresh_default_configuration_repository,
    select_configuration_path,
)
from .models import (
    CloneProtocol,
    RepositoryInspection,
    RepositoryResult,
    RepositoryResultStatus,
    RepositoryStatusCheckStatus,
    ValidatedConfiguration,
)
from .progress import (
    advance_overall_repository,
    finish_overall_progress,
    repository_progress,
    set_overall_repository,
)
from .status import (
    RepositoryStatusResult,
    collect_repository_statuses,
)
from .synchronisation import (
    build_result,
    count_results,
    synchronisation_succeeded,
    synchronise_repositories,
    without_repository_path,
)
from .tables import (
    print_configuration_table,
    print_failure_summary_table,
    print_failure_table,
    print_repository_results_table,
    print_status_results_table,
    print_status_summary_table,
    print_summary_table,
)
from .utils import (
    count_repositories,
    resolve_path,
)
from .validation import validate_configuration


def load_and_validate_configuration(
    config_path: Path,
) -> ValidatedConfiguration:
    """
    Load and validate an application configuration file.

    Args:
        config_path:
            Path to the YAML, JSON, or JSON5 configuration file.

    Returns:
        Validated and normalised configuration.

    Raises:
        ConfigurationError:
            If the configuration cannot be loaded or is invalid.

    """

    resolved_config_path = select_configuration_path(config_path)
    raw_configuration = load_configuration(resolved_config_path)

    return validate_configuration(raw_configuration)


def run_sync(
    *,
    config_path: Path,
    show_header: bool = True,
    show_configuration: bool = True,
    show_configuration_table: bool = False,
    show_progress: bool = True,
    show_repository_output: bool = True,
    show_results_table: bool = False,
    show_failure_table: bool = True,
    show_summary_table: bool = True,
    recover_rewritten_history: bool = False,
    workers: int | None = None,
) -> int:
    """
    Synchronise repositories from a configuration file.

    Args:
        config_path:
            Path to the YAML, JSON, or JSON5 configuration file.
        show_header:
            Print the application heading.
        show_configuration:
            Print the validated configuration summary.
        show_configuration_table:
            Print every configured repository before synchronisation.
        show_progress:
            Display the Rich repository progress bar.
        show_repository_output:
            Print one final status line per repository.
        show_results_table:
            Print the detailed repository results table.
        show_failure_table:
            Print detailed failed repository results.
        show_summary_table:
            Print the final Rich summary table.
        recover_rewritten_history:
            Reset a clean local branch onto rewritten remote history.
        workers:
            Maximum number of repositories processed at once.

    Returns:
        Process exit code.

    """

    resolved_config_path = resolve_path(config_path)

    if show_header:
        print_program_header()

    refresh_result = refresh_default_configuration_repository(resolved_config_path)

    try:
        configuration = load_and_validate_configuration(resolved_config_path)
    except ConfigurationError as exc:
        print_error(str(exc))
        return EXIT_CONFIGURATION_ERROR

    if refresh_result is not None:
        configuration = without_repository_path(
            configuration,
            Path(refresh_result["path"]),
        )

    if show_configuration:
        _print_configuration_summary(
            configuration=configuration,
            config_path=resolved_config_path,
        )

    if show_configuration_table:
        print_section("Synchronisation Plan")

        print_configuration_table(
            organisations=configuration["organisations"],
        )

    result_callback = _print_repository_result if show_repository_output else None
    configuration_result = _configuration_sync_result(refresh_result)

    if configuration_result is not None and result_callback is not None:
        result_callback(configuration_result)

    try:
        results = synchronise_repositories(
            configuration=configuration,
            recover_rewritten_history=recover_rewritten_history,
            workers=DEFAULT_WORKER_COUNT if workers is None else workers,
            show_progress=show_progress,
            result_callback=result_callback,
            already_completed=(
                (configuration_result,) if configuration_result is not None else ()
            ),
        )
    except RepositorySyncError as exc:
        print_error(str(exc))
        return EXIT_FAILURE
    except KeyboardInterrupt:
        print_system("Synchronisation interrupted by the user.")
        return EXIT_FAILURE

    if configuration_result is not None:
        results = [configuration_result, *results]

    _print_sync_output(
        results=results,
        show_results_table=show_results_table,
        show_failure_table=show_failure_table,
        show_summary_table=show_summary_table,
    )

    if synchronisation_succeeded(results):
        return EXIT_SUCCESS

    return EXIT_FAILURE


def run_status(
    *,
    config_path: Path,
    show_header: bool = True,
    ignore_clean: bool = False,
    offline: bool = False,
    show_progress: bool = True,
    show_repository_output: bool = True,
    show_results_table: bool = False,
    show_summary_table: bool = True,
    workers: int | None = None,
) -> int:
    """Check configured repositories for clean, synchronised working trees."""

    resolved_config_path = resolve_path(config_path)

    if show_header:
        print_program_header()

    try:
        configuration = load_and_validate_configuration(resolved_config_path)
    except ConfigurationError as exc:
        print_error(str(exc))
        return EXIT_CONFIGURATION_ERROR

    mode = "offline" if offline else "online"
    print_section(f"Status check ({mode})")
    configuration_status = _configuration_status_result(
        configuration_repository_status_message(
            resolved_config_path,
            offline=offline,
        ),
    )

    if configuration_status is not None:
        configuration = without_repository_path(
            configuration,
            Path(configuration_status["path"]),
        )

        if show_repository_output and not (
            ignore_clean and configuration_status["status"] == "clean"
        ):
            print_status_check(
                configuration_status["status"],
                configuration_status["organisation"],
                configuration_status["repository"],
                message=configuration_status["message"],
                path=Path(configuration_status["path"]),
            )

    total_repositories = count_repositories(configuration)

    if configuration_status is not None:
        total_repositories += 1

    try:
        with repository_progress(
            total=total_repositories,
            action="CHECK",
            detail="Checking repository status.",
            disable=not show_progress,
        ) as (progress, progress_task):
            if configuration_status is not None:
                set_overall_repository(
                    progress,
                    progress_task,
                    action="CHECKED",
                    organisation_name=configuration_status["organisation"],
                    repository_name=configuration_status["repository"],
                    detail=configuration_status["message"],
                )
                advance_overall_repository(
                    progress,
                    progress_task,
                    detail=configuration_status["message"],
                )

            def handle_result(result: RepositoryStatusResult) -> None:
                set_overall_repository(
                    progress,
                    progress_task,
                    action="CHECKED",
                    organisation_name=result["organisation"],
                    repository_name=result["repository"],
                    detail=result["message"],
                )

                if show_repository_output and not (
                    ignore_clean and result["status"] == "clean"
                ):
                    print_status_check(
                        result["status"],
                        result["organisation"],
                        result["repository"],
                        message=result["message"],
                        path=Path(result["path"]),
                    )

                advance_overall_repository(
                    progress,
                    progress_task,
                    detail=result["message"],
                )

            results = collect_repository_statuses(
                configuration,
                offline=offline,
                workers=DEFAULT_WORKER_COUNT if workers is None else workers,
                result_callback=handle_result,
            )

            if configuration_status is not None:
                results = [configuration_status, *results]

            clean_count = sum(result["status"] == "clean" for result in results)
            finish_overall_progress(
                progress,
                progress_task,
                detail=(
                    f"{clean_count} clean, {len(results) - clean_count} not clean."
                ),
            )
    except RepositorySyncError as exc:
        print_error(str(exc))
        return EXIT_FAILURE
    except KeyboardInterrupt:
        print_system("Status check interrupted by the user.")
        return EXIT_FAILURE

    displayed_results = [
        result
        for result in results
        if not (ignore_clean and result["status"] == "clean")
    ]

    if show_results_table:
        print_section("Results")
        print_status_results_table(displayed_results)

    print_section("Summary")

    if show_summary_table:
        print_status_summary_table(results)
    else:
        clean_count = sum(result["status"] == "clean" for result in results)
        print_info(f"Clean: {clean_count}  Not clean: {len(results) - clean_count}")

    if all(result["status"] == "clean" for result in results):
        print_success("All configured repositories are clean and synchronised.")
        return EXIT_SUCCESS

    print_warning("One or more configured repositories are not clean.")
    return EXIT_FAILURE


def run_validate(
    *,
    config_path: Path,
    show_header: bool = True,
) -> int:
    """
    Validate a repository synchronisation configuration.

    The configuration is loaded, validated, and normalised. No Git commands
    are executed and no repository filesystem modifications are performed.

    Args:
        config_path:
            Path to the YAML, JSON, or JSON5 configuration file.
        show_header:
            Print the application heading.

    Returns:
        Process exit code.

    """

    resolved_config_path = resolve_path(config_path)

    if show_header:
        print_program_header()

    try:
        configuration = load_and_validate_configuration(resolved_config_path)
    except ConfigurationError as exc:
        print_error(str(exc))
        return EXIT_CONFIGURATION_ERROR

    print_section("Validation")

    print_info(f"Configuration file: {config_path}")

    print_success("Configuration is valid.")

    print_info(f"Organisations: {len(configuration['organisations'])}")

    print_info(f"Repositories: {count_repositories(configuration)}")

    return EXIT_SUCCESS


def run_plan(
    *,
    config_path: Path,
    show_header: bool = True,
) -> int:
    """
    Display the resolved repository synchronisation plan.

    The plan includes the effective clone protocol and local destination for
    every configured repository. No Git commands are executed and no
    repository filesystem modifications are performed.

    Args:
        config_path:
            Path to the YAML, JSON, or JSON5 configuration file.
        show_header:
            Print the application heading.

    Returns:
        Process exit code.

    """

    resolved_config_path = resolve_path(config_path)

    if show_header:
        print_program_header()

    try:
        configuration = load_and_validate_configuration(resolved_config_path)
    except ConfigurationError as exc:
        print_error(str(exc))
        return EXIT_CONFIGURATION_ERROR

    _print_configuration_summary(
        configuration=configuration,
        config_path=resolved_config_path,
    )

    print_section("Synchronisation Plan")

    print_configuration_table(
        organisations=configuration["organisations"],
    )

    return EXIT_SUCCESS


def _print_configuration_summary(
    *,
    configuration: ValidatedConfiguration,
    config_path: Path,
) -> None:
    """
    Print the common validated configuration summary.

    Args:
        configuration:
            Validated application configuration.
        config_path:
            Resolved configuration file path.

    """

    print_configuration_summary(
        config_path=config_path,
        clone_protocol=configuration["config"]["clone_protocol"],
        organisation_count=len(configuration["organisations"]),
        repository_count=count_repositories(configuration),
    )


def _configuration_sync_result(
    refresh_result: dict[str, str] | None,
) -> RepositoryResult | None:
    """Turn a configuration-repository update into a normal sync result."""

    if refresh_result is None:
        return None

    clone_protocol: CloneProtocol = (
        "https" if refresh_result["clone_protocol"] == "https" else "ssh"
    )

    return build_result(
        organisation_name=refresh_result["organisation"],
        repository_name=refresh_result["repository"],
        local_name=refresh_result["repository"],
        repository_path=Path(refresh_result["path"]),
        clone_protocol=clone_protocol,
        action="updated" if refresh_result["result"] == "success" else "skipped",
        result_status=cast(RepositoryResultStatus, refresh_result["result"]),
        message=refresh_result["message"],
    )


def _configuration_status_result(
    status_result: dict[str, str | int] | None,
) -> RepositoryStatusResult | None:
    """Turn a configuration-repository inspection into a normal status result."""

    if status_result is None:
        return None

    return {
        "organisation": str(status_result["organisation"]),
        "repository": str(status_result["repository"]),
        "path": str(status_result["path"]),
        "status": cast(RepositoryStatusCheckStatus, status_result["status"]),
        "message": str(status_result["message"]),
        "ahead": int(status_result["ahead"]),
        "behind": int(status_result["behind"]),
    }


def _print_repository_result(
    result: RepositoryResult,
) -> None:
    """
    Print one completed repository result.

    Args:
        result:
            Repository synchronisation result.

    """

    repository_path = Path(result["path"])

    result_status = result["result"]

    if result_status == "failed":
        print_repository_failure(
            status=result_status,
            organisation_name=result["organisation"],
            repository_name=result["repository"],
            message=result["message"],
            path=repository_path,
        )
        return

    print_repository_result(
        status=result_status,
        organisation_name=result["organisation"],
        repository_name=result["repository"],
        message=result["message"],
        path=repository_path,
    )


def _print_sync_output(
    *,
    results: list[RepositoryResult],
    show_results_table: bool,
    show_failure_table: bool,
    show_summary_table: bool,
) -> None:
    """
    Print final synchronisation output.

    Args:
        results:
            Repository synchronisation results.
        show_results_table:
            Print all detailed repository results.
        show_failure_table:
            Print detailed failed repository results.
        show_summary_table:
            Print the Rich summary table.

    """

    counts = count_results(results)

    if show_results_table:
        print_section("Results")

        print_repository_results_table(results)

    if show_failure_table and counts["failed"]:
        print_section("Failures")

        print_failure_table(results)

        print_failure_summary_table(results)

    print_section("Summary")

    if show_summary_table:
        print_summary_table(results)

    print_completion_summary(
        total=counts["total"],
        cloned=counts["cloned"],
        updated=counts["updated"],
        skipped=counts["skipped"],
        failed=counts["failed"],
        show_totals=not show_summary_table,
    )


def inspection_to_dict(
    inspection: RepositoryInspection,
) -> dict[str, object]:
    """
    Convert a repository inspection into a plain dictionary.

    This helper provides a stable extension point for future structured
    output formats such as JSON without coupling those formats to TypedDict
    internals.

    Args:
        inspection:
            Repository inspection result.

    Returns:
        Plain dictionary containing the inspection fields.

    """

    return {
        "status": inspection["status"],
        "message": inspection["message"],
    }


def print_command_start(
    command_name: str,
) -> None:
    """
    Print a compact command start message.

    Args:
        command_name:
            Command being executed.

    """

    print_info(f"Running command: {command_name}")
