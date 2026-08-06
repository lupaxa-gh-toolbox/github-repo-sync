<p align="center">
  <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/the-lupaxa-blueprints/readme-logo.png" alt="Logo" />
</p>

<h1 align="center">Lupaxa GitHub Repository Sync</h1>

Welcome to the official documentation for **Lupaxa GitHub Repository Sync**.

Lupaxa GitHub Repository Sync is a command-line application designed to safely clone, organise and synchronise collections of GitHub repositories from a
single declarative configuration file.

Rather than manually cloning and maintaining repositories individually, the application reads a configuration file describing the organisations and
repositories you wish to manage, then performs the required synchronisation operations automatically whilst protecting existing repositories and local changes.

The project has been designed with reliability, predictability and safety as its primary goals, making it suitable for individual developers, teams and
organisations managing anything from a handful of repositories to hundreds or even thousands.

## Features

Some of the key capabilities include:

- Declarative JSON5 configuration.
- Safe repository synchronisation.
- Automatic cloning of missing repositories.
- Fast-forward updates of existing repositories.
- Protection against overwriting local changes.
- Validation before synchronisation begins.
- Comprehensive progress reporting.
- Clear error messages and exit codes.
- Cross-platform operation.
- Strongly typed implementation.
- Modular architecture.
- Suitable for automation and scheduled execution.

## Documentation Structure

The documentation is organised into the following sections.

### Getting Started

Learn how to install the application, configure your environment and perform your first synchronisation.

Recommended for all new users.

### Configuration

Learn how configuration files are structured, what options are available and how to organise larger synchronisation projects.

### Usage

Detailed information about the available commands, synchronisation behaviour and automation.

### Concepts

Background information explaining how the application works internally, including the safety model, repository states and overall architecture.

### Reference

Reference material including exit codes, troubleshooting guidance and answers to frequently asked questions.

### Development

Information for contributors, including development setup, testing and contribution guidelines.

## Requirements

Lupaxa GitHub Repository Sync requires:

- Python 3.11 or later.
- Git installed and available on the system PATH.
- Access to the repositories being synchronised.
- Appropriate authentication for private repositories.

## Design Principles

The application has been built around a small number of core principles.

- Safety before convenience.
- Predictable behaviour.
- Clear validation.
- Strong typing.
- Separation of responsibilities.
- Maintainable architecture.
- Consistent user experience.

These principles influence every stage of the synchronisation process, from configuration loading through to repository updates and reporting.

## Getting Help

If you encounter problems or have questions about using the application, consult the following sections:

- **Getting Started** for installation and initial setup.
- **Configuration** for configuration file guidance.
- **Reference** for troubleshooting and frequently asked questions.

## Next Steps

If you are new to the application, continue with **Getting Started** to install Lupaxa GitHub Repository Sync and perform your first synchronisation.
