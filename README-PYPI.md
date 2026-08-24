<!-- markdownlint-disable -->
<p align="center">
  <a href="https://github.com/lupaxa-gh-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/gh-toolbox/readme-logo.png" alt="Project Logo" width="256"/><br/>
  </a>
</p>
<h3 align="center">
  The Lupaxa GitHub Toolbox<br />
  Part of The Lupaxa Project
</h3>

<br />

# lupaxa-github-repo-sync

A command-line application that **clones**, **organises**, and **safely synchronises** large collections of GitHub repositories from a single declarative YAML, JSON, or JSON5 configuration.

Unlike many repository synchronisation tools, it does not assume every repository can be updated automatically. Each repository is inspected before any Git operation, so only repositories in a safe state are modified.

## Features

- Safe repository inspection before synchronisation
- Automatic cloning of missing repositories
- Fast-forward updates where safe
- Protection against unsafe local states
- HTTPS and SSH clone protocols
- YAML, JSON, or JSON5 configuration with inherited defaults
- Multiple GitHub organisations, aliases, and destination paths
- Concurrent clone, update, and status checks (`--workers`, default: CPU count)
- Ordered per-repository output (alphabetical by GitHub name after load)
- Rich console output with progress reporting
- Configuration validation and synchronisation plan preview
- Status check (optional fetch of tracking refs)
- Transient GitHub SSH retries during bulk sync
- Cross-platform: macOS, Linux, and Windows

## Installation

### From PyPI

```bash
pip install lupaxa-github-repo-sync
```

Verify the installation:

```bash
grs --version
```

or:

```bash
github-repo-sync --version
```

The shorter `grs` command is used in the examples below.

### From source (development mode)

```bash
pip install -e ".[dev]"
```

## Quick Start

Create `~/.github-repo-sync.yaml`:

```yaml
config:
  clone_path: ~/Desktop/GitMaster
  clone_protocol: ssh

organisations:
  - name: the-lupaxa-project
    alias: Lupaxa/TheLupaxaProject
    repositories:
      - name: .github
        alias: github
      - name: workflows
      - name: brand-assets
```

Local layout resolves to `clone_path/<organisation-alias>/<repository-alias-or-name>`.

Organisation aliases may be a single directory name or a relative path under `clone_path`. Repository aliases must remain a single directory name.

If `--config` is not specified, the application looks for
`~/.github-repo-sync.yaml`, then `.yml`, then `.json`, then `.json5`. Config
files may be YAML, JSON, or JSON5.

Validate the configuration:

```bash
grs --validate
```

Review the synchronisation plan:

```bash
grs --plan
```

Synchronise your repositories:

```bash
grs
```

## Command-Line Interface

Synchronisation is the default operation.

| Command          | Description                                                                 |
| ---------------- | --------------------------------------------------------------------------- |
| `grs`            | Synchronise all configured repositories.                                    |
| `grs --validate` | Validate the configuration and exit.                                        |
| `grs --plan`     | Display the resolved synchronisation plan and exit.                         |
| `grs --status`   | Check repositories for a clean, synchronised state (may fetch tracking refs). |

Use `-c FILE` / `--config FILE` to point at a different YAML, JSON, or JSON5 file.

```bash
grs --config work.yaml --validate
grs --status --ignore-clean --offline
grs --recover-rewritten-history
grs --workers 8
grs --results-table
```

## Documentation

Online documentation:

[Documentation](https://github-repo-sync.thelupaxaproject.org/)

Serve the docs locally:

```bash
mkdocs serve
```

Then open the local URL printed by MkDocs in your browser.

## Development

Clone the repository and install development dependencies:

```bash
pip install -e ".[dev]"
```

Useful make targets:

```bash
make test   # run tests
make type   # type checking (mypy)
make check  # lint, type check, and tests
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
