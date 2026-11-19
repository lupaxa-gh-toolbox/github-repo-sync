# GitHub Repository Sync

`grs` clones and fast-forwards the GitHub repositories listed in one configuration file. An existing repository is updated only when the update is a fast-forward and the working tree is safe to change. Anything else is skipped and reported.

## Behaviour

- Configuration is YAML, JSON, or JSON5.
- Missing repositories are cloned.
- Existing repositories are fast-forwarded.
- Local changes are not overwritten.
- When `~/.config/github-repo-sync` is the Git checkout in use, `grs` fast-forwards it before the file is read. It is not listed in the file.
- `grs` and `grs --status` show that checkout first and include it in the progress total. Status does not update it.
- The configuration is validated before the listed repositories are changed.
- Repositories are processed concurrently (`--workers`, default: CPU count).
- After that checkout, per-repository output is alphabetical by GitHub name.
- The process exit code reports the outcome.

## Requirements

- Python 3.11 or later.
- Git on `PATH`.
- Git credentials for private repositories. `grs` uses the existing Git configuration (SSH keys, a personal access token, or the system credential helper) and does not authenticate itself.
