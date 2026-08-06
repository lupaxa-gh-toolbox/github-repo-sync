# Quick Start

This guide walks you through creating a minimal configuration and performing your first repository synchronisation.

By the end of this guide you will have:

- Created a configuration file.
- Configured a local repository directory.
- Added a GitHub organisation.
- Validated the configuration.
- Performed your first synchronisation.

## Step 1: Create the Configuration File

Unless another configuration file is specified on the command line, Lupaxa GitHub Repository Sync automatically loads:

```text
~/.github-repo-sync.json5
```

Create the file if it does not already exist.

## Step 2: Create a Basic Configuration

The following example demonstrates the smallest practical configuration.

> **Note**
>
> The exact configuration schema is documented in the **Configuration Reference**. This example is intended only to demonstrate the basic structure.

```json5
{
  // Base directory used to store cloned repositories.
  base_directory: "~/Development",

  organisations: [
    {
      name: "the-lupaxa-project",

      repositories: [
        {
          name: "workflows"
        },
        {
          name: "brand-assets"
        }
      ]
    }
  ]
}
```

## Step 3: Verify the Installation

Confirm that the application is installed correctly.

```bash
grs --version
```

You can also display the available command-line options.

```bash
grs --help
```

## Step 4: Validate Your Configuration

Before synchronising repositories, validate that your configuration is correct.

```bash
grs validate
```

If validation succeeds, you are ready to perform your first synchronisation.

If validation reports errors, correct them before continuing.

## Step 5: Synchronise Your Repositories

Run the synchronisation.

```bash
grs sync
```

The application will:

1. Load the configuration.
2. Validate the configuration.
3. Inspect each configured repository.
4. Clone repositories that do not already exist.
5. Update repositories that can be safely synchronised.
6. Skip repositories that require manual intervention.
7. Display a summary when processing has completed.

## Understanding the Output

During synchronisation the application provides progress information describing the work being performed.

Depending on the state of each repository you may see operations such as:

- Repository discovery.
- Repository cloning.
- Fetching remote changes.
- Fast-forward updates.
- Repository skipped.
- Validation warnings.
- Error messages.

At the end of the run a summary is displayed showing the overall result.

## Where to Go Next

Once you have successfully synchronised your repositories, the following documentation is recommended:

- **Configuration Guide** to learn about all available configuration options.
- **Commands** for the complete command-line reference.
- **Synchronisation** to understand how repositories are processed.
- **Safety Model** to understand how the application protects existing repositories.

## Need Help?

If your first synchronisation does not behave as expected, consult the **Troubleshooting** guide for common problems and recommended solutions.
