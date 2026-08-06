# Commands

Lupaxa GitHub Repository Sync is operated using the `grs` command-line application.

Every command follows the same high-level workflow:

1. Load the configuration.
2. Validate the configuration.
3. Perform the requested operation.
4. Display a summary.
5. Return an appropriate exit code.

The application has been designed to provide predictable behaviour, clear feedback and meaningful exit codes suitable for both interactive use and automation.

> **Important**
>
> The commands shown in this document reflect the current release of the application. Use `grs --help` to display the commands and options available in your installed version.

## General Syntax

The general command syntax is:

```text
grs [OPTIONS] COMMAND
```

Some commands may support additional command-specific options.

## Display Help

Display the built-in help:

```bash
grs --help
```

This displays the available commands, global options and a brief description of each.

## Display the Installed Version

Display the installed application version:

```bash
grs --version
```

The version displayed is taken directly from the installed package metadata.

## Using an Alternative Configuration File

By default, the application loads:

```text
~/.github-repo-sync.json5
```

If you need to use a different configuration file, specify it using the appropriate command-line option.

This is useful when maintaining multiple synchronisation environments.

## Validating a Configuration

Before synchronising repositories, validate the configuration:

```bash
grs validate
```

Validation checks the entire configuration for problems including:

- Missing required properties.
- Invalid values.
- Invalid property types.
- Duplicate organisations.
- Duplicate repositories.
- Invalid configuration structure.

If validation fails, synchronisation does not begin.

## Synchronising Repositories

To synchronise repositories:

```bash
grs sync
```

The application performs the following steps:

1. Loads the configuration.
2. Validates the configuration.
3. Inspects each configured repository.
4. Clones repositories that do not already exist.
5. Updates repositories where it is safe to do so.
6. Skips repositories that require manual intervention.
7. Displays a summary of the results.

## Exit Codes

Every command returns an exit code indicating the overall result.

Typical outcomes include:

- Successful completion.
- Validation failure.
- Synchronisation failure.
- Unexpected internal error.

A complete list of exit codes is available in the **Reference** section.

## Command Output

During execution the application reports progress describing the work being performed.

Depending on the command, output may include:

- Configuration loading.
- Validation results.
- Repository discovery.
- Clone operations.
- Repository updates.
- Warnings.
- Errors.
- Final summary information.

The amount of output depends on the command and any selected options.

## Getting Help

If a command does not behave as expected:

1. Verify that the configuration is valid.
2. Confirm that Git is installed.
3. Ensure that GitHub authentication is correctly configured.
4. Review any error messages displayed by the application.
5. Consult the **Troubleshooting** guide.

## Next Steps

Continue to **Synchronisation** to learn how Lupaxa GitHub Repository Sync inspects repositories, determines the required actions and performs safe updates.
