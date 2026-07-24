---
title: Configuration Examples
---

# Configuration Examples

This page contains a collection of practical configuration examples for common deployment scenarios.

The examples build progressively from simple single-organisation configurations through to larger multi-organisation deployments, demonstrating how configuration inheritance can reduce duplication while keeping configuration files easy to read and maintain.

These examples are intended as starting points and can be adapted to suit your own workflow.

---

# Example 1 - Single Organisation

The simplest configuration manages repositories from a single GitHub organisation.

```json5
{
  clone_path: "~/Development",

  organisations: [

    {
      name: "the-lupaxa-project",

      repositories: [

        {
          name: "github"
        },

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

This produces the following local directory structure.

```text
~/Development/
└── the-lupaxa-project/
    ├── brand-assets/
    ├── github/
    └── workflows/
```

---

# Example 2 - Multiple Organisations

A single configuration file can manage repositories from multiple GitHub organisations.

```json5
{
  clone_path: "~/Development",

  organisations: [

    {
      name: "the-lupaxa-project",

      repositories: [

        { name: "github" },
        { name: "workflows" }

      ]
    },

    {
      name: "lupaxa-security-toolbox",

      repositories: [

        { name: "certtool" },
        { name: "scanner" }

      ]
    }

  ]
}
```

Resulting directory structure.

```text
~/Development/
├── the-lupaxa-project/
│   ├── github/
│   └── workflows/
│
└── lupaxa-security-toolbox/
    ├── certtool/
    └── scanner/
```

---

# Example 3 - Using SSH

Configure every repository to use SSH.

```json5
{
  clone_path: "~/Development",

  clone_protocol: "ssh",

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
}
```

Every repository inherits the SSH clone protocol.

---

# Example 4 - Mixing HTTPS and SSH

Global settings can be overridden where necessary.

```json5
{
  clone_path: "~/Development",

  clone_protocol: "https",

  organisations: [

    {
      name: "public-projects",

      repositories: [

        {
          name: "documentation"
        }

      ]
    },

    {
      name: "private-projects",

      clone_protocol: "ssh",

      repositories: [

        {
          name: "internal-tools"
        },

        {
          name: "automation"
        }

      ]
    }

  ]
}
```

Public repositories use HTTPS, while repositories in the `private-projects` organisation use SSH.

---

# Example 5 - Custom Organisation Directory

The local directory does not have to match the GitHub organisation name.

```json5
{
  clone_path: "~/Development",

  organisations: [

    {
      name: "the-lupaxa-project",

      destination_name: "TheLupaxaProject",

      repositories: [

        {
          name: "github"
        }

      ]
    }

  ]
}
```

Local layout.

```text
~/Development/
└── TheLupaxaProject/
    └── github/
```

---

# Example 6 - Custom Repository Directory

Repositories may also use custom local directory names.

```json5
{
  clone_path: "~/Development",

  organisations: [

    {
      name: "the-lupaxa-project",

      repositories: [

        {
          name: "github",
          destination_name: ".github"
        }

      ]
    }

  ]
}
```

Result.

```text
~/Development/
└── the-lupaxa-project/
    └── .github/
```

---

# Example 7 - Large Repository Collection

Large configurations remain easy to organise by grouping repositories beneath their owning organisation.

```json5
{
  clone_path: "~/Development",

  organisations: [

    {
      name: "the-lupaxa-project",

      repositories: [

        { name: "github" },
        { name: "workflows" },
        { name: "brand-assets" },
        { name: "templates" }

      ]
    },

    {
      name: "lupaxa-security-toolbox",

      repositories: [

        { name: "certtool" },
        { name: "scanner" },
        { name: "hash-tool" }

      ]
    },

    {
      name: "lupaxa-devops-toolbox",

      repositories: [

        { name: "docker-helper" },
        { name: "terraform-helper" },
        { name: "kubernetes-helper" }

      ]
    }

  ]
}
```

The application automatically creates the required directory structure beneath the configured clone path.

---

# Best Practices

When creating configuration files, consider the following recommendations.

- Group repositories by GitHub organisation.
- Use inheritance wherever possible.
- Avoid duplicate repository definitions.
- Keep related repositories together.
- Use custom destination names only when required.
- Validate configurations before synchronising.
- Store configuration files in version control if they are shared across multiple systems.

---

# Next Steps

Now that you are familiar with the configuration system, continue to the **Usage** section to learn how to use the command-line interface, perform synchronisation operations, and automate repository management.
