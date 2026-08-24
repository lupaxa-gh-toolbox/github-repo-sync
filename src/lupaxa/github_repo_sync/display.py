"""
Console presentation helpers for Lupaxa GitHub Repository Sync.

This module contains the high-level Rich console functions used to present
application headings, informational messages, repository actions, warnings,
errors, and completion summaries.

Rich tables and progress displays are implemented separately by the tables
and progress modules.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import TextIO

from rich.console import Console
from rich.markup import escape
from rich.text import Text

from .constants import (
    DEFAULT_CONSOLE_WIDTH,
    MAX_CONSOLE_WIDTH,
    MIN_CONSOLE_WIDTH,
    PROGRAM_ALIAS,
    PROGRAM_NAME,
)
from .models import (
    RepositoryAction,
    RepositoryFailureStatus,
    RepositoryInspectionStatus,
    RepositoryResultStatus,
    RepositoryStatusCheckStatus,
)
from .styles import (
    LABEL_ERROR,
    LABEL_INFORMATION,
    LABEL_SUCCESS,
    LABEL_SYSTEM,
    LABEL_WARNING,
    REPOSITORY_ACTION_LABELS,
    REPOSITORY_ACTION_STYLES,
    REPOSITORY_INSPECTION_LABELS,
    REPOSITORY_INSPECTION_STYLES,
    REPOSITORY_RESULT_LABELS,
    REPOSITORY_RESULT_STYLES,
    REPOSITORY_STATUS_CHECK_LABELS,
    REPOSITORY_STATUS_CHECK_STYLES,
    STYLE_DETAIL_LABEL,
    STYLE_ERROR,
    STYLE_HEADING,
    STYLE_INFORMATION,
    STYLE_MUTED,
    STYLE_PATH,
    STYLE_REPOSITORY,
    STYLE_RULE_PRIMARY,
    STYLE_SUCCESS,
    STYLE_SUMMARY_CLONED,
    STYLE_SUMMARY_FAILED,
    STYLE_SUMMARY_SKIPPED,
    STYLE_SUMMARY_UPDATED,
    STYLE_SYSTEM,
    STYLE_WARNING,
)
from .utils import abbreviate_home_path


def create_console(
    *,
    width: int | None = None,
    file: TextIO | None = None,
    no_colour: bool = False,
    force_terminal: bool | None = None,
) -> Console:
    """
    Create the Rich console used by the application.

    The application default width is used when no explicit width is supplied.
    Explicit and default widths are constrained to the supported application
    range.

    Args:
        width:
            Optional explicit console width. When omitted, the application
            default console width is used.
        file:
            Optional output stream.
        no_colour:
            Disable colour output.
        force_terminal:
            Explicitly enable or disable terminal behaviour.

    Returns:
        Configured Rich console.

    """

    effective_width = DEFAULT_CONSOLE_WIDTH if width is None else width

    effective_width = max(
        MIN_CONSOLE_WIDTH,
        min(
            effective_width,
            MAX_CONSOLE_WIDTH,
        ),
    )

    return Console(
        file=file,
        width=effective_width,
        color_system=None if no_colour else "auto",
        force_terminal=force_terminal,
        soft_wrap=False,
    )


console = create_console()


def configure_console(
    *,
    width: int | None = None,
    file: TextIO | None = None,
    no_colour: bool = False,
    force_terminal: bool | None = None,
) -> Console:
    """
    Replace the module-level console.

    This allows the CLI to apply command-line presentation options before any
    application output is produced.

    Args:
        width: Optional explicit console width.
        file: Optional output stream.
        no_colour: Disable colour output.
        force_terminal: Explicitly enable or disable terminal behaviour.

    Returns:
        Newly configured console.

    """

    global console

    console = create_console(
        width=width,
        file=file,
        no_colour=no_colour,
        force_terminal=force_terminal,
    )

    return console


def get_command_name() -> str:
    """
    Return the executable name used to launch the application.

    Returns:
        Executable name, such as ``github-repo-sync`` or ``grs``.

    """

    if not sys.argv:
        return PROGRAM_ALIAS

    executable_name = Path(sys.argv[0]).name.strip()

    if not executable_name or executable_name in {
        "-c",
        "__main__.py",
    }:
        return PROGRAM_ALIAS

    if executable_name.startswith("python"):
        return f"python -m {PROGRAM_NAME}"

    return executable_name


def print_program_header() -> None:
    """
    Print the application heading.
    """

    console.print()

    console.rule(
        Text(
            PROGRAM_NAME,
            style=STYLE_HEADING,
        ),
        style=STYLE_RULE_PRIMARY,
    )

    console.print(
        Text(
            f"Command: {get_command_name()}",
            style=STYLE_MUTED,
        ),
        justify="center",
    )

    console.print()


def print_section(
    title: str,
) -> None:
    """
    Print a section rule.

    Args:
        title: Section title.

    """

    console.print()

    console.rule(
        Text(
            title,
            style=STYLE_HEADING,
        ),
        style=STYLE_RULE_PRIMARY,
    )


def print_blank_line() -> None:
    """
    Print one blank line.
    """

    console.print()


def format_bracket_label(label: str) -> str:
    """
    Format a console prompt label as ``[ <text> ]``.

    Args:
        label: Short label text.

    Returns:
        Label wrapped with spaced brackets.

    """

    return f"[ {label.strip()} ]"


def print_message(
    label: str,
    message: str,
    *,
    label_style: str,
    message_style: str | None = None,
) -> None:
    """
    Print a labelled console message.

    Args:
        label: Short message label.
        message: Message body.
        label_style: Rich style applied to the label.
        message_style: Optional Rich style applied to the message.

    """

    output = Text()

    output.append(
        format_bracket_label(label),
        style=label_style,
    )
    output.append(" ")
    output.append(
        message,
        style=message_style,
    )

    console.print(
        output,
        overflow="fold",
    )


def print_info(
    message: str,
) -> None:
    """
    Print an informational message.

    Args:
        message: Message body.

    """

    print_message(
        LABEL_INFORMATION,
        message,
        label_style=STYLE_INFORMATION,
    )


def print_success(
    message: str,
) -> None:
    """
    Print a success message.

    Args:
        message: Message body.

    """

    print_message(
        LABEL_SUCCESS,
        message,
        label_style=STYLE_SUCCESS,
    )


def print_warning(
    message: str,
) -> None:
    """
    Print a warning message.

    Args:
        message: Message body.

    """

    print_message(
        LABEL_WARNING,
        message,
        label_style=STYLE_WARNING,
    )


def print_error(
    message: str,
) -> None:
    """
    Print an error message.

    Args:
        message: Message body.

    """

    print_message(
        LABEL_ERROR,
        message,
        label_style=STYLE_ERROR,
    )


def print_system(
    message: str,
) -> None:
    """
    Print a system message.

    Used for user interrupts and other non-error process notices.

    Args:
        message: Message body.

    """

    print_message(
        LABEL_SYSTEM,
        message,
        label_style=STYLE_SYSTEM,
        message_style=STYLE_SYSTEM,
    )


def print_detail(
    label: str,
    value: object,
) -> None:
    """
    Print a labelled detail line.

    Args:
        label: Detail label.
        value: Detail value.

    """

    output = Text()

    output.append(
        f"{label}:",
        style=STYLE_DETAIL_LABEL,
    )
    output.append(" ")
    output.append(str(value))

    console.print(
        output,
        overflow="fold",
    )


def print_path_detail(
    label: str,
    path: Path,
) -> None:
    """
    Print a labelled filesystem path.

    The user's home directory is abbreviated with a tilde where possible.

    Args:
        label: Detail label.
        path: Filesystem path.

    """

    output = Text()

    output.append(
        f"{label}:",
        style=STYLE_DETAIL_LABEL,
    )
    output.append(" ")
    output.append(
        abbreviate_home_path(path),
        style=STYLE_PATH,
    )

    console.print(
        output,
        overflow="fold",
    )


def format_repository_name(
    organisation_name: str,
    repository_name: str,
) -> str:
    """
    Format a GitHub repository's full name.

    Args:
        organisation_name: GitHub organisation name.
        repository_name: GitHub repository name.

    Returns:
        Full repository name.

    """

    return f"{organisation_name}/{repository_name}"


def print_repository_message(
    label: str,
    organisation_name: str,
    repository_name: str,
    *,
    label_style: str,
    message: str | None = None,
    path: Path | None = None,
) -> None:
    """
    Print a labelled repository message.

    Repository details are kept on a compact first line. Longer paths or
    explanations are placed on indented continuation lines so output remains
    readable on narrower terminals.

    Args:
        label: Short action or status label.
        organisation_name: GitHub organisation name.
        repository_name: GitHub repository name.
        label_style: Rich style applied to the label.
        message: Optional explanatory message.
        path: Optional local repository path.

    """

    heading = Text()

    heading.append(
        format_bracket_label(label),
        style=label_style,
    )
    heading.append(" ")
    heading.append(
        format_repository_name(
            organisation_name,
            repository_name,
        ),
        style=STYLE_REPOSITORY,
    )

    console.print(
        heading,
        overflow="fold",
    )

    if path is not None:
        path_output = Text("    ")
        path_output.append(
            "Path:",
            style=STYLE_DETAIL_LABEL,
        )
        path_output.append(" ")
        path_output.append(
            abbreviate_home_path(path),
            style=STYLE_PATH,
        )

        console.print(
            path_output,
            overflow="fold",
        )

    if message:
        message_output = Text("    ")
        message_output.append(
            message,
            style=STYLE_MUTED,
        )

        console.print(
            message_output,
            overflow="fold",
        )


def print_repository_action(
    action: RepositoryAction,
    organisation_name: str,
    repository_name: str,
    *,
    path: Path | None = None,
    message: str | None = None,
) -> None:
    """
    Print a repository action.

    Args:
        action: Repository action.
        organisation_name: GitHub organisation name.
        repository_name: GitHub repository name.
        path: Optional local repository path.
        message: Optional explanatory message.

    """

    label = REPOSITORY_ACTION_LABELS[action]
    style = REPOSITORY_ACTION_STYLES[action]

    print_repository_message(
        label,
        organisation_name,
        repository_name,
        label_style=style,
        message=message,
        path=path,
    )


def print_inspection_status(
    status: RepositoryInspectionStatus,
    organisation_name: str,
    repository_name: str,
    *,
    message: str | None = None,
    path: Path | None = None,
) -> None:
    """
    Print a repository inspection status.

    Args:
        status: Inspection status.
        organisation_name: GitHub organisation name.
        repository_name: GitHub repository name.
        message: Optional status explanation.
        path: Optional local repository path.

    """

    label = REPOSITORY_INSPECTION_LABELS[status]
    style = REPOSITORY_INSPECTION_STYLES[status]

    print_repository_message(
        label,
        organisation_name,
        repository_name,
        label_style=style,
        message=message,
        path=path,
    )


def print_status_check(
    status: RepositoryStatusCheckStatus,
    organisation_name: str,
    repository_name: str,
    *,
    message: str | None = None,
    path: Path | None = None,
) -> None:
    """Print a repository status check."""

    print_repository_message(
        REPOSITORY_STATUS_CHECK_LABELS[status],
        organisation_name,
        repository_name,
        label_style=REPOSITORY_STATUS_CHECK_STYLES[status],
        message=message,
        path=path,
    )


def print_repository_result(
    status: RepositoryResultStatus,
    organisation_name: str,
    repository_name: str,
    *,
    message: str | None = None,
    path: Path | None = None,
) -> None:
    """
    Print a completed repository result.

    Args:
        status: Repository result status.
        organisation_name: GitHub organisation name.
        repository_name: GitHub repository name.
        message: Optional result explanation.
        path: Optional local repository path.

    """

    label = REPOSITORY_RESULT_LABELS[status]
    style = REPOSITORY_RESULT_STYLES[status]

    print_repository_message(
        label,
        organisation_name,
        repository_name,
        label_style=style,
        message=message,
        path=path,
    )


def print_repository_failure(
    status: RepositoryFailureStatus,
    organisation_name: str,
    repository_name: str,
    message: str,
    *,
    path: Path | None = None,
) -> None:
    """
    Print a failed repository result.

    Args:
        status: Failure status.
        organisation_name: GitHub organisation name.
        repository_name: GitHub repository name.
        message: Failure explanation.
        path: Optional local repository path.

    """

    label = REPOSITORY_RESULT_LABELS[status]
    style = REPOSITORY_RESULT_STYLES[status]

    print_repository_message(
        label,
        organisation_name,
        repository_name,
        label_style=style,
        message=message,
        path=path,
    )


def print_organisation_header(
    organisation_name: str,
    *,
    destination_name: str | None = None,
) -> None:
    """
    Print an organisation heading.

    Args:
        organisation_name: GitHub organisation name.
        destination_name: Optional local directory alias.

    """

    heading = Text()

    heading.append(
        organisation_name,
        style=STYLE_HEADING,
    )

    if destination_name is not None and destination_name != organisation_name:
        heading.append(" ")
        heading.append(
            f"({destination_name})",
            style=STYLE_MUTED,
        )

    console.print()

    console.rule(
        heading,
        style=STYLE_RULE_PRIMARY,
    )


def print_configuration_summary(
    *,
    config_path: Path,
    clone_path: Path,
    clone_protocol: str,
    organisation_count: int,
    repository_count: int,
) -> None:
    """
    Print a summary of the validated configuration.

    Args:
        config_path: Loaded configuration file.
        clone_path: Root repository clone path.
        clone_protocol: Default clone protocol.
        organisation_count: Number of configured organisations.
        repository_count: Number of configured repositories.

    """

    print_section("Configuration")

    print_path_detail(
        "Configuration file",
        config_path,
    )
    print_path_detail(
        "Clone path",
        clone_path,
    )
    print_detail(
        "Default clone protocol",
        clone_protocol.upper(),
    )
    print_detail(
        "Organisations",
        organisation_count,
    )
    print_detail(
        "Repositories",
        repository_count,
    )


def print_completion_totals(
    *,
    total: int,
    cloned: int,
    updated: int,
    skipped: int,
    failed: int,
) -> None:
    """
    Print compact synchronisation totals without a section heading.

    This is intended for use when the Rich summary table is disabled.

    Args:
        total: Total repositories processed.
        cloned: Successfully cloned repositories.
        updated: Successfully updated repositories.
        skipped: Skipped repositories.
        failed: Failed repositories.

    """

    console.print(
        Text.assemble(
            ("Total: ", STYLE_DETAIL_LABEL),
            (str(total), STYLE_REPOSITORY),
            ("  Cloned: ", STYLE_DETAIL_LABEL),
            (str(cloned), STYLE_SUMMARY_CLONED),
            ("  Updated: ", STYLE_DETAIL_LABEL),
            (str(updated), STYLE_SUMMARY_UPDATED),
            ("  Skipped: ", STYLE_DETAIL_LABEL),
            (str(skipped), STYLE_SUMMARY_SKIPPED),
            ("  Failed: ", STYLE_DETAIL_LABEL),
            (str(failed), STYLE_SUMMARY_FAILED),
        ),
        overflow="fold",
    )


def print_completion_status(
    *,
    skipped: int,
    failed: int,
) -> None:
    """
    Print the final synchronisation status message.

    Args:
        skipped: Number of skipped repositories.
        failed: Number of failed repositories.

    """

    console.print()

    if failed:
        repository_word = "repository" if failed == 1 else "repositories"

        print_error(
            f"Synchronisation completed with {failed} failed {repository_word}."
        )
        return

    if skipped:
        repository_word = "repository" if skipped == 1 else "repositories"

        print_warning(
            "Synchronisation completed successfully, with "
            f"{skipped} skipped {repository_word}."
        )
        return

    print_success("All configured repositories were synchronised successfully.")


def print_completion_summary(
    *,
    total: int,
    cloned: int,
    updated: int,
    skipped: int,
    failed: int,
    show_totals: bool = True,
) -> None:
    """
    Print compact totals and the final synchronisation status.

    No section heading is printed here. The caller is responsible for printing
    a Summary section when required, preventing duplicate summary headings
    when a Rich summary table is displayed.

    Args:
        total: Total repositories processed.
        cloned: Successfully cloned repositories.
        updated: Successfully updated repositories.
        skipped: Skipped repositories.
        failed: Failed repositories.
        show_totals: Print compact totals before the completion message.

    """

    if show_totals:
        print_completion_totals(
            total=total,
            cloned=cloned,
            updated=updated,
            skipped=skipped,
            failed=failed,
        )

    print_completion_status(
        skipped=skipped,
        failed=failed,
    )


def print_unhandled_error(
    error: BaseException,
) -> None:
    """
    Print an unexpected application error safely.

    Args:
        error: Unexpected exception.

    """

    error_name = type(error).__name__
    error_message = str(error).strip()

    if error_message:
        print_error(f"{error_name}: {escape(error_message)}")
        return

    print_error(error_name)
