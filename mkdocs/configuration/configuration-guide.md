---
title: Configuration Guide
---

# Configuration Guide

This guide explains how to configure **Lupaxa GitHub Repository Sync** using a JSON5 configuration file.

The configuration file defines the repositories that should exist on your local machine and how they should be organised. Rather than executing individual clone or update commands, you describe the desired state and allow the application to determine the actions required to achieve it safely.

This document introduces the overall structure of the configuration file, explains how settings are inherited, and provides guidance on organising configurations for projects of different sizes.

---

## Why JSON5?

The application uses **JSON5** rather than standard JSON.

JSON5 offers several quality-of-life improvements that make configuration files easier to write and maintain, including:

- Comments.
- Trailing commas.
- Unquoted property names.
- Single or double quoted strings.
- Improved readability for larger files.

For example:

```json5
{
  // Where repositories will be cloned
  clone_path: "~/Development",

  organisations: [

    {
      name: "the-lupaxa-project",

      repositories: [

        {
          name: "github",
        },

      ],
    },

  ],
}
```

---

## Configuration Hierarchy

Configuration is organised into three levels.

```text
Global Configuration
│
├── Organisation
│   │
│   ├── Repository
│   ├── Repository
│   └── Repository
│
├── Organisation
│   │
│   ├── Repository
│   └── Repository
│
└── Organisation
```

Each level can define settings that are inherited by the levels beneath it.

---

## Global Configuration

Global settings apply to every organisation and repository unless explicitly overridden.

Typical global settings include:

- Clone directory.
- Default clone protocol.
- Default output behaviour.
- Validation settings.

Example:

```json5
{
  clone_path: "~/Development",
  clone_protocol: "https",
}
```

These values become the defaults used throughout the configuration.

---

## Organisations

Repositories are grouped by GitHub organisation.

Each organisation contains:

- The GitHub organisation name.
- Optional organisation-wide settings.
- A list of repositories.

Example:

```json5
{
  name: "the-lupaxa-project",

  repositories: [

    {
      name: "github",
    },

    {
      name: "workflows",
    },

  ],
}
```

The application creates one local directory for each organisation.

For example:

```text
~/Development/
└── the-lupaxa-project/
```

---

## Repositories

Each repository entry represents a single GitHub repository.

The smallest valid repository definition is simply:

```json5
{
  name: "github",
}
```

Additional options may be specified when required.

Repositories inherit settings from both the global configuration and their parent organisation.

---

## Configuration Inheritance

Inheritance keeps configuration files concise.

Rather than repeating the same values for every repository, common settings are defined once and inherited automatically.

For example:

```json5
{
  clone_protocol: "https",

  organisations: [

    {
      name: "the-lupaxa-project",

      repositories: [

        {
          name: "github",
        },

        {
          name: "workflows",
        },

      ],
    },

  ],
}
```

Both repositories inherit the HTTPS clone protocol.

---

## Overriding Inherited Values

Inherited values can be overridden whenever necessary.

For example, one organisation may use SSH while another continues to use HTTPS.

```json5
{
  clone_protocol: "https",

  organisations: [

    {
      name: "private-tools",
      clone_protocol: "ssh",

      repositories: [

        {
          name: "internal-library",
        },

      ],
    },

  ],
}
```

Repository-level settings always take precedence over organisation and global values.

---

## Local Directory Names

By default, local directories use the same names as their corresponding GitHub organisations and repositories.

For example:

```text
~/Development/
└── the-lupaxa-project/
    └── workflows/
```

However, custom directory names may be specified if preferred.

This can be useful when:

- Preserving historical directory structures.
- Shortening long names.
- Matching existing local layouts.

---

## Multiple Organisations

A single configuration file may manage repositories from any number of GitHub organisations.

For example:

```json5
{
  organisations: [

    {
      name: "the-lupaxa-project",

      repositories: [
        { name: "github" },
        { name: "workflows" },
      ],
    },

    {
      name: "lupaxa-security-toolbox",

      repositories: [
        { name: "certtool" },
        { name: "scanner" },
      ],
    },

  ],
}
```

Each organisation receives its own directory beneath the configured clone path.

---

## Configuration Validation

Before synchronisation begins, the configuration is validated.

Validation checks include:

- Required properties.
- Duplicate organisations.
- Duplicate repositories.
- Invalid property types.
- Unsupported configuration values.
- Invalid hierarchy.

If validation fails, synchronisation does not continue.

---

## Keeping Configurations Organised

For small collections of repositories, a single configuration file is usually sufficient.

As deployments grow, consider grouping repositories logically.

For example:

- Open source projects.
- Internal tooling.
- Client repositories.
- Build infrastructure.
- Documentation.

A well-organised configuration is easier to maintain and review over time.

---

## Best Practices

When creating configuration files, the following recommendations are encouraged.

- Keep related repositories together.
- Avoid duplicate repository definitions.
- Use inheritance wherever possible.
- Add comments to explain unusual configuration choices.
- Validate the configuration before synchronising.
- Store configuration files in version control where appropriate.

---

## Next Steps

Now that you understand how configuration files are structured, continue to the **Configuration Reference** for a complete description of every supported configuration option and its behaviour.
