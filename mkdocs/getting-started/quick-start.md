---
title: Quick Start
---

# Quick Start

This guide walks through the quickest way to get **Lupaxa GitHub Repository Sync** up and running.

By the end of this guide you will have:

- Created your first configuration file.
- Validated the configuration.
- Cloned one or more GitHub repositories.
- Performed your first synchronisation.
- Understood the output produced by the application.

The examples in this guide are intentionally simple. More advanced configuration options are covered later in the documentation.

---

## Step 1 - Create a Working Directory

Choose a directory where your GitHub repositories will be stored.

For example:

```text
~/Development/
```

or

```text
C:\Development\
```

The application will automatically organise repositories beneath this directory by GitHub organisation.

---

## Step 2 - Create a Configuration File

Create a new file named `config.json5`.

A minimal configuration might look like this:

```json5
{
  clone_path: "~/Development",

  organisations: [

    {
      name: "the-lupaxa-project",

      repositories: [

        {
          name: "github"
        },

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

This configuration tells the application to:

- Store repositories beneath `~/Development`.
- Clone repositories from the `the-lupaxa-project` GitHub organisation.
- Manage three repositories.

---

## Step 3 - Validate the Configuration

Before synchronising repositories, validate the configuration file.

```bash
github-repo-sync validate
```

or specify the configuration explicitly.

```bash
github-repo-sync validate --config config.json5
```

If the configuration is valid, a confirmation message will be displayed.

If any errors are found, they should be corrected before continuing.

---

## Step 4 - Review the Configuration

Display the repositories defined in the configuration.

```bash
github-repo-sync list
```

Typical output might resemble:

```text
Organisation: the-lupaxa-project

  • github
  • workflows
  • brand-assets
```

This provides a quick opportunity to confirm that the correct repositories will be synchronised.

---

## Step 5 - Synchronise Repositories

Run the synchronisation.

```bash
github-repo-sync
```

or

```bash
grs
```

During execution the application will:

1. Load the configuration.
2. Validate the configuration.
3. Create missing organisation directories.
4. Clone repositories that do not already exist.
5. Inspect existing repositories.
6. Update repositories that are safe to synchronise.
7. Skip repositories requiring manual attention.
8. Produce a summary report.

---

## Example Output

A successful synchronisation might produce output similar to:

```text
Loading configuration...
✓ Configuration loaded

Inspecting repositories...
✓ github
✓ workflows
✓ brand-assets

Summary

Repositories processed : 3
Repositories updated   : 2
Repositories cloned    : 1
Repositories skipped   : 0
Errors                 : 0
```

The exact formatting will vary depending on your selected output style and terminal capabilities.

---

## Understanding Skipped Repositories

Not every repository can be updated safely.

For example, repositories may be skipped because they contain:

- Local modifications.
- Untracked files.
- Detached HEAD states.
- Diverged branches.
- Incorrect remotes.
- Missing upstream branches.

This behaviour is intentional.

Rather than risking unexpected changes, the application reports these repositories and leaves them unchanged.

---

## Typical Directory Structure

After synchronisation your directory might resemble:

```text
~/Development/
└── the-lupaxa-project/
    ├── brand-assets/
    ├── github/
    └── workflows/
```

As additional organisations are added, each receives its own directory beneath the configured clone path.

---

## What's Next?

Now that you have successfully synchronised your first repositories, you can begin exploring the more advanced capabilities of the application.

The next section explains how the configuration system works in detail, including:

- Global settings.
- Organisation-level options.
- Repository overrides.
- Clone protocols.
- Custom destination directories.
- Future configuration features.

Continue to the **Configuration Guide** to learn how to build larger and more flexible configurations.
