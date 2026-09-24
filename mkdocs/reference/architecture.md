# Architecture

Configuration loading, validation, repository processing, Git operations, and presentation are separate components.

## High-Level Architecture

At a high level, the application follows the workflow below.

```text
                 Command Line Interface
                          │
                          ▼
                  Argument Processing
                          │
                          ▼
               Configuration Loading
                          │
                          ▼
              Configuration Validation
                          │
                          ▼
             Repository Synchronisation
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   Git Operations   Progress Reporting   Console Output
        │
        ▼
      Summary
```

Each stage performs a single responsibility before passing control to the next.

## Command-Line Interface

The command-line interface provides the entry point to the application.

Its responsibilities include:

- Processing command-line arguments.
- Selecting the requested command.
- Loading the requested configuration.
- Reporting success or failure.
- Returning the appropriate exit code.

The command-line interface intentionally contains very little business logic.

## Configuration

Configuration is loaded before any repository processing begins.

The configuration layer is responsible for:

- Reading the YAML, JSON, or JSON5 configuration file.
- Parsing configuration data.
- Constructing internal models.
- Reporting configuration errors.

Once loaded, the configuration is passed to the validation layer.

## Validation

Validation ensures that the configuration is complete and internally consistent.

Typical validation includes:

- Required properties.
- Property types.
- Duplicate organisations.
- Duplicate repositories.
- Invalid values.
- Configuration hierarchy.

If validation fails, synchronisation does not begin.

## Synchronisation Engine

The synchronisation engine coordinates the processing of repositories.

Its responsibilities include:

1. Processing each configured organisation.
2. Processing configured repositories concurrently (`--workers`).
3. Determining the required action for each repository.
4. Calling the appropriate Git operations.
5. Recording outcomes in the post-load sort (case-insensitive GitHub names).
6. Producing the final summary.

The synchronisation engine does not perform Git operations directly.

## Git Operations

All interactions with Git are isolated within dedicated components.

Typical operations include:

- Repository discovery.
- Repository cloning.
- Fetching remote changes.
- Repository inspection.
- Branch inspection.
- Safe repository updates.

Keeping Git operations separate from synchronisation logic simplifies testing and future maintenance.

## User Interface

Presentation is separated from application logic.

User interface components are responsible for:

- Console formatting.
- Progress reporting.
- Tables.
- Colours and styling.
- Summary generation.

This separation makes it easier to support alternative output formats in the future.

## Error Handling

Errors are handled as close as possible to their source.

Where practical:

- Validation errors stop processing before synchronisation begins.
- Repository-specific failures do not prevent unrelated repositories from being processed.
- Errors are reported clearly and consistently.
- The application always attempts to produce a useful summary.

## Extensibility

A new behaviour belongs in the component that already owns that responsibility.
