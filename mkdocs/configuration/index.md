---
title: Configuration
---

# Configuration

The configuration system is the heart of **Lupaxa GitHub Repository Sync**.

Rather than relying on long command-line arguments or interactive prompts, the application uses a declarative **JSON5** configuration file to describe exactly which repositories should be managed and how they should be synchronised.

This approach makes configurations:

- Easy to read.
- Easy to maintain.
- Easy to version control.
- Suitable for automation.
- Reusable across multiple machines.

Whether you are managing five repositories or several hundred, the configuration file becomes the single source of truth for your local repository layout.

---

## Configuration Philosophy

The configuration system has been designed around a few simple principles.

### Human Readable

Configuration files should be understandable at a glance.

JSON5 allows comments, trailing commas, and unquoted property names, making configurations significantly easier to maintain than strict JSON.

---

### Declarative

The configuration describes the desired end state rather than the steps required to achieve it.

For example, instead of instructing the application to clone individual repositories, you simply declare which repositories should exist locally.

The application determines the work required to achieve that state.

---

### Safe by Default

Configuration options are intentionally conservative.

The application will never perform destructive operations simply because they appear in the configuration.

Repository safety checks always take precedence over synchronisation.

---

### Hierarchical

Settings can be defined at multiple levels.

In general, values inherit from their parent unless explicitly overridden.

This allows large configurations to remain concise while still supporting repository-specific behaviour where required.

---

## Configuration Structure

A configuration file consists of several logical layers.

```text
Configuration
│
├── Global Settings
│
├── Organisations
│   │
│   ├── Organisation Settings
│   │
│   └── Repositories
│       │
│       └── Repository Settings
│
└── Future Extensions
```

Each layer provides progressively more specific configuration options.

---

## Global Configuration

Global settings apply to every organisation and repository unless overridden.

Typical examples include:

- Clone directory.
- Default clone protocol.
- Output preferences.
- Validation behaviour.
- Future global options.

---

## Organisation Configuration

Organisation settings allow repositories belonging to the same GitHub organisation to share common behaviour.

Examples include:

- Organisation name.
- Local destination directory.
- Clone protocol.
- Repository list.

These settings remove the need to repeat common values for every repository.

---

## Repository Configuration

Repository settings describe an individual GitHub repository.

Repository-specific options always take precedence over inherited values.

Typical settings include:

- Repository name.
- Local destination directory.
- Clone protocol override.
- Future repository-specific options.

---

## Configuration Validation

Every configuration is validated before synchronisation begins.

Validation includes checks such as:

- Required properties.
- Invalid property types.
- Duplicate organisations.
- Duplicate repositories.
- Missing repository names.
- Invalid configuration hierarchy.

If validation fails, synchronisation does not begin.

This helps identify configuration problems before any repositories are modified.

---

## Configuration Files

The application can load configuration files from a user-specified location.

For example:

```bash
github-repo-sync --config config.json5
```

Multiple configuration files can also be maintained for different environments, such as:

- Personal development.
- Work projects.
- Continuous integration.
- Build servers.
- Testing environments.

---

## Documentation in This Section

The Configuration section is divided into three guides.

### Configuration Guide

A detailed walkthrough of every configuration level and how settings interact.

Recommended reading for all users.

---

### Configuration Reference

A complete reference for every supported configuration option, including default values, accepted types, and inheritance behaviour.

Useful when looking up individual properties.

---

### Examples

A collection of practical configuration examples covering common deployment scenarios, including:

- Single organisation.
- Multiple organisations.
- HTTPS and SSH combinations.
- Custom directory layouts.
- Large repository collections.

---

## Recommended Reading Order

If you are new to the configuration system, read the documents in the following order:

1. Configuration Guide
2. Configuration Reference
3. Configuration Examples

This introduces concepts first before moving on to the complete reference documentation.

---

## Next Steps

Continue to the **Configuration Guide** to learn how configuration files are structured and how settings are inherited throughout the application.
