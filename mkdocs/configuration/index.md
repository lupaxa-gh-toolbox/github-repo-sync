# Configuration

Synchronisation settings live in one YAML, JSON, or JSON5 file. YAML is the default.

## Default Location

If `--config` is omitted, `grs` searches the home directory in this order:

```text
~/.github-repo-sync.yaml
~/.github-repo-sync.yml
~/.github-repo-sync.json
~/.github-repo-sync.json5
```

Pass `--config` to use another file.

## Formats

YAML and JSON5 allow comments. JSON5 also allows trailing commas and unquoted object keys. JSON is strict JSON.

## Structure

- Global settings under `config`, including `clone_path`.
- One or more GitHub organisations.
- Optional organisation aliases: a single directory name, or a relative path under `clone_path`.
- The repositories that belong to each organisation.
- Optional repository aliases: a single directory name.

The whole file is validated before any Git operation. If validation fails, nothing is cloned or updated.

## Validation

Validation rejects:

- Missing required properties.
- Invalid values.
- Incorrect types.
- Duplicate entries.
- Invalid organisation or repository definitions.

## Pages

- [Configuration Guide](configuration-guide.md) — file layout and how aliases resolve on disk.
- [Configuration Reference](configuration-reference.md) — every property, type, and default.
- [Examples](examples.md) — complete files, including relative organisation aliases.

## Conventions

- Group repositories by GitHub organisation.
- Match organisation aliases to the local directory layout.
- Comment choices that are not obvious from the keys.
- Validate after edits (`grs --validate`).
- Keep the file in version control when more than one person runs it.
