---
title: Contributing
---

# Contributing

Thank you for your interest in contributing to **Lupaxa GitHub Repository Sync**.

Contributions of all sizes are welcome, whether they involve fixing bugs, improving documentation, enhancing usability, or implementing new features.

This document outlines the development workflow and coding standards used throughout the project.

---

# Before You Start

Before making changes, it is recommended that you:

- Read the project documentation.
- Search existing issues and discussions.
- Confirm that the work is not already in progress.
- Open an issue to discuss significant changes before beginning implementation.

Early discussion helps ensure that proposed changes align with the long-term direction of the project.

---

# Development Environment

Clone the repository.

```bash
git clone https://github.com/the-lupaxa-project/lupaxa-github-repo-sync.git
```

Change into the project directory.

```bash
cd lupaxa-github-repo-sync
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the virtual environment.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install the project in editable mode together with the development dependencies.

```bash
pip install -e ".[dev]"
```

---

# Development Workflow

The typical workflow is:

1. Create a feature branch.
2. Implement the required changes.
3. Update the documentation if necessary.
4. Run the project's quality checks.
5. Run the test suite.
6. Commit your changes.
7. Submit a pull request.

Keeping changes focused and self-contained makes them easier to review.

---

# Coding Standards

The project aims to follow modern Python best practices.

General guidelines include:

- Use descriptive names.
- Prefer clarity over cleverness.
- Keep functions focused on a single responsibility.
- Avoid unnecessary complexity.
- Add type hints where appropriate.
- Write docstrings for public interfaces.

Consistency across the codebase is more important than individual style preferences.

---

# Code Formatting

Source code should be formatted using the project's chosen formatting tools before submission.

Typical checks include:

```bash
ruff check .
```

```bash
ruff format .
```

Any reported issues should be resolved before creating a pull request.

---

# Testing

Contributors are expected to run the test suite before submitting changes.

For example:

```bash
pytest
```

Where practical, new functionality should be accompanied by appropriate tests.

---

# Documentation

Documentation should be updated whenever changes affect:

- User-visible behaviour.
- Configuration.
- Command-line options.
- Synchronisation behaviour.
- Installation.
- Development workflows.

Keeping documentation up to date is considered an important part of maintaining the project.

---

# Commit Messages

Commit messages should be concise and clearly describe the purpose of the change.

For example:

```text
Improve repository validation
```

```text
Add support for SSH clone protocol
```

Avoid vague commit messages such as:

```text
Update
```

or

```text
Fix stuff
```

Meaningful commit messages make the project's history easier to understand.

---

# Pull Requests

Before opening a pull request, ensure that:

- The code builds successfully.
- Tests pass.
- Documentation has been updated where necessary.
- Formatting and linting have been completed.
- Unrelated changes have not been included.

Smaller, focused pull requests are generally easier to review than large collections of unrelated changes.

---

# Reporting Bugs

Bug reports should include as much relevant information as possible, including:

- Operating system.
- Python version.
- Git version.
- Application version.
- Steps to reproduce the issue.
- Expected behaviour.
- Actual behaviour.
- Relevant console output.

Providing reproducible examples greatly improves the likelihood of a quick resolution.

---

# Suggesting New Features

Feature requests are welcome.

When proposing a new feature, consider including:

- The problem being solved.
- Why the existing behaviour is insufficient.
- A suggested approach.
- Any alternatives that were considered.

Clear proposals encourage productive discussion and help shape future development.

---

# Code of Conduct

All contributors are expected to follow the project's Code of Conduct and interact respectfully with other members of the community.

---

# Thank You

Every contribution, whether large or small, helps improve **Lupaxa GitHub Repository Sync**.

Thank you for taking the time to contribute to the project.
