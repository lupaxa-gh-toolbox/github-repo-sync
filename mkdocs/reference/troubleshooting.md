---
title: Troubleshooting
---

# Troubleshooting

This guide provides solutions to the most common issues encountered when installing, configuring and running **Lupaxa GitHub Repository Sync**.

Many problems can be resolved by carefully reviewing the error message reported by the application and verifying the configuration, Git environment and authentication.

## General Troubleshooting Process

When an issue occurs, work through the following steps:

1. Read the complete error message.
2. Verify the configuration file.
3. Confirm Git is installed and working correctly.
4. Verify authentication with GitHub.
5. Confirm network connectivity.
6. Retry the operation.
7. Enable verbose output if additional information is required.

Following this sequence resolves the majority of common issues.

---

## Configuration Could Not Be Loaded

### Symptoms

Examples include:

- The application exits immediately.
- A configuration file cannot be found.
- JSON5 parsing errors are reported.

### Possible Causes

- The configuration file does not exist.
- The file path is incorrect.
- Invalid JSON5 syntax.
- The current user cannot read the file.

### Resolution

Verify that the configuration file exists.

For the default configuration:

```text
~/.github-repo-sync.json5
```

If using an alternative configuration file, confirm the path is correct:

```bash
grs --config /path/to/config.json5 validate
```

Correct any reported validation errors before continuing.

---

## Configuration Validation Failed

### Symptoms

Validation reports one or more errors before synchronisation begins.

### Possible Causes

- Missing required properties.
- Duplicate organisations.
- Duplicate repositories.
- Invalid property values.
- Incorrect configuration structure.

### Resolution

Run configuration validation independently.

```bash
grs validate
```

Correct all reported validation errors before running synchronisation.

---

## Git Is Not Installed

### Symptoms

The application reports that Git cannot be found.

### Resolution

Verify that Git is installed.

```bash
git --version
```

If Git is not installed, install it using your operating system's preferred package manager.

After installation, ensure that the `git` executable is available on your system `PATH`.

---

## Authentication Failed

### Symptoms

Repository access is denied.

Examples include:

- Authentication failed.
- Permission denied.
- Repository not accessible.

### Possible Causes

- Invalid credentials.
- Expired Personal Access Token.
- Incorrect SSH configuration.
- Insufficient repository permissions.

### Resolution

Verify that Git authentication is working independently of the application.

For example:

```bash
git ls-remote git@github.com:organisation/repository.git
```

or

```bash
git ls-remote https://github.com/organisation/repository.git
```

Correct any authentication issues before retrying synchronisation.

---

## Repository Cannot Be Cloned

### Symptoms

A repository cannot be cloned during synchronisation.

### Possible Causes

- Repository does not exist.
- Repository URL is incorrect.
- Authentication failure.
- Network problem.

### Resolution

Verify:

- Repository name.
- Organisation name.
- Repository URL.
- Repository permissions.
- Internet connectivity.

---

## Repository Update Failed

### Symptoms

An existing repository cannot be updated.

### Possible Causes

- Repository is not in an expected state.
- Local Git issues.
- Remote repository unavailable.
- Authentication problems.

### Resolution

Inspect the repository manually.

Useful commands include:

```bash
git status
```

```bash
git remote -v
```

```bash
git branch
```

Resolve any reported Git issues before running synchronisation again.

---

## Network Problems

### Symptoms

The application reports network or remote access errors.

### Possible Causes

- Internet connection unavailable.
- DNS issues.
- Firewall restrictions.
- Proxy configuration.
- Temporary GitHub outage.

### Resolution

Confirm Internet connectivity.

For example:

```bash
ping github.com
```

or

```bash
curl https://github.com
```

Retry the operation once connectivity has been restored.

---

## Slow Synchronisation

### Symptoms

Synchronisation appears slower than expected.

### Possible Causes

- Large repository collections.
- Slow network connection.
- Large repositories.
- GitHub rate limiting.
- Local storage performance.

### Resolution

This behaviour is generally expected when synchronising many repositories.

If performance changes significantly compared with previous runs, investigate:

- Network performance.
- Disk performance.
- Authentication delays.
- GitHub service status.

---

## Unexpected Application Error

### Symptoms

The application terminates unexpectedly or reports an internal error.

### Resolution

Collect the following information before reporting the issue:

- Application version.
- Python version.
- Operating system.
- Command executed.
- Console output.
- Configuration details (where appropriate).
- Steps required to reproduce the problem.

This information greatly assists with diagnosis.

---

## Enabling Verbose Output

If additional diagnostic information is required, enable verbose mode.

```bash
grs --verbose sync
```

Verbose output provides additional information about configuration loading, repository processing and synchronisation progress.

---

## Still Need Help?

If the issue cannot be resolved:

- Confirm you are using the latest version of the application.
- Validate the configuration.
- Verify Git authentication independently.
- Review the error message carefully.
- Gather diagnostic information before reporting the issue.

Providing clear reproduction steps and relevant diagnostic information will significantly reduce the time required to identify and resolve the problem.

## Related Documentation

See also:

- **Configuration Guide**
- **Command Reference**
- **Exit Codes**
- **Safety Model**
