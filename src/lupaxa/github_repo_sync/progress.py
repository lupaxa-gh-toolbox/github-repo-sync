"""
Rich progress display helpers for Lupaxa GitHub Repository Sync.

This module provides compact progress bars and spinner displays used while
inspecting, cloning, and updating configured repositories.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)

from . import display
from .styles import (
    STYLE_DETAIL_LABEL,
    STYLE_ERROR,
    STYLE_INFORMATION,
    STYLE_MUTED,
    STYLE_REPOSITORY,
)


def create_progress(
    *,
    transient: bool = False,
    disable: bool = False,
) -> Progress:
    """
    Create the main repository progress display.

    The overall display intentionally avoids a full progress bar. Repository
    names, action labels, counts, and elapsed time provide a compact status
    line that remains readable on narrower terminals.

    Args:
        transient:
            Remove the progress display after it finishes.
        disable:
            Disable progress rendering while retaining the same API.

    Returns:
        Configured Rich progress display.

    """

    return Progress(
        SpinnerColumn(
            style=STYLE_INFORMATION,
            finished_text="✓",
        ),
        TextColumn(
            "[{task.fields[action_style]}]{task.fields[action]:<8}[/]",
            justify="left",
        ),
        MofNCompleteColumn(),
        TextColumn(
            "[{task.fields[repository_style]}]{task.fields[repository]}[/]",
            table_column=None,
        ),
        TextColumn(
            "[{task.fields[detail_style]}]{task.fields[detail]}[/]",
        ),
        TimeElapsedColumn(),
        console=display.console,
        transient=transient,
        disable=disable,
        expand=False,
    )


def create_spinner(
    *,
    transient: bool = True,
    disable: bool = False,
) -> Progress:
    """
    Create a spinner for an individual long-running operation.

    Args:
        transient:
            Remove the spinner after it finishes.
        disable:
            Disable rendering while retaining the same API.

    Returns:
        Configured Rich spinner display.

    """

    return Progress(
        SpinnerColumn(
            style=STYLE_INFORMATION,
            finished_text="✓",
        ),
        TextColumn(
            "[{task.fields[action_style]}]{task.fields[action]:<8}[/]",
            justify="left",
        ),
        TextColumn(
            "[{task.fields[repository_style]}]{task.fields[repository]}[/]",
        ),
        TextColumn(
            "[{task.fields[detail_style]}]{task.fields[detail]}[/]",
        ),
        TimeElapsedColumn(),
        console=display.console,
        transient=transient,
        disable=disable,
        expand=False,
    )


def add_repository_task(
    progress: Progress,
    *,
    action: str,
    repository: str,
    total: float = 1,
    detail: str = "",
) -> TaskID:
    """
    Add a repository task to a progress display.

    Args:
        progress:
            Progress display receiving the task.
        action:
            Short operation label, such as ``INSPECT`` or ``CLONE``.
        repository:
            Full repository name.
        total:
            Total task units.
        detail:
            Optional task detail text.

    Returns:
        Rich task identifier.

    """

    return progress.add_task(
        description=repository,
        total=total,
        action=action,
        repository=repository,
        detail=detail,
        action_style=STYLE_INFORMATION,
        repository_style=STYLE_REPOSITORY,
        detail_style=STYLE_MUTED,
    )


def update_repository_task(
    progress: Progress,
    task_id: TaskID,
    *,
    action: str | None = None,
    repository: str | None = None,
    detail: str | None = None,
    completed: float | None = None,
    advance: float | None = None,
    total: float | None = None,
    visible: bool | None = None,
    action_style: str | None = None,
    detail_style: str | None = None,
) -> None:
    """
    Update a repository progress task.

    Args:
        progress:
            Progress display containing the task.
        task_id:
            Task to update.
        action:
            Optional replacement action label.
        repository:
            Optional replacement repository name.
        detail:
            Optional replacement detail text.
        completed:
            Optional absolute completed value.
        advance:
            Optional amount by which to advance the task.
        total:
            Optional replacement task total.
        visible:
            Optional visibility setting.
        action_style:
            Optional replacement action style.
        detail_style:
            Optional replacement detail style.

    """

    update_arguments: dict[str, Any] = {}

    if action is not None:
        update_arguments["action"] = action

    if repository is not None:
        update_arguments["repository"] = repository

    if detail is not None:
        update_arguments["detail"] = detail

    if completed is not None:
        update_arguments["completed"] = completed

    if advance is not None:
        update_arguments["advance"] = advance

    if total is not None:
        update_arguments["total"] = total

    if visible is not None:
        update_arguments["visible"] = visible

    if action_style is not None:
        update_arguments["action_style"] = action_style

    if detail_style is not None:
        update_arguments["detail_style"] = detail_style

    progress.update(
        task_id,
        **update_arguments,
    )


def complete_repository_task(
    progress: Progress,
    task_id: TaskID,
    *,
    action: str | None = None,
    detail: str = "",
) -> None:
    """
    Mark a repository task as complete.

    Args:
        progress:
            Progress display containing the task.
        task_id:
            Task to complete.
        action:
            Optional final action label.
        detail:
            Optional final detail text.

    """

    task = progress.tasks[task_id]

    update_repository_task(
        progress,
        task_id,
        action=action,
        detail=detail,
        completed=task.total,
    )


def fail_repository_task(
    progress: Progress,
    task_id: TaskID,
    *,
    detail: str,
) -> None:
    """
    Mark a repository task as failed.

    The task is completed so the containing progress display can finish while
    retaining the supplied failure detail.

    Args:
        progress:
            Progress display containing the task.
        task_id:
            Task to mark as failed.
        detail:
            Failure description.

    """

    task = progress.tasks[task_id]

    update_repository_task(
        progress,
        task_id,
        action="FAILED",
        detail=detail,
        completed=task.total,
        action_style=STYLE_ERROR,
        detail_style=STYLE_ERROR,
    )


@contextmanager
def repository_progress(
    *,
    total: int,
    action: str = "SYNC",
    detail: str = "",
    transient: bool = True,
    disable: bool = False,
) -> Iterator[tuple[Progress, TaskID]]:
    """
    Run a managed repository progress display.

    This display is intended for the outer loop that processes all configured
    repositories.

    Args:
        total:
            Number of repositories to process.
        action:
            Initial operation label.
        detail:
            Initial detail text.
        transient:
            Remove the display after completion.
        disable:
            Disable progress rendering.

    Yields:
        Progress display and task identifier.

    """

    progress = create_progress(
        transient=transient,
        disable=disable,
    )

    with progress:
        task_id = add_repository_task(
            progress,
            action=action,
            repository="Configured repositories",
            total=max(total, 1),
            detail=detail,
        )

        if total == 0:
            update_repository_task(
                progress,
                task_id,
                completed=1,
                detail="No repositories configured.",
            )

        yield progress, task_id


@contextmanager
def repository_spinner(
    *,
    action: str,
    repository: str,
    detail: str = "",
    transient: bool = True,
    disable: bool = False,
) -> Iterator[tuple[Progress, TaskID]]:
    """
    Run a managed spinner for one repository operation.

    Args:
        action:
            Operation label.
        repository:
            Full repository name.
        detail:
            Optional operation detail.
        transient:
            Remove the spinner after completion.
        disable:
            Disable spinner rendering.

    Yields:
        Progress display and task identifier.

    """

    progress = create_spinner(
        transient=transient,
        disable=disable,
    )

    with progress:
        task_id = add_repository_task(
            progress,
            action=action,
            repository=repository,
            total=1,
            detail=detail,
        )

        yield progress, task_id


def set_overall_repository(
    progress: Progress,
    task_id: TaskID,
    *,
    action: str,
    organisation_name: str,
    repository_name: str,
    detail: str = "",
) -> None:
    """
    Update the overall progress display with the current repository.

    Args:
        progress:
            Main repository progress display.
        task_id:
            Overall progress task.
        action:
            Current operation label.
        organisation_name:
            GitHub organisation name.
        repository_name:
            GitHub repository name.
        detail:
            Optional operation detail.

    """

    update_repository_task(
        progress,
        task_id,
        action=action,
        repository=f"{organisation_name}/{repository_name}",
        detail=detail,
        action_style=STYLE_INFORMATION,
        detail_style=STYLE_MUTED,
    )


def advance_overall_repository(
    progress: Progress,
    task_id: TaskID,
    *,
    detail: str = "",
) -> None:
    """
    Advance the overall repository progress by one.

    Args:
        progress:
            Main repository progress display.
        task_id:
            Overall progress task.
        detail:
            Optional completion detail for the processed repository.

    """

    update_repository_task(
        progress,
        task_id,
        detail=detail,
        advance=1,
    )


def finish_overall_progress(
    progress: Progress,
    task_id: TaskID,
    *,
    detail: str = "Synchronisation complete.",
) -> None:
    """
    Complete the overall repository progress task.

    Args:
        progress:
            Main repository progress display.
        task_id:
            Overall progress task.
        detail:
            Final progress message.

    """

    task = progress.tasks[task_id]

    update_repository_task(
        progress,
        task_id,
        action="COMPLETE",
        detail=detail,
        completed=task.total,
        action_style=STYLE_DETAIL_LABEL,
        detail_style=STYLE_MUTED,
    )
