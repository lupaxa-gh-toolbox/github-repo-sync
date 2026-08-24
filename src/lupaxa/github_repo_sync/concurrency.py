"""
Ordered concurrent task execution for Lupaxa GitHub Repository Sync.

Workers run in a thread pool. Results are delivered in submission order so
console output stays consistent with sequential runs.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from typing import TypeVar, cast

_T = TypeVar("_T")
_R = TypeVar("_R")
_UNSET = object()


def default_worker_count() -> int:
    """
    Return the default number of worker threads.

    Returns:
        The process CPU count, or 1 when the count is unavailable.

    """

    return os.cpu_count() or 1


def run_ordered_tasks(
    items: Sequence[_T],
    worker: Callable[[_T], _R],
    *,
    workers: int,
    on_result: Callable[[int, _R], None] | None = None,
) -> list[_R]:
    """
    Run tasks concurrently and yield results in submission order.

    Args:
        items:
            Work items in the order they should be reported.
        worker:
            Function applied to each item in a worker thread.
        workers:
            Maximum number of worker threads.
        on_result:
            Optional callback invoked on the calling thread once every
            preceding result is available.

    Returns:
        Results in the same order as ``items``.

    Raises:
        ValueError:
            If ``workers`` is less than 1.
        Exception:
            The first worker exception, after earlier results have been
            reported in order.

    """

    if workers < 1:
        raise ValueError("workers must be greater than zero.")

    if not items:
        return []

    values: list[object] = [_UNSET] * len(items)
    errors: list[Exception | None] = [None] * len(items)
    next_index = 0

    def emit_ready() -> None:
        nonlocal next_index

        while next_index < len(items):
            error = errors[next_index]

            if error is not None:
                raise error

            if values[next_index] is _UNSET:
                return

            if on_result is not None:
                on_result(next_index, values[next_index])  # type: ignore[arg-type]

            next_index += 1

    with ThreadPoolExecutor(max_workers=min(workers, len(items))) as executor:
        future_to_index = {
            executor.submit(worker, item): index for index, item in enumerate(items)
        }

        try:
            for future in as_completed(future_to_index):
                index = future_to_index[future]

                try:
                    values[index] = future.result()
                except Exception as exc:
                    errors[index] = exc

                emit_ready()
        except Exception:
            executor.shutdown(wait=False, cancel_futures=True)
            raise

    return cast("list[_R]", values)
