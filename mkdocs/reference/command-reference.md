# Command Reference

## Command Syntax

The general command syntax is:

```text
grs [OPTIONS]
```

Where:

- **Options** select an operating mode, configuration file, presentation settings, and command-specific behaviour.
- When no operating mode is selected, configured repositories are synchronised.

## Global Options

The following options are available regardless of the command being executed.

| Option                | Description                                                     |
| :-------------------- | :-------------------------------------------------------------- |
| `-c`, `--config FILE` | Path to a YAML, JSON, or JSON5 configuration file.              |
| `--version`           | Print the version and exit.                                     |
| `--help`              | Print command-line help and exit.                               |

## Presentation

| Option                      | Description                                                               |
| :-------------------------- | :------------------------------------------------------------------------ |
| `--no-header`               | Do not print the application heading.                                     |
| `--no-colour`, `--no-color` | Disable coloured console output.                                          |
| `--console-width COLUMNS`   | Set the console width. Values are clamped to 80-300. The default is 180.  |

## Synchronisation Output

These options apply to a synchronisation run. They are ignored for `--validate` and `--plan`.

| Option                    | Description                                                    |
| :------------------------ | :------------------------------------------------------------- |
| `--no-configuration`      | Do not print the configuration summary before synchronising.   |
| `--no-progress`           | Disable the synchronisation progress display.                  |
| `--no-repository-output`  | Do not print a result line for each repository.                |
| `--results-table`         | Print a table of every repository result.                      |
| `--no-failure-table`      | Do not print the repository failure table.                     |
| `--no-summary-table`      | Do not print the synchronisation summary table.                |

> **Note**
>
> The exact set of options may change between releases. Use `grs --help` for the installed version.

## Operating Modes

The application uses a flat command-line interface. Repository synchronisation is the default operation; alternative modes are selected with flags.

| Mode         | Description                                                                  |
| :----------- | :--------------------------------------------------------------------------- |
| *(default)*  | Synchronise repositories defined in the configuration file.                  |
| `--validate` | Validate the configuration without performing synchronisation.               |
| `--plan`     | Display the resolved synchronisation plan without modifying repositories.    |
| `--status`   | Check repositories for clean, synchronised state (may fetch tracking refs).  |

The exact set of modes may evolve between releases. Always refer to `grs --help` for the version you are using.

## Default synchronisation

Synchronises the configured repositories when no operating mode flag is selected.

### Syntax

```bash
grs
```

### Typical Usage

Synchronise all configured repositories.

```bash
grs
```

Synchronise using an alternative configuration file.

```bash
grs --config ~/work/github.yaml
```

Disable coloured output.

```bash
grs --no-colour
```

Reset clean local clones after a remote history rewrite.

```bash
grs --recover-rewritten-history
```

### Synchronisation Options

| Option                        | Description                                                                                          |
| :---------------------------- | :--------------------------------------------------------------------------------------------------- |
| `--recover-rewritten-history` | Reset a clean local branch onto rewritten remote history. Without this flag those repos are skipped. |
| `--workers N`                 | Process this many repositories at once (default: CPU count). Output is alphabetical after load.      |

`--recover-rewritten-history` is only valid during synchronisation. A dirty
working tree is still skipped. `--workers` also applies to `--status`.

```bash
grs --workers 8
```

## Validate

Validates the configuration file without modifying any repositories.

### Syntax

```bash
grs --validate
```

### Typical Usage

Validate the default configuration.

```bash
grs --validate
```

Validate an alternative configuration.

```bash
grs --config custom.yaml --validate
```

This command is recommended before making significant configuration changes.

## Plan

Displays the resolved synchronisation plan without modifying any repositories.

### Syntax

```bash
grs --plan
```

### Typical Usage

Preview the default configuration plan.

```bash
grs --plan
```

Preview an alternative configuration.

```bash
grs --config custom.yaml --plan
```

## Status

Checks configured repositories for clean, synchronised working trees. This mode does not change working trees, branches, or commits.

In online mode (the default), it may `git fetch` from each repository's `origin` remote to update remote-tracking refs before comparing local commits with the upstream branch.

Use `--offline` to skip fetch and compare against existing tracking refs.

A repository is **clean** when it has a healthy local layout, a clean working tree, and its current branch matches the configured upstream tracking branch
(neither ahead nor behind). Rewritten remote history with no shared ancestor is reported as **history-rewritten**.

### Syntax

```bash
grs --status [STATUS OPTIONS]
```

### Status Options

| Option            | Description                                                              |
| :---------------- | :----------------------------------------------------------------------- |
| `--ignore-clean`  | Omit fully clean repositories from per-repository output and results.    |
| `--offline`       | Skip fetching remotes; compare against existing remote-tracking refs.    |
| `--workers N`     | Check this many repositories at once (default: CPU count).               |

### Typical Usage

Check all configured repositories (online mode fetches remotes first).

```bash
grs --status
```

Report only repositories that are not clean.

```bash
grs --status --ignore-clean
```

Check status without network access.

```bash
grs --status --offline
```

Check repositories concurrently.

```bash
grs --status --workers 8
```

### Exit Codes

| Exit Code | Meaning                                           |
| :-------: | :------------------------------------------------ |
| `0`       | All configured repositories are clean.            |
| `1`       | One or more repositories are not clean.           |
| `3`       | Configuration validation failed.                  |

## Command Behaviour

All commands follow the same general execution model.

1. Parse command-line arguments.
2. Load configuration where required.
3. Validate input.
4. Execute the requested command.
5. Report the outcome.
6. Return an appropriate exit code.

## Command Exit Status

Every command returns an exit code. Scripts and CI should use that status, not stdout. The codes are in [Exit Codes](exit-codes.md).

## Getting Help

Command-line help is available at any time.

Display the main help page.

```bash
grs --help
```

The built-in help always reflects the capabilities of the installed version and should be considered the authoritative source for command syntax.

## Related Documentation

- [Configuration Guide](../configuration/configuration-guide.md)
- [Commands](../usage/commands.md)
- [Automation](../usage/automation.md)
- [Exit Codes](exit-codes.md)
