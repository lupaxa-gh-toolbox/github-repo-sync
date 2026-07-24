---
title: Commands
---

# Commands

**Lupaxa GitHub Repository Sync** provides a simple command-line interface designed to make repository synchronisation predictable and easy to automate.

Two executable names are installed:

```bash
github-repo-sync
```

and the shorter alias:

```bash
grs
```

Both commands are identical and may be used interchangeably throughout this documentation.

---

# Command Syntax

The general command syntax is:

```text
github-repo-sync [GLOBAL OPTIONS] COMMAND [COMMAND OPTIONS]
```

For example:

```bash
github-repo-sync validate
```

```bash
github-repo-sync list
```

```bash
github-repo-sync sync
```

If no command is supplied, the application performs a synchronisation using the configured repositories.

```bash
github-repo-sync
```

---

# Global Options

The following options are available for all commands.

## `--config`

Specify an alternative configuration file.

```bash
github-repo-sync --config config.json5
```

Example:

```bash
github-repo-sync --config production.json5
```

---

## `--verbose`

Increase the amount of information displayed during execution.

```bash
github-repo-sync --verbose
```

Future releases may support multiple verbosity levels.

---

## `--quiet`

Reduce console output to warnings, errors, and the final summary.

```bash
github-repo-sync --quiet
```

This option is useful when running the application from scheduled tasks or automation.

---

## `--version`

Display the installed application version.

```bash
github-repo-sync --version
```

Example output:

```text
github-repo-sync 1.0.0
```

---

## `--help`

Display the built-in command reference.

```bash
github-repo-sync --help
```

Help is also available for individual commands.

```bash
github-repo-sync validate --help
```

---

# Commands

The application currently provides the following commands.

| Command | Description |
| -------- | ----------- |
| `sync` | Synchronise repositories. |
| `validate` | Validate the configuration file. |
| `list` | Display configured organisations and repositories. |
| `config` | Display configuration information. *(Planned)* |

> **Note**
>
> Some commands described in this documentation may be planned for future releases. Where applicable, these are clearly identified.

---

# `sync`

Synchronise repositories defined in the configuration.

```bash
github-repo-sync sync
```

If no command is supplied, this command is executed automatically.

```bash
github-repo-sync
```

During synchronisation the application will:

1. Load the configuration.
2. Validate the configuration.
3. Create missing organisation directories.
4. Clone missing repositories.
5. Inspect existing repositories.
6. Update repositories that are safe to synchronise.
7. Skip repositories requiring manual attention.
8. Display a summary.

---

# `validate`

Validate the configuration file without performing any Git operations.

```bash
github-repo-sync validate
```

Typical uses include:

- Checking new configuration files.
- Validating changes before deployment.
- Testing automation environments.
- Identifying configuration errors.

Validation failures prevent synchronisation from starting.

---

# `list`

Display the organisations and repositories defined in the configuration.

```bash
github-repo-sync list
```

Example output:

```text
the-lupaxa-project
 ├── github
 ├── workflows
 └── brand-assets
```

This command is useful for confirming that the expected repositories will be managed.

---

# `config`

> **Planned Feature**

Display information about the currently loaded configuration.

Possible future output may include:

- Configuration file location.
- Clone directory.
- Clone protocol.
- Number of organisations.
- Number of repositories.
- Validation status.

---

# Exit Status

Every command returns an operating system exit code.

Typical values include:

| Exit Code | Meaning |
| ----------|---------|
| `0` | Successful completion. |
| `1` | An unexpected application error occurred. |
| `2` | Configuration validation failed. |
| `3` | One or more repository operations failed. *(Planned)* |

A complete list is provided in the **Exit Codes** reference.

---

# Typical Workflows

## Validate Before Synchronising

```bash
github-repo-sync validate
github-repo-sync sync
```

---

## Review the Repository List

```bash
github-repo-sync list
```

---

## Synchronise Using a Specific Configuration

```bash
github-repo-sync --config production.json5
```

---

## Display Help

```bash
github-repo-sync --help
```

---

## Display the Installed Version

```bash
github-repo-sync --version
```

---

# Best Practices

When using the command-line interface, consider the following recommendations.

- Validate configuration files before synchronising.
- Use version control for shared configuration files.
- Use `--quiet` when running from scheduled tasks.
- Use `--verbose` when troubleshooting.
- Review skipped repositories after every synchronisation.

---

# Next Steps

Continue to **Synchronisation** to learn exactly how repositories are inspected, cloned, updated, and safely skipped during a synchronisation run.
