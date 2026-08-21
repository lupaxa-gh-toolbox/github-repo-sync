"""
Shared type definitions for Lupaxa GitHub Repository Sync.

This module contains the project's type aliases and structured data models.
It deliberately contains no application logic.
"""

from __future__ import annotations

from typing import Literal, TypeAlias, TypedDict

#
# Clone configuration types
#

CloneProtocol: TypeAlias = Literal[
    "https",
    "ssh",
]


#
# Repository inspection types
#

RepositoryProblemStatus: TypeAlias = Literal[
    "invalid",
    "bare",
    "detached",
    "no-origin",
    "origin-mismatch",
    "dirty",
    "no-upstream",
    "upstream-mismatch",
    "inaccessible",
]

RepositoryInspectionStatus: TypeAlias = Literal[
    "clone",
    "update",
    "invalid",
    "bare",
    "detached",
    "no-origin",
    "origin-mismatch",
    "dirty",
    "no-upstream",
    "upstream-mismatch",
    "inaccessible",
]


#
# Repository synchronisation types
#

RepositorySuccessStatus: TypeAlias = Literal["success",]

RepositoryFailureStatus: TypeAlias = Literal[
    "invalid",
    "bare",
    "detached",
    "no-origin",
    "origin-mismatch",
    "dirty",
    "history-rewritten",
    "no-upstream",
    "upstream-mismatch",
    "inaccessible",
    "failed",
]

RepositoryResultStatus: TypeAlias = Literal[
    "success",
    "invalid",
    "bare",
    "detached",
    "no-origin",
    "origin-mismatch",
    "dirty",
    "history-rewritten",
    "no-upstream",
    "upstream-mismatch",
    "inaccessible",
    "failed",
]

RepositoryUpdateOutcome: TypeAlias = Literal[
    "fast-forwarded",
    "reset-rewritten",
]

RepositoryPlannedAction: TypeAlias = Literal[
    "clone",
    "update",
]

RepositoryCompletedAction: TypeAlias = Literal[
    "cloned",
    "updated",
    "skipped",
]

RepositoryAction: TypeAlias = Literal[
    "clone",
    "cloned",
    "update",
    "updated",
    "skipped",
]


#
# Repository status check types
#

RepositoryStatusCheckStatus: TypeAlias = Literal[
    "clean",
    "missing",
    "ahead",
    "behind",
    "diverged",
    "history-rewritten",
    "fetch-failed",
    "dirty",
    "invalid",
    "bare",
    "detached",
    "no-origin",
    "origin-mismatch",
    "no-upstream",
    "upstream-mismatch",
    "inaccessible",
]


class RepositoryStatusCheck(TypedDict):
    """
    Result from checking one local repository's sync status.

    Attributes:
        status:
            Repository cleanliness or synchronisation classification.
        message:
            Human-readable explanation of the status check result.
        ahead:
            Number of commits ahead of upstream; zero when not applicable.
        behind:
            Number of commits behind upstream; zero when not applicable.

    """

    status: RepositoryStatusCheckStatus
    message: str
    ahead: int
    behind: int


#
# Configuration models
#


class RepositoryConfiguration(TypedDict):
    """
    Validated repository configuration.

    Attributes:
        name:
            GitHub repository name.
        alias:
            Optional local repository alias.
        destination_name:
            Effective local repository directory name.
        clone_protocol:
            Effective clone protocol for the repository.

    """

    name: str
    alias: str | None
    destination_name: str
    clone_protocol: CloneProtocol


class OrganisationConfiguration(TypedDict):
    """
    Validated organisation configuration.

    Attributes:
        name:
            GitHub organisation name.
        alias:
            Optional local organisation alias.
        destination_name:
            Effective local organisation directory name.
        repositories:
            Validated repositories belonging to the organisation.

    """

    name: str
    alias: str | None
    destination_name: str
    repositories: list[RepositoryConfiguration]


class GlobalConfiguration(TypedDict):
    """
    Validated global configuration.

    Attributes:
        clone_path:
            Root directory under which repositories are stored.
        clone_protocol:
            Default clone protocol used when no override is supplied.

    """

    clone_path: str
    clone_protocol: CloneProtocol


class ValidatedConfiguration(TypedDict):
    """
    Complete validated application configuration.

    Attributes:
        config:
            Validated global configuration.
        organisations:
            Validated organisation and repository configurations.

    """

    config: GlobalConfiguration
    organisations: list[OrganisationConfiguration]


#
# Synchronisation models
#


class RepositoryInspection(TypedDict):
    """
    Result from inspecting one local repository destination.

    Attributes:
        status:
            Required repository action or detected local repository problem.
        message:
            Human-readable explanation of the inspection result.

    """

    status: RepositoryInspectionStatus
    message: str


class RepositoryResult(TypedDict):
    """
    Result from synchronising one configured repository.

    Attributes:
        organisation:
            GitHub organisation name.
        repository:
            GitHub repository name.
        local_name:
            Effective local repository directory name.
        path:
            Local repository destination path.
        clone_protocol:
            Clone protocol used for the repository.
        action:
            Planned or completed repository action.
        result:
            Final repository result status.
        message:
            Human-readable result explanation.

    """

    organisation: str
    repository: str
    local_name: str
    path: str
    clone_protocol: CloneProtocol
    action: RepositoryAction
    result: RepositoryResultStatus
    message: str


class RepositoryResultCounts(TypedDict):
    """
    Aggregated repository result totals.

    Attributes:
        total:
            Total repository results.
        cloned:
            Successfully cloned repositories.
        updated:
            Successfully updated repositories.
        skipped:
            Repositories skipped without an operational failure.
        failed:
            Repositories whose final result was failed.

    """

    total: int
    cloned: int
    updated: int
    skipped: int
    failed: int
