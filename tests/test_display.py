"""Tests for console presentation helpers."""

from __future__ import annotations

from io import StringIO

import pytest

from lupaxa.github_repo_sync.display import (
    configure_console,
    format_bracket_label,
    get_command_name,
    print_error,
    print_system,
)


def test_get_command_name_includes_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["/Users/wolf/.pyenv/shims/grs", "--status", "--ignore-clean"],
    )

    assert get_command_name() == "grs --status --ignore-clean"


def test_get_command_name_quotes_arguments_with_spaces(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["grs", "--config", "my config.yaml"],
    )

    assert get_command_name() == "grs --config 'my config.yaml'"


def test_format_bracket_label_adds_spaces() -> None:
    assert format_bracket_label("Error") == "[ Error ]"
    assert format_bracket_label(" System ") == "[ System ]"


def test_print_system_uses_system_label() -> None:
    buffer = StringIO()
    configure_console(file=buffer, no_colour=True, force_terminal=True)

    print_system("Status check interrupted by the user.")

    output = buffer.getvalue()
    assert "[ System ] Status check interrupted by the user." in output
    assert "[Error]" not in output


def test_print_error_uses_spaced_label() -> None:
    buffer = StringIO()
    configure_console(file=buffer, no_colour=True, force_terminal=True)

    print_error("Something failed.")

    output = buffer.getvalue()
    assert "[ Error ] Something failed." in output
    assert "[Error]" not in output
