---
title: Troubleshooting
---

# Troubleshooting

This guide provides solutions to the most common issues encountered when using **Lupaxa GitHub Repository Sync**.

Most problems fall into one of four categories:

- Configuration issues.
- Git repository issues.
- Authentication problems.
- Environment or operating system issues.

This document explains how to identify these problems, understand their causes, and resolve them safely.

---

# Before You Begin

Before investigating a specific issue, verify the following:

- You are using a supported version of Python.
- Git is installed and available.
- The application is installed correctly.
- Your configuration validates successfully.
- You can clone the affected repository manually using Git.

If all of the above are true, the issue is likely to be isolated to the repository or environment rather than the application itself.

---

# Configuration Problems

## Configuration File Cannot Be Found

### Symptoms

- The application reports that the configuration file does not exist.
- Synchronisation does not begin.

### Possible Causes

- Incorrect file path.
- Typographical error.
- Incorrect working directory.
- Missing configuration file.

### Resolution

Verify the path supplied to the application.

```bash
github-repo-sync --config config.json5
```

Ensure the file exists and that the current user has permission to read it.

---

## Configuration Validation Failed

### Symptoms

Validation reports one or more errors.

### Possible Causes

- Missing required properties.
- Duplicate organisations.
- Duplicate repositories.
- Invalid property types.
- Unsupported configuration values.
- Invalid JSON5 syntax.

### Resolution

Run the validator directly.

```bash
github-repo-sync validate
```

Correct the reported issues before attempting synchronisation.

---

# Git Authentication Problems

## Repository Cannot Be Cloned

### Symptoms

Clone operations fail.

### Possible Causes

- Incorrect repository name.
- Repository does not exist.
- Private repository.
- Missing authentication.
- Insufficient permissions.

### Resolution

Attempt to clone the repository manually using Git.

If the manual clone fails, resolve the authentication issue before running the application again.

---

## Authentication Failed

### Symptoms

Git reports permission or authentication errors.

### Possible Causes

- Expired credentials.
- Invalid Personal Access Token.
- Missing SSH key.
- Incorrect SSH configuration.

### Resolution

Verify that Git authentication works independently of the application.

For example:

```bash
git clone git@github.com:organisation/repository.git
```

or

```bash
git clone https://github.com/organisation/repository.git
```

---

# Repository Problems

## Repository Is Skipped

### Symptoms

The synchronisation summary reports that a repository was skipped.

### Possible Causes

- Local modifications.
- Untracked files.
- Detached `HEAD`.
- Diverged branches.
- Missing upstream branch.
- Incorrect remote configuration.

### Resolution

Review the repository manually.

The application intentionally skips repositories that require user intervention.

---

## Repository Is Not a Valid Git Repository

### Symptoms

The application reports an invalid repository.

### Possible Causes

- The directory is not a Git repository.
- The `.git` directory is missing.
- Repository metadata has become corrupted.

### Resolution

Determine whether the directory should be:

- Deleted and cloned again.
- Converted into a valid Git repository.
- Removed from the configuration.

---

## Repository Has Diverged

### Symptoms

The local branch has diverged from the remote branch.

### Resolution

Review the repository manually using Git.

Typical approaches include:

- Merging changes.
- Rebasing.
- Resetting the repository.

The application deliberately avoids performing these operations automatically.

---

# Network Problems

## Fetch Failed

### Possible Causes

- Internet connection unavailable.
- GitHub unavailable.
- Firewall restrictions.
- Proxy configuration.
- Temporary network interruption.

### Resolution

Verify network connectivity.

Retry the synchronisation after connectivity has been restored.

---

# Performance Issues

## Synchronisation Appears Slow

Several factors influence synchronisation performance.

Examples include:

- Number of repositories.
- Repository size.
- Internet connection speed.
- GitHub response time.
- Storage performance.

Large repositories naturally require more time to clone and update.

---

## Large Numbers of Repositories

Synchronising several hundred repositories may take noticeable time.

Recommendations include:

- Synchronise regularly.
- Use fast local storage.
- Ensure a reliable network connection.
- Avoid unnecessary repository duplication.

Future releases may introduce optional parallel processing.

---

# Installation Problems

## Command Not Found

### Symptoms

```text
command not found: github-repo-sync
```

### Resolution

Verify that the package has been installed correctly.

```bash
pip show lupaxa-github-repo-sync
```

Also ensure that your Python scripts directory is included in your system `PATH`.

---

## Incorrect Python Version

Verify which version of Python is being used.

```bash
python --version
```

or

```bash
python3 --version
```

The application requires Python 3.11 or later.

---

# Still Having Problems?

If you cannot resolve the issue:

1. Validate the configuration.
2. Run the application with verbose output.
3. Review the reported error messages.
4. Attempt the equivalent Git commands manually.
5. Gather the relevant console output before reporting the issue.

Providing detailed information makes diagnosing problems significantly easier.

---

# Reporting Issues

When reporting an issue, include as much relevant information as possible, including:

- Operating system.
- Python version.
- Git version.
- Application version.
- Configuration (where appropriate).
- Console output.
- Error messages.
- Steps required to reproduce the issue.

Please avoid including sensitive information such as authentication tokens, passwords, or private repository URLs.

---

# Next Steps

If your question is not answered here, continue to the **Frequently Asked Questions** section, which explains many of the design decisions and behaviours of **Lupaxa GitHub Repository Sync**.
