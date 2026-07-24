---
title: Contributing
---

# Contributing

Thank you for your interest in contributing to **Lupaxa GitHub Repository Sync**.

Whether you are fixing a bug, improving the documentation, adding a new feature or suggesting an enhancement, your contribution is appreciated.

This guide describes the standards and workflow used throughout the project to ensure that contributions remain consistent, maintainable and easy to review.

## Before You Start

Before beginning any work, ensure that you have:

- Read the project documentation.
- Set up a local development environment.
- Run the existing test suite successfully.
- Familiarised yourself with the project structure.

Understanding the existing architecture before making changes will usually result in smaller, cleaner contributions.

## Types of Contributions

Contributions may include:

- Bug fixes.
- New features.
- Performance improvements.
- Documentation improvements.
- Test improvements.
- Refactoring.
- Build and tooling improvements.

Every contribution should improve the project without introducing unnecessary complexity.

## Development Workflow

The recommended development workflow is:

1. Fork the repository (if applicable).
2. Clone the repository locally.
3. Create a new feature branch.
4. Implement the required changes.
5. Add or update automated tests.
6. Update the documentation where required.
7. Run the complete test suite.
8. Submit a pull request.

Keeping changes focused on a single objective makes reviews significantly easier.

## Branch Naming

Branches should use clear, descriptive names.

Examples include:

```text
feature/add-json5-validation
bugfix/fix-repository-discovery
docs/update-installation-guide
refactor/simplify-config-loader
```

Avoid generic branch names such as:

```text
new
changes
test
update
```

## Coding Standards

All code should:

- Be readable.
- Be well structured.
- Follow the project's formatting standards.
- Use descriptive names.
- Include appropriate type annotations where applicable.
- Avoid unnecessary complexity.

Code should be written for long-term maintainability rather than minimal line count.

## Documentation

Documentation is considered part of the source code.

Whenever user-facing behaviour changes:

- Update the relevant documentation.
- Add examples where appropriate.
- Remove obsolete information.
- Keep terminology consistent.

Changes should never leave the documentation out of sync with the application.

## Testing

Every functional change should include appropriate automated tests.

Before submitting a contribution:

- Run the complete test suite.
- Ensure all tests pass.
- Add regression tests for bug fixes.
- Update existing tests where behaviour has changed.

Changes that reduce test quality should be avoided.

## Commit Messages

Commit messages should clearly describe the purpose of the change.

Examples:

```text
Add repository validation for duplicate entries

Improve configuration error reporting

Update installation documentation

Fix repository discovery when organisation is empty
```

Avoid commit messages such as:

```text
Fix stuff

Changes

Update

Misc
```

Clear commit messages make the project history significantly easier to understand.

## Pull Requests

When submitting a pull request:

- Keep the scope focused.
- Describe the purpose of the change.
- Explain any significant design decisions.
- Reference related issues where appropriate.
- Ensure all automated checks pass.

Smaller pull requests are generally easier to review than large, unrelated collections of changes.

## Code Review

Code review helps maintain the overall quality of the project.

Reviewers may consider:

- Correctness.
- Readability.
- Maintainability.
- Performance.
- Documentation.
- Test coverage.
- Consistency with the existing architecture.

Feedback should be constructive, respectful and focused on improving the project.

## Backwards Compatibility

Where practical, changes should preserve compatibility with existing configurations and workflows.

If a breaking change is unavoidable:

- Clearly document it.
- Update the migration guidance.
- Include it in the release notes.

Minimising unnecessary breaking changes helps provide a stable experience for users.

## Reporting Issues

When reporting an issue, include as much relevant information as possible.

Useful information includes:

- Application version.
- Python version.
- Operating system.
- Command executed.
- Configuration details (where appropriate).
- Console output.
- Steps required to reproduce the issue.

Providing complete information significantly reduces the time required to investigate and resolve problems.

## Summary

Successful contributions are typically:

- Well scoped.
- Well tested.
- Well documented.
- Easy to review.
- Consistent with the existing architecture.

Following the guidance in this document helps ensure that contributions can be reviewed and integrated efficiently.

## Next Steps

Continue to **Release Process** to learn how new versions of Lupaxa GitHub Repository Sync are prepared, validated and published.
