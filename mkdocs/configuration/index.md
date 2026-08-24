# Configuration

The behaviour of **GitHub Repository Sync** is controlled by a YAML, JSON, or JSON5 configuration file.

Rather than supplying numerous command-line arguments each time the application is executed, all synchronisation settings are stored in a single,
human-readable configuration file. This approach makes configurations easier to understand, maintain and version alongside other project assets.

## Default Configuration Location

Unless another configuration file is specified on the command line, the
application searches the home directory in this order:

```text
~/.github-repo-sync.yaml
~/.github-repo-sync.yml
~/.github-repo-sync.json
~/.github-repo-sync.json5
```

A different configuration file can be specified when running the application, allowing multiple synchronisation configurations to be maintained for different environments or projects.

## Supported Formats

YAML is the default and recommended format. JSON and JSON5 remain supported.
YAML and JSON5 allow comments; JSON5 also allows trailing commas and unquoted
object keys.

If `--config` is omitted, the application searches the home directory in this
order: `.github-repo-sync.yaml`, then `.yml`, then `.json`, then `.json5`.

## Configuration Structure

A configuration file typically contains:

- Global settings under `config`, including `clone_path`.
- One or more GitHub organisations.
- Optional organisation aliases (single directory names or relative paths under `clone_path`).
- The repositories that belong to each organisation.
- Optional repository aliases (single directory names).

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

Contains practical configuration examples ranging from simple personal setups through to larger multi-organisation environments, including relative path organisation aliases.

## Best Practices

For most users, the following recommendations are worth following:

- Keep related repositories together within the same organisation.
- Choose organisation aliases that match your local directory layout.
- Add comments describing non-obvious configuration choices.
- Use meaningful directory names.
- Validate the configuration before synchronising repositories.
- Keep configuration files under version control where appropriate.

## Next Steps

If you are creating a configuration for the first time, continue to the **Configuration Guide**.

If you are looking for a specific property or option, refer to the **Configuration Reference**.
