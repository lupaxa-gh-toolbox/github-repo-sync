"""Package entry point for ``python -m lupaxa_github_repo_sync``."""

from __future__ import annotations

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
