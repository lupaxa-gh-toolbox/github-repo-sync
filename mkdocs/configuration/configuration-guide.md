# Configuration Guide

GitHub Repository Sync is configured using a single YAML, JSON, or JSON5
configuration file. YAML is the default and recommended format.

The file lists the GitHub organisations and repositories to synchronise, the local `clone_path`, and the synchronisation options.

## Configuration File Location

By default, the application searches `~/.config/github-repo-sync/` and then the home directory:

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

A different YAML, JSON, or JSON5 file may be specified with `-c` / `--config`.

This allows multiple configurations to be maintained for different environments, teams or projects.

## Supported Formats

The application accepts configuration files in this order of preference:

- YAML (`.yaml`, then `.yml`) — default and recommended.
- JSON (`.json`).
- JSON5 (`.json5`).

If `--config` is omitted, `~/.config/github-repo-sync/` is searched first for `github-repo-sync.yaml`, then `.yml`, then `.json`, then `.json5`. The home directory is searched next for those names with a leading dot.

YAML and JSON5 allow comments. JSON5 also allows trailing commas, unquoted
property names, and single-quoted strings.

## Overall Structure

At a high level, a configuration consists of:

- Global settings under `config` (`clone_path` and `clone_protocol` are both required).
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
    │   ├── clone_path (optional)
    │   └── repositories
    │
    └── Organisation
        ├── name
        ├── alias (optional)
        ├── clone_path (optional)
        └── repositories
```

Every property is defined in the [Configuration Reference](configuration-reference.md).

## Local Directory Layout

Each repository is stored at:

```text
<effective-clone-path>/<organisation-destination>/<repository-destination>
```

`effective-clone-path` is the repository `clone_path` when set, otherwise the organisation `clone_path` when set, otherwise `config.clone_path`.

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

An alias of `.` places that organisation's repositories directly under its effective `clone_path`.
With `clone_path: "~"` and repository `bin`, the destination is `~/bin`. The same GitHub organisation
may be listed again with a different alias and `clone_path`.

### Repository aliases

Repository aliases must be a single directory name. They are commonly used when the GitHub repository name is unsuitable as a local folder name, for example:

```yaml
name: .github
alias: github
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

After a successful validation, organisations and repositories are sorted
case-insensitively by their real GitHub names. That order is what later
output follows, not the order in the file.

If validation fails, synchronisation does not begin.

This ensures configuration problems are detected before any changes are made to local repositories.

## Comments

One of the advantages of YAML and JSON5 is the ability to include comments.

Comments are strongly recommended for larger configurations as they make the purpose of organisations, repositories and configuration choices much easier to understand.

## Maintaining Large Configurations

For larger environments, consider the following recommendations:

-   Group repositories by GitHub organisation.
-   Use organisation aliases that match your local directory layout.
-   Keep repository names alphabetically ordered where practical. After load,
  organisations and repositories are sorted case-insensitively by GitHub
  name; per-repository output follows that order, not the order in the file.
-   Remove repositories that are no longer required.
-   Add comments explaining unusual configuration choices.
-   Validate the configuration after making changes.

These practices make configuration files easier to review and maintain over time.

Every property, type, and default is in the [Configuration Reference](configuration-reference.md).
