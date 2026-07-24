---
title: Automation
---

# Automation

One of the strengths of **Lupaxa GitHub Repository Sync** is that it has been designed from the outset to run unattended.

Once a configuration has been created and validated, repository synchronisation can be scheduled to run automatically, ensuring local repository collections remain up to date with minimal manual intervention.

Typical automation targets include:

- Development workstations.
- Build servers.
- Continuous Integration (CI) runners.
- Shared development environments.
- Self-hosted GitHub Actions runners.
- Dedicated maintenance systems.

---

# Why Automate?

Regular synchronisation offers several advantages over manually updating repositories.

Automated synchronisation can:

- Keep repositories current throughout the day.
- Reduce the size of individual updates.
- Detect repository issues earlier.
- Ensure build environments remain consistent.
- Prepare repositories before scheduled tasks or builds.

Because the application only performs safe updates, unattended execution is well suited to routine maintenance.

---

# General Recommendations

Before enabling automation, ensure that:

- The configuration validates successfully.
- Git authentication is already configured.
- The clone directory is accessible.
- The account running the task has sufficient permissions.
- Repository safety checks are understood.

A failed authentication or inaccessible directory cannot be corrected automatically.

---

# Running from Cron (Linux and macOS)

A common approach is to schedule synchronisation using `cron`.

For example, to synchronise repositories every morning at 06:00:

```cron
0 6 * * * github-repo-sync --quiet
```

The `--quiet` option reduces console output, making it more suitable for unattended execution.

For environments where logging is required, redirect the output to a log file.

```cron
0 6 * * * github-repo-sync --quiet >> ~/logs/github-repo-sync.log 2>&1
```

---

# Running from Windows Task Scheduler

On Windows, synchronisation can be scheduled using **Task Scheduler**.

Typical configuration:

| Setting | Value |
| ------- | ----- |
| Trigger | Daily |
| Action | Start a Program |
| Program | `github-repo-sync.exe` or `python` |
| Arguments | `--quiet` |
| Start In | Configuration directory |

Scheduling details will vary depending on how Python and the application were installed.

---

# Continuous Integration

The application may also be used within CI environments to prepare repositories before build or deployment tasks.

Typical workflow:

1. Validate the configuration.
2. Synchronise repositories.
3. Execute build or testing tasks.

Keeping repository synchronisation separate from the build process simplifies troubleshooting and improves visibility.

---

# Self-Hosted GitHub Actions Runners

For organisations using self-hosted GitHub Actions runners, repository synchronisation can be performed as part of the runner maintenance schedule.

This helps ensure that shared repositories remain current without requiring manual intervention.

Depending on the environment, synchronisation may be performed:

- Before each workflow run.
- On a fixed schedule.
- During maintenance windows.

---

# Logging

When running unattended, retaining logs is recommended.

Typical log information includes:

- Execution time.
- Number of repositories processed.
- Clone operations.
- Updated repositories.
- Skipped repositories.
- Errors encountered.

These logs can assist with troubleshooting and provide a history of synchronisation activity.

---

# Notifications

The application itself does not currently send notifications.

If notifications are required, consider using your scheduling platform to report:

- Failed executions.
- Non-zero exit codes.
- Repository errors.
- Validation failures.

This keeps notification behaviour consistent with the surrounding automation environment.

---

# Scheduling Frequency

There is no universally correct synchronisation interval.

The most appropriate schedule depends on how frequently repositories change.

Typical examples include:

| Environment | Suggested Frequency |
| ----------- | ------------------- |
| Personal workstation | Daily |
| Active development machine | Every few hours |
| Build server | Before each build |
| Shared development server | Hourly |
| Self-hosted runner | Before scheduled workflows |

Choose a schedule that balances repository freshness with network and system usage.

---

# Best Practices

When automating synchronisation, consider the following recommendations.

- Validate configuration changes before deployment.
- Use `--quiet` for unattended execution.
- Capture logs for troubleshooting.
- Monitor exit codes.
- Review skipped repositories regularly.
- Ensure Git authentication remains valid.
- Keep configuration files under version control.

Following these practices helps ensure reliable long-term operation.

---

# Future Enhancements

Future releases may introduce additional automation-related features, such as:

- Machine-readable output formats.
- Structured logging.
- Enhanced exit codes.
- Repository filtering.
- Parallel synchronisation.
- Integration with external monitoring systems.

These capabilities will build on the existing automation model while maintaining the application's safety-first philosophy.

---

# Next Steps

Continue to the **Concepts** section to learn more about the design principles behind the application, including the repository safety model, repository states, and overall architecture.
