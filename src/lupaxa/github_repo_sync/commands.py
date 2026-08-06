"""
Command implementations for Lupaxa GitHub Repository Sync.

This module contains the application behaviour invoked by the command-line
interface. Argument parsing remains in cli.py, allowing command functions to
be called directly from tests or other Python code.
"""

from __future__ import annotations

from pathlib import Path

from .constants import (
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
    print_success,
)
from .exceptions import (
    ConfigurationError,
    RepositorySyncError,
)
from .loader import load_configuration
from .models import (
    RepositoryInspection,
    RepositoryResult,
    ValidatedConfiguration,
)
from .synchronisation import (
    count_results,
    synchronisation_succeeded,
    synchronise_repositories,
)
from .tables import (
    print_configuration_table,
    print_failure_summary_table,
    print_failure_table,
    print_repository_results_table,
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
            Path to the JSON5 configuration file.

    Returns:
        Validated and normalised configuration.

    Raises:
        ConfigurationError:
            If the configuration cannot be loaded or is invalid.

    """

    resolved_config_path = resolve_path(config_path)

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
) -> int:
    """
    Synchronise repositories from a configuration file.

    Args:
        config_path:
            Path to the JSON5 configuration file.
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

    clone_path = Path(configuration["config"]["clone_path"])

    if show_configuration:
        _print_configuration_summary(
            configuration=configuration,
            config_path=resolved_config_path,
            clone_path=clone_path,
        )

    if show_configuration_table:
        print_section("Synchronisation Plan")

        print_configuration_table(
            organisations=configuration["organisations"],
            clone_path=clone_path,
        )

    result_callback = _print_repository_result if show_repository_output else None

    try:
        results = synchronise_repositories(
            configuration=configuration,
            show_progress=show_progress,
            result_callback=result_callback,
        )
    except RepositorySyncError as exc:
        print_error(str(exc))
        return EXIT_FAILURE
    except KeyboardInterrupt:
        print_error("Synchronisation interrupted by the user.")
        return EXIT_FAILURE

    _print_sync_output(
        results=results,
        show_results_table=show_results_table,
        show_failure_table=show_failure_table,
        show_summary_table=show_summary_table,
    )

    if synchronisation_succeeded(results):
        return EXIT_SUCCESS

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
            Path to the JSON5 configuration file.
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
            Path to the JSON5 configuration file.
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

    clone_path = Path(configuration["config"]["clone_path"])

    _print_configuration_summary(
        configuration=configuration,
        config_path=resolved_config_path,
        clone_path=clone_path,
    )

    print_section("Synchronisation Plan")

    print_configuration_table(
        organisations=configuration["organisations"],
        clone_path=clone_path,
    )

    return EXIT_SUCCESS


def _print_configuration_summary(
    *,
    configuration: ValidatedConfiguration,
    config_path: Path,
    clone_path: Path,
) -> None:
    """
    Print the common validated configuration summary.

    Args:
        configuration:
            Validated application configuration.
        config_path:
            Resolved configuration file path.
        clone_path:
            Resolved repository clone root.

    """

    print_configuration_summary(
        config_path=config_path,
        clone_path=clone_path,
        clone_protocol=configuration["config"]["clone_protocol"],
        organisation_count=len(configuration["organisations"]),
        repository_count=count_repositories(configuration),
    )


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
