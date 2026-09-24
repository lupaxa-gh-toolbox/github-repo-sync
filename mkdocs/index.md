# GitHub Repository Sync

`grs` clones and fast-forwards the GitHub repositories listed in one configuration file. An existing repository is updated only when the update is a fast-forward and the working tree is safe to change. Anything else is skipped and reported.

## Behaviour

- Configuration is YAML, JSON, or JSON5.
- Missing repositories are cloned.
- Existing repositories are fast-forwarded.
- Local changes are not overwritten.
- The configuration is validated before any Git operation.
- Repositories are processed concurrently (`--workers`, default: CPU count).
- Per-repository output is alphabetical by GitHub name after load.
- The process exit code reports the outcome.

## Requirements

- Python 3.11 or later.
- Git on `PATH`.
- Git credentials for private repositories. `grs` uses the existing Git configuration (SSH keys, a personal access token, or the system credential helper) and does not authenticate itself.
