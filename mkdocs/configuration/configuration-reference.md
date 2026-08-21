# Configuration Reference

This section provides a complete reference for every configuration property supported by **GitHub Repository Sync**.

The configuration file is written using the JSON5 format and is validated before any synchronisation operations begin.

Unless another configuration file is specified on the command line, the application automatically loads:

```text
~/.github-repo-sync.yaml
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
| `clone_protocol`  | No       | Default clone protocol for repositories (`ssh` or `https`).                 |

`clone_path` supports `~` expansion and environment variables.

## Organisation Properties

Each organisation represents a GitHub organisation whose repositories should be managed.

| Property        | Required | Description                                                                 |
| --------------- | -------- | --------------------------------------------------------------------------- |
| `name`          | Yes      | GitHub organisation login.                                                  |
| `alias`         | No       | Local destination under `clone_path`.                                       |
| `repositories`  | Yes      | One or more repository definitions.                                         |

Organisation names must be unique.

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
- Must not contain `.` or `..` path segments.

Duplicate organisations (by GitHub name or resolved local destination) are reported as validation errors.

## Repository Properties

Each repository entry describes a single GitHub repository.

| Property          | Required | Description                                                       |
| ----------------- | -------- | ----------------------------------------------------------------- |
| `name`            | Yes      | GitHub repository name.                                           |
| `alias`           | No       | Local directory name for the repository.                          |
| `clone_protocol`  | No       | Per-repository protocol override (`ssh` or `https`).              |

Repository names must be unique within an organisation.

### Repository `alias`

When omitted, the local repository directory is the GitHub repository `name`.

When set, the alias must be a single directory name (not a path). This is typically used when the GitHub name is unsuitable as a folder name:

```json5
{
  name: ".github",
  alias: "github",
}
```

Duplicate repository entries, or repositories that resolve to the same local directory within an organisation, are reported during validation.

## Resolved Local Path

For each repository, the local path is:

```text
<config.clone_path>/<organisation alias or name>/<repository alias or name>
```

## Validation Rules

Before synchronisation begins, the configuration is checked for:

- Missing required properties.
- Invalid property types.
- Duplicate organisations.
- Duplicate repositories.
- Duplicate local destinations.
- Invalid alias values.
- Invalid configuration hierarchy.

If any validation errors are detected, synchronisation is aborted.

## Comments

Because JSON5 is used, comments are permitted throughout the configuration file.

For example:

```json5
{
  config: {
    // Local repository root.
    clone_path: "~/Desktop/GitMaster",
    clone_protocol: "ssh",
  },

  organisations: [
    {
      // Main GitHub organisation.
      name: "the-lupaxa-project",
      alias: "Lupaxa/TheLupaxaProject",

      repositories: [
        {
          name: "workflows",
        },
      ],
    },
  ],
}
```

Comments are ignored by the application but are recommended for larger configurations.

## Best Practices

When creating configuration files:

- Keep organisations grouped logically.
- Choose organisation aliases that match your local directory layout.
- Keep repository lists alphabetically ordered where practical.
- Add comments describing unusual configuration choices.
- Remove obsolete repositories.
- Validate the configuration after making changes.
- Store configuration files under version control where appropriate.

## Examples

Practical configuration examples are provided in the **Examples** section.

These demonstrate common configurations ranging from a single organisation through to larger multi-organisation environments with path aliases.

## Next Steps

Continue to **Examples** to see complete configuration files for common deployment scenarios.
