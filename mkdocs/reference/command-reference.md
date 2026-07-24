---
title: Command Reference
---

# Command Reference

This document provides a complete reference for the commands supported by **Lupaxa GitHub Repository Sync**.

The command-line interface has been designed to provide a consistent and predictable experience, with each command performing a single well-defined task.

## Command Syntax

The general command syntax is:

```text
grs [GLOBAL OPTIONS] COMMAND [COMMAND OPTIONS]
```

Where:

- **Global Options** affect the behaviour of the application as a whole.
- **Command** specifies the action to perform.
- **Command Options** modify the behaviour of the selected command.

## Global Options

The following options are available regardless of the command being executed.

| Option            | Description                                                          |
| :---------------- | :------------------------------------------------------------------- |
| `--config <file>` | Specify an alternative configuration file.                           |
| `--verbose`       | Enable verbose output. May be specified multiple times if supported. |
| `--quiet`         | Reduce console output to warnings and errors.                        |
| `--version`       | Display the application version.                                     |
| `--help`          | Display command-line help.                                           |

> **Note**
>
> The exact set of global options may evolve between releases. Always refer to `grs --help` for the version you are using.

## Available Commands

The application currently provides the following high-level commands.

| Command    | Description                                                    |
| :--------- | :------------------------------------------------------------- |
| `sync`     | Synchronise repositories defined in the configuration file.    |
| `validate` | Validate the configuration without performing synchronisation. |
| `list`     | Display configured organisations and repositories.             |
| `config`   | Display configuration information.                             |
| `version`  | Display application version information.                       |

The commands available may expand as new functionality is introduced.

## Sync

Synchronises the configured repositories.

### Syntax

```bash
grs sync
```

### Typical Usage

Synchronise all configured repositories.

```bash
grs sync
```

Synchronise using an alternative configuration file.

```bash
grs --config ~/work/github.json5 sync
```

Enable verbose output.

```bash
grs --verbose sync
```

## Validate

Validates the configuration file without modifying any repositories.

### Syntax

```bash
grs validate
```

### Typical Usage

Validate the default configuration.

```bash
grs validate
```

Validate an alternative configuration.

```bash
grs --config custom.json5 validate
```

This command is recommended before making significant configuration changes.

## List

Displays the organisations and repositories defined in the configuration.

### Syntax

```bash
grs list
```

Typical output may include:

- Configured organisations.
- Repository names.
- Local paths.
- Repository URLs.

This command performs no Git operations.

## Config

Displays information about the active configuration.

### Syntax

```bash
grs config
```

Depending on the implementation, this command may display:

- Configuration file location.
- Configuration version.
- Repository root.
- Organisation count.
- Repository count.

No synchronisation is performed.

## Version

Displays version information.

### Syntax

```bash
grs version
```

Typical information includes:

- Application version.
- Python version.
- Platform information.

This command is useful when reporting issues or requesting support.

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

Display help for a specific command, if supported.

```bash
grs sync --help
```

The built-in help always reflects the capabilities of the installed version and should be considered the authoritative source for command syntax.

## Related Documentation

For additional information, see:

- **Configuration Guide**
- **Commands**
- **Automation**
- **Exit Codes**
