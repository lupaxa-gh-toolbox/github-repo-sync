# Configuration Examples

This section contains example configuration files demonstrating common ways to use **Lupaxa GitHub Repository Sync**.

The examples are intended to illustrate the overall structure of a configuration rather than every supported option. Refer to the **Configuration Reference** for complete details of each available property.

All examples use JSON5 syntax.

## Example 1: Single Organisation

This example synchronises two repositories from a single GitHub organisation.

```json5
{
  base_directory: "~/Development",

  organisations: [
    {
      name: "the-lupaxa-project",

      repositories: [
        {
          name: "workflows"
        },
        {
          name: "brand-assets"
        }
      ]
    }
  ]
}
```

This is an ideal starting point for individual developers or small projects.

## Example 2: Multiple Organisations

The application can manage repositories from multiple GitHub organisations within a single configuration.

```json5
{
  base_directory: "~/Development",

  organisations: [
    {
      name: "the-lupaxa-project",

      repositories: [
        {
          name: "workflows"
        }
      ]
    },

    {
      name: "lupaxa-devops-toolbox",

      repositories: [
        {
          name: "terraform-toolkit"
        },
        {
          name: "docker-toolkit"
        }
      ]
    }
  ]
}
```

Repositories from each organisation are stored beneath the configured local repository root.

## Example 3: Using Comments

One advantage of JSON5 is the ability to document your configuration using comments.

```json5
{
  // Root directory used to store repositories.
  base_directory: "~/Development",

  organisations: [
    {
      // Primary organisation.
      name: "the-lupaxa-project",

      repositories: [
        {
          // Shared reusable workflows.
          name: "workflows"
        },

        {
          // Branding assets.
          name: "brand-assets"
        }
      ]
    }
  ]
}
```

Comments are ignored by the application but make larger configurations significantly easier to understand and maintain.

## Example 4: Organising Large Configurations

As configurations grow, keeping repositories grouped by organisation makes them easier to manage.

```text
Development
├── the-lupaxa-project
│   ├── workflows
│   ├── brand-assets
│   └── github-private
│
├── lupaxa-devops-toolbox
│   ├── terraform-toolkit
│   ├── docker-toolkit
│   └── kubernetes-toolkit
│
└── lupaxa-security-toolbox
    ├── certtool
    ├── secrets-scanner
    └── compliance-toolkit
```

Keeping related repositories together also makes configurations easier to review and maintain.

## Example 5: Maintaining Large Configurations

For larger repository collections, the following practices are recommended:

- Group repositories by GitHub organisation.
- Keep repository names alphabetically ordered.
- Add comments explaining unusual configuration choices.
- Remove obsolete repositories.
- Validate the configuration before synchronising.

These simple practices improve readability and reduce the likelihood of configuration errors.

## Next Steps

Once you have created your configuration, continue to the **Usage** section to learn how to validate it, inspect planned operations and synchronise your repositories.
