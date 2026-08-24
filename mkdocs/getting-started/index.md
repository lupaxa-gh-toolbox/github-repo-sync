# Getting Started

Welcome to the **Getting Started** guide for **GitHub Repository Sync**.

This section introduces the application and walks you through everything required to install it, configure it and perform your first repository synchronisation.

Whether you are managing a single GitHub organisation or hundreds of repositories across multiple organisations, this guide provides the knowledge required to
get up and running quickly and safely.

## What You Will Learn

The Getting Started guide covers:

- Installing GitHub Repository Sync.
- Verifying your installation.
- Understanding the application requirements.
- Creating your first configuration file.
- Performing your first synchronisation.
- Learning where to find more detailed documentation.

By the end of this section you will have a working installation and understand the basic workflow used by the application.

## Prerequisites

Before installing the application, ensure that your environment includes:

- Python 3.11 or later.
- Git installed and available on your system `PATH`.
- Access to GitHub.
- Appropriate authentication for any private repositories you intend to synchronise.

You should also decide where your local repository collection will be stored.

## Installation

GitHub Repository Sync is distributed as a standard Python package and installs a command-line application named `grs`.

The installation guide explains how to:

- Install the application.
- Verify that the installation completed successfully.
- Confirm the installed version.
- Upgrade to newer releases.
- Remove the application if required.

Continue to **Installation** for the complete installation process.

## Configuration

The application is configured using a YAML, JSON, or JSON5 configuration file.

Unless another location is specified on the command line, the application
searches the home directory in this order:

```text
~/.github-repo-sync.yaml
~/.github-repo-sync.yml
~/.github-repo-sync.json
~/.github-repo-sync.json5
```

The configuration file defines:

- The local directory used to store repositories.
- The GitHub organisations to synchronise.
- The repositories that should be managed.
- Synchronisation behaviour and application options.

YAML is the default and recommended format. JSON and JSON5 remain supported.
YAML and JSON5 allow comments; JSON5 also allows trailing commas and unquoted
object keys.

## Typical Workflow

A typical synchronisation workflow consists of the following steps:

1. Install the application.
2. Create the configuration file.
3. Define the organisations and repositories to synchronise.
4. Validate the configuration.
5. Review the planned operations.
6. Run the synchronisation.
7. Review the final summary.

Before any repository operations are performed, the application validates the configuration and checks that repositories are in a safe state to be updated.

## Documentation Structure

Once you have completed this section, the remainder of the documentation is organised into the following areas:

- **Configuration** explains every available configuration option.
- **Usage** describes the available commands and synchronisation behaviour.
- **Concepts** explains the application's internal design and safety model.
- **Reference** contains troubleshooting guidance, exit codes and frequently asked questions.
- **Development** provides information for contributors and maintainers.

## Safety First

Protecting existing repositories and local changes is one of the primary design goals of GitHub Repository Sync.

Before updating an existing repository, the application inspects its current state to ensure that synchronisation can be performed safely.

More information is available in the **Safety Model** documentation.

## Next Steps

Continue to **Installation** to install GitHub Repository Sync and prepare your system for your first synchronisation.
