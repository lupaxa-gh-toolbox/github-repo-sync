# Usage

This section explains how to use **Lupaxa GitHub Repository Sync** to validate configuration files, inspect planned operations and synchronise GitHub repositories.

Whether you are running the application interactively or as part of an automated workflow, the commands follow a consistent and predictable process designed to
protect your repositories whilst providing clear progress information.

## Command Overview

The application is operated using the `grs` command-line application.

Typical usage consists of:

1. Loading a configuration file.
2. Validating the configuration.
3. Inspecting repositories.
4. Determining the required actions.
5. Performing safe synchronisation.
6. Displaying a summary of the results.

Every command returns an appropriate exit code, making the application suitable for scripting and automation.

## Command Categories

The usage documentation is organised into the following sections.

### Commands

A complete reference for every supported command-line option and command.

This section explains how to:

- Display help.
- Display the application version.
- Specify configuration files.
- Validate configuration.
- Execute synchronisation.
- Interpret exit codes.

### Synchronisation

Describes exactly how repositories are processed.

Topics include:

- Repository discovery.
- Cloning missing repositories.
- Updating existing repositories.
- Repository state inspection.
- Safe synchronisation behaviour.
- Summary reporting.

### Automation

Explains how to integrate Lupaxa GitHub Repository Sync into automated environments.

Examples include:

- Cron jobs.
- Scheduled tasks.
- Continuous Integration (CI) pipelines.
- Unattended execution.
- Logging.
- Exit code handling.

## Typical Workflow

Most users follow the same workflow each time they use the application.

1. Update the configuration file.
2. Validate the configuration.
3. Review any validation errors.
4. Run synchronisation.
5. Review the summary output.

The application performs validation before making any changes to local repositories, helping to detect problems as early as possible.

## Safety

Lupaxa GitHub Repository Sync is designed to perform safe synchronisation.

Before updating a repository, the application verifies that it is in a suitable state for synchronisation. Repositories that require manual intervention are skipped rather than modified automatically.

This behaviour helps protect local work and avoids destructive Git operations.

## Logging and Output

During execution the application provides progress information describing the work being performed.

Depending on the command being executed, output may include:

- Configuration loading.
- Validation results.
- Repository discovery.
- Clone operations.
- Repository updates.
- Warnings.
- Errors.
- Final summary information.

The amount of output may vary depending on the command-line options used.

## Next Steps

Begin with the **Commands** section to learn how to use the command-line interface, then continue to **Synchronisation** to understand how repositories are processed.
