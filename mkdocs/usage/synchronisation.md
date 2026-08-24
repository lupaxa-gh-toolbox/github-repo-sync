# Synchronisation

Synchronisation is the core function of **GitHub Repository Sync**.

During a synchronisation run, the application compares your local repository collection with the configuration file and safely performs the operations required to bring the two into alignment.

Every repository is processed independently, allowing problems affecting one repository to be reported without necessarily preventing the remaining repositories from being processed.

## Synchronisation Workflow

Each synchronisation follows the same sequence of operations.

```text
Load Configuration
        │
        ▼
Validate Configuration
        │
        ▼
Discover Repositories
        │
        ▼
Inspect Local Repository
        │
        ▼
Determine Required Action
        │
        ▼
Clone / Update / Skip
        │
        ▼
Record Result
        │
        ▼
Display Summary
```

Each stage must complete successfully before the next begins.

## Configuration Validation

Before any repository operations are performed, the application validates the configuration file.

Validation includes checks such as:

- Required properties.
- Invalid property types.
- Duplicate organisations.
- Duplicate repositories.
- Invalid configuration structure.
- Unsupported values.

If validation fails, synchronisation is aborted before any repositories are modified.

## Repository Discovery

Once the configuration has been validated, the application begins processing the configured organisations and repositories.

For each configured repository it determines whether:

- The repository already exists locally.
- The repository must be cloned.
- The repository can be updated.
- Manual intervention is required.

Each repository is processed independently.

## Cloning Repositories

If a configured repository does not already exist locally, the application clones it into the configured repository directory.

Repositories are organised according to the configuration, typically beneath a common repository root.

## Updating Existing Repositories

When a repository already exists locally, the application inspects its current Git state before attempting an update.

Depending on that state, the repository may be:

- Updated.
- Left unchanged.
- Skipped.

The application does not assume that every repository is safe to update automatically.

If the remote history has been rewritten and no longer shares an ancestor with
the local branch, the repository is skipped as **history-rewritten**. Re-run with
`--recover-rewritten-history` to reset a clean local branch onto the new
upstream tip.

## Safe Synchronisation

One of the primary design goals of GitHub Repository Sync is protecting existing repositories.

Before updating a repository, the application performs a series of safety checks to determine whether synchronisation can proceed safely.

Repositories requiring manual intervention are skipped rather than modified automatically.

This helps prevent accidental loss of local work.

Further information is available in the **Safety Model** documentation.

## Processing Large Repository Collections

Repositories are processed concurrently. Use `--workers` to set the thread
count (default: the number of CPUs). Per-repository results are printed in
the post-load sort (case-insensitive GitHub names), not file order.

The application is designed to scale from small personal collections through to much larger multi-organisation environments.

Each repository is still inspected and decided independently. A problem in one
repository does not stop the others, and the summary reports every outcome.

```bash
grs --workers 8
```

## Progress Reporting

During synchronisation the application reports its progress.

Depending on the repository state, messages may indicate:

- Configuration loading.
- Validation.
- Repository discovery.
- Clone operations.
- Repository inspection.
- Repository updates.
- Skipped repositories.
- Warnings.
- Errors.

When processing has completed, a summary of the overall synchronisation is displayed.

## Error Handling

Errors are handled as close as possible to their source.

Where practical, errors affecting a single repository do not terminate the entire synchronisation process.

Examples include:

- Repository access failures.
- Authentication failures.
- Network errors.
- Git operation failures.
- Configuration problems.

A summary is displayed at the end of the run to help identify any repositories requiring manual attention.

## Best Practices

For reliable synchronisation:

- Validate the configuration before synchronising.
- Commit or stash local changes before updating repositories.
- Resolve repository-specific issues before re-running synchronisation.
- Keep Git authentication up to date.
- Review warnings and errors after each run.

Following these recommendations helps ensure consistent and predictable synchronisation results.

## Next Steps

If you intend to run GitHub Repository Sync unattended or as part of a scheduled workflow, continue to **Automation**.
