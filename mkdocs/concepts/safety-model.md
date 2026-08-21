# Safety Model

One of the primary design goals of **GitHub Repository Sync** is to protect your repositories from unintended or destructive changes.

Unlike tools that blindly execute Git commands, GitHub Repository Sync evaluates the state of every repository before deciding whether it is safe to perform a synchronisation.

If the application cannot safely determine what action should be taken, it will stop processing that repository and report the reason to the user.

## Design Principles

The safety model is built around a small number of principles.

- Never overwrite local work.
- Never assume a repository is in a valid state.
- Validate before performing actions.
- Make every decision predictable.
- Prefer skipping a repository over risking data loss.
- Clearly report why an action was or was not taken.

These principles apply throughout every synchronisation run.

## Repository Inspection

Before performing any Git operations, the application inspects each repository.

Typical checks may include:

- Whether the repository exists.
- Whether the directory is a valid Git repository.
- The configured remote repository.
- The current branch.
- The working tree status.
- The availability of the remote repository.

Only after these checks have completed can the application determine the appropriate action.

## Safe Decision Making

Every repository is evaluated independently.

Depending on its current state, the application may decide to:

- Clone the repository.
- Update the repository.
- Leave the repository unchanged.
- Skip the repository.
- Report an error.

The decision made for one repository does not affect the processing of any other repository.

## Non-Destructive Behaviour

The application has been designed to avoid destructive Git operations.

For example, it does not automatically:

- Delete repositories.
- Reset local branches.
- Force checkout another branch.
- Force push changes.
- Discard local commits.
- Remove untracked files.

The one exception is `--recover-rewritten-history`, which hard-resets a *clean* local branch onto rewritten remote history (no shared ancestor). Without that flag those repositories are skipped.

Any operation that could potentially result in data loss is intentionally avoided.

## Validation Before Action

Safety begins before repository processing.

The application validates the configuration before attempting to access any repositories.

If configuration validation fails:

- Repository processing does not begin.
- No repositories are modified.
- Validation errors are reported to the user.

This helps prevent problems caused by invalid or incomplete configuration files.

## Repository Isolation

Repositories are processed independently.

If one repository encounters an error, the application attempts to continue processing the remaining repositories wherever possible.

This provides two important benefits:

- A single failure does not necessarily terminate the entire synchronisation.
- The final summary provides a complete picture of the overall synchronisation.

## Clear Reporting

Whenever the application decides not to perform an operation, it reports the reason.

Examples include:

- Validation errors.
- Repository access failures.
- Authentication problems.
- Repository state prevents synchronisation.
- Network failures.
- Git operation failures.

Providing clear feedback helps users resolve problems without having to investigate the application's internal behaviour.

## Why Repositories May Be Skipped

Skipping a repository should not be considered a failure.

Instead, it indicates that the application determined that automatic synchronisation could not be completed safely.

Typical reasons include:

- Manual intervention is required.
- The repository is not in an expected state.
- A required resource is unavailable.
- An operation could not be completed safely.

Once the underlying issue has been resolved, the repository can be synchronised during the next run.

## Summary

The safety model is central to the design of GitHub Repository Sync.

By validating configuration, inspecting every repository and avoiding destructive Git operations, the application provides a predictable and reliable way to
manage large collections of GitHub repositories while protecting existing local work.

## Next Steps

Continue to **Repository States** to learn how the application classifies repositories and how those classifications influence synchronisation decisions.
