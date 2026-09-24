# Repository States

`grs` inspects each configured repository and picks one action from that state: clone, fast-forward, skip, or report an error. Repositories are evaluated independently. The checks that make an update safe are in the [Safety Model](safety-model.md).

## Repository Processing Workflow

Every repository follows the same high-level workflow.

```text
Repository
     │
     ▼
Inspect Repository
     │
     ▼
Determine Current State
     │
     ▼
Select Appropriate Action
     │
     ▼
Clone • Update • Skip • Report Error
```

Each repository is processed independently.

## Repository Does Not Exist

If the configured repository does not exist locally, the application prepares the destination directory and clones the repository.

This is the simplest state and normally requires no user intervention.

Typical action:

- Clone the repository.

## Repository Exists

If the repository already exists locally, the application performs additional inspection before deciding whether synchronisation can continue.

Typical checks include:

- Is the directory a valid Git repository?
- Is the expected remote configured?
- Is the repository accessible?
- Is the repository in a state suitable for synchronisation?

The results of these checks determine the next action.

## Repository Can Be Updated

If the repository passes all safety checks, the application performs the required synchronisation.

Typical action:

- Fetch remote changes.
- Perform a safe update.
- Record the result.

## Repository Requires Manual Intervention

Some repository states cannot be resolved automatically.

Examples may include:

- Unexpected repository configuration.
- Repository corruption.
- Authentication failures.
- Network failures.
- Rewritten remote history with no shared ancestor.
- Repository-specific Git errors.

A rewritten remote (for example after `git-reset-history`) is reported as **history-rewritten**. Default synchronisation skips it. Use `--recover-rewritten-history` only when you intend to discard the old local history on a clean working tree.

In these situations, the application skips the repository and reports the reason.

## Repository Is Skipped

Skipping a repository does not necessarily indicate an error.

Instead, it means the application determined that automatic synchronisation could not be completed safely.

Skipping one repository does not prevent the remaining repositories from being processed.

## Independent Processing

A failure on one repository does not stop the others. The summary lists every repository.

## Summary Reporting

After every repository has been processed, the application displays a summary describing the outcome.

Depending on the synchronisation, the summary may include:

- Repositories cloned.
- Repositories updated.
- Repositories skipped.
- Errors encountered.
- Overall success or failure.

The checks behind those states are in the [Safety Model](safety-model.md).
