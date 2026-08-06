"""
Rich table construction for Lupaxa GitHub Repository Sync.

This module contains presentation helpers for configuration previews,
repository results, failures, and final synchronisation statistics.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from pathlib import Path

from rich.table import Table
from rich.text import Text

from . import display
from .models import (
    OrganisationConfiguration,
    RepositoryAction,
    RepositoryResult,
    RepositoryResultStatus,
)
from .styles import (
    REPOSITORY_ACTION_LABELS,
    REPOSITORY_ACTION_STYLES,
    REPOSITORY_RESULT_LABELS,
    REPOSITORY_RESULT_STYLES,
    STYLE_DETAIL_LABEL,
    STYLE_ERROR,
    STYLE_MUTED,
    STYLE_PATH,
    STYLE_REPOSITORY,
    STYLE_SUMMARY_CLONED,
    STYLE_SUMMARY_FAILED,
    STYLE_SUMMARY_SKIPPED,
    STYLE_SUMMARY_UPDATED,
    STYLE_TABLE_HEADER,
)
from .utils import abbreviate_home_path


def create_table(
    *,
    title: str | None = None,
    show_header: bool = True,
    show_lines: bool = False,
    expand: bool = True,
) -> Table:
    """
    Create a consistently configured Rich table.

    Args:
        title:
            Optional table title.
        show_header:
            Whether to display column headers.
        show_lines:
            Whether to draw separators between rows.
        expand:
            Whether the table should fill the available console width.

    Returns:
        Configured Rich table.

    """

    return Table(
        title=title,
        title_style=STYLE_DETAIL_LABEL,
        header_style=STYLE_TABLE_HEADER,
        show_header=show_header,
        show_lines=show_lines,
        expand=expand,
        border_style=STYLE_MUTED,
        row_styles=None,
    )


def format_repository_action(
    action: RepositoryAction,
) -> Text:
    """
    Format a repository action for table output.

    Args:
        action:
            Repository action.

    Returns:
        Styled Rich text.

    """

    return Text(
        REPOSITORY_ACTION_LABELS[action],
        style=REPOSITORY_ACTION_STYLES[action],
    )


def format_repository_result_status(
    status: RepositoryResultStatus,
) -> Text:
    """
    Format a repository result status for table output.

    Args:
        status:
            Repository result status.

    Returns:
        Styled Rich text.

    """

    return Text(
        REPOSITORY_RESULT_LABELS[status],
        style=REPOSITORY_RESULT_STYLES[status],
    )


def format_repository_path(
    path: Path | str,
) -> Text:
    """
    Format a repository path for table output.

    Args:
        path:
            Repository path.

    Returns:
        Styled abbreviated path.

    """

    return Text(
        abbreviate_home_path(Path(path)),
        style=STYLE_PATH,
        overflow="fold",
    )


def create_configuration_table(
    organisations: Sequence[OrganisationConfiguration],
    clone_path: Path,
) -> Table:
    """
    Create a table showing the validated repository configuration.

    Args:
        organisations:
            Validated organisation configurations.
        clone_path:
            Root clone directory.

    Returns:
        Configuration table.

    """

    table = create_table(
        show_lines=False,
    )

    table.add_column(
        "Organisation",
        style=STYLE_REPOSITORY,
        no_wrap=True,
    )
    table.add_column(
        "Repository",
        style=STYLE_REPOSITORY,
        no_wrap=True,
    )
    table.add_column(
        "Protocol",
        justify="center",
        no_wrap=True,
    )
    table.add_column(
        "Destination",
        style=STYLE_PATH,
        overflow="fold",
        ratio=2,
    )

    for organisation in organisations:
        organisation_name = organisation["name"]
        organisation_destination = organisation["destination_name"]

        for repository in organisation["repositories"]:
            repository_destination = repository["destination_name"]

            destination_path = (
                clone_path / organisation_destination / repository_destination
            )

            table.add_row(
                organisation_name,
                repository["name"],
                repository["clone_protocol"].upper(),
                format_repository_path(destination_path),
            )

    return table


def print_configuration_table(
    organisations: Sequence[OrganisationConfiguration],
    clone_path: Path,
) -> None:
    """
    Print the validated repository configuration table.

    Args:
        organisations:
            Validated organisation configurations.
        clone_path:
            Root clone directory.

    """

    display.console.print(
        create_configuration_table(
            organisations=organisations,
            clone_path=clone_path,
        )
    )


def create_repository_results_table(
    results: Iterable[RepositoryResult],
    *,
    include_paths: bool = True,
    include_messages: bool = True,
) -> Table:
    """
    Create a detailed table of repository synchronisation results.

    Args:
        results:
            Repository results.
        include_paths:
            Include local destination paths.
        include_messages:
            Include result detail messages.

    Returns:
        Repository results table.

    """

    table = create_table(
        show_lines=True,
    )

    table.add_column(
        "Repository",
        style=STYLE_REPOSITORY,
        no_wrap=True,
    )
    table.add_column(
        "Action",
        justify="center",
        no_wrap=True,
    )
    table.add_column(
        "Result",
        justify="center",
        no_wrap=True,
    )

    if include_paths:
        table.add_column(
            "Destination",
            style=STYLE_PATH,
            overflow="fold",
            ratio=2,
        )

    if include_messages:
        table.add_column(
            "Details",
            style=STYLE_MUTED,
            overflow="fold",
            ratio=2,
        )

    for result in results:
        repository_name = f"{result['organisation']}/{result['repository']}"

        row: list[Text | str] = [
            repository_name,
            format_repository_action(result["action"]),
            format_repository_result_status(result["result"]),
        ]

        if include_paths:
            row.append(format_repository_path(result["path"]))

        if include_messages:
            row.append(result["message"])

        table.add_row(*row)

    return table


def print_repository_results_table(
    results: Sequence[RepositoryResult],
    *,
    include_paths: bool = True,
    include_messages: bool = True,
) -> None:
    """
    Print a detailed repository results table.

    An informational row is displayed when no results are available.

    Args:
        results:
            Repository results.
        include_paths:
            Include local destination paths.
        include_messages:
            Include result detail messages.

    """

    if results:
        display.console.print(
            create_repository_results_table(
                results,
                include_paths=include_paths,
                include_messages=include_messages,
            )
        )
        return

    table = create_table(
        show_header=False,
    )

    table.add_column(
        "Message",
        style=STYLE_MUTED,
    )
    table.add_row("No repository results were recorded.")

    display.console.print(table)


def create_failure_table(
    results: Iterable[RepositoryResult],
) -> Table:
    """
    Create a table containing only failed repository results.

    Args:
        results:
            Repository results.

    Returns:
        Failure table.

    """

    table = create_table(
        show_lines=True,
    )

    table.add_column(
        "Repository",
        style=STYLE_REPOSITORY,
        no_wrap=True,
    )
    table.add_column(
        "Failure",
        justify="center",
        no_wrap=True,
    )
    table.add_column(
        "Destination",
        style=STYLE_PATH,
        overflow="fold",
        ratio=2,
    )
    table.add_column(
        "Details",
        style=STYLE_ERROR,
        overflow="fold",
        ratio=2,
    )

    for result in results:
        if result["result"] != "failed":
            continue

        table.add_row(
            (f"{result['organisation']}/{result['repository']}"),
            format_repository_result_status(result["result"]),
            format_repository_path(result["path"]),
            (result["message"] or "Repository synchronisation failed."),
        )

    return table


def print_failure_table(
    results: Sequence[RepositoryResult],
) -> None:
    """
    Print failed repository results when any failures are present.

    Args:
        results:
            Repository results.

    """

    failed_results = [result for result in results if result["result"] == "failed"]

    if not failed_results:
        return

    display.console.print(create_failure_table(failed_results))


def count_repository_actions(
    results: Iterable[RepositoryResult],
) -> Counter[RepositoryAction]:
    """
    Count repository results by completed action.

    Args:
        results:
            Repository results.

    Returns:
        Repository action counter.

    """

    counts: Counter[RepositoryAction] = Counter()

    for result in results:
        counts[result["action"]] += 1

    return counts


def count_repository_result_statuses(
    results: Iterable[RepositoryResult],
) -> Counter[RepositoryResultStatus]:
    """
    Count repository results by outcome status.

    Args:
        results:
            Repository results.

    Returns:
        Repository result status counter.

    """

    counts: Counter[RepositoryResultStatus] = Counter()

    for result in results:
        counts[result["result"]] += 1

    return counts


def create_summary_table(
    results: Sequence[RepositoryResult],
) -> Table:
    """
    Create the final synchronisation summary table.

    Args:
        results:
            Repository results.

    Returns:
        Summary table.

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

    summary_rows = (
        (
            "Cloned",
            cloned,
            STYLE_SUMMARY_CLONED,
        ),
        (
            "Updated",
            updated,
            STYLE_SUMMARY_UPDATED,
        ),
        (
            "Skipped",
            skipped,
            STYLE_SUMMARY_SKIPPED,
        ),
        (
            "Failed",
            failed,
            STYLE_SUMMARY_FAILED,
        ),
    )

    table = create_table(
        show_header=False,
        show_lines=False,
        expand=False,
    )

    table.add_column(
        "Status",
        style=STYLE_DETAIL_LABEL,
        no_wrap=True,
    )
    table.add_column(
        "Count",
        justify="right",
        no_wrap=True,
    )

    table.add_row(
        Text(
            "Total",
            style=STYLE_DETAIL_LABEL,
        ),
        Text(
            str(len(results)),
            style=STYLE_REPOSITORY,
        ),
    )

    for label, count, style in summary_rows:
        table.add_row(
            Text(
                label,
                style=STYLE_DETAIL_LABEL,
            ),
            Text(
                str(count),
                style=style,
            ),
        )

    return table


