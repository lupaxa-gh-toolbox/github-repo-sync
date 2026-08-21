# Commands

GitHub Repository Sync is operated using the `grs` command-line application.

Every command follows the same high-level workflow:

1. Load the configuration.
2. Validate the configuration.
3. Perform the requested operation.
4. Display a summary.
5. Return an appropriate exit code.

The application has been designed to provide predictable behaviour, clear feedback and meaningful exit codes suitable for both interactive use and automation.

> **Important**
>
> The commands shown in this document reflect the current release of the application. Use `grs --help` to display the commands and options available in your installed version.

## General Syntax

The general command syntax is:

```text
grs [OPTIONS]
```

Some options are only valid with a specific operating mode (for example, `--ignore-clean` requires `--status`).

## Display Help

Display the built-in help:

```bash
grs --help
```

This displays the available commands, global options and a brief description of each.

## Display the Installed Version

Display the installed application version:

```bash
grs --version
```

The version displayed is taken directly from the installed package metadata.

## Using an Alternative Configuration File

By default, the application loads:

```text
~/.github-repo-sync.yaml
```

If you need to use a different configuration file, specify it using the appropriate command-line option.

This is useful when maintaining multiple synchronisation environments.

## Validating a Configuration

Before synchronising repositories, validate the configuration:

```bash
grs --validate
```

Validation checks the entire configuration for problems including:

- Missing required properties.
- Invalid values.
- Invalid property types.
- Duplicate organisations.
- Duplicate repositories.
- Invalid configuration structure.

If validation fails, synchronisation does not begin.

## Checking Repository Status

Check whether configured repositories are clean and synchronised with their upstream branches. This mode does not change working trees, branches, or commits; in online mode it may `git fetch` to update remote-tracking refs
(use `--offline` to skip fetch):

```bash
grs --status
```

A repository is considered **clean** when it has a healthy local layout, a clean working tree, and its current branch matches the configured upstream tracking branch (neither ahead nor behind).

Repositories that are missing, dirty, detached, rewritten on the remote with no shared ancestor, or otherwise unsuitable for synchronisation are reported as not clean.

Status checks report a dirty working tree before comparing commits, so a repository that is both dirty and ahead is reported as **dirty**.

By default, the status check runs in **online** mode and fetches from each repository's `origin` remote before comparing local commits with the upstream branch.

Skip fetching and compare against existing remote-tracking refs instead:

```bash
grs --status --offline
```

Omit fully clean repositories from the per-repository output and results table (the summary still counts all configured repositories):

```bash
grs --status --ignore-clean
```

Combine both options when you want a compact report of only repositories that need attention:

```bash
grs --status --ignore-clean --offline
```

Exit codes for status checks:

- `0` — every configured repository is clean and synchronised.
- `1` — one or more repositories are not clean.
- `3` — the configuration could not be validated.

## Synchronising Repositories

To synchronise repositories:

```bash
grs
```

The application performs the following steps:

1. Loads the configuration.
2. Validates the configuration.
3. Inspects each configured repository.
4. Clones repositories that do not already exist.
5. Updates repositories where it is safe to do so.
6. Skips repositories that require manual intervention.
7. Displays a summary of the results.

If a remote branch was rewritten (for example with `git-reset-history`) and the
local clone shares no ancestor with the new history, the repository is skipped as
**history-rewritten**. Detect this with `grs --status`. To reset a *clean* local
branch onto the new upstream tip:

```bash
grs --recover-rewritten-history
```

This flag is only valid during synchronisation. Dirty working trees are still skipped.

## Exit Codes

Every command returns an exit code indicating the overall result.

Typical outcomes include:

- Successful completion.
- Validation failure.
- Synchronisation failure.
- Unexpected internal error.

A complete list of exit codes is available in the **Reference** section.

## Command Output

During execution the application reports progress describing the work being performed.

Depending on the command, output may include:

- Configuration loading.
- Validation results.
- Repository discovery.
- Clone operations.
- Repository updates.
- Warnings.
- Errors.
- Final summary information.

The amount of output depends on the command and any selected options.

## Getting Help

If a command does not behave as expected:

1. Verify that the configuration is valid.
2. Confirm that Git is installed.
3. Ensure that GitHub authentication is correctly configured.
4. Review any error messages displayed by the application.
5. Consult the **Troubleshooting** guide.

## Next Steps

Continue to **Synchronisation** to learn how GitHub Repository Sync inspects repositories, determines the required actions and performs safe updates.
