---
title: Usage
---

# Usage

The **Usage** section explains how to use **Lupaxa GitHub Repository Sync** once it has been installed and configured.

While the **Getting Started** and **Configuration** sections focus on installation and creating a valid configuration file, this section covers the day-to-day operation of the application, including the available command-line interface, the synchronisation process, and automation.

Whether you are synchronising repositories manually from your workstation or running unattended synchronisation on a build server, the principles remain the same.

---

## What You'll Learn

This section explains how to:

- Use the command-line interface.
- Validate configuration files.
- List configured repositories.
- Synchronise repositories safely.
- Understand application output.
- Automate synchronisation tasks.
- Troubleshoot common operational issues.

---

## The Command-Line Interface

The application is designed to be operated entirely from the command line.

Two executable names are provided:

```bash
github-repo-sync
```

and the shorter alias:

```bash
grs
```

Both commands expose exactly the same functionality.

---

## Typical Workflow

For most users, repository synchronisation follows a simple workflow.

```text
Create Configuration
          │
          ▼
Validate Configuration
          │
          ▼
Review Repository List
          │
          ▼
Synchronise Repositories
          │
          ▼
Review Summary
```

Each stage is intentionally independent, allowing configurations to be validated before any Git operations are performed.

---

## Safety Before Speed

A key design goal of the application is safe operation.

During synchronisation, every existing repository is inspected before it is modified.

Repositories that cannot be updated safely are skipped and reported to the user rather than being modified automatically.

This behaviour helps protect local development work and avoids unexpected changes to repositories that require manual attention.

---

## Documentation in This Section

The Usage section is divided into three guides.

### Commands

A complete reference for every command-line option supported by the application.

This includes:

- Global options.
- Configuration selection.
- Validation.
- Repository listing.
- Synchronisation.
- Exit codes.

---

### Synchronisation

A detailed explanation of what happens during a synchronisation run.

Topics include:

- Repository discovery.
- Clone operations.
- Repository inspection.
- Fast-forward updates.
- Skipped repositories.
- Summary reporting.

---

### Automation

Guidance for running repository synchronisation automatically.

Topics include:

- Cron jobs.
- Scheduled Tasks.
- CI/CD environments.
- Build servers.
- Shared development systems.
- Best practices for unattended operation.

---

## Recommended Reading Order

For users new to the application, the recommended reading order is:

1. Commands
2. Synchronisation
3. Automation

This introduces the user interface before explaining the underlying synchronisation process and finally covering unattended execution.

---

## Next Steps

Continue to the **Commands** guide to learn about the command-line interface and the operations supported by **Lupaxa GitHub Repository Sync**.
