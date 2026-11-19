# Configuration Reference

The configuration file is YAML, JSON, or JSON5. It is validated
before any synchronisation operations begin. YAML is the default and
recommended format.

Unless another configuration file is specified on the command line, the
application searches `~/.config/github-repo-sync/` and then the home directory:

```text
~/.config/github-repo-sync/github-repo-sync.yaml
~/.config/github-repo-sync/github-repo-sync.yml
~/.config/github-repo-sync/github-repo-sync.json
~/.config/github-repo-sync/github-repo-sync.json5
~/.github-repo-sync.yaml
~/.github-repo-sync.yml
~/.github-repo-sync.json
~/.github-repo-sync.json5
```

> **Important**
>
> This reference describes the configuration schema used by the application. Every property is validated before synchronisation begins. If validation fails, no repository operations are performed.

## Configuration Overview

A configuration consists of:

- Global settings under `config`.
- One or more GitHub organisations.
- One or more repositories within each organisation.

The overall structure resembles the following:

```text
Configuration
│
├── config
│   ├── clone_path
│   └── clone_protocol
│
└── organisations
    ├── Organisation
    │   ├── name
    │   ├── alias
    │   ├── clone_path
    │   └── repositories
    │
    └── Organisation
        └── ...
```

## Root Properties

| Property         | Required | Description                                      |
| ---------------- | -------- | ------------------------------------------------ |
| `config`         | Yes      | Global synchronisation settings.                 |
| `organisations`  | Yes      | List of GitHub organisations to synchronise.     |

## `config` Properties

| Property          | Required | Description                                                                 |
| ----------------- | -------- | --------------------------------------------------------------------------- |
| `clone_path`      | Yes      | Local root directory under which organisations and repositories are stored. |
| `clone_protocol`  | Yes      | Default clone protocol for repositories (`ssh` or `https`).                 |

`clone_path` supports `~` expansion and environment variables.

## Organisation Properties

Each organisation represents a GitHub organisation whose repositories should be managed.

| Property        | Required | Description                                                                 |
| --------------- | -------- | --------------------------------------------------------------------------- |
| `name`          | Yes      | GitHub organisation login.                                                  |
| `alias`         | No       | Local destination under the effective `clone_path`.                         |
| `clone_path`    | No       | Root for this organisation. Overrides `config.clone_path`.                  |
| `repositories`  | Yes      | One or more repository definitions.                                         |

The same GitHub organisation may be listed more than once. Each repository may appear only once for that organisation.

### Organisation `alias`

When omitted, the local organisation directory is the GitHub organisation `name`.

When set, the alias becomes the organisation destination under `clone_path`. It may be:

- A single directory name, for example `TheLupaxaProject`.
- A relative path, for example `Lupaxa/TheLupaxaProject`.

Relative path aliases allow one configuration to place organisations into different local trees under the same `clone_path`.

Alias validation rules:

- Must not be empty.
- Must be relative (no leading `/`).
- Must not end with `/`.
- Must not contain `\` separators.
- Must not contain empty path segments.
- Must not contain `..` path segments.
- `.` is allowed only as the whole alias. Repositories are then placed directly under the effective `clone_path`.

A repeated repository for one GitHub organisation, and organisations that resolve to the same local directory, are reported as validation errors.

## Repository Properties

Each repository entry describes a single GitHub repository.

| Property          | Required | Description                                                                   |
| ----------------- | -------- | ----------------------------------------------------------------------------- |
| `name`            | Yes      | GitHub repository name.                                                       |
| `alias`           | No       | Local directory name for the repository.                                      |
| `clone_path`      | No       | Root for this repository. Overrides the organisation and `config.clone_path`. |
| `clone_protocol`  | No       | Per-repository protocol override (`ssh` or `https`).                          |

Repository names must be unique within an organisation.

### Repository `alias`

When omitted, the local repository directory is the GitHub repository `name`.

When set, the alias must be a single directory name (not a path). This is typically used when the GitHub name is unsuitable as a folder name:

```yaml
name: .github
alias: github
```

Duplicate repository entries, or repositories that resolve to the same local directory within an organisation, are reported during validation.

## Resolved Local Path

For each repository, the local path is:

```text
<effective clone path>/<organisation alias or name>/<repository alias or name>
```

The effective clone path is the repository `clone_path`, otherwise the organisation `clone_path`,
otherwise `config.clone_path`. A repository `clone_path` is the same kind of override as
`clone_protocol`: omit it to keep the inherited value. `~` and environment variables are expanded.

## Validation Rules

Before synchronisation begins, the configuration is checked for:

- Missing required properties.
- Invalid property types.
- The same organisation and repository listed twice.
- Duplicate repositories.
- Duplicate local destinations.
- Invalid alias values.
- Invalid configuration hierarchy.

If any validation errors are detected, synchronisation is aborted.

## Comments

YAML and JSON5 permit comments throughout the configuration file.

For example:

```yaml
config:
  # Local repository root.
  clone_path: ~/Desktop/GitMaster
  clone_protocol: ssh

organisations:
  # Main GitHub organisation.
  - name: the-lupaxa-project
    alias: Lupaxa/TheLupaxaProject
    repositories:
      - name: workflows
```

Comments are ignored by the application but are recommended for larger configurations.

## Best Practices

When creating configuration files:

-   Keep organisations grouped logically.
-   Choose organisation aliases that match your local directory layout.
-   Keep repository lists alphabetically ordered where practical. After load,
  organisations and repositories are sorted case-insensitively by GitHub
  name. Per-repository output follows that order, not the file. The
  configuration checkout, when shown, stays first.
-   Add comments describing unusual configuration choices.
-   Remove obsolete repositories.
-   Validate the configuration after making changes.
-   Store configuration files under version control where appropriate.

## Examples

Complete files are in [Examples](examples.md).
