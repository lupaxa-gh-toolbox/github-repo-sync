---
title: Getting Started
---

# Getting Started

Welcome to the **Getting Started** section.

This section introduces the fundamentals of installing, configuring, and using **Lupaxa GitHub Repository Sync** for the first time.

Whether you are synchronising a handful of repositories or managing hundreds across multiple GitHub organisations, these guides will help you get up and running quickly and establish a solid foundation for the more advanced topics covered later in the documentation.

---

## What You'll Learn

After completing this section you will know how to:

- Install the application.
- Verify your installation.
- Create your first configuration file.
- Validate your configuration.
- Synchronise repositories safely.
- Understand the default repository layout.
- Perform your first successful synchronisation.

---

## Before You Begin

Before installing the application, ensure your system meets the minimum requirements.

### Operating Systems

The application supports:

- macOS
- Linux
- Windows

---

### Python

Python **3.11** or later is required.

You can verify your Python version by running:

```bash
python --version
```

or

```bash
python3 --version
```

---

### Git

Git **2.x** or later must be installed and available on your system `PATH`.

Verify your installation:

```bash
git --version
```

---

### GitHub Access

The application can clone both public and private repositories.

For private repositories, ensure that your preferred authentication method has already been configured.

For example:

- GitHub SSH keys
- GitHub Personal Access Tokens
- Git Credential Manager
- Existing Git credentials

The application uses your existing Git configuration and does not implement its own authentication mechanism.

---

## Documentation Structure

The Getting Started section consists of two guides.

### Installation

Learn how to:

- Install the application.
- Install optional development dependencies.
- Verify the installation.
- Upgrade to newer releases.
- Remove the application.

---

### Quick Start

Build your first working configuration.

This guide walks through:

1. Creating a configuration file.
2. Validating the configuration.
3. Reviewing the planned repositories.
4. Running the first synchronisation.
5. Understanding the output.

By the end of the guide you will have a working synchronisation environment ready for everyday use.

---

## Recommended Reading Order

If you are new to the application, the recommended order is:

1. Installation
2. Quick Start
3. Configuration Guide
4. Command Reference
5. Repository Safety Model

Following this order introduces new concepts gradually while building a complete understanding of how the application works.

---

## Need More Detail?

The Getting Started guides intentionally focus on the most common workflows.

For comprehensive documentation covering every configuration option, command-line argument, and repository state, continue with the later sections of the documentation.

---

## Next Steps

Continue to the **Installation** guide to install the application and verify that your environment is ready for synchronising repositories.
