---
title: Installation
---

# Installation

This guide explains how to install **Lupaxa GitHub Repository Sync**, verify your installation and ensure your environment is correctly configured before
performing your first synchronisation.

## System Requirements

Before installing the application, ensure that your system meets the following requirements.

### Python

Lupaxa GitHub Repository Sync requires:

- Python 3.11 or later.

Verify your installed version:

```bash
python3 --version
```

### Git

Git must be installed and available on your system `PATH`.

Verify your installation:

```bash
git --version
```

If Git is not installed, refer to the official Git documentation for installation instructions appropriate for your operating system.

### GitHub Access

You should ensure that you can access any repositories you intend to synchronise.

For private repositories, configure Git authentication before using the application. Supported authentication methods include:

- SSH keys.
- Personal Access Tokens (PATs).
- Git Credential Manager.
- Operating system credential stores.

The application uses your existing Git configuration and does not implement its own authentication mechanism.

## Installing from PyPI

Install the latest stable release using `pip`:

```bash
python3 -m pip install lupaxa-github-repo-sync
```

Using `python3 -m pip` ensures that the package is installed for the intended Python interpreter.

## Upgrading

To upgrade an existing installation:

```bash
python3 -m pip install --upgrade lupaxa-github-repo-sync
```

## Verifying the Installation

Confirm that the application has been installed successfully:

```bash
grs --version
```

The command should display the installed version of **Lupaxa GitHub Repository Sync**.

You can also display the available command-line options:

```bash
grs --help
```

## Default Configuration Location

Unless another configuration file is specified on the command line, the application automatically loads:

```text
~/.github-repo-sync.json5
```

This file contains the organisations, repositories and synchronisation options used by the application.

Detailed information about the configuration format is provided in the **Configuration** section of this documentation.

## Installing in a Virtual Environment

Although not required, installing the application inside a Python virtual environment is recommended when working on development systems.

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it.

On Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Install the application:

```bash
python3 -m pip install lupaxa-github-repo-sync
```

## Uninstalling

To remove the application:

```bash
python3 -m pip uninstall lupaxa-github-repo-sync
```

## Troubleshooting Installation

If installation fails:

- Verify that Python 3.11 or later is installed.
- Verify that Git is installed and available on the system `PATH`.
- Ensure that `pip` is up to date.
- Confirm that the `grs` command is available after installation.
- Verify that your GitHub authentication is working if you intend to synchronise private repositories.

Further troubleshooting guidance is available in the **Reference** section of this documentation.

## Next Steps

Once the application has been installed successfully, continue to **Quick Start** to create your first configuration file and perform your first synchronisation.
