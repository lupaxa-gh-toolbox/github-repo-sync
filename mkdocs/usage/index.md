# Usage

`grs` loads a configuration file, validates it, then clones or fast-forwards each configured repository. A repository that fails a safety check is skipped. The process exit code is the result to use in scripts.

When `~/.config/github-repo-sync` is the Git checkout in use, `grs` fast-forwards it before reading the file. It is not an entry in the file. `grs` and `grs --status` show it first and include it in the progress total.

```bash
grs --validate
grs --plan
grs
```

- [Commands](commands.md) — how to run `grs`.
- [Synchronisation](synchronisation.md) — the order of a run.
- [Safety Model](safety-model.md) — when a repository is updated, skipped, or left alone.
- [Repository States](repository-states.md) — how each inspected state maps to an action.
- [Automation](automation.md) — unattended runs and exit status.
