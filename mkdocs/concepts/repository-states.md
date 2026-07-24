---
title: Repository States
---

# Repository States

During synchronisation, every configured repository is evaluated and assigned a **repository state**.

The repository state describes the current condition of the local repository and determines the action that the application will take.

Understanding these states makes it much easier to interpret synchronisation results and understand why a repository was cloned, updated, skipped, or reported as requiring manual attention.

---

# Repository Lifecycle

Every repository progresses through a simple decision process.

```text
Configured Repository
         │
         ▼
Does the Repository Exist?
         │
   ┌─────┴─────┐
   │           │
  No          Yes
   │           │
   ▼           ▼
Clone      Inspect Repository
                 │
                 ▼
         Determine State
                 │
                 ▼
        Select Appropriate Action
```

The detected state always determines the action. No repository is modified without first identifying its current state.

---

# Missing Repository

A repository that does not exist locally is considered **Missing**.

## Characteristics

- Directory does not exist.
- No local clone is present.
- Repository has never been synchronised.

## Action

The repository is cloned from GitHub.

---

# Invalid Repository

An existing directory that is not recognised as a valid Git repository.

## Characteristics

- Missing `.git` directory.
- Corrupted Git metadata.
- Incorrect directory contents.

## Action

The repository is skipped.

Manual investigation is required before synchronisation can continue.

---

# Clean Repository

A repository with no local modifications and a correctly configured remote.

## Characteristics

- Valid Git repository.
- Clean working tree.
- Attached to a branch.
- Correct remote.
- Upstream configured.

## Action

The repository is eligible for synchronisation.

---

# Up-to-Date Repository

A clean repository that already matches the latest state of its upstream branch.

## Characteristics

- Working tree clean.
- No incoming commits.
- No outgoing commits.

## Action

No update is required.

The repository is reported as already up to date.

---

# Fast-Forward Repository

A repository that is behind its upstream branch but can be updated safely using a fast-forward operation.

## Characteristics

- Working tree clean.
- No local commits.
- Remote contains newer commits.

## Action

Perform a fast-forward update.

No merge or rebase is required.

---

# Dirty Repository

A repository containing local modifications.

## Characteristics

- Modified files.
- Staged changes.
- Unstaged changes.

## Action

The repository is skipped.

Updating the repository could interfere with local development work.

---

# Repository with Untracked Files

The repository contains files that are not tracked by Git.

## Characteristics

- Untracked files present.
- Working tree not considered clean.

## Action

The repository is skipped.

Untracked files may indicate work in progress or locally generated content that requires review.

---

# Detached HEAD

The repository is not currently checked out on a branch.

## Characteristics

- Detached `HEAD`.
- No active branch.

## Action

The repository is skipped.

Automatic updates are intentionally avoided while the repository is in this state.

---

# Diverged Repository

The local and remote branches have both advanced independently.

## Characteristics

- Local commits exist.
- Remote commits exist.
- Fast-forward update impossible.

## Action

The repository is skipped.

The divergence must be resolved manually before synchronisation can continue.

---

# Missing Upstream Branch

The current branch has no configured upstream.

## Characteristics

- Branch exists.
- No upstream tracking branch.

## Action

The repository is skipped.

An upstream branch must be configured before automatic synchronisation is possible.

---

# Remote Configuration Error

The configured Git remote does not match the repository defined in the configuration.

Examples include:

- Incorrect remote URL.
- Repository renamed.
- Remote removed.
- Repository pointing to an unrelated project.

## Action

The repository is skipped.

Updating an unexpected repository could result in serious mistakes, so manual intervention is required.

---

# Fetch Failure

The application could not retrieve the latest information from the remote repository.

Possible causes include:

- Network failure.
- Authentication problems.
- Repository permissions.
- Remote server unavailable.

## Action

The repository is skipped.

Other repositories continue to be processed.

---

# Clone Failure

The repository could not be cloned successfully.

Possible causes include:

- Repository does not exist.
- Authentication failure.
- Network interruption.
- Insufficient permissions.
- Invalid clone URL.

## Action

The failure is recorded in the final summary.

Remaining repositories continue to be processed.

---

# State Transitions

The application attempts to move repositories through a predictable lifecycle.

```text
Missing
    │
    ▼
Cloned
    │
    ▼
Clean
    │
    ▼
Up-to-Date
    │
    ▼
Fast-Forward Available
    │
    ▼
Updated
```

Some repositories may temporarily move into states such as **Dirty** or **Detached HEAD**, in which case they remain unchanged until manually corrected.

---

# Why States Matter

Repository states provide several benefits.

They allow the application to:

- Make consistent synchronisation decisions.
- Avoid destructive operations.
- Explain why repositories were skipped.
- Produce meaningful reports.
- Continue processing other repositories when problems occur.

This state-based approach is one of the key design principles behind **Lupaxa GitHub Repository Sync**.

---

# Next Steps

Continue to **Architecture** for an overview of the internal structure of the application and how the various components work together during synchronisation.
