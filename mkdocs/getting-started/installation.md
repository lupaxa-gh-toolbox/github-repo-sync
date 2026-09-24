# Installation

```bash
python3 -m pip install lupaxa-github-repo-sync
```

`python3 -m pip` installs the package for that interpreter. The console script is `grs`.

## System Requirements

### Python

GitHub Repository Sync requires:

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

Private repositories need Git authentication before `grs` runs. Supported methods:

- SSH keys.
- Personal Access Tokens (PATs).
- Git Credential Manager.
- Operating system credential stores.

The application uses your existing Git configuration and does not implement its own authentication mechanism.

## Upgrading

To upgrade an existing installation:

```bash
python3 -m pip install --upgrade lupaxa-github-repo-sync
```

## Verifying the Installation

```bash
grs --version
grs --help
```

## Default Configuration Location

Unless another configuration file is specified on the command line, the
application searches the home directory in this order:

```text
~/.github-repo-sync.yaml
~/.github-repo-sync.yml
~/.github-repo-sync.json
~/.github-repo-sync.json5
```

YAML is the default. The file format is specified in [Configuration](../configuration/index.md).

## Virtual Environment

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

Other failures are listed in [Troubleshooting](../reference/troubleshooting.md).