def print_summary_table(
    results: Sequence[RepositoryResult],
) -> None:
    """
    Print the final synchronisation summary table.

    Args:
        results:
            Repository results.

    """

    display.console.print(create_summary_table(results))


def create_failure_summary_table(
    results: Iterable[RepositoryResult],
) -> Table:
    """
    Create a grouped summary of explicit failure categories.

    Only repository results whose final status is ``failed`` are included.
    Skipped repositories are excluded because they are reported separately in
    the normal synchronisation summary.

    Args:
        results:
            Repository results.

    Returns:
        Failure category summary table.

    """

    counts: Counter[RepositoryResultStatus] = Counter()

    for result in results:
        if result["result"] != "failed":
            continue

        counts[result["result"]] += 1

    table = create_table(
        show_header=True,
        show_lines=False,
        expand=False,
    )

    table.add_column(
        "Failure",
        style=STYLE_ERROR,
        no_wrap=True,
    )
    table.add_column(
        "Count",
        justify="right",
        style=STYLE_ERROR,
        no_wrap=True,
    )

    for status, count in sorted(
        counts.items(),
        key=lambda item: REPOSITORY_RESULT_LABELS[item[0]].casefold(),
    ):
        table.add_row(
            Text(
                REPOSITORY_RESULT_LABELS[status],
                style=REPOSITORY_RESULT_STYLES[status],
            ),
            Text(
                str(count),
                style=REPOSITORY_RESULT_STYLES[status],
            ),
        )

    if not counts:
        table.add_row(
            Text(
                "None",
                style=STYLE_MUTED,
            ),
            Text(
                "0",
                style=STYLE_MUTED,
            ),
        )

    return table


def print_failure_summary_table(
    results: Sequence[RepositoryResult],
) -> None:
    """
    Print a grouped failure summary when failures exist.

    Args:
        results:
            Repository results.

    """

    if not any(result["result"] == "failed" for result in results):
        return

    display.console.print(create_failure_summary_table(results))
