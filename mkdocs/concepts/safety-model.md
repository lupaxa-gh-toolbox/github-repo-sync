---
title: Repository Safety Model
---

# Repository Safety Model

The repository safety model is the foundation of **Lupaxa GitHub Repository Sync**.

Every design decision within the application ultimately supports one primary objective:

> **Never modify a repository unless it is safe to do so.**

This philosophy influences every stage of the synchronisation process, from configuration validation through to Git operations.

Unlike many synchronisation tools that assume every repository can simply be updated, Lupaxa GitHub Repository Sync performs a series of safety checks before deciding whether any action should be taken.

---

## Why Safety Matters

A Git repository often contains far more than committed source code.

It may also contain:

- Uncommitted work.
- Experimental changes.
- Work in progress.
- Temporary branches.
- Debugging changes.
- Local configuration.
- Generated files.
- Untracked content.

Automatically updating repositories without understanding their current state can lead to merge conflicts, interrupted development, or even accidental data loss.

Protecting local work is therefore considered more important than keeping every repository up to date.

---

## Safety Before Synchronisation

Every repository passes through the same decision-making process.

```text
Repository Found
        │
        ▼
Inspect Repository
        │
        ▼
Safe?
   │        │
  Yes       No
   │        │
   ▼        ▼
Update     Skip
```

Only repositories that successfully pass every required safety check are updated automatically.

All others are left untouched.

---

## Safety Checks

Before performing any Git operation, the application evaluates a number of conditions.

Typical checks include:

- Does the directory exist?
- Is the directory a valid Git repository?
- Does the configured remote exist?
- Does the remote match the expected repository?
- Is the working tree clean?
- Are there untracked files?
- Is the repository attached to a branch?
- Does an upstream branch exist?
- Has the latest remote information been fetched?
- Has the local branch diverged from the remote?

These checks provide confidence that a fast-forward update can be performed safely.

---

## Safe Repository States

Examples of repositories considered safe include:

- Newly cloned repositories.
- Clean repositories with no local changes.
- Repositories that are already up to date.
- Repositories that can be fast-forwarded without conflict.

These repositories may be synchronised automatically.

---

## Unsafe Repository States

Repositories may be skipped for a variety of reasons.

Examples include:

- Local modifications.
- Untracked files.
- Detached `HEAD`.
- Missing upstream branch.
- Diverged history.
- Invalid Git repository.
- Incorrect remote configuration.
- Failed fetch operation.

Rather than attempting to resolve these situations automatically, the application reports them for manual review.

---

## Why Repositories Are Skipped

Skipping a repository should not be considered an error.

In many cases it is evidence that the safety model has worked exactly as intended.

For example:

- A developer may be working on a feature branch.
- Local changes may not yet have been committed.
- A repository may have been repointed to another remote intentionally.
- The repository may require manual intervention before it can be updated safely.

Automatically modifying these repositories would introduce unnecessary risk.

---

## Operations That Are Never Performed Automatically

The application deliberately avoids potentially destructive Git operations.

It will never automatically:

- Discard local changes.
- Perform a hard reset.
- Delete branches.
- Delete repositories.
- Rewrite Git history.
- Rebase commits.
- Resolve merge conflicts.
- Force checkout another branch.
- Clean untracked files.
- Execute force pushes.

If any of these actions are required, they must be performed manually by the user.

---

## Repository Isolation

Each repository is processed independently.

If one repository cannot be synchronised safely, it does not prevent the remaining repositories from being processed.

For example:

```text
Repository A    ✓ Updated
Repository B    ✓ Updated
Repository C    Skipped
Repository D    ✓ Updated
Repository E    ✓ Updated
```

This isolation improves reliability when synchronising large collections of repositories.

---

## Transparency

The application attempts to make every important decision visible.

When a repository is skipped, the reason is reported to the user.

Examples include:

- Working tree is not clean.
- Repository has diverged.
- Invalid remote configuration.
- Detached `HEAD`.
- Fetch failed.

Providing clear explanations helps users resolve issues without needing to inspect every repository manually.

---

## Designing for Trust

One of the long-term goals of the project is that users should be able to run synchronisation without wondering what has changed behind the scenes.

If the application reports that a repository has been updated, users should have confidence that:

- The repository was inspected.
- Safety checks passed.
- The update was non-destructive.
- No unexpected Git operations were performed.

Predictable behaviour builds confidence, particularly when managing large repository collections.

---

## Summary

The repository safety model can be summarised in four principles:

1. Inspect every repository.
2. Update only when safe.
3. Skip anything uncertain.
4. Never perform destructive Git operations automatically.

These principles underpin every synchronisation performed by **Lupaxa GitHub Repository Sync**.

---

## Next Steps

Continue to **Repository States** to learn about the individual repository states recognised by the application and how each state influences the synchronisation process.
