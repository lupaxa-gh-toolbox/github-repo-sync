# Command Reference

This document provides a complete reference for the commands supported by **GitHub Repository Sync**.

The command-line interface has been designed to provide a consistent and predictable experience, with each command performing a single well-defined task.

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

| Option            | Description                                                          |
| :---------------- | :------------------------------------------------------------------- |
| `--config <file>` | Specify an alternative configuration file.                           |
| `--no-colour`     | Disable coloured console output.                                     |
| `--version`       | Display the application version.                                     |
| `--help`          | Display command-line help.                                           |

> **Note**
>
> The exact set of global options may evolve between releases. Always refer to `grs --help` for the version you are using.

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
grs --config ~/work/github.json5
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

This option is only valid during synchronisation. A dirty working tree is still skipped.

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
grs --config custom.json5 --validate
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
grs --config custom.json5 --plan
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

This consistent behaviour makes the application suitable for both interactive use and automation.

## Command Exit Status

Every command returns an exit code indicating whether it completed successfully.

Automation systems should always use the exit code rather than parsing console output to determine success or failure.

Complete details are provided in the **Exit Codes** guide.

## Getting Help

Command-line help is available at any time.

Display the main help page.

```bash
grs --help
```

The built-in help always reflects the capabilities of the installed version and should be considered the authoritative source for command syntax.

## Related Documentation

For additional information, see:

- **Configuration Guide**
- **Commands**
- **Automation**
- **Exit Codes**
