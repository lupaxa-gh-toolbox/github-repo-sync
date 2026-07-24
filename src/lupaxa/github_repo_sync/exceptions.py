"""
Custom exceptions for Lupaxa GitHub Repository Sync.
"""

from __future__ import annotations

from .models import RepositoryFailureStatus


class ConfigurationError(Exception):
    """Raised when the configuration file or its contents are invalid."""


class RepositorySyncError(Exception):
    """
    Raised when a repository cannot be cloned, inspected, or updated.

    Attributes:
        result: Structured result category associated with the failure.

    """

    result: RepositoryFailureStatus

    def __init__(
        self,
        message: str,
        result: RepositoryFailureStatus = "failed",
    ) -> None:
        """
        Initialise a repository synchronisation error.

        Args:
            message: Human-readable error description.
            result: Structured failure category.

        """

        super().__init__(message)
        self.result = result
