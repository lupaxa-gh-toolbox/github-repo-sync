---
title: Frequently Asked Questions
---

# Frequently Asked Questions

This page answers some of the most common questions about **Lupaxa GitHub Repository Sync**.

Many of these questions relate to design decisions that intentionally differ from other Git repository management tools.

---

# General Questions

## What is Lupaxa GitHub Repository Sync?

Lupaxa GitHub Repository Sync is a command-line application for cloning, organising, and safely synchronising GitHub repositories.

It is designed to manage anything from a handful of repositories to several hundred across multiple GitHub organisations while protecting local development work.

---

## Why does the application use a configuration file?

The configuration file acts as the single source of truth.

Rather than discovering repositories automatically, you explicitly define which repositories should be managed.

This makes synchronisation:

- Predictable.
- Repeatable.
- Easy to review.
- Easy to version control.
- Suitable for automation.

---

## Why JSON5 instead of JSON?

JSON5 is significantly easier to maintain by hand.

It supports:

- Comments.
- Trailing commas.
- Unquoted property names.
- Single-quoted strings.

These features make large configuration files easier to read and edit.

---

# Repository Safety

## Why was my repository skipped?

Repositories are skipped whenever the application cannot guarantee that an automatic update would be safe.

Typical reasons include:

- Local modifications.
- Untracked files.
- Detached `HEAD`.
- Diverged branches.
- Missing upstream branches.
- Incorrect remote configuration.

Skipping a repository is considered normal behaviour and is an important part of the application's safety model.

---

## Why doesn't the application automatically resolve merge conflicts?

Resolving merge conflicts requires human judgement.

Automatically attempting to resolve them could overwrite local work or produce unexpected results.

Instead, the application reports the issue and leaves the repository unchanged.

---

## Why doesn't the application use `git reset --hard`?

A hard reset permanently discards local changes.

Because protecting local work is one of the primary goals of the project, destructive Git operations are intentionally excluded from automatic synchronisation.

---

## Why aren't untracked files deleted automatically?

Untracked files may represent:

- Work in progress.
- Generated files.
- Local configuration.
- Temporary experiments.

Automatically deleting them could result in accidental data loss.

---

# Configuration

## Can I manage multiple GitHub organisations?

Yes.

A single configuration file can manage repositories belonging to any number of GitHub organisations.

Each organisation is synchronised independently.

---

## Can I use both HTTPS and SSH?

Yes.

Clone protocols may be specified:

- Globally.
- Per organisation.
- Per repository.

Repository settings always take precedence over inherited values.

---

## Can I change the local directory names?

Yes.

Both organisations and repositories support custom destination names.

This allows local directory structures to differ from GitHub repository names where required.

---

# Synchronisation

## Does the application delete repositories?

No.

Repositories are never deleted automatically.

If a repository is removed from the configuration, it simply stops being managed.

The local repository remains untouched.

---

## Does the application remove local branches?

No.

The application never deletes branches automatically.

---

## Does the application rewrite Git history?

No.

History rewriting operations such as rebasing or force pushes are never performed automatically.

---

## Can the application update repositories with local changes?

No.

Repositories containing local modifications are skipped until they are returned to a safe state.

---

## Does synchronisation stop if one repository fails?

No.

Repositories are processed independently.

A failure affecting one repository does not prevent other repositories from being synchronised.

---

# Automation

## Can I run the application from cron?

Yes.

The application is well suited to scheduled execution using:

- Cron.
- Windows Task Scheduler.
- CI/CD systems.
- Self-hosted GitHub Actions runners.

---

## Is unattended synchronisation safe?

Provided the repository safety model aligns with your workflow, yes.

Repositories that require manual attention are skipped rather than modified automatically.

---

# Development

## Is the project open source?

Yes.

The project is part of **The Lupaxa Project** and is developed in the open.

---

## How can I contribute?

See the **Development** section of this documentation for guidance on contributing, testing, and development workflows.

---

## Where can I report bugs?

Issues, feature requests, and suggestions should be reported through the project's GitHub repository.

When reporting an issue, include:

- Application version.
- Python version.
- Git version.
- Operating system.
- Relevant console output.
- Steps required to reproduce the issue.

---

# Future Development

## Will additional Git hosting providers be supported?

The architecture has been designed to support future expansion.

While GitHub is currently the primary focus, the modular design allows support for additional Git hosting platforms to be considered in future releases.

---

## Will parallel synchronisation be supported?

Potentially.

Parallel processing is a planned enhancement for future versions, provided it can be implemented without compromising the application's safety model or predictability.

---

## Will plugin support be added?

The modular architecture has been designed with extensibility in mind.

Although plugin support is not currently implemented, the project structure has been organised to make future expansion practical.

---

# Still Have a Question?

If your question is not answered here, please consult the relevant section of the documentation or open an issue in the project's GitHub repository.

Feedback, suggestions, and contributions are always welcome.
