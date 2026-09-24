# Getting Started

Install the package, write a configuration file, validate it, then run `grs`.

## Requirements

- Python 3.11 or later.
- Git on `PATH`.
- Git credentials for private repositories.

[Installation](installation.md) covers install, upgrade, and uninstall.

## Configuration File

If `--config` is omitted, `grs` searches the home directory in this order:

```text
~/.github-repo-sync.yaml
~/.github-repo-sync.yml
~/.github-repo-sync.json
~/.github-repo-sync.json5
```

YAML is the default. JSON and JSON5 are accepted. YAML and JSON5 allow comments. JSON5 also allows trailing commas and unquoted keys.

The file sets `clone_path`, the GitHub organisations, and the repositories to manage. An organisation alias is a single directory name or a relative path under `clone_path`. A repository alias is a single directory name.

Property definitions are in the [Configuration Guide](../configuration/configuration-guide.md) and the [Configuration Reference](../configuration/configuration-reference.md).

## First Run

[Quick Start](quick-start.md) is a minimal configuration and the commands that validate and synchronise it.

```bash
grs --validate
grs --plan
grs
```

`grs` validates the configuration, inspects each repository, clones those that are missing, fast-forwards those that are safe to update, and skips the rest. Skip rules are in the [Safety Model](../usage/safety-model.md).
