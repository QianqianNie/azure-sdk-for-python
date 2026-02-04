# Guide: Creating a New Repository or SDK Package under Azure Organization

This guide provides instructions for creating a new repository or adding a new SDK package to the Azure SDK for Python ecosystem.

## Table of Contents

1. [Creating a New SDK Package in This Repository](#creating-a-new-sdk-package-in-this-repository)
2. [Creating a Standalone Repository](#creating-a-standalone-repository)
3. [Repository Structure Requirements](#repository-structure-requirements)
4. [Configuration Files](#configuration-files)
5. [CI/CD Setup](#cicd-setup)

## Creating a New SDK Package in This Repository

Most Azure SDK packages should be added to the existing `azure-sdk-for-python` repository rather than creating a new standalone repository. This approach provides:

- Consistent tooling and CI/CD
- Shared infrastructure and testing
- Easier maintenance and collaboration

### Prerequisites

- Python 3.7 or later installed
- Git installed and configured
- Access to Azure organization (for official packages)
- Understanding of [Azure SDK Design Guidelines](https://azure.github.io/azure-sdk/python/guidelines/index.html)

### Step 1: Determine Package Name

Follow the naming convention: `azure-<service>-<specific>`

Examples:
- `azure-storage-blob`
- `azure-keyvault-secrets`
- `azure-mgmt-compute`

### Step 2: Create Package Structure

```bash
# Navigate to the SDK directory
cd /path/to/azure-sdk-for-python/sdk

# Create a new service directory (if it doesn't exist)
mkdir <service-name>
cd <service-name>

# Create the package directory
mkdir azure-<service>-<specific>
cd azure-<service>-<specific>
```

### Step 3: Initialize Package Structure

Create the following structure:

```
azure-<service>-<specific>/
├── azure/
│   ├── __init__.py
│   └── <service>/
│       ├── __init__.py
│       ├── <specific>/
│       │   ├── __init__.py
│       │   ├── _client.py
│       │   ├── _models.py
│       │   └── _version.py
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_<specific>.py
│   └── conftest.py
├── samples/
│   └── README.md
├── README.md
├── CHANGELOG.md
├── setup.py
├── setup.cfg
├── MANIFEST.in
├── dev_requirements.txt
└── sdk_packaging.toml
```

### Step 4: Create Essential Files

#### setup.py

```python
from setuptools import setup, find_packages

setup(
    name="azure-<service>-<specific>",
    version="1.0.0b1",
    description="Microsoft Azure <Service> <Specific> Client Library for Python",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="MIT License",
    author="Microsoft Corporation",
    author_email="azpysdkhelp@microsoft.com",
    url="https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/<service>/azure-<service>-<specific>",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(exclude=["tests", "samples"]),
    install_requires=[
        "azure-core>=1.24.0",
    ],
    python_requires=">=3.7",
)
```

#### README.md

```markdown
# Azure <Service> <Specific> client library for Python

This is the Microsoft Azure <Service> <Specific> Client Library.

## Getting started

### Prerequisites

- Python 3.7 or later
- An Azure subscription
- An <Service> resource

### Install the package

```bash
pip install azure-<service>-<specific>
```

## Key concepts

[Describe the main concepts]

## Examples

[Provide usage examples]

## Contributing

This project welcomes contributions and suggestions.
```

#### CHANGELOG.md

```markdown
# Release History

## 1.0.0b1 (Unreleased)

### Features Added

- Initial release
```

### Step 5: Register the Package

1. Add the package to `ci_template.yml` in the repository root
2. Add the package to appropriate CI/CD pipelines
3. Update `CODEOWNERS` if needed

## Creating a Standalone Repository

In rare cases, you may need to create a completely separate repository under the Azure organization.

### When to Create a Standalone Repository

- The package is not part of the Azure SDK ecosystem
- Special infrastructure requirements that conflict with the monorepo
- Approved by Azure SDK architecture board

### Steps to Create a Standalone Repository

1. **Get Approval**: Contact the Azure SDK team for approval
2. **Repository Creation**: Work with Azure GitHub administrators to create the repository
3. **Set up Repository Structure**: Follow the structure documented above
4. **Configure CI/CD**: Set up Azure Pipelines or GitHub Actions
5. **Add Required Files**:
   - LICENSE
   - CODE_OF_CONDUCT.md
   - CONTRIBUTING.md
   - SECURITY.md
   - .gitignore
   - README.md

### Required GitHub Settings

- **Branch Protection**: Enable for main/master branch
- **Required Reviews**: At least one approval required
- **Status Checks**: CI must pass before merging
- **Signed Commits**: Recommended

## Repository Structure Requirements

All Azure SDK repositories should follow these conventions:

### Root Level Files

- `README.md`: Overview and getting started
- `LICENSE`: MIT License
- `CODE_OF_CONDUCT.md`: Microsoft Open Source Code of Conduct
- `CONTRIBUTING.md`: Contribution guidelines
- `SECURITY.md`: Security policy and reporting
- `.gitignore`: Standard Python gitignore
- `setup.py` or `pyproject.toml`: Package configuration

### Required Directories

- `azure/`: Source code namespace package
- `tests/`: Test files
- `samples/`: Usage examples
- `doc/` or `docs/`: Additional documentation

## Configuration Files

### .gitignore

Include standard Python patterns:

```
*.pyc
__pycache__/
*.egg-info/
dist/
build/
.venv/
.pytest_cache/
.coverage
htmlcov/
```

### tox.ini

For testing across multiple Python versions:

```ini
[tox]
envlist = py37,py38,py39,py310,py311

[testenv]
deps = -r dev_requirements.txt
commands = pytest tests/
```

### sdk_packaging.toml

For Azure SDK specific configuration:

```toml
[packaging]
package_name = "azure-<service>-<specific>"
package_pprint_name = "Azure <Service> <Specific>"
package_doc_id = ""
is_stable = false
is_arm = false
```

## CI/CD Setup

### GitHub Actions (if standalone repository)

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.7', '3.8', '3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r dev_requirements.txt
        pip install -e .
    - name: Run tests
      run: pytest tests/
    - name: Run linting
      run: |
        pylint azure/
        black --check azure/ tests/
```

### Azure Pipelines (for azure-sdk-for-python)

The monorepo already has pipelines configured. Add your package to:
- `ci_template.yml`
- `eng/pipelines/templates/jobs/`

## Best Practices

1. **Follow Azure SDK Guidelines**: https://azure.github.io/azure-sdk/python/guidelines/
2. **Use Type Hints**: Add type annotations to all public APIs
3. **Write Tests**: Aim for >80% code coverage
4. **Document Everything**: Clear docstrings and README
5. **Version Semantically**: Follow semantic versioning
6. **Review Security**: Use CodeQL and security scanning

## Resources

- [Azure SDK for Python Guidelines](https://azure.github.io/azure-sdk/python/guidelines/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Contributing Guide](../../CONTRIBUTING.md)
- [Azure SDK Blog](https://devblogs.microsoft.com/azure-sdk/)

## Getting Help

- File issues on GitHub: https://github.com/Azure/azure-sdk-for-python/issues
- Ask on Stack Overflow with tags: `azure` and `python`
- Contact: azpysdkhelp@microsoft.com
