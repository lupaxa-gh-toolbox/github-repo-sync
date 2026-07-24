---
title: Installation
---

# Installation

This guide explains how to install **Lupaxa GitHub Repository Sync**, verify your installation, and ensure your system is ready to synchronise GitHub repositories.

---

## System Requirements

Before installing the application, ensure your system meets the following minimum requirements.

| Requirement | Version |
| ------------ | ------- |
| Python | 3.11 or later |
| Git | 2.x or later |
| Operating System | macOS, Linux or Windows |

---

## Verify Python

Check that Python is installed.

```bash
python --version
```

or

```bash
python3 --version
```

The output should report Python 3.11 or later.

---

## Verify Git

Ensure Git is available.

```bash
git --version
```

Example output:

```text
git version 2.51.0
```

---

## Install from PyPI

Install the latest released version using `pip`.

```bash
pip install lupaxa-github-repo-sync
```

Alternatively:

```bash
python -m pip install lupaxa-github-repo-sync
```

---

## Upgrade an Existing Installation

To upgrade to the latest release:

```bash
pip install --upgrade lupaxa-github-repo-sync
```

or

```bash
python -m pip install --upgrade lupaxa-github-repo-sync
```

---

## Verify the Installation

After installation, verify that the command-line interface is available.

```bash
github-repo-sync --version
```

Example:

```text
github-repo-sync 1.0.0
```

A shorter command is also provided.

```bash
grs --version
```

Both commands provide identical functionality.

---

## Confirm the Installation Path

If multiple Python versions are installed, you may wish to verify which executable is being used.

### macOS / Linux

```bash
which github-repo-sync
```

or

```bash
which grs
```

### Windows

```powershell
where github-repo-sync
```

---

## Installing Inside a Virtual Environment

Using a virtual environment is recommended when developing or contributing to the project.

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install the package.

```bash
pip install lupaxa-github-repo-sync
```

---

## Installing from Source

Clone the repository.

```bash
git clone https://github.com/the-lupaxa-project/lupaxa-github-repo-sync.git
```

Change into the project directory.

```bash
cd lupaxa-github-repo-sync
```

Install the package in editable mode.

```bash
pip install -e .
```

This is the recommended approach when developing or testing new features.

---

## Installing Development Dependencies

Development dependencies can be installed using the optional extras defined by the project.

```bash
pip install -e ".[dev]"
```

These include tools used during development, such as formatters, linters, type checkers, and test frameworks.

---

## Authentication

The application uses your existing Git configuration for authentication.

No additional login process is required.

Public repositories can normally be cloned without authentication.

Private repositories require an authentication method that Git already recognises, such as:

- SSH keys
- GitHub Personal Access Tokens
- Git Credential Manager
- Existing Git credential helpers

If Git can clone a repository manually, the application will normally be able to clone it as well.

---

## Confirm Everything Works

Run the application.

```bash
github-repo-sync --help
```

You should see the full command-line help.

If the help page appears successfully, the installation is complete.

---

## Troubleshooting

### Command Not Found

If the command cannot be found:

- Verify that the installation completed successfully.
- Ensure your Python scripts directory is included in your `PATH`.
- Restart your terminal after installation.

---

### Incorrect Python Version

If an older Python interpreter is being used, install the package explicitly with the required version.

For example:

```bash
python3.13 -m pip install lupaxa-github-repo-sync
```

---

### Git Not Installed

If Git is unavailable, install Git before continuing.

The application cannot function without Git.

---

## Next Steps

Continue to the **Quick Start** guide to create your first configuration and perform your first repository synchronisation.
