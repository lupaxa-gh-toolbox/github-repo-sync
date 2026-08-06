# Configuration Guide

Lupaxa GitHub Repository Sync is configured using a single JSON5 configuration file.

The configuration defines which GitHub organisations and repositories should be synchronised, where they should be stored locally and how the synchronisation process should behave.

Using a declarative configuration makes synchronisation repeatable, easy to review and suitable for both interactive and automated use.

## Configuration File Location

By default, the application looks for the following file:

```text
~/.github-repo-sync.json5
```

A different configuration file may be specified using the appropriate command-line option.

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

- Global application settings.
- A local repository root.
- One or more GitHub organisations.
- One or more repositories within each organisation.
- Optional repository-specific settings.

A simplified structure looks like this:

```text
Configuration
│
├── Global Settings
│
├── Repository Root
│
└── Organisations
    │
    ├── Organisation
    │   ├── Repository
    │   ├── Repository
    │   └── Repository
    │
    └── Organisation
        ├── Repository
        └── Repository
```

The exact configuration properties are documented in the **Configuration Reference**.

## Validation

Before any repository operations begin, the entire configuration is validated.

Validation checks include:

- Required properties.
- Property types.
- Duplicate organisations.
- Duplicate repositories.
- Invalid values.
- Invalid configuration structure.

If validation fails, synchronisation does not begin.

This ensures configuration problems are detected before any changes are made to local repositories.

## Organisation Layout

Repositories are grouped by GitHub organisation.

This keeps larger configurations organised and makes it easy to manage multiple organisations from a single configuration file.

For example:

```text
Development
├── the-lupaxa-project
├── lupaxa-actions-toolbox
├── lupaxa-security-toolbox
└── lupaxa-devops-toolbox
```

Each organisation contains one or more repositories that will be synchronised beneath the configured local repository root.

## Repository Definitions

Each repository definition identifies a GitHub repository that should be managed by the application.

Depending on the configuration, repositories may be:

- Cloned if they do not already exist.
- Updated if they already exist locally.
- Skipped if synchronisation would not be safe.

The application never blindly overwrites existing repositories.

## Comments

One of the advantages of JSON5 is the ability to include comments.

Comments are strongly recommended for larger configurations as they make the purpose of organisations, repositories and configuration choices much easier to understand.

## Maintaining Large Configurations

For larger environments, consider the following recommendations:

- Group repositories by GitHub organisation.
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
