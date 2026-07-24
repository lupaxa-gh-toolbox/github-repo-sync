---
title: Concepts
---

# Concepts

Understanding how **Lupaxa GitHub Repository Sync** works internally will help you get the most from the application.

While the earlier sections of this documentation focus on installation, configuration, and day-to-day usage, this section explains the design principles that influence how the application behaves.

These concepts are fundamental to the project and explain why the application often behaves differently from traditional repository synchronisation tools.

---

## Philosophy

Lupaxa GitHub Repository Sync was designed around a simple principle:

> **Protect local repositories first, synchronise them second.**

Many repository management tools prioritise keeping repositories up to date, sometimes at the expense of local changes or repository integrity.

This application takes the opposite approach.

Every synchronisation decision is made with the goal of preserving local work and avoiding unexpected repository modifications.

---

## Core Design Principles

Several principles guide the design of the application.

### Safety First

Repositories are never modified unless they have been confirmed to be in a safe state.

If there is any uncertainty, the repository is skipped and reported to the user.

---

### Predictable Behaviour

Running the application multiple times with the same configuration should produce consistent and repeatable results.

The application avoids hidden behaviour and makes every significant decision visible through its console output and summary reporting.

---

### Explicit Over Implicit

Configuration is intentionally explicit.

Repositories are managed because they have been declared in the configuration file, not because they happen to exist on disk.

This keeps synchronisation deterministic and makes configuration files the single source of truth.

---

### Conservative Git Operations

Only non-destructive Git operations are performed automatically.

Potentially destructive operations always require manual intervention.

Examples include:

- Hard resets.
- Force checkouts.
- Cleaning untracked files.
- Rebasing.
- History rewriting.

---

### Scalable by Design

Whether managing ten repositories or several hundred, the synchronisation process remains the same.

Repositories are processed independently, allowing large synchronisation runs to remain reliable even when individual repositories encounter problems.

---

## Documentation in This Section

The Concepts section is divided into three documents.

### Repository Safety Model

Explains the safety checks performed before any repository is modified.

Topics include:

- Repository inspection.
- Safe and unsafe repository states.
- Why repositories are skipped.
- Design decisions behind the safety model.

---

### Repository States

Describes the different states a repository may be in during synchronisation and how those states influence the actions taken by the application.

Examples include:

- Missing repositories.
- Clean repositories.
- Dirty repositories.
- Detached HEAD states.
- Diverged branches.
- Invalid repositories.

---

### Architecture

Provides an overview of the internal architecture of the application.

Topics include:

- High-level design.
- Configuration loading.
- Validation.
- Synchronisation pipeline.
- Git operations.
- Console output.
- Extensibility.

This document is particularly useful for contributors and anyone wishing to understand how the application is structured internally.

---

## Recommended Reading Order

The documents in this section are intended to be read in the following order:

1. Repository Safety Model
2. Repository States
3. Architecture

This order introduces the core design philosophy before exploring how those principles are implemented within the application.

---

## Who Should Read This Section?

This section is recommended for:

- Power users.
- System administrators.
- Contributors.
- Developers extending the application.
- Anyone interested in understanding the reasoning behind the application's behaviour.

---

## Next Steps

Continue to the **Repository Safety Model** to learn why repository safety is central to the design of **Lupaxa GitHub Repository Sync** and how the application determines whether a repository can be updated safely.
