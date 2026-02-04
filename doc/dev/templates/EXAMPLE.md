# Example: Creating a New SDK Package

This example demonstrates how to use the `create_new_sdk_package.py` script to create a new Azure SDK package.

## Scenario

We want to create a new SDK package for Azure Widget Service's Client API.

- Service name: `widget`
- Package name: `client`
- Full package name: `azure-widget-client`

## Steps

### 1. Preview the Structure (Dry Run)

First, let's preview what will be created without actually creating any files:

```bash
cd /path/to/azure-sdk-for-python
python scripts/create_new_sdk_package.py --service widget --package client --dry-run
```

**Output:**
```
================================================================================
DRY RUN - Would create package: azure-widget-client
================================================================================

Directories to create:
  📁 sdk/widget
  📁 sdk/widget/azure-widget-client
  📁 sdk/widget/azure-widget-client/azure
  📁 sdk/widget/azure-widget-client/azure/widget
  📁 sdk/widget/azure-widget-client/azure/widget/client
  📁 sdk/widget/azure-widget-client/tests
  📁 sdk/widget/azure-widget-client/samples

Files to create:
  📄 sdk/widget/azure-widget-client/setup.py
  📄 sdk/widget/azure-widget-client/README.md
  📄 sdk/widget/azure-widget-client/CHANGELOG.md
  ... (more files)
```

### 2. Create the Package

Once you're satisfied with the preview, create the actual package:

```bash
python scripts/create_new_sdk_package.py --service widget --package client
```

**Output:**
```
Creating package structure for azure-widget-client...
✓ Created directory: sdk/widget
✓ Created directory: sdk/widget/azure-widget-client
✓ Created directory: sdk/widget/azure-widget-client/azure
... (more directories)

✓ Created file: sdk/widget/azure-widget-client/setup.py
✓ Created file: sdk/widget/azure-widget-client/README.md
... (more files)

================================================================================
✓ Package structure created successfully!
================================================================================

Package location: sdk/widget/azure-widget-client

Next steps:
  1. Review and customize the generated files
  2. Implement the client logic in azure/widget/client/_client.py
  3. Add tests in tests/
  4. Add samples in samples/
  5. Update README.md with specific documentation
  6. Register the package in ci_template.yml

For more information, see: doc/dev/create_new_repository.md
```

### 3. Examine the Created Structure

```bash
cd sdk/widget/azure-widget-client
tree .
```

**Structure:**
```
azure-widget-client/
├── azure/
│   ├── __init__.py
│   └── widget/
│       ├── __init__.py
│       └── client/
│           ├── __init__.py
│           ├── _client.py
│           └── _version.py
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   └── conftest.py
├── samples/
│   └── README.md
├── README.md
├── CHANGELOG.md
├── setup.py
├── MANIFEST.in
├── dev_requirements.txt
└── sdk_packaging.toml
```

### 4. Review Generated Client Code

The script creates a basic client template in `azure/widget/client/_client.py`:

```python
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from typing import Any

from azure.core import PipelineClient
from azure.core.credentials import AzureKeyCredential

from ._version import VERSION


class WidgetClientClient:
    """Azure Widget Client Client.
    
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
        # Implementation...
```

### 5. Customize the Package

Now you can customize the generated files:

#### Update the Client Implementation

Edit `azure/widget/client/_client.py` to add your service-specific methods:

```python
class WidgetClientClient:
    # ... existing __init__ ...
    
    def create_widget(self, name: str, **kwargs: Any) -> Dict[str, Any]:
        """Create a new widget.
        
        :param name: The name of the widget.
        :type name: str
        :return: The created widget.
        :rtype: dict
        """
        # Your implementation here
        pass
    
    def get_widget(self, widget_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Get a widget by ID.
        
        :param widget_id: The ID of the widget.
        :type widget_id: str
        :return: The widget.
        :rtype: dict
        """
        # Your implementation here
        pass
```

#### Add Tests

Edit `tests/test_client.py`:

```python
import pytest

from azure.widget.client import WidgetClientClient
from azure.core.credentials import AzureKeyCredential


class TestWidgetClientClient:
    """Test suite for WidgetClientClient."""

    def test_client_creation(self):
        """Test that the client can be created."""
        client = WidgetClientClient(
            endpoint="https://example.azure.com",
            credential=AzureKeyCredential("fake-key")
        )
        assert client is not None
    
    def test_create_widget(self):
        """Test creating a widget."""
        # Your test implementation
        pass
```

#### Update README

Edit `README.md` to add specific examples and documentation for your service.

#### Add Samples

Create sample files in `samples/` directory:

```python
# samples/sample_create_widget.py
"""
Example showing how to create a widget.
"""

from azure.identity import DefaultAzureCredential
from azure.widget.client import WidgetClientClient

# Create a client
credential = DefaultAzureCredential()
client = WidgetClientClient(
    endpoint="https://myaccount.azure.com",
    credential=credential
)

# Create a widget
widget = client.create_widget(name="My Widget")
print(f"Created widget: {widget}")
```

### 6. Install and Test Locally

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install test dependencies
pip install -r dev_requirements.txt

# Run tests
pytest tests/
```

### 7. Register with CI/CD

Add your package to the repository's CI/CD configuration:

1. Edit `ci_template.yml` in the repository root
2. Add an entry for your package
3. Commit and push your changes

### 8. Create Pull Request

```bash
git checkout -b feature/add-widget-client
git add sdk/widget/
git commit -m "Add azure-widget-client package"
git push origin feature/add-widget-client
```

Then create a pull request on GitHub.

## Tips

- **Use Type Hints**: Add type annotations to all public APIs
- **Write Docstrings**: Follow Azure SDK docstring conventions
- **Add Async Support**: Consider creating an async version in `_async/` directory
- **Test Coverage**: Aim for >80% code coverage
- **Follow Guidelines**: Review [Azure SDK Python Guidelines](https://azure.github.io/azure-sdk/python/guidelines/)

## Common Customizations

### Management (Resource Manager) SDK

For ARM SDKs, use different conventions:

```bash
python scripts/create_new_sdk_package.py --service widget --package mgmt
```

This creates `azure-widget-mgmt` suitable for Azure Resource Manager operations.

### Multi-service Package

If your service has multiple sub-services:

```bash
python scripts/create_new_sdk_package.py --service widget --package config
python scripts/create_new_sdk_package.py --service widget --package data
python scripts/create_new_sdk_package.py --service widget --package management
```

This creates:
- `azure-widget-config`
- `azure-widget-data`
- `azure-widget-management`

All under `sdk/widget/` directory.

## Troubleshooting

### Package Already Exists

If you get an error that the package already exists, either:
- Choose a different name
- Delete the existing package if it's a mistake
- Work on the existing package

### Import Errors

Make sure you've installed the package in development mode:
```bash
pip install -e .
```

### Test Failures

Check that all dependencies are installed:
```bash
pip install -r dev_requirements.txt
```

## Next Steps

- Read the [full documentation](../create_new_repository.md)
- Review [existing packages](../../../sdk/) for examples
- Check [Azure SDK Guidelines](https://azure.github.io/azure-sdk/python/guidelines/)
- Join the [Azure SDK community](https://github.com/Azure/azure-sdk-for-python/discussions)
