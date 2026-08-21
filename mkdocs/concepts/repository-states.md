# Repository States

Before any synchronisation takes place, **GitHub Repository Sync** inspects each configured repository to determine its current state.

The state of a repository determines what action, if any, the application will perform. This process ensures that repositories are only modified when it is safe to do so.

Every repository is evaluated independently, allowing the application to make the most appropriate decision for each repository without affecting the processing of others.

## Why Repository States Matter

Not every repository requires the same action.

For example, a repository may:

- Not exist locally.
- Already be up to date.
- Require an update.
- Contain local changes.
- Be inaccessible.
- Require manual intervention.

Rather than applying the same operation to every repository, GitHub Repository Sync determines the current state before deciding what to do.

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

## Repository Processing Is Independent

Each repository is processed independently from every other repository.

This provides several advantages:

- A failure affecting one repository does not necessarily stop the synchronisation.
- Progress continues wherever possible.
- The final summary accurately reflects the state of every repository.

This behaviour is particularly important when synchronising large collections of repositories.

## Summary Reporting

After every repository has been processed, the application displays a summary describing the outcome.

Depending on the synchronisation, the summary may include:

- Repositories cloned.
- Repositories updated.
- Repositories skipped.
- Errors encountered.
- Overall success or failure.

This provides a clear overview of the synchronisation without requiring the user to inspect every individual repository.

## Relationship to the Safety Model

Repository states form part of the application's overall safety model.

The current state of a repository is used to determine whether synchronisation can proceed safely or whether manual intervention is required.

Further information is available in the **Safety Model** documentation.

## Next Steps

Continue to **Architecture** for an overview of the application's internal structure and the components responsible for configuration, validation and synchronisation.
