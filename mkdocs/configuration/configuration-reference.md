# Configuration Reference

This section provides a complete reference for every configuration property supported by **Lupaxa GitHub Repository Sync**.

The configuration file is written using the JSON5 format and is validated before any synchronisation operations begin.

Unless another configuration file is specified on the command line, the application automatically loads:

```text
~/.github-repo-sync.json5
```

> **Important**
>
> This reference describes the configuration schema used by the application. Every property is validated before synchronisation begins. If validation fails, no repository operations are performed.

## Configuration Overview

A configuration consists of:

- Global settings.
- One or more GitHub organisations.
- One or more repositories within each organisation.

The overall structure resembles the following:

```text
Configuration
│
├── Global Settings
│
└── Organisations
    ├── Organisation
    │   ├── Repository
    │   ├── Repository
    │   └── Repository
    │
    └── Organisation
        ├── Repository
        └── Repository
```

## Root Properties

The root of the configuration contains the application-wide settings.

The exact properties available depend on the version of the application.

Each property is described in the following sections.

## Organisation Properties

Each organisation represents a GitHub organisation whose repositories should be managed.

An organisation typically contains:

- The organisation name.
- A collection of repositories.
- Any organisation-specific options supported by the application.

Organisation names must be unique.

Duplicate organisations are reported as validation errors.

## Repository Properties

Each repository entry describes a single GitHub repository.

Repository definitions typically include:

- Repository name.
- Optional repository-specific settings.

Repository names must be unique within an organisation.

Duplicate repository entries are reported during validation.

## Validation Rules

Before synchronisation begins, the configuration is checked for:

- Missing required properties.
- Invalid property types.
- Duplicate organisations.
- Duplicate repositories.
- Invalid values.
- Invalid configuration hierarchy.

If any validation errors are detected, synchronisation is aborted.

## Comments

Because JSON5 is used, comments are permitted throughout the configuration file.

For example:

```json5
{
  // Local repository root.
  base_directory: "~/Development",

  organisations: [
    {
      // Main GitHub organisation.
      name: "the-lupaxa-project",

      repositories: [
        {
          name: "workflows"
        }
      ]
    }
  ]
}
```

Comments are ignored by the application but are recommended for larger configurations.

## Best Practices

When creating configuration files:

- Keep organisations grouped logically.
- Keep repository lists alphabetically ordered where practical.
- Add comments describing unusual configuration choices.
- Remove obsolete repositories.
- Validate the configuration after making changes.
- Store configuration files under version control where appropriate.

## Examples

Practical configuration examples are provided in the **Examples** section.

These demonstrate common configurations ranging from a single organisation through to larger multi-organisation environments.

## Next Steps

Continue to **Examples** to see complete configuration files for common deployment scenarios.
