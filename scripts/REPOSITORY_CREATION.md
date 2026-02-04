# Repository Creation Tools

This directory contains tools and scripts for creating new repositories and SDK packages within the Azure SDK for Python ecosystem.

## Available Tools

### 1. create_new_sdk_package.py

A Python script that automates the creation of a new Azure SDK package with proper structure, configuration, and boilerplate code.

**Usage:**

```bash
# Basic usage
python scripts/create_new_sdk_package.py --service <service> --package <package-name>

# Example: Create azure-storage-blob package
python scripts/create_new_sdk_package.py --service storage --package blob

# Preview changes without creating files (dry run)
python scripts/create_new_sdk_package.py --service storage --package blob --dry-run

# Specify custom repository root
python scripts/create_new_sdk_package.py --service storage --package blob --repo-root /path/to/repo
```

**What it creates:**

```
sdk/<service>/azure-<service>-<package>/
├── azure/
│   └── <service>/
│       └── <package>/
│           ├── __init__.py
│           ├── _client.py
│           ├── _models.py
│           └── _version.py
├── tests/
│   ├── __init__.py
│   ├── test_<package>.py
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

**After running the script:**

1. Review and customize the generated files
2. Implement the client logic
3. Add tests
4. Add samples
5. Update documentation
6. Register the package in `ci_template.yml`

## Documentation

For comprehensive guides on creating repositories and packages, see:

- [Creating New Repositories Guide](../doc/dev/create_new_repository.md) - Complete guide for creating new repositories or SDK packages
- [Contributing Guide](../CONTRIBUTING.md) - General contribution guidelines
- [Azure SDK Guidelines](https://azure.github.io/azure-sdk/python/guidelines/) - Design guidelines for Azure SDK

## Common Scenarios

### Adding a new service SDK to this repository

This is the most common scenario. Use the `create_new_sdk_package.py` script:

```bash
python scripts/create_new_sdk_package.py --service myservice --package client
```

### Creating a management (control plane) SDK

For Azure Resource Manager SDKs, follow the same process but use the `mgmt` naming convention:

```bash
python scripts/create_new_sdk_package.py --service myservice --package mgmt
```

The package will be named `azure-myservice-mgmt`.

### Creating a standalone repository

In rare cases, you may need a standalone repository. See the [Creating New Repositories Guide](../doc/dev/create_new_repository.md) for detailed instructions.

## Requirements

- Python 3.7 or later
- Git
- Write access to the repository (for creating packages)
- Azure organization membership (for standalone repositories)

## Getting Help

If you encounter issues or need assistance:

1. Check the [documentation](../doc/dev/create_new_repository.md)
2. Review existing packages in the `sdk/` directory for examples
3. Ask on GitHub Discussions: https://github.com/Azure/azure-sdk-for-python/discussions
4. File an issue: https://github.com/Azure/azure-sdk-for-python/issues
5. Contact: azpysdkhelp@microsoft.com
