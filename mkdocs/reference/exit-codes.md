---
title: Exit Codes
---

# Exit Codes

Every execution of **Lupaxa GitHub Repository Sync** returns an operating system exit code.

Exit codes provide a reliable way for scripts, scheduled tasks, CI/CD pipelines, and other automation tools to determine whether an operation completed successfully or whether user intervention may be required.

A successful synchronisation does not simply mean that every repository was updated. It means the application completed its work without encountering an unrecoverable error. Individual repositories may still have been skipped because they were not in a safe state.

---

## Why Exit Codes Matter

Exit codes are particularly useful when the application is executed automatically.

Typical examples include:

- Cron jobs.
- Windows Task Scheduler.
- CI/CD pipelines.
- Build servers.
- Self-hosted GitHub Actions runners.
- Monitoring systems.

These systems typically determine success or failure solely from the application's exit status.

---

## Exit Code Reference

| Exit Code | Name | Description |
| ----------|------|-------------|
| `0` | Success | The requested operation completed successfully. |
| `1` | General Error | An unexpected application error occurred. |
| `2` | Configuration Error | The configuration file could not be loaded or validated. |
| `3` | Repository Error* | One or more repository operations failed. |
| `4` | Git Error* | A Git operation failed before processing could continue. |
| `5` | Internal Error* | An unexpected internal application error occurred. |

> **Note**
>
> Exit codes marked with an asterisk (*) are reserved for future releases. At present, most operational failures are reported using a general error code while detailed reporting continues to evolve.

---

## Exit Code `0`

A value of `0` indicates that the requested command completed successfully.

Examples include:

- Configuration validated successfully.
- Repository list displayed successfully.
- Synchronisation completed successfully.

A successful synchronisation may still report:

- Repositories already up to date.
- Repositories skipped because they were not safe to update.
- Informational warnings.

These situations are not considered application failures.

---

## Exit Code `1`

A value of `1` indicates that the application encountered an unexpected error.

Possible causes include:

- Unexpected exception.
- Filesystem failure.
- Invalid runtime environment.
- Unexpected dependency failure.

Further information is normally displayed in the console output.

---

## Exit Code `2`

Returned when the configuration cannot be processed.

Examples include:

- Configuration file missing.
- Invalid JSON5 syntax.
- Missing required properties.
- Duplicate repositories.
- Invalid configuration hierarchy.

No synchronisation is attempted when configuration validation fails.

---

## Reserved Exit Codes

Additional exit codes are reserved to provide more detailed reporting in future versions.

Possible future categories include:

- Individual repository failures.
- Authentication failures.
- Git command failures.
- Partial synchronisation results.
- Network connectivity issues.

Introducing additional exit codes will improve integration with monitoring systems and automation platforms while maintaining backwards compatibility wherever possible.

---

## Using Exit Codes in Shell Scripts

### Bash

```bash
github-repo-sync

if [ $? -eq 0 ]; then
    echo "Synchronisation completed successfully."
else
    echo "Synchronisation failed."
fi
```

---

### PowerShell

```powershell
github-repo-sync

if ($LASTEXITCODE -eq 0) {
    Write-Host "Synchronisation completed successfully."
}
else {
    Write-Host "Synchronisation failed."
}
```

---

## Using Exit Codes in CI/CD

Exit codes can be used to determine whether subsequent pipeline stages should continue.

Typical workflow:

```text
Validate Configuration
        │
        ▼
Synchronise Repositories
        │
        ▼
Exit Code == 0 ?
      │       │
     Yes      No
      │       │
      ▼       ▼
 Continue   Stop Pipeline
```

This allows build systems to terminate early if repository synchronisation fails.

---

## Best Practices

When using exit codes in automation:

- Always check the application's exit status.
- Log both the exit code and console output.
- Treat non-zero exit codes as requiring investigation.
- Review skipped repositories separately from application failures.

Exit codes indicate the success or failure of the application itself, while the synchronisation summary provides additional detail about the repositories that were processed.

---

## Next Steps

Continue to **Troubleshooting** for guidance on diagnosing common configuration, Git, and synchronisation issues.
