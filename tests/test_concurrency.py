"""Tests for concurrent repository work with ordered output."""

from __future__ import annotations

import json
from pathlib import Path
import threading
import time

import pytest

from lupaxa.github_repo_sync.concurrency import (
    default_worker_count,
    run_ordered_tasks,
)
from lupaxa.github_repo_sync.constants import DEFAULT_WORKER_COUNT


def test_default_worker_count_is_at_least_one() -> None:
    assert default_worker_count() >= 1
    assert default_worker_count() == DEFAULT_WORKER_COUNT


def test_run_ordered_tasks_emits_in_submission_order() -> None:
    started = threading.Barrier(3)
    emitted: list[str] = []

    def work(name: str) -> str:
        started.wait(timeout=2)
        if name == "first":
            time.sleep(0.08)
        return name

    results = run_ordered_tasks(
        ["first", "second", "third"],
        work,
        workers=3,
        on_result=lambda _index, value: emitted.append(value),
    )

    assert results == ["first", "second", "third"]
    assert emitted == ["first", "second", "third"]


def test_run_ordered_tasks_raises_after_emitting_prior_results() -> None:
    emitted: list[str] = []

    def work(name: str) -> str:
        if name == "second":
            raise RuntimeError("boom")
        return name

    with pytest.raises(RuntimeError, match="boom"):
        run_ordered_tasks(
            ["first", "second", "third"],
            work,
            workers=3,
            on_result=lambda _index, value: emitted.append(value),
        )

    assert emitted == ["first"]


def test_collect_repository_statuses_callbacks_in_config_order(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from lupaxa.github_repo_sync.commands import load_and_validate_configuration
    from lupaxa.github_repo_sync.status import collect_repository_statuses

    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "config": {
                    "clone_path": str(tmp_path / "clones"),
                    "clone_protocol": "https",
                },
                "organisations": [
                    {
                        "name": "org",
                        "repositories": [
                            {"name": "alpha"},
                            {"name": "beta"},
                            {"name": "gamma"},
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    configuration = load_and_validate_configuration(config_path)
    started = threading.Barrier(3)

    def check(path: Path, *args, **kwargs):
        started.wait(timeout=2)
        if path.name == "alpha":
            time.sleep(0.08)
        return {
            "status": "clean",
            "message": path.name,
            "ahead": 0,
            "behind": 0,
        }

    monkeypatch.setattr(
        "lupaxa.github_repo_sync.status.check_repository_status",
        check,
    )

    seen: list[str] = []
    results = collect_repository_statuses(
        configuration,
        offline=True,
        workers=3,
        result_callback=lambda item: seen.append(item["repository"]),
    )

    assert [result["repository"] for result in results] == [
        "alpha",
        "beta",
        "gamma",
    ]
    assert seen == ["alpha", "beta", "gamma"]


def test_workers_cli_defaults_and_parses() -> None:
    from lupaxa.github_repo_sync.cli import create_parser

    parser = create_parser()
    default_args = parser.parse_args([])
    assert default_args.workers == DEFAULT_WORKER_COUNT

    parsed = parser.parse_args(["--workers", "4"])
    assert parsed.workers == 4


def test_workers_rejects_zero() -> None:
    from lupaxa.github_repo_sync.cli import create_parser

    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--workers", "0"])


def test_main_passes_workers_to_run_sync(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from lupaxa.github_repo_sync.cli import main

    seen: dict[str, object] = {}

    def fake_run_sync(**kwargs: object) -> int:
        seen.update(kwargs)
        return 0

    monkeypatch.setattr("lupaxa.github_repo_sync.cli.run_sync", fake_run_sync)

    assert main(["--workers", "6"]) == 0
    assert seen["workers"] == 6
