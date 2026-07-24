---
title: Exit Codes
---

# Exit Codes

Every command executed by **Lupaxa GitHub Repository Sync** returns an exit code when it finishes.

Exit codes provide a reliable way for shell scripts, automation platforms and Continuous Integration (CI) systems to determine whether an operation completed successfully.

Unlike console output, exit codes are intended for machine-readable processing and should always be used when automating the application.

## Why Exit Codes Matter

Automation should never rely on parsing console output.

Instead, scripts should check the exit code returned by the application.

For example:

```bash
grs sync

if [ $? -eq 0 ]; then
    echo "Synchronisation completed successfully."
else
    echo "Synchronisation failed."
fi
```

Most automation systems provide native support for evaluating command exit codes.

## Standard Exit Codes

The following exit codes are reserved by the application.

| Exit Code | Meaning                             |
| :-------: | :---------------------------------- |
| `0`       | Operation completed successfully.   |
| `1`       | General application error.          |
| `2`       | Invalid command-line arguments.     |
| `3`       | Configuration validation failed.    |
| `4`       | Configuration could not be loaded.  |
| `5`       | Synchronisation failed.             |
| `6`       | Git operation failed.               |
| `7`       | Authentication failed.              |
| `8`       | Network or remote repository error. |
| `9`       | Unexpected internal error.          |

> **Note**
>
> The exact exit codes may change as the application evolves. Refer to the release notes for any changes introduced in future versions.

## Successful Execution

A successful command returns:

```text
Exit Code: 0
```

This indicates that:

- The requested command completed successfully.
- No unrecoverable errors occurred.
- The application terminated normally.

Warnings do not necessarily result in a non-zero exit code.

## Configuration Errors

Configuration-related problems return a non-zero exit code.

Typical causes include:

- Invalid JSON5 syntax.
- Missing required properties.
- Invalid configuration values.
- Duplicate entries.
- Unsupported configuration versions.

Correct the configuration before attempting another synchronisation.

## Synchronisation Errors

A synchronisation error indicates that the requested operation could not be completed successfully.

Examples include:

- Repository access failures.
- Clone failures.
- Git update failures.
- Repository processing errors.

Depending on the error, some repositories may still have been processed successfully.

## Authentication Errors

Authentication failures occur when GitHub credentials cannot be used to access one or more repositories.

Common causes include:

- Expired credentials.
- Invalid Personal Access Tokens.
- Incorrect SSH configuration.
- Insufficient repository permissions.

Verify authentication before retrying the operation.

## Network Errors

Network-related exit codes indicate that communication with GitHub or another remote service could not be completed.

Possible causes include:

- Internet connectivity problems.
- DNS resolution failures.
- Firewall restrictions.
- Temporary service interruptions.
- Remote server errors.

In many cases, retrying the operation after the issue has been resolved is sufficient.

## Internal Errors

Internal errors indicate that the application encountered an unexpected condition.

These errors are uncommon and may indicate:

- A software defect.
- Corrupted application state.
- An unexpected external dependency failure.

If an internal error can be reproduced consistently, consider reporting it with:

- Application version.
- Python version.
- Operating system.
- Configuration (where appropriate).
- Console output.
- Steps required to reproduce the problem.

## Using Exit Codes in Automation

Exit codes make it straightforward to integrate Lupaxa GitHub Repository Sync into automation.

Typical examples include:

- Scheduled synchronisation jobs.
- Continuous Integration pipelines.
- Deployment workflows.
- Build servers.
- Maintenance scripts.

Automation should always evaluate the exit code before assuming that synchronisation completed successfully.

## Best Practices

When writing automation:

- Always check the exit code.
- Treat non-zero exit codes as failures unless explicitly documented otherwise.
- Record console output for troubleshooting.
- Retry transient failures where appropriate.
- Alert administrators when repeated failures occur.

Following these recommendations helps ensure reliable and predictable automated execution.

## Related Documentation

For more information, see:

- **Automation**
- **Troubleshooting**
- **Command Reference**
