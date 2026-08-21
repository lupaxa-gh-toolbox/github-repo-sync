# Configuration Guide

GitHub Repository Sync is configured using a single JSON5 configuration file.

The configuration defines which GitHub organisations and repositories should be synchronised, where they should be stored locally and how the synchronisation process should behave.

Using a declarative configuration makes synchronisation repeatable, easy to review and suitable for both interactive and automated use.

## Configuration File Location

By default, the application looks for the following file:

```text
~/.github-repo-sync.yaml
```

A different configuration file may be specified with `-c` / `--config`.

This allows multiple configurations to be maintained for different environments, teams or projects.

## Why JSON5?

The application uses JSON5 instead of standard JSON because it is considerably easier to maintain.

JSON5 supports features including:

- Comments.
- Trailing commas.
- Unquoted property names.
- Single-quoted strings.
- Improved readability.

This makes configuration files significantly easier to edit, particularly as they grow larger.

## Overall Structure

At a high level, a configuration consists of:

- Global settings under `config` (including `clone_path` and optional `clone_protocol`).
- One or more GitHub organisations.
- One or more repositories within each organisation.
- Optional organisation and repository aliases.

A simplified structure looks like this:

```text
Configuration
│
├── config
│   ├── clone_path
│   └── clone_protocol
│
└── organisations
    │
    ├── Organisation
    │   ├── name
    │   ├── alias (optional)
    │   └── repositories
    │
    └── Organisation
        ├── name
        ├── alias (optional)
        └── repositories
```

The exact configuration properties are documented in the **Configuration Reference**.

## Local Directory Layout

Each repository is stored at:

```text
<clone_path>/<organisation-destination>/<repository-destination>
```

Where:

- Organisation destination is `alias` when set, otherwise the GitHub organisation `name`.
- Repository destination is `alias` when set, otherwise the GitHub repository `name`.

### Organisation aliases

Organisation aliases may be:

- A single directory name, such as `TheLupaxaProject`.
- A relative path under `clone_path`, such as `Lupaxa/TheLupaxaProject`.

Relative path aliases nest organisations under a shared local tree. For example, with `clone_path: "~/Desktop/GitMaster"`:

```text
GitMaster
└── Lupaxa
    ├── TheLupaxaProject
    │   ├── github
    │   └── workflows
    └── GitHubToolbox
        └── github-repo-sync
```

Corresponding aliases would be `Lupaxa/TheLupaxaProject` and `Lupaxa/GitHubToolbox`.

Organisation path aliases:

- Must be relative (no leading `/`).
- Must not contain `..` segments.
- Must use `/` as the separator.
- Must not have empty segments or a trailing `/`.

### Repository aliases

Repository aliases must be a single directory name. They are commonly used when the GitHub repository name is unsuitable as a local folder name, for example:

```json5
{
  name: ".github",
  alias: "github",
}
```

## Validation

Before any repository operations begin, the entire configuration is validated.

Validation checks include:

- Required properties.
- Property types.
- Duplicate organisations.
- Duplicate repositories.
- Duplicate local destinations.
- Invalid alias values.
- Invalid configuration structure.

If validation fails, synchronisation does not begin.

This ensures configuration problems are detected before any changes are made to local repositories.

## Comments

One of the advantages of JSON5 is the ability to include comments.

Comments are strongly recommended for larger configurations as they make the purpose of organisations, repositories and configuration choices much easier to understand.

## Maintaining Large Configurations

For larger environments, consider the following recommendations:

- Group repositories by GitHub organisation.
- Use organisation aliases that match your local directory layout.
- Keep repository names alphabetically ordered where practical.
- Remove repositories that are no longer required.
- Add comments explaining unusual configuration choices.
- Validate the configuration after making changes.

These practices make configuration files easier to review and maintain over time.

## Configuration Reference

This guide introduces the overall configuration structure.

For detailed information about every supported configuration property, including data types, defaults and validation rules, continue to the **Configuration Reference**.

## Next Steps

Continue to the **Configuration Reference** for a complete description of every supported configuration option.
