# Development Environment

This guide explains how to prepare a local development environment for **Lupaxa GitHub Repository Sync**.

A consistent development environment helps ensure that contributors can build, test and debug the application reliably across different operating systems.

## Prerequisites

Before working on the project, ensure the following software is installed.

### Python

Lupaxa GitHub Repository Sync requires a supported version of Python.

Verify your installation:

```bash
python3 --version
```

or

```bash
python --version
```

Refer to the project's installation documentation for the currently supported Python versions.

---

### Git

Git is required for cloning the repository and contributing changes.

Verify your installation:

```bash
git --version
```

---

### pip

The Python package installer is required for installing project dependencies.

Verify your installation:

```bash
python -m pip --version
```

---

### Virtual Environment Support

A virtual environment is strongly recommended to isolate project dependencies.

Verify that the `venv` module is available:

```bash
python -m venv --help
```

## Clone the Repository

Clone the repository using Git.

```bash
git clone https://github.com/lupaxa-gh-toolbox/github-repo-sync.git
```

Change into the project directory.

```bash
cd github-repo-sync
```

## Create a Virtual Environment

Create a virtual environment inside the project.

```bash
python -m venv .venv
```

Activate the environment.

### Linux

```bash
source .venv/bin/activate
```

### macOS

```bash
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

Once activated, the shell prompt should indicate that the virtual environment is active.

## Install Development Dependencies

Install the project in editable mode together with its development dependencies.

```bash
pip install -e ".[dev]"
```

Editable mode allows source code changes to take effect immediately without reinstalling the package.

## Verify the Installation

Confirm that the application starts successfully.

```bash
grs --version
```

or

```bash
python -m lupaxa.github_repo_sync --version
```

The exact invocation may vary depending on your installation method.

## Recommended Development Tools

The following tools are recommended during development.

| Tool              | Purpose                           |
| :---------------- | :-------------------------------- |
| Git               | Source control.                   |
| Python            | Application runtime.              |
| pip               | Package management.               |
| virtualenv / venv | Isolated development environment. |
| pytest            | Test execution.                   |
| Ruff              | Linting and formatting.           |
| MkDocs            | Documentation preview.            |

Depending on your workflow, additional IDE or editor extensions may also be useful.

## Documentation Preview

The project documentation is built using MkDocs.

Start the local documentation server.

```bash
mkdocs serve
```

The documentation can then be viewed in your web browser.

The server automatically rebuilds the documentation whenever files are modified.

## Running the Test Suite

Execute the complete test suite.

```bash
pytest
```

Run a specific test file.

```bash
pytest tests/test_example.py
```

Run a specific test.

```bash
pytest tests/test_example.py::test_function
```

## Keeping Dependencies Up to Date

Development dependencies should be updated periodically.

```bash
pip install --upgrade -e ".[dev]"
```

Always run the test suite after updating dependencies.

## Development Workflow

A typical development workflow is:

1. Clone the repository.
2. Create a virtual environment.
3. Install development dependencies.
4. Create a feature branch.
5. Implement the required changes.
6. Run the test suite.
7. Update the documentation where necessary.
8. Commit the changes.
9. Submit a pull request.

Following a consistent workflow helps maintain the quality of the project.

## Next Steps

Continue to **Project Structure** for an overview of the repository layout and the purpose of each directory.
