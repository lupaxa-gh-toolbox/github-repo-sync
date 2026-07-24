---
title: Home
---

<p align="center">
    <img src="assets/images/logo.png" alt="Lupaxa GitHub Repository Sync Logo" width="320" />
</p>

<h1 align="center">Lupaxa GitHub Repository Sync</h1>

<p align="center">
    Safely clone and synchronise large collections of GitHub repositories from a single declarative configuration.
</p>

<p align="center">
    Clone missing repositories, fast-forward existing repositories, and protect repositories that are not safe to update automatically.
</p>

---

## Welcome

Welcome to the documentation for **Lupaxa GitHub Repository Sync**.

This project provides a safe and repeatable way to clone, organise, and synchronise large collections of GitHub repositories. Rather than assuming every repository can be updated automatically, each repository is inspected before any Git operation is performed. Repositories that are safe are updated, while repositories that require manual attention are left untouched and reported to the user.

Whether you are maintaining a handful of repositories or several hundred across multiple GitHub organisations, the application is designed to make repository management predictable, reliable, and safe.

---

## Why This Project Exists

Many synchronisation tools simply iterate through a directory and execute `git pull` in every repository they find.

Whilst this approach is simple, it assumes that every repository:

- is a valid Git repository
- uses the correct remote
- has a clean working tree
- is attached to a branch
- has not diverged from its upstream branch
- can be updated safely

In practice, these assumptions are often incorrect.

A single repository with local changes, an incorrect remote, or an interrupted clone can cause synchronisation failures or, in the worst case, unexpected modifications to active development work.

Lupaxa GitHub Repository Sync takes a different approach.

Every repository is inspected before synchronisation begins, ensuring that only repositories confirmed to be safe are updated automatically.

---

## Key Features

- Safe repository inspection before every update.
- Automatic cloning of missing repositories.
- Fast-forward updates for repositories that are safe to modify.
- Support for both HTTPS and SSH clone protocols.
- Organisation-based repository grouping.
- Declarative JSON5 configuration.
- Rich terminal output with progress bars and summary tables.
- Cross-platform support for macOS, Linux, and Windows.
- Fully typed modern Python implementation.

---

## Typical Repository Layout

Repositories are organised beneath a single clone directory and grouped by GitHub organisation.

```text
~/Development/
├── the-lupaxa-project/
│   ├── brand-assets/
│   ├── github/
│   └── workflows/
│
├── lupaxa-security-toolbox/
│   ├── certtool/
│   ├── scanner/
│   └── hash-tool/
│
└── lupaxa-devops-toolbox/
    ├── docker-helper/
    ├── kubernetes-helper/
    └── terraform-helper/
```

This structure remains consistent regardless of how many organisations or repositories are configured.

---

## Repository Safety

One of the primary goals of the project is to protect local development work.

The application will never automatically:

- discard local changes
- reset repositories
- clean untracked files
- delete branches
- rebase branches
- rewrite repository history
- resolve merge conflicts
- delete existing repositories

If a repository cannot be updated safely, it is skipped and included in the final report.

For a detailed explanation, see the **Repository Safety Model**.

---

## Documentation

The documentation is organised into several sections.

### Getting Started

Learn how to install the application, create your first configuration, and perform your first synchronisation.

- Installation
- Quick Start

---

### Configuration

Learn how to configure organisations, repositories, clone protocols, and destination directories.

- Configuration Guide
- Configuration Reference
- Configuration Examples

---

### Usage

Understand the available commands, synchronisation process, and recommended automation workflows.

- Command Reference
- Synchronisation
- Automation

---

### Concepts

Learn about the design principles that underpin the application.

- Repository Safety Model
- Repository States
- Architecture

---

### Reference

Detailed reference documentation.

- Exit Codes
- Troubleshooting
- Frequently Asked Questions

---

### Development

Information for contributors and maintainers.

- Contributing
- Testing

---

## Example

A minimal configuration consists of only a clone directory and one or more organisations.

```json5
{
  clone_path: "~/Development",

  organisations: [

    {
      name: "the-lupaxa-project",

      repositories: [

        {
          name: "brand-assets"
        },

        {
          name: "github"
        },

        {
          name: "workflows"
        }

      ]
    }

  ]
}
```

Synchronising repositories is then as simple as:

```bash
github-repo-sync
```

or

```bash
grs
```

---

## Next Steps

If this is your first time using the application, continue with the **Getting Started** guide.

Experienced users may prefer to jump directly to the **Configuration Guide** or **Command Reference**.

---

*Lupaxa GitHub Repository Sync is part of **The Lupaxa Project**, a collection of open-source tools, reusable workflows, and supporting resources for software engineering, automation, DevOps, and infrastructure.*
