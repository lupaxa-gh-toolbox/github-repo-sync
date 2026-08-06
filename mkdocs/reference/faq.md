# Frequently Asked Questions

This guide answers some of the questions most commonly asked by users of **Lupaxa GitHub Repository Sync**.

If you cannot find the answer to your question here, refer to the **Troubleshooting** guide or the command-line help.

## General

### What is Lupaxa GitHub Repository Sync?

Lupaxa GitHub Repository Sync is a command-line application for managing and synchronising collections of GitHub repositories from a single configuration file.

It is designed to simplify the management of large numbers of repositories whilst providing safe, predictable and repeatable synchronisation.

---

### Who is the application intended for?

The application is suitable for:

- Individual developers.
- Open source maintainers.
- Development teams.
- DevOps engineers.
- System administrators.
- Organisations managing multiple GitHub repositories.

---

### Does the application only work with GitHub?

The current version is designed specifically for GitHub.

Future versions may introduce support for additional Git hosting platforms.

---

## Configuration

### Where is the configuration file stored?

By default, the application uses:

```text
~/.github-repo-sync.json5
```

An alternative configuration file can be specified using the `--config` option.

---

### Why does the application use JSON5 instead of JSON?

JSON5 provides a more user-friendly configuration format by supporting features such as:

- Comments.
- Trailing commas.
- Unquoted object keys.
- Improved readability.

These features make larger configuration files significantly easier to maintain.

---

### Can I maintain multiple configurations?

Yes.

You can create multiple configuration files and specify which one to use when running the application.

For example:

```bash
grs --config work.json5 sync
```

---

## Synchronisation

### Will the application overwrite my local work?

No.

Protecting existing repositories is a fundamental design goal of the application.

Repositories are inspected before synchronisation, and operations that could result in unintended data loss are intentionally avoided.

---

### Does the application delete repositories?

No.

Repositories are never deleted automatically during synchronisation.

Repository removal remains a manual operation.

---

### What happens if one repository fails?

Repositories are processed independently.

Where possible, synchronisation continues with the remaining repositories, and a summary is displayed when processing has completed.

---

### Why was a repository skipped?

Repositories are skipped whenever the application determines that synchronisation cannot be completed safely.

Common reasons include:

- Authentication problems.
- Repository configuration issues.
- Repository state requiring manual intervention.
- Network failures.

The application reports the reason whenever possible.

---

## Authentication

### Does the application manage GitHub credentials?

No.

Authentication is handled using your existing Git configuration and authentication mechanism.

This may include:

- SSH keys.
- Personal Access Tokens (PATs).
- Git Credential Manager.
- Operating system credential stores.

---

### Can I use SSH instead of HTTPS?

Yes.

The application supports whichever repository URLs are defined in your configuration.

If your configuration uses SSH repository URLs, Git will authenticate using your configured SSH credentials.

---

## Automation

### Can the application run unattended?

Yes.

The application has been designed for unattended execution and integrates well with:

- cron.
- launchd.
- Windows Task Scheduler.
- Continuous Integration systems.
- Automation platforms.

---

### Can I use the application in CI pipelines?

Yes.

The application returns meaningful exit codes, making it suitable for automation and Continuous Integration workflows.

Automation should evaluate exit codes rather than parsing console output.

---

## Performance

### Can the application synchronise hundreds of repositories?

Yes.

The application has been designed to process repositories individually, making it suitable for synchronising large repository collections.

The overall execution time depends primarily on:

- Repository count.
- Repository size.
- Network performance.
- GitHub responsiveness.
- Local storage performance.

---

### Why does synchronisation sometimes take longer?

Longer execution times are usually caused by external factors, such as:

- Large repositories.
- Slow network connections.
- Authentication delays.
- GitHub service performance.

This behaviour is generally expected.

---

## Troubleshooting

### The application reports a validation error. What should I do?

Run configuration validation independently.

```bash
grs validate
```

Correct all reported validation errors before attempting synchronisation.

---

### The application cannot access GitHub.

Verify:

- Internet connectivity.
- Git authentication.
- Repository permissions.
- Repository URLs.

You can also verify authentication independently using standard Git commands.

---

### Where can I get more help?

If the documentation does not answer your question:

1. Review the **Troubleshooting** guide.
2. Check the command-line help.
3. Confirm you are using the latest version.
4. Gather diagnostic information before reporting an issue.

Providing clear reproduction steps and complete error messages makes issues much easier to diagnose.

## Related Documentation

See also:

- **Troubleshooting**
- **Command Reference**
- **Exit Codes**
- **Configuration Guide**
