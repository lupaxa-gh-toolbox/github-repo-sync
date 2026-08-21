# Release Process

This guide describes the process used to prepare, validate and publish new releases of **GitHub Repository Sync**.

Following a consistent release process helps ensure that every published version is stable, well tested and fully documented.

The release process applies to both feature releases and maintenance releases.

## Release Objectives

Every release should:

- Be stable.
- Be fully tested.
- Include accurate documentation.
- Be versioned consistently.
- Be reproducible.
- Be easy to verify.

No release should be published until all validation steps have been completed successfully.

## Release Workflow

The overall release process follows the workflow below.

```text
Complete Development
         │
         ▼
Run Automated Tests
         │
         ▼
Update Documentation
         │
         ▼
Update Version Number
         │
         ▼
Create Release Commit
         │
         ▼
Create Git Tag
         │
         ▼
Build Distribution
         │
         ▼
Validate Package
         │
         ▼
Publish Release
         │
         ▼
Publish Documentation
```

Each stage should be completed before progressing to the next.

## Preparing a Release

Before creating a release:

- Complete all planned development.
- Merge approved pull requests.
- Resolve known defects scheduled for the release.
- Ensure the repository is in a clean state.
- Verify that all automated checks are passing.

Releases should always begin from a stable branch.

## Version Management

The project follows a consistent versioning scheme.

Whenever a release is prepared:

- Update the application version.
- Update package metadata.
- Update any version references within the documentation.
- Ensure the reported version matches the release tag.

Version numbers should only be changed as part of the release process.

## Documentation Review

Documentation should be reviewed before every release.

Verify that:

- New features are documented.
- Removed features are no longer referenced.
- Examples remain accurate.
- Command-line documentation matches the application.
- Configuration documentation reflects the current implementation.

Documentation should always be released alongside the corresponding version of the application.

## Running Automated Validation

Before publishing a release, execute the complete validation process.

Typical validation includes:

- Static analysis.
- Code formatting checks.
- Automated tests.
- Documentation build.
- Package build.
- Installation verification.

Every validation stage should complete successfully before publishing.

## Building the Package

Build the distribution packages.

For example:

```bash
python -m build
```

Typical build artefacts include:

- Source distribution (`sdist`).
- Python wheel (`wheel`).

Generated artefacts should be inspected before publication.

## Package Verification

Before publishing:

- Verify the package builds successfully.
- Confirm the package installs correctly.
- Verify the command-line interface starts successfully.
- Confirm the reported version matches the release.

Installation testing should be performed using a clean virtual environment wherever practical.

## Creating a Release Tag

Once validation has completed successfully, create a Git tag for the release.

Example:

```bash
git tag v1.2.0
git push origin v1.2.0
```

Release tags should uniquely identify every published version.

## Publishing

Once the release has been validated:

- Publish the package.
- Publish the release notes.
- Publish the updated documentation.
- Verify that published artefacts are accessible.

Stable tags (`vX.Y.Z`) run **Generate Release**, which builds the sdist/wheel
and uploads to PyPI via Trusted Publishing. Release-candidate tags
(`vX.Y.Z-rcN`) run **Generate Test Release** and upload to TestPyPI. This
repository must be registered as a Trusted Publisher on both indexes
(workflow files `generate-release.yml` and `generate-test-release.yml`; no
API token). See
[PyPI trusted publishers](https://docs.pypi.org/trusted-publishers/).

Any automated publication workflows should be monitored until they complete successfully.

## Post-Release Verification

After publication:

- Confirm the package can be installed.
- Verify the documentation site has updated.
- Confirm the correct version is reported.
- Review automated workflow results.
- Check that release assets are available.

Any issues discovered after publication should be investigated immediately.

## Hotfix Releases

Where a critical issue is identified after publication:

1. Prepare a focused fix.
2. Validate the change.
3. Increment the version appropriately.
4. Publish a maintenance release.
5. Update the release notes.

Hotfix releases should contain only the changes required to resolve the issue.

## Release Checklist

Before publishing a release, confirm that:

- Development is complete.
- All automated tests pass.
- Static analysis passes.
- Documentation has been updated.
- Version numbers have been updated.
- Distribution packages build successfully.
- Installation has been verified.
- Release notes have been prepared.
- The Git tag has been created.
- Publication workflows complete successfully.

Using a consistent checklist reduces the likelihood of release errors.

## Summary

A consistent release process helps ensure that every version of GitHub Repository Sync is reliable, reproducible and fully documented.

By validating the application, reviewing the documentation and verifying the published artefacts, maintainers can confidently deliver high-quality releases.

## Next Steps

You have now reached the end of the documentation.

If you are new to the project, return to **Getting Started**. If you are contributing to the project, the **Development** section should serve as your primary reference for future work.
