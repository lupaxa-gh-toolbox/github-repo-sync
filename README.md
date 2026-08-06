<p align="center">
    <a href="https://github.com/lupaxa-gh-toolbox">
        <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/gh-toolbox/readme-logo.png" alt="Organisation Logo" />
    </a>
</p>

<h1 align="center">Lupaxa GitHub Repository Sync</h1>

Safely clone and synchronise large collections of GitHub repositories from a single declarative configuration.

## Overview

**Lupaxa GitHub Repository Sync** is a command-line application that clones, organises, and safely synchronises GitHub repositories using a declarative JSON5
configuration file.

Unlike many repository synchronisation tools, it does not assume every repository can be updated automatically. Instead, each repository is inspected before
any Git operation is performed, ensuring that only repositories confirmed to be in a safe state are modified.

The application is suitable for managing anything from a handful of repositories to several hundred repositories across multiple GitHub organisations.

Synchronisation is the default operation. Running the application without an alternative operating mode validates the configuration, inspects each configured
repository, clones any missing repositories, and safely updates existing repositories where appropriate.

## Features

- Safe repository inspection before synchronisation.
- Automatic cloning of missing repositories.
- Fast-forward updates where safe.
- Protection against repositories with unsafe local states.
- Support for HTTPS and SSH clone protocols.
- JSON5 configuration with inherited defaults.
- Multiple GitHub organisation support.
- Organisation and repository aliases.
- Configurable repository destinations.
- Rich console output with progress reporting.
- Compact configuration validation.
- Synchronisation plan preview.
- Detailed synchronisation result tables.
- Cross-platform support for macOS, Linux, and Windows.
- Suitable for interactive use, automation, and scheduled execution.

## Installation

Install the latest release from PyPI.

```bash
pip install lupaxa-github-repo-sync
```

Verify the installation.

```bash
grs --version
```

or

```bash
github-repo-sync --version
```

The shorter `grs` command is used throughout the remainder of this document.

## Quick Start

Create a configuration file.

```json5
{
  clone_path: "~/Development",

  organisations: [

    {
      name: "the-lupaxa-project",

      repositories: [

        { name: "github" },
        { name: "workflows" },
        { name: "brand-assets" }

      ]
    }

  ]
}
```

Validate the configuration.

```bash
grs --validate
```

Review the synchronisation plan.

```bash
grs --plan
```

Synchronise your repositories.

```bash
grs
```

## Command-Line Interface

Lupaxa GitHub Repository Sync uses a simple flat command-line interface.

Repository synchronisation is the default operation. Alternative operating modes allow you to inspect or validate your configuration without modifying any
repositories.

### Operating Modes

| Command          | Description                                         |
| :--------------- | :-------------------------------------------------- |
| `grs`            | Synchronise all configured repositories.            |
| `grs --validate` | Validate the configuration and exit.                |
| `grs --plan`     | Display the resolved synchronisation plan and exit. |

### Configuration

| Option                     | Description                                 |
| :------------------------- | :------------------------------------------ |
| `-c FILE`, `--config FILE` | Use the specified JSON5 configuration file. |

> [!NOTE]
> If `--config` is not specified, the application looks for the default configuration file in the users home directory.
> Default config file is called `.github-repo-sync.json5`.

### Presentation

| Option                    | Description                            |
| :------------------------ | :------------------------------------- |
| `--no-header`             | Do not display the application header. |
| `--no-colour`             | Disable coloured console output.       |
| `--console-width COLUMNS` | Override the console width.            |
| `--version`               | Display the application version.       |

### Synchronisation Output

| Option                   | Description                                    |
| :----------------------- | :--------------------------------------------- |
| `--no-configuration`     | Do not display the configuration summary.      |
| `--no-progress`          | Disable the repository progress display.       |
| `--no-repository-output` | Suppress per-repository status messages.       |
| `--results-table`        | Display the detailed repository results table. |
| `--no-failure-table`     | Do not display the failure table.              |
| `--no-summary-table`     | Do not display the Rich summary table.         |

### Examples

Validate a configuration file.

```bash
grs --validate
```

Validate a different configuration file.

```bash
grs --config repositories.json5 --validate
```

Display the synchronisation plan.

```bash
grs --plan
```

Synchronise repositories using the default configuration.

```bash
grs
```

Synchronise repositories using an alternative configuration.

```bash
grs --config work.json5
```

Synchronise repositories without displaying progress.

```bash
grs --no-progress
```

Display the detailed repository results table after synchronisation.

```bash
grs --results-table
```

Run quietly without displaying the configuration summary.

```bash
grs --no-configuration --no-progress
```

## Documentation

Complete documentation is available in the `docs` directory and can also be published using MkDocs.

The documentation includes:

- Getting Started
- Installation
- Configuration Guide
- Configuration Reference
- Configuration Examples
- Command Reference
- Synchronisation Guide
- Repository Safety Model
- Automation
- Architecture
- Troubleshooting
- Frequently Asked Questions
- Development Guide

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
