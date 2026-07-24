---
title: Synchronisation
---

# Synchronisation

Synchronisation is the core function of **Lupaxa GitHub Repository Sync**.

Its purpose is simple:

> Ensure that the repositories defined in your configuration exist locally and are safely synchronised with their corresponding GitHub repositories.

Unlike many synchronisation tools, this application does **not** blindly execute `git pull` against every repository it finds. Instead, every repository is evaluated before any Git operation is performed.

This conservative approach helps protect local development work while ensuring repositories remain up to date whenever it is safe to do so.

---

# The Synchronisation Process

A synchronisation run follows a predictable sequence of operations.

```text
Load Configuration
        │
        ▼
Validate Configuration
        │
        ▼
Create Organisation Directories
        │
        ▼
Process Each Repository
        │
        ├── Repository Missing
        │       │
        │       ▼
        │     Clone Repository
        │
        └── Repository Exists
                │
                ▼
        Inspect Repository
                │
                ▼
        Safe to Update?
           │         │
          Yes        No
           │         │
           ▼         ▼
   Fast-forward     Skip
      Update
                │
                ▼
        Produce Summary
```

Every repository progresses independently through this workflow.

An issue affecting one repository does not prevent the remaining repositories from being processed.

---

# Loading the Configuration

The application begins by loading the configured JSON5 file.

During this stage it:

- Parses the configuration.
- Applies default values.
- Resolves inherited settings.
- Builds the in-memory configuration model.

If the configuration cannot be loaded, synchronisation stops immediately.

---

# Configuration Validation

Before any filesystem or Git operations begin, the configuration is validated.

Validation includes checks such as:

- Required properties.
- Duplicate organisations.
- Duplicate repositories.
- Invalid property types.
- Unsupported values.

If validation fails, no repositories are modified.

---

# Creating Organisation Directories

Each configured organisation receives its own directory beneath the configured clone path.

For example:

```text
~/Development/
├── the-lupaxa-project/
├── lupaxa-security-toolbox/
└── lupaxa-devops-toolbox/
```

Directories are created automatically if they do not already exist.

Existing directories are reused.

---

# Repository Discovery

Each configured repository is then processed individually.

For every repository, the application determines whether:

- the repository already exists locally
- the directory exists but is not a Git repository
- the repository must be cloned

The required action is then selected automatically.

---

# Cloning Missing Repositories

Repositories that do not exist locally are cloned automatically.

Clone URLs are generated using the configured clone protocol.

For HTTPS:

```text
https://github.com/the-lupaxa-project/workflows.git
```

For SSH:

```text
git@github.com:the-lupaxa-project/workflows.git
```

Successful clones are included in the final summary.

---

# Inspecting Existing Repositories

Repositories that already exist are inspected before any update is attempted.

Typical inspections include:

- Valid Git repository.
- Expected remote URL.
- Working tree status.
- Detached HEAD detection.
- Upstream branch configuration.
- Branch divergence.
- Fetch success.

Only repositories that pass every safety check are eligible for synchronisation.

---

# Updating Repositories

When a repository is considered safe, the application performs a fast-forward update.

No rebasing, merging, or history rewriting is performed.

The application only applies updates that Git can perform safely without requiring user intervention.

---

# Skipped Repositories

Some repositories cannot be updated automatically.

Common reasons include:

- Local modifications.
- Untracked files.
- Detached HEAD.
- Diverged branches.
- Incorrect remote configuration.
- Missing upstream branch.
- Failed fetch.
- Invalid Git repository.

Skipped repositories are left unchanged and reported at the end of the run.

This behaviour is intentional and helps prevent accidental data loss.

---

# Error Handling

Errors are isolated to individual repositories wherever possible.

For example:

- A failed clone does not stop other repositories from being processed.
- A fetch failure only affects the current repository.
- A skipped repository does not interrupt synchronisation.

This allows large synchronisation jobs to complete even when individual repositories require manual attention.

---

# Synchronisation Summary

At the end of every run, a summary is displayed.

Typical information includes:

- Organisations processed.
- Repositories processed.
- Repositories cloned.
- Repositories updated.
- Repositories skipped.
- Errors encountered.
- Total execution time.

This provides a concise overview of the synchronisation results.

---

# Safe by Design

One of the primary design goals of the application is protecting local repositories.

During synchronisation the application will never automatically:

- discard local changes
- delete repositories
- clean untracked files
- reset branches
- perform forced checkouts
- resolve merge conflicts
- rewrite Git history
- delete branches

Any repository requiring these operations is skipped for manual review.

---

# Performance

Synchronisation is designed to scale from a handful of repositories to several hundred.

Typical performance depends on:

- Number of repositories.
- Network speed.
- Repository size.
- Git hosting performance.
- Local storage performance.

Because only configured repositories are processed, synchronisation remains predictable even for large repository collections.

---

# Best Practices

For reliable synchronisation, it is recommended to:

- Validate configurations before synchronising.
- Commit or stash local work before running updates.
- Review skipped repositories after each run.
- Keep Git authentication configured correctly.
- Synchronise regularly rather than infrequently.

Regular synchronisation generally results in smaller updates and fewer conflicts.

---

# Next Steps

If you intend to run synchronisation automatically, continue to the **Automation** guide to learn how to schedule unattended synchronisation on development workstations, build servers, and continuous integration environments.
