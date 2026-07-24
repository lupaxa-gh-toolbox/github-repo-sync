---
title: Concepts
---

# Concepts

This section explains the concepts and design principles that underpin **Lupaxa GitHub Repository Sync**.

While the **Getting Started**, **Configuration** and **Usage** sections describe how to use the application, the **Concepts** section explains *why* it behaves the way it does.

Understanding these concepts is particularly useful for administrators, maintainers and contributors who want a deeper understanding of the application's design and decision-making process.

## Why Concepts Matter

Lupaxa GitHub Repository Sync has been designed around a number of core principles:

- Safety before convenience.
- Predictable behaviour.
- Clear validation.
- Separation of responsibilities.
- Non-destructive synchronisation.
- Maintainable architecture.

These principles influence every stage of execution, from loading the configuration file through to updating repositories and reporting results.

## Topics Covered

The Concepts section is divided into three areas.

### Safety Model

Explains how the application protects existing repositories and local changes.

Topics include:

- Repository inspection.
- Safe update decisions.
- Non-destructive operations.
- When repositories are skipped.
- Manual intervention.

This section is recommended for anyone wanting to understand why the application may choose not to update a repository.

### Repository States

Describes the various states a repository can be in when inspected by the application and how those states influence synchronisation.

Understanding repository states makes it easier to interpret synchronisation results and determine why a particular repository was cloned, updated or skipped.

### Architecture

Provides an overview of the application's internal design.

Topics include:

- High-level architecture.
- Configuration loading.
- Validation.
- Synchronisation workflow.
- Git operations.
- Error handling.
- Extensibility.

This section is primarily intended for contributors and maintainers.

## Relationship Between Sections

The documentation is organised so that each section builds upon the previous one.

- **Getting Started** explains how to install and run the application.
- **Configuration** explains what should be synchronised.
- **Usage** explains how synchronisation works.
- **Concepts** explains why the application behaves as it does.
- **Reference** provides detailed technical information.
- **Development** describes how the application is developed and maintained.

## Recommended Reading

Most users will only need the **Safety Model** and **Repository States** sections.

Contributors and maintainers are encouraged to read all three concept guides, as they explain many of the architectural decisions used throughout the codebase.

## Next Steps

Continue to **Safety Model** to learn how Lupaxa GitHub Repository Sync protects your repositories during synchronisation.
