# GitHub Actions Workflow Templates

This directory contains template GitHub Actions workflows for Azure SDK Python packages and repositories.

## Available Templates

### 1. ci.yml - Continuous Integration

A comprehensive CI workflow that includes:
- **Linting**: black, flake8, pylint, mypy
- **Testing**: Multi-version Python testing (3.7-3.11) across OS platforms (Linux, Windows, macOS)
- **Code Coverage**: Integration with Codecov
- **Build**: Package building and validation
- **Security**: Bandit and Safety security scanning

**Usage:**
Copy to `.github/workflows/ci.yml` in your repository and customize as needed.

### 2. release.yml - Release Automation

A release workflow that handles:
- **Version Validation**: Ensures consistency between tags and package version
- **CHANGELOG Validation**: Checks for version entry in CHANGELOG
- **Build & Test**: Builds package and tests installation across platforms
- **TestPyPI**: Optional publishing to TestPyPI for validation
- **PyPI**: Automated publishing to PyPI on version tags
- **GitHub Releases**: Automatic GitHub release creation with extracted notes

**Usage:**
1. Copy to `.github/workflows/release.yml`
2. Set up PyPI API tokens as secrets:
   - `PYPI_API_TOKEN`: For production PyPI
   - `TEST_PYPI_API_TOKEN`: For TestPyPI (optional)

**Triggering releases:**

```bash
# Tag-based release (automatic PyPI publish)
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Manual release (TestPyPI)
# Use GitHub Actions UI to manually trigger with version input
```

## Customization Guide

### Adjusting Python Versions

Edit the matrix in workflows:

```yaml
matrix:
  python-version: ['3.7', '3.8', '3.9', '3.10', '3.11']
```

### Adjusting Operating Systems

```yaml
matrix:
  os: [ubuntu-latest, windows-latest, macos-latest]
```

### Adding Custom Steps

Add steps before or after existing ones:

```yaml
- name: Custom step
  run: |
    echo "Custom command"
```

### Configuring Secrets

Required secrets for release workflow:
- `PYPI_API_TOKEN`: Get from https://pypi.org/manage/account/token/
- `TEST_PYPI_API_TOKEN`: Get from https://test.pypi.org/manage/account/token/

Add secrets at: `Settings > Secrets and variables > Actions > New repository secret`

## Best Practices

1. **Branch Protection**: Enable required status checks for CI workflow
2. **Code Review**: Require at least one approval before merge
3. **Automated Testing**: Run tests on every PR
4. **Security Scanning**: Enable and monitor security workflow results
5. **Version Tags**: Use semantic versioning (v1.0.0 format)
6. **CHANGELOG**: Always update CHANGELOG.md before releases

## Integration with Azure Pipelines

If your repository uses Azure Pipelines instead of GitHub Actions, you can:
1. Use these as reference for implementing similar pipelines
2. Run both systems in parallel during migration
3. Gradually transition from Azure Pipelines to GitHub Actions

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Azure SDK Guidelines](https://azure.github.io/azure-sdk/python/guidelines/)
- [Semantic Versioning](https://semver.org/)

## Troubleshooting

### Workflow not triggering

- Check branch name matches trigger configuration
- Verify workflow file is in `.github/workflows/` directory
- Ensure YAML syntax is valid

### Test failures

- Check Python version compatibility
- Verify all dependencies are installed
- Review test logs for specific error messages

### Release failures

- Verify version numbers match (tag, setup.py, CHANGELOG)
- Check PyPI token is valid and has correct permissions
- Ensure package name is available on PyPI

## Getting Help

- GitHub Actions: https://github.com/features/actions
- Azure SDK Python: https://github.com/Azure/azure-sdk-for-python
- File issues: https://github.com/Azure/azure-sdk-for-python/issues
