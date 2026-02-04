#!/usr/bin/env python3
"""
Script to create a new Azure SDK package structure.

This script automates the creation of a new SDK package following Azure SDK
guidelines and repository conventions.

Usage:
    python create_new_sdk_package.py --service <service> --package <package-name>

Example:
    python create_new_sdk_package.py --service storage --package blob
    # Creates: sdk/storage/azure-storage-blob/
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


SETUP_PY_TEMPLATE = '''"""
Setup configuration for {package_name}
"""
from setuptools import setup, find_packages

VERSION = "1.0.0b1"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{package_name}",
    version=VERSION,
    description="Microsoft Azure {service_title} {specific_title} Client Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    author="Microsoft Corporation",
    author_email="azpysdkhelp@microsoft.com",
    url="https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/{service}/{package_name}",
    keywords="azure, azure sdk",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(
        exclude=[
            "tests",
            "samples",
            "*.tests",
            "*.tests.*",
            "tests.*",
        ]
    ),
    install_requires=[
        "azure-core>=1.24.0",
        "typing-extensions>=4.0.1",
    ],
    python_requires=">=3.7",
)
'''

README_TEMPLATE = '''# Azure {service_title} {specific_title} client library for Python

This is the Microsoft Azure {service_title} {specific_title} Client Library.
This package has been tested with Python 3.7+.

For a more complete view of Azure libraries, see the [azure-sdk-for-python repository](https://github.com/Azure/azure-sdk-for-python).

## Getting started

### Prerequisites

- Python 3.7 or later is required to use this package.
- You must have an [Azure subscription](https://azure.microsoft.com/free/) and an Azure {service_title} resource to use this package.

### Install the package

Install the Azure {service_title} {specific_title} client library for Python with [pip](https://pypi.org/project/pip/):

```bash
pip install {package_name}
```

## Key concepts

TODO: Add key concepts documentation

## Examples

TODO: Add usage examples

### Create a client

```python
from azure.identity import DefaultAzureCredential
from azure.{service}.{specific} import {client_class}

credential = DefaultAzureCredential()
client = {client_class}(endpoint="<your-endpoint>", credential=credential)
```

## Troubleshooting

### General

TODO: Add troubleshooting information

### Logging

This library uses the standard [logging](https://docs.python.org/3/library/logging.html) library for logging.
Basic information about HTTP sessions (URLs, headers, etc.) is logged at INFO level.

## Next steps

### More sample code

TODO: Add links to samples

### Additional documentation

For more extensive documentation on Azure {service_title}, see the [Azure {service_title} documentation](https://docs.microsoft.com/azure/) on docs.microsoft.com.

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
'''

CHANGELOG_TEMPLATE = '''# Release History

## 1.0.0b1 (Unreleased)

### Features Added

- Initial preview release of Azure {service_title} {specific_title} Client Library for Python

### Breaking Changes

- N/A

### Bugs Fixed

- N/A

### Other Changes

- N/A
'''

INIT_PY = '''# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------
'''

VERSION_PY_TEMPLATE = '''# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

VERSION = "1.0.0b1"
'''

CLIENT_PY_TEMPLATE = '''# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

from typing import Any

from azure.core import PipelineClient
from azure.core.credentials import AzureKeyCredential

from ._version import VERSION


class {client_class}:
    """Azure {service_title} {specific_title} Client.
    
    :param endpoint: The endpoint URL for the service.
    :type endpoint: str
    :param credential: Credential used to authenticate requests to the service.
    :type credential: ~azure.core.credentials.AzureKeyCredential
    """

    def __init__(
        self,
        endpoint: str,
        credential: AzureKeyCredential,
        **kwargs: Any
    ) -> None:
        if not endpoint:
            raise ValueError("endpoint cannot be None or empty")
        if not credential:
            raise ValueError("credential cannot be None")

        self._client = PipelineClient(base_url=endpoint, **kwargs)
        self._credential = credential

    def __enter__(self):
        self._client.__enter__()
        return self

    def __exit__(self, *args):
        self._client.__exit__(*args)

    def close(self) -> None:
        """Close the client session."""
        self._client.close()
'''

MAIN_INIT_PY_TEMPLATE = '''# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

from ._version import VERSION
from ._client import {client_class}

__version__ = VERSION
__all__ = [
    "{client_class}",
]
'''

TEST_TEMPLATE = '''# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

import pytest

from azure.{service}.{specific} import {client_class}


class Test{client_class}:
    """Test suite for {client_class}."""

    def test_client_creation(self):
        """Test that the client can be created."""
        # TODO: Implement test
        pass
'''

CONFTEST_PY = '''# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

import pytest


@pytest.fixture
def client():
    """Fixture to create a client instance."""
    # TODO: Implement fixture
    pass
'''

DEV_REQUIREMENTS_TXT = '''pytest>=7.0.0
pytest-cov>=3.0.0
pytest-asyncio>=0.18.0
azure-core>=1.24.0
azure-identity>=1.10.0
typing-extensions>=4.0.1
'''

MANIFEST_IN = '''include *.md
include azure/__init__.py
recursive-include tests *.py
recursive-include samples *.py *.md
'''

SDK_PACKAGING_TOML_TEMPLATE = '''[packaging]
package_name = "{package_name}"
package_pprint_name = "Azure {service_title} {specific_title}"
package_doc_id = ""
is_stable = false
is_arm = false
'''

SAMPLES_README = '''# Samples for Azure {service_title} {specific_title}

These code samples show common scenario operations with the Azure {service_title} {specific_title} client library.

## Prerequisites

* Python 3.7 or later
* An Azure subscription
* An Azure {service_title} resource

## Setup

1. Install the package:

```bash
pip install {package_name}
```

2. Clone or download this repository
3. Open the sample folder in your preferred IDE

## Running the samples

Each sample is a standalone Python script that can be run directly:

```bash
python sample_basic.py
```

## Samples

TODO: Add sample descriptions
'''


def title_case(text: str) -> str:
    """Convert text to title case."""
    return text.replace("-", " ").replace("_", " ").title()


def to_class_name(service: str, specific: str) -> str:
    """Generate a client class name from service and specific parts."""
    service_part = "".join(word.title() for word in service.replace("-", "_").split("_"))
    specific_part = "".join(word.title() for word in specific.replace("-", "_").split("_"))
    return f"{service_part}{specific_part}Client"


def create_package_structure(
    repo_root: Path,
    service: str,
    specific: str,
    package_name: str,
    dry_run: bool = False
) -> None:
    """
    Create the directory structure and files for a new SDK package.
    
    :param repo_root: Root directory of the repository
    :param service: Service name (e.g., 'storage')
    :param specific: Specific package name (e.g., 'blob')
    :param package_name: Full package name (e.g., 'azure-storage-blob')
    :param dry_run: If True, only print actions without creating files
    """
    
    # Calculate paths
    service_dir = repo_root / "sdk" / service
    package_dir = service_dir / package_name
    azure_dir = package_dir / "azure"
    service_namespace_dir = azure_dir / service
    specific_namespace_dir = service_namespace_dir / specific
    tests_dir = package_dir / "tests"
    samples_dir = package_dir / "samples"
    
    # Prepare template variables
    service_title = title_case(service)
    specific_title = title_case(specific)
    client_class = to_class_name(service, specific)
    
    template_vars = {
        "package_name": package_name,
        "service": service,
        "specific": specific,
        "service_title": service_title,
        "specific_title": specific_title,
        "client_class": client_class,
    }
    
    # Define directory structure
    directories = [
        service_dir,
        package_dir,
        azure_dir,
        service_namespace_dir,
        specific_namespace_dir,
        tests_dir,
        samples_dir,
    ]
    
    # Define files to create
    files = {
        package_dir / "setup.py": SETUP_PY_TEMPLATE.format(**template_vars),
        package_dir / "README.md": README_TEMPLATE.format(**template_vars),
        package_dir / "CHANGELOG.md": CHANGELOG_TEMPLATE.format(**template_vars),
        package_dir / "MANIFEST.in": MANIFEST_IN,
        package_dir / "dev_requirements.txt": DEV_REQUIREMENTS_TXT,
        package_dir / "sdk_packaging.toml": SDK_PACKAGING_TOML_TEMPLATE.format(**template_vars),
        azure_dir / "__init__.py": INIT_PY,
        service_namespace_dir / "__init__.py": INIT_PY,
        specific_namespace_dir / "__init__.py": MAIN_INIT_PY_TEMPLATE.format(**template_vars),
        specific_namespace_dir / "_version.py": VERSION_PY_TEMPLATE,
        specific_namespace_dir / "_client.py": CLIENT_PY_TEMPLATE.format(**template_vars),
        tests_dir / "__init__.py": INIT_PY,
        tests_dir / f"test_{specific}.py": TEST_TEMPLATE.format(**template_vars),
        tests_dir / "conftest.py": CONFTEST_PY,
        samples_dir / "README.md": SAMPLES_README.format(**template_vars),
    }
    
    if dry_run:
        print(f"\\n{'='*80}")
        print(f"DRY RUN - Would create package: {package_name}")
        print(f"{'='*80}\\n")
        print("Directories to create:")
        for directory in directories:
            print(f"  📁 {directory.relative_to(repo_root)}")
        print("\\nFiles to create:")
        for file_path in files.keys():
            print(f"  📄 {file_path.relative_to(repo_root)}")
        print(f"\\n{'='*80}")
        return
    
    # Create directories
    print(f"\\nCreating package structure for {package_name}...")
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory.relative_to(repo_root)}")
    
    # Create files
    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Created file: {file_path.relative_to(repo_root)}")
    
    print(f"\\n{'='*80}")
    print(f"✓ Package structure created successfully!")
    print(f"{'='*80}")
    print(f"\\nPackage location: {package_dir.relative_to(repo_root)}")
    print(f"\\nNext steps:")
    print(f"  1. Review and customize the generated files")
    print(f"  2. Implement the client logic in {specific_namespace_dir / '_client.py'}")
    print(f"  3. Add tests in {tests_dir}")
    print(f"  4. Add samples in {samples_dir}")
    print(f"  5. Update README.md with specific documentation")
    print(f"  6. Register the package in ci_template.yml")
    print(f"\\nFor more information, see: doc/dev/create_new_repository.md")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Create a new Azure SDK package structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Create a new storage blob package:
    python %(prog)s --service storage --package blob
  
  Create a new keyvault secrets package:
    python %(prog)s --service keyvault --package secrets
  
  Dry run (preview changes without creating files):
    python %(prog)s --service storage --package blob --dry-run
        """
    )
    
    parser.add_argument(
        "--service",
        required=True,
        help="Service name (e.g., 'storage', 'keyvault', 'compute')"
    )
    
    parser.add_argument(
        "--package",
        required=True,
        help="Specific package name (e.g., 'blob', 'secrets', 'vm')"
    )
    
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Root directory of the repository (default: auto-detect)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without creating files"
    )
    
    args = parser.parse_args()
    
    # Determine repository root
    if args.repo_root:
        repo_root = args.repo_root.resolve()
    else:
        # Try to auto-detect from script location
        script_dir = Path(__file__).parent.resolve()
        # Script is in scripts/, so parent is the repo root
        repo_root = script_dir.parent
        
        # Verify this looks like the azure-sdk-for-python repo
        if not (repo_root / "sdk").exists():
            print("ERROR: Could not auto-detect repository root.", file=sys.stderr)
            print("Please specify --repo-root explicitly.", file=sys.stderr)
            sys.exit(1)
    
    # Validate inputs
    service = args.service.lower().replace("_", "-")
    specific = args.package.lower().replace("_", "-")
    package_name = f"azure-{service}-{specific}"
    
    # Check if package already exists
    package_dir = repo_root / "sdk" / service / package_name
    if package_dir.exists() and not args.dry_run:
        print(f"ERROR: Package already exists at {package_dir}", file=sys.stderr)
        print("Please choose a different service or package name.", file=sys.stderr)
        sys.exit(1)
    
    # Create the package structure
    try:
        create_package_structure(
            repo_root=repo_root,
            service=service,
            specific=specific,
            package_name=package_name,
            dry_run=args.dry_run
        )
    except Exception as e:
        print(f"\\nERROR: Failed to create package structure: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
