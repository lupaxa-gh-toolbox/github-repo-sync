# Automation

GitHub Repository Sync has been designed to operate reliably in both interactive and unattended environments.

Its predictable behaviour, comprehensive validation and meaningful exit codes make it well suited for scheduled execution, Continuous Integration (CI) systems and other automated workflows.

## Before Automating

Before scheduling synchronisation jobs, ensure that:

- The configuration file has been validated.
- Git authentication is configured correctly.
- The destination directory is accessible.
- The account running the job has the required filesystem permissions.
- The account has access to all required GitHub repositories.

Automated jobs should always run using a dedicated service account or user account where appropriate.

## Default Configuration

Unless another configuration file is specified, the application automatically loads:

```text
~/.github-repo-sync.yaml
```

This allows scheduled jobs to run without repeatedly specifying the configuration location.

If multiple configurations are maintained, the appropriate configuration file can be supplied on the command line.

## Scheduled Execution

The application can be executed using any operating system scheduler.

Common examples include:

- cron (Linux)
- launchd (macOS)
- Windows Task Scheduler
- Continuous Integration systems
- Build servers
- Self-hosted automation platforms

Because the application is non-interactive, it is well suited to unattended execution.

## Example Cron Job

The following example executes the synchronisation every morning at 02:00.

```cron
0 2 * * * grs
```

Ensure that the scheduled environment has access to:

- Python.
- Git.
- The `grs` executable.
- Git authentication credentials.
- The configuration file.

## Logging

When running unattended, it is recommended that output is redirected to a log file.

For example:

```bash
grs > sync.log 2>&1
```

Retaining historical logs makes it easier to investigate failures and identify recurring issues.

## Exit Codes

Every command returns an exit code describing the overall result.

Automation platforms should always check the exit code to determine whether synchronisation completed successfully.

Typical outcomes include:

- Successful completion.
- Configuration validation failure.
- Synchronisation failure.
- Unexpected application error.

A complete list of exit codes is provided in the **Reference** section.

## Authentication

The application uses your existing Git authentication.

Depending on your environment, this may include:

- SSH keys.
- Personal Access Tokens (PATs).
- Git Credential Manager.
- Operating system credential stores.

Before enabling unattended execution, verify that repositories can be cloned and updated without requiring interactive authentication.

## Best Practices

For reliable unattended execution:

- Validate configuration changes before deployment.
- Use a dedicated account where appropriate.
- Monitor exit codes.
- Retain execution logs.
- Keep Git credentials up to date.
- Periodically review synchronisation results.

Following these recommendations will help ensure reliable and predictable operation over time.

## Continuous Integration

GitHub Repository Sync can also be incorporated into Continuous Integration workflows.

Typical uses include:

- Preparing development environments.
- Synchronising shared repository collections.
- Validating configuration files.
- Updating local mirrors.
- Supporting scheduled maintenance tasks.

The application's predictable behaviour makes it suitable for integration with a wide range of automation platforms.

## Next Steps

Once you are familiar with the command-line interface and synchronisation process, continue to the **Concepts** section to learn more about the application's
safety model, repository processing and internal architecture.
