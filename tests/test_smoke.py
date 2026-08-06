"""Minimal smoke tests so makefile CI has a tests/ tree to lint and run."""

from __future__ import annotations

from lupaxa.github_repo_sync import main


def test_main_is_callable() -> None:
    assert callable(main)
