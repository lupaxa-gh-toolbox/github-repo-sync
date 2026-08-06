# Configuration

The behaviour of **Lupaxa GitHub Repository Sync** is controlled by a JSON5 configuration file.

Rather than supplying numerous command-line arguments each time the application is executed, all synchronisation settings are stored in a single,
human-readable configuration file. This approach makes configurations easier to understand, maintain and version alongside other project assets.

## Default Configuration Location

Unless another configuration file is specified on the command line, the application automatically loads:

```text
~/.github-repo-sync.json5
```

A different configuration file can be specified when running the application, allowing multiple synchronisation configurations to be maintained for different environments or projects.

## Why JSON5?

Lupaxa GitHub Repository Sync uses **JSON5** rather than standard JSON because it provides several features that improve readability and maintainability.

These include:

- Comments.
- Trailing commas.
- Unquoted object keys.
- Single or double quoted strings.
- More forgiving formatting.

This makes larger configuration files significantly easier to manage.

## Configuration Structure

A configuration file typically contains:

- Global application settings.
- The local directory used to store repositories.
- One or more GitHub organisations.
- The repositories that belong to each organisation.
- Repository-specific options where required.

The application validates the entire configuration before performing any synchronisation.

If validation fails, no repository operations are performed.

## Validation

Before synchronisation begins, the configuration is checked for problems including:

- Missing required properties.
- Invalid property values.
- Incorrect data types.
- Duplicate entries.
- Invalid repository definitions.
- Invalid organisation definitions.

This validation process helps identify configuration errors before any changes are made to local repositories.

## Configuration Guides

This section is divided into three parts.

### Configuration Guide

Explains the overall configuration structure, recommended practices and how larger configurations should be organised.

### Configuration Reference

Provides a complete reference for every supported configuration property, including expected data types, defaults and validation rules.

### Examples

Contains practical configuration examples ranging from simple personal setups through to larger multi-organisation environments.

## Best Practices

For most users, the following recommendations are worth following:

- Keep related repositories together within the same organisation.
- Add comments describing non-obvious configuration choices.
- Use meaningful directory names.
- Validate the configuration before synchronising repositories.
- Keep configuration files under version control where appropriate.

## Next Steps

If you are creating a configuration for the first time, continue to the **Configuration Guide**.

If you are looking for a specific property or option, refer to the **Configuration Reference**.
