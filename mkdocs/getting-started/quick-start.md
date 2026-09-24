# Quick Start

Create `~/.github-repo-sync.yaml`, validate it, then run `grs`.

## Step 1: Create the Configuration File

Unless another configuration file is specified on the command line, GitHub
Repository Sync searches the home directory in this order:

```text
~/.github-repo-sync.yaml
~/.github-repo-sync.yml
~/.github-repo-sync.json
~/.github-repo-sync.json5
```

Create `~/.github-repo-sync.yaml` if it does not already exist. YAML is the
default and recommended format.

## Step 2: Create a Basic Configuration

Property definitions are in the [Configuration Reference](../configuration/configuration-reference.md).

```yaml
config:
  # Base directory used to store cloned repositories.
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

Organisation aliases may be a single directory name or a relative path under `clone_path`. Repository aliases must be a single directory name.

## Step 3: Verify the Installation

```bash
grs --version
```

```bash
grs --help
```

## Step 4: Validate Your Configuration

```bash
grs --validate
```

Preview the resolved plan:

```bash
grs --plan
```

## Step 5: Synchronise Your Repositories

```bash
grs
```

To process several repositories at once (default is the CPU count):

```bash
grs --workers 8
```

The application will:

1. Load the configuration.
2. Validate the configuration.
3. Inspect each configured repository.
4. Clone repositories that do not already exist.
5. Update repositories that can be safely synchronised.
6. Skip repositories that require manual intervention.
7. Display a summary when processing has completed.

Per-repository lines report discovery, clone, fetch, fast-forward, skip, validation warnings, and errors. Failures during a first run are listed in [Troubleshooting](../reference/troubleshooting.md).
