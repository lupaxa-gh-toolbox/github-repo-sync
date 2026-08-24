# Configuration Examples

This section contains example configuration files demonstrating common ways to use **GitHub Repository Sync**.

The examples are intended to illustrate the overall structure of a configuration rather than every supported option. Refer to the **Configuration Reference** for complete details of each available property.

All examples use YAML, the default and recommended format. Equivalent JSON and
JSON5 files are also accepted.

## Example 1: Single Organisation

This example synchronises two repositories from a single GitHub organisation.

```yaml
config:
  clone_path: ~/Development
  clone_protocol: ssh

organisations:
  - name: the-lupaxa-project
    repositories:
      - name: workflows
      - name: brand-assets
```

This is an ideal starting point for individual developers or small projects.

## Example 2: Multiple Organisations

The application can manage repositories from multiple GitHub organisations within a single configuration.

```yaml
config:
  clone_path: ~/Development
  clone_protocol: ssh

organisations:
  - name: the-lupaxa-project
    alias: TheLupaxaProject
    repositories:
      - name: workflows

  - name: lupaxa-gh-toolbox
    alias: GitHubToolbox
    repositories:
      - name: github-repo-sync
```

Repositories from each organisation are stored beneath the configured local repository root.

## Example 3: Relative Path Organisation Aliases

Organisation aliases may include `/` so repositories nest under a shared local tree.

```yaml
config:
  clone_path: ~/Desktop/GitMaster
  clone_protocol: ssh

organisations:
  - name: the-lupaxa-project
    alias: Lupaxa/TheLupaxaProject
    repositories:
      - name: .github
        alias: github
      - name: workflows

  - name: lupaxa-gh-toolbox
    alias: Lupaxa/GitHubToolbox
    repositories:
      - name: github-repo-sync
```

This resolves to:

```text
GitMaster
└── Lupaxa
    ├── TheLupaxaProject
    │   ├── github
    │   └── workflows
    └── GitHubToolbox
        └── github-repo-sync
```

Repository aliases remain single directory names. Organisation aliases may be either a directory name or a relative path under `clone_path`.

## Example 4: Using Comments

YAML and JSON5 allow comments, which is useful for documenting larger files.

```yaml
config:
  # Root directory used to store repositories.
  clone_path: ~/Development
  clone_protocol: ssh

organisations:
  # Primary organisation.
  - name: the-lupaxa-project
    alias: TheLupaxaProject
    repositories:
      # Shared reusable workflows.
      - name: workflows
      # Branding assets.
      - name: brand-assets
```

Comments are ignored by the application but make larger configurations significantly easier to understand and maintain.

## Example 5: Maintaining Large Configurations

For larger repository collections, the following practices are recommended:

-   Group repositories by GitHub organisation.
-   Choose organisation aliases that match your local directory layout.
-   Keep repository names alphabetically ordered. After load, organisations
  and repositories are sorted case-insensitively by GitHub name.
-   Add comments explaining unusual configuration choices.
-   Remove obsolete repositories.
-   Validate the configuration before synchronising.

These simple practices improve readability and reduce the likelihood of configuration errors.

## Next Steps

Once you have created your configuration, continue to the **Usage** section to learn how to validate it, inspect planned operations and synchronise your repositories.
