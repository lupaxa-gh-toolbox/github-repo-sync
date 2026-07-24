"""
Lupaxa GitHub Repository Sync.

Synchronise large collections of GitHub repositories safely by cloning
missing repositories and fast-forward updating existing repositories while
protecting repositories in unsafe local states.
"""

from __future__ import annotations

from .cli import main

__all__ = [
    "main",
]
