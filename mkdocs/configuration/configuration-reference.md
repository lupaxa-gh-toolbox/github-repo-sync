---
title: Configuration Reference
---

# Configuration Reference

This document provides a complete reference for every configuration option supported by **Lupaxa GitHub Repository Sync**.

Unlike the **Configuration Guide**, which explains concepts and best practices, this document serves as a technical reference describing each property, its purpose, accepted values, default behaviour, and inheritance rules.

---

# Configuration Structure

A configuration file consists of a small number of top-level sections.

```text
Configuration
├── clone_path
├── clone_protocol
├── organisations
│   ├── organisation
│   │   ├── repositories
│   │   └── ...
│   └── ...
└── ...
```

The exact set of supported properties will evolve over time as new features are introduced.

---

# Global Configuration

Global properties apply to every organisation and repository unless overridden further down the configuration hierarchy.

---

## clone_path

**Type**

```text
String
```

**Required**

Yes

**Inherited**

Yes

**Description**

Specifies the root directory where repositories will be cloned.

Every organisation is created beneath this directory.

**Example**

```json5
clone_path: "~/Development"
```

---

## clone_protocol

**Type**

```text
String
```

**Required**

No

**Default**

```text
https
```

**Inherited**

Yes

**Allowed Values**

- `https`
- `ssh`

**Description**

Determines which Git clone URL should be used unless overridden.

**Example**

```json5
clone_protocol: "ssh"
```

---

# organisations

**Type**

```text
Array
```

**Required**

Yes

**Inherited**

No

**Description**

Defines one or more GitHub organisations.

Each organisation contains its own settings and list of repositories.

**Example**

```json5
organisations: [

  {
    name: "the-lupaxa-project",

    repositories: [
      {
        name: "github"
      }
    ]
  }

]
```

---

# Organisation Properties

Each organisation object supports the following properties.

---

## name

**Type**

```text
String
```

**Required**

Yes

**Inherited**

No

**Description**

The GitHub organisation name.

This is also used as the default local directory name.

**Example**

```json5
name: "the-lupaxa-project"
```

---

## destination_name

**Type**

```text
String
```

**Required**

No

**Inherited**

No

**Description**

Overrides the local directory name used for the organisation.

This does **not** change the GitHub organisation name.

**Example**

```json5
destination_name: "TheLupaxaProject"
```

Result:

```text
~/Development/
└── TheLupaxaProject/
```

---

## clone_protocol

**Type**

```text
String
```

**Required**

No

**Inherited**

Yes

**Allowed Values**

- `https`
- `ssh`

**Description**

Overrides the global clone protocol for every repository within this organisation.

Repository-level settings take precedence.

---

## repositories

**Type**

```text
Array
```

**Required**

Yes

**Inherited**

No

**Description**

Defines the repositories that belong to the organisation.

---

# Repository Properties

Each repository object supports the following properties.

---

## name

**Type**

```text
String
```

**Required**

Yes

**Inherited**

No

**Description**

The GitHub repository name.

**Example**

```json5
name: "workflows"
```

---

## destination_name

**Type**

```text
String
```

**Required**

No

**Inherited**

No

**Description**

Overrides the local directory name for this repository.

Useful when preserving an existing local directory layout.

**Example**

```json5
destination_name: ".github"
```

---

## clone_protocol

**Type**

```text
String
```

**Required**

No

**Inherited**

Yes

**Allowed Values**

- `https`
- `ssh`

**Description**

Overrides both the global and organisation clone protocol for this repository only.

---

# Inheritance Order

Configuration values are resolved in the following order.

```text
Repository
        │
        ▼
Organisation
        │
        ▼
Global
        │
        ▼
Default
```

The first value found is used.

---

# Example

```json5
{
  clone_path: "~/Development",
  clone_protocol: "https",

  organisations: [

    {
      name: "the-lupaxa-project",

      clone_protocol: "ssh",

      repositories: [

        {
          name: "github"
        },

        {
          name: "workflows",
          clone_protocol: "https"
        }

      ]
    }

  ]
}
```

Resolved values:

| Repository | Clone Protocol |
|------------|----------------|
| github | ssh |
| workflows | https |

---

# Validation Rules

The configuration validator checks for a range of common problems before synchronisation begins.

Examples include:

- Missing required properties.
- Empty organisation names.
- Empty repository names.
- Duplicate organisations.
- Duplicate repositories within an organisation.
- Invalid property types.
- Unsupported property values.
- Invalid configuration hierarchy.

Validation errors prevent synchronisation from starting.

---

# Future Configuration Options

Additional configuration options are expected in future releases.

Examples may include:

- Include and exclude filters.
- Branch selection.
- Repository tags.
- Parallel clone limits.
- Custom authentication profiles.
- Per-repository update policies.
- Logging configuration.
- Output formatting options.

These features are intentionally omitted until their behaviour is fully defined.

---

# Next Steps

See **Configuration Examples** for practical examples covering common repository layouts and real-world deployment scenarios.
