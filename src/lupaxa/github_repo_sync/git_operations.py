"""
Git and filesystem operations for Lupaxa GitHub Repository Sync.

This module contains repository inspection, clone, update, remote validation,
Git error formatting, and directory preparation logic.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
from urllib.parse import urlparse

from git import (
    GitCommandError,
    InvalidGitRepositoryError,
    NoSuchPathError,
    Repo,
)

from .constants import (
    DEFAULT_REMOTE_NAME,
    GITHUB_HOSTNAME,
    GITHUB_HTTPS_BASE_URL,
    GITHUB_SSH_USER,
)
from .exceptions import RepositorySyncError
from .models import (
    CloneProtocol,
    RepositoryInspection,
)
from .utils import is_repository_problem_status


def build_clone_url(
    organisation_name: str,
    repository_name: str,
    clone_protocol: CloneProtocol,
) -> str:
    """
    Build the Git clone URL for a GitHub repository.

    Args:
        organisation_name: Real GitHub organisation name.
        repository_name: Real GitHub repository name.
        clone_protocol: Clone protocol.

    Returns:
        Git clone URL.

    """

    if clone_protocol == "ssh":
        return (
            f"{GITHUB_SSH_USER}@{GITHUB_HOSTNAME}:"
            f"{organisation_name}/{repository_name}.git"
        )

    return f"{GITHUB_HTTPS_BASE_URL}/{organisation_name}/{repository_name}.git"


def ensure_git_available() -> None:
    """
    Confirm that the Git executable is available.

    The GIT_PYTHON_GIT_EXECUTABLE environment variable is honoured when set.

    Raises:
        RepositorySyncError: If the Git executable cannot be found.

    """

    configured_git = os.environ.get(
        "GIT_PYTHON_GIT_EXECUTABLE",
        "git",
    )

    if shutil.which(configured_git) is not None:
        return

    configured_path = Path(configured_git).expanduser()

    if configured_path.is_file() and os.access(configured_path, os.X_OK):
        return

    raise RepositorySyncError(
        "Git is not installed or is not available in PATH.",
        result="failed",
    )


def ensure_directory(
    directory: Path,
    description: str,
) -> None:
    """
    Ensure a directory exists and provides the required permissions.

    Missing directories are created recursively.

    Args:
        directory: Directory to inspect or create.
        description: Human-readable directory description.

    Raises:
        RepositorySyncError:
            If the path cannot be created, is not a directory, or does not
            provide read, write, and traversal permissions.

    """

    try:
        exists = directory.exists()
    except OSError as exc:
        raise RepositorySyncError(
            f"Could not inspect {description.lower()} '{directory}': {exc}",
            result="inaccessible",
        ) from exc

    if exists:
        try:
            is_directory = directory.is_dir()
        except OSError as exc:
            raise RepositorySyncError(
                f"Could not inspect {description.lower()} '{directory}': {exc}",
                result="inaccessible",
            ) from exc

        if not is_directory:
            raise RepositorySyncError(
                f"{description} exists but is not a directory: {directory}",
                result="invalid",
            )

    if not exists:
        try:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )
        except PermissionError as exc:
            raise RepositorySyncError(
                f"Permission denied while creating "
                f"{description.lower()} '{directory}'.",
                result="inaccessible",
            ) from exc
        except OSError as exc:
            raise RepositorySyncError(
                f"Could not create {description.lower()} '{directory}': {exc}",
                result="inaccessible",
            ) from exc

    missing_permissions: list[str] = []

    if not os.access(directory, os.R_OK):
        missing_permissions.append("read")

    if not os.access(directory, os.W_OK):
        missing_permissions.append("write")

    if not os.access(directory, os.X_OK):
        missing_permissions.append("traverse")

    if missing_permissions:
        permissions = ", ".join(missing_permissions)

        raise RepositorySyncError(
            f"{description} does not provide the required "
            f"permissions ({permissions}): {directory}",
            result="inaccessible",
        )


def format_git_error(error: GitCommandError) -> str:
    """
    Extract a concise message from a GitPython command error.

    Args:
        error: Git command failure.

    Returns:
        Human-readable Git failure message.

    """

    for candidate in (
        error.stderr,
        error.stdout,
    ):
        message = str(candidate).strip()

        if message:
            return message

    message = str(error).strip()

    if message:
        return message

    if error.status is not None:
        return f"Git command exited with status {error.status}."

    return "Git command failed without an error message."


def parse_github_remote_identity(
    remote_url: str,
) -> tuple[str, str] | None:
    """
    Extract a GitHub organisation and repository from a remote URL.

    Supported formats include:

    - git@github.com:organisation/repository.git
    - ssh://git@github.com/organisation/repository.git
    - https://github.com/organisation/repository.git
    - git://github.com/organisation/repository.git

    Args:
        remote_url: Git remote URL.

    Returns:
        Organisation and repository names, or None when the URL is not a
        recognised GitHub repository URL.

    """

    normalized_url = remote_url.strip()

    if not normalized_url:
        return None

    escaped_hostname = re.escape(GITHUB_HOSTNAME)

    scp_match = re.fullmatch(
        rf"(?:[^@/\s]+@)?{escaped_hostname}:(?P<path>[^?#]+)",
        normalized_url,
        flags=re.IGNORECASE,
    )

    if scp_match:
        repository_path = scp_match.group("path")
    else:
        parsed_url = urlparse(normalized_url)

        if parsed_url.hostname is None:
            return None

        if parsed_url.hostname.casefold() != GITHUB_HOSTNAME.casefold():
            return None

        repository_path = parsed_url.path

    repository_path = repository_path.strip("/")

    if repository_path.casefold().endswith(".git"):
        repository_path = repository_path[:-4]

    path_parts = repository_path.split("/")

    if len(path_parts) != 2:
        return None

    organisation_name, repository_name = path_parts

    if not organisation_name or not repository_name:
        return None

    return organisation_name, repository_name


def remote_matches_repository(
    remote_url: str,
    expected_organisation: str,
    expected_repository: str,
) -> bool:
    """
    Check whether a remote URL represents the expected GitHub repository.

    GitHub organisation and repository names are compared case-insensitively.

    Args:
        remote_url: Existing Git remote URL.
        expected_organisation: Expected GitHub organisation.
        expected_repository: Expected GitHub repository.

    Returns:
        True when the remote points to the expected repository.

    """

    identity = parse_github_remote_identity(remote_url)

    if identity is None:
        return False

    actual_organisation, actual_repository = identity

    return (
        actual_organisation.casefold() == expected_organisation.casefold()
        and actual_repository.casefold() == expected_repository.casefold()
    )


def inspect_repository(
    repository_path: Path,
    expected_organisation: str,
    expected_repository: str,
) -> RepositoryInspection:
    """
    Inspect a configured local repository destination without modifying it.

    Args:
        repository_path: Local repository destination.
        expected_organisation: Expected GitHub organisation.
        expected_repository: Expected GitHub repository.

    Returns:
        Repository inspection result.

    """

    try:
        if not repository_path.exists():
            return {
                "status": "clone",
                "message": "Repository destination does not exist.",
            }

        if not repository_path.is_dir():
            return {
                "status": "invalid",
                "message": ("Repository destination exists but is not a directory."),
            }
    except PermissionError as exc:
        return {
            "status": "inaccessible",
            "message": f"Permission denied while inspecting destination: {exc}",
        }
    except OSError as exc:
        return {
            "status": "inaccessible",
            "message": f"Could not inspect destination: {exc}",
        }

    try:
        repository = Repo(
            repository_path,
            search_parent_directories=False,
        )
    except InvalidGitRepositoryError:
        return {
            "status": "invalid",
            "message": ("Destination exists but is not a valid Git repository."),
        }
    except NoSuchPathError:
        return {
            "status": "inaccessible",
            "message": "Repository destination disappeared during inspection.",
        }
    except (GitCommandError, OSError) as exc:
        return {
            "status": "inaccessible",
            "message": f"Could not open Git repository: {exc}",
        }

    if repository.bare:
        return {
            "status": "bare",
            "message": (
                "Destination is a bare Git repository and has no working tree."
            ),
        }

    try:
        if repository.head.is_detached:
            return {
                "status": "detached",
                "message": "Repository HEAD is detached.",
            }
    except (GitCommandError, ValueError, TypeError) as exc:
        return {
            "status": "inaccessible",
            "message": f"Could not determine repository HEAD state: {exc}",
        }

    try:
        origin = repository.remote(DEFAULT_REMOTE_NAME)
    except ValueError:
        return {
            "status": "no-origin",
            "message": (f"Repository does not have a '{DEFAULT_REMOTE_NAME}' remote."),
        }

    try:
        origin_urls = list(origin.urls)
    except (GitCommandError, OSError) as exc:
        return {
            "status": "inaccessible",
            "message": (f"Could not read {DEFAULT_REMOTE_NAME} remote URLs: {exc}"),
        }

    if not origin_urls:
        return {
            "status": "no-origin",
            "message": (
                f"Repository {DEFAULT_REMOTE_NAME} remote does not contain a URL."
            ),
        }

    matching_origin_found = any(
        remote_matches_repository(
            remote_url=remote_url,
            expected_organisation=expected_organisation,
            expected_repository=expected_repository,
        )
        for remote_url in origin_urls
    )

    if not matching_origin_found:
        actual_urls = ", ".join(origin_urls)

        return {
            "status": "origin-mismatch",
            "message": (
                f"Origin points to '{actual_urls}', expected "
                f"'{expected_organisation}/{expected_repository}'."
            ),
        }

    try:
        if repository.is_dirty(
            untracked_files=True,
            submodules=True,
        ):
            return {
                "status": "dirty",
                "message": (
                    "Repository contains staged, modified, untracked, "
                    "or submodule changes."
                ),
            }
    except (GitCommandError, OSError) as exc:
        return {
            "status": "inaccessible",
            "message": f"Could not inspect repository working tree: {exc}",
        }

    try:
        active_branch = repository.active_branch
    except (TypeError, ValueError, GitCommandError) as exc:
        return {
            "status": "inaccessible",
            "message": f"Could not determine the active branch: {exc}",
        }

    try:
        tracking_branch = active_branch.tracking_branch()
    except (GitCommandError, ValueError) as exc:
        return {
            "status": "inaccessible",
            "message": f"Could not determine the upstream branch: {exc}",
        }

    if tracking_branch is None:
        return {
            "status": "no-upstream",
            "message": (
                f"Active branch '{active_branch.name}' does not have an "
                "upstream branch."
            ),
        }

    tracking_remote_name = tracking_branch.remote_name

    if tracking_remote_name != DEFAULT_REMOTE_NAME:
        return {
            "status": "upstream-mismatch",
            "message": (
                f"Active branch '{active_branch.name}' tracks remote "
                f"'{tracking_remote_name}', expected "
                f"'{DEFAULT_REMOTE_NAME}'."
            ),
        }

    return {
        "status": "update",
        "message": (f"Repository is ready to update from '{tracking_branch.name}'."),
    }


def update_repository(
    repository_path: Path,
    expected_organisation: str,
    expected_repository: str,
) -> None:
    """
    Fetch and fast-forward pull an existing repository.

    Fetching prunes deleted remote-tracking branches. Pulling is restricted to
    fast-forward updates so the synchronisation tool never creates a merge
    commit automatically.

    Args:
        repository_path: Local Git repository path.
        expected_organisation: Expected GitHub organisation.
        expected_repository: Expected GitHub repository.

    Raises:
        RepositorySyncError: If the repository cannot be updated safely.

    """

    inspection = inspect_repository(
        repository_path=repository_path,
        expected_organisation=expected_organisation,
        expected_repository=expected_repository,
    )

    inspection_status = inspection["status"]

    if inspection_status == "clone":
        raise RepositorySyncError(
            (
                "Repository destination disappeared before it could be "
                f"updated: {repository_path}"
            ),
            result="inaccessible",
        )

    if is_repository_problem_status(inspection_status):
        raise RepositorySyncError(
            inspection["message"],
            result=inspection_status,
        )

    try:
        repository = Repo(
            repository_path,
            search_parent_directories=False,
        )

        active_branch = repository.active_branch
        tracking_branch = active_branch.tracking_branch()

        if tracking_branch is None:
            raise RepositorySyncError(
                f"Active branch '{active_branch.name}' does not have "
                "an upstream branch.",
                result="no-upstream",
            )

        origin = repository.remote(DEFAULT_REMOTE_NAME)

        origin.fetch(
            prune=True,
        )

        origin.pull(
            tracking_branch.remote_head,
            ff_only=True,
        )
    except RepositorySyncError:
        raise
    except InvalidGitRepositoryError as exc:
        raise RepositorySyncError(
            f"Destination is not a valid Git repository: {repository_path}",
            result="invalid",
        ) from exc
    except NoSuchPathError as exc:
        raise RepositorySyncError(
            f"Repository directory does not exist: {repository_path}",
            result="inaccessible",
        ) from exc
    except GitCommandError as exc:
        raise RepositorySyncError(
            f"Git update failed for '{repository_path}': {format_git_error(exc)}",
            result="failed",
        ) from exc
    except OSError as exc:
        raise RepositorySyncError(
            f"Could not update repository '{repository_path}': {exc}",
            result="inaccessible",
        ) from exc


def remove_incomplete_clone(
    repository_path: Path,
) -> str | None:
    """
    Remove a destination created by a failed clone attempt.

    Args:
        repository_path: Failed clone destination.

    Returns:
        None when cleanup succeeds or is unnecessary, otherwise an error
        description.

    """

    try:
        if not repository_path.exists() and not repository_path.is_symlink():
            return None

        if repository_path.is_symlink() or repository_path.is_file():
            repository_path.unlink()
        else:
            shutil.rmtree(repository_path)
    except OSError as exc:
        return str(exc)

    return None


def clone_repository(
    clone_url: str,
    repository_path: Path,
) -> None:
    """
    Clone a repository into its configured destination.

    An incomplete destination created during a failed clone is removed when
    possible.

    Args:
        clone_url: Repository clone URL.
        repository_path: Local destination path.

    Raises:
        RepositorySyncError: If the repository cannot be cloned.

    """

    parent_directory = repository_path.parent

    ensure_directory(
        parent_directory,
        "Repository parent directory",
    )

    if repository_path.exists() or repository_path.is_symlink():
        raise RepositorySyncError(
            f"Repository destination already exists: {repository_path}",
            result="invalid",
        )

    try:
        Repo.clone_from(
            url=clone_url,
            to_path=repository_path,
        )
    except GitCommandError as exc:
        cleanup_error = remove_incomplete_clone(repository_path)
        message = format_git_error(exc)

        if cleanup_error is not None:
            message += (
                f" The incomplete destination could not be removed: {cleanup_error}"
            )

        raise RepositorySyncError(
            f"Git clone failed for '{clone_url}': {message}",
            result="failed",
        ) from exc
    except OSError as exc:
        cleanup_error = remove_incomplete_clone(repository_path)
        message = str(exc)

        if cleanup_error is not None:
            message += (
                f" The incomplete destination could not be removed: {cleanup_error}"
            )

        raise RepositorySyncError(
            f"Could not clone '{clone_url}' into '{repository_path}': {message}",
            result="failed",
        ) from exc
