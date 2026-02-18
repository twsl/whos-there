# Conda-Forge Feedstock Upgrade Guide

## Overview

This document provides instructions for upgrading the [whos-there conda-forge feedstock](https://github.com/conda-forge/whos-there-feedstock) to use the new build system and latest version.

## Current Status

- **Current conda-forge version**: 0.4.1
- **Latest PyPI version**: 0.6.0
- **Current build system**: Poetry + poetry-dynamic-versioning
- **New build system**: Hatchling + uv-dynamic-versioning

## Why Upgrade?

The whos-there project has migrated from Poetry to a modern build system using:
- **Hatchling**: PEP 517 compliant build backend
- **uv-dynamic-versioning**: Dynamic versioning from git tags
- **uv**: Fast Python package manager for development dependencies

This migration improves:
- Build speed and reliability
- Standards compliance (PEP 517/518/621)
- Compatibility with modern Python packaging tools

## Azure Build Issues

If you're seeing Azure build failures on the conda-forge feedstock, it's likely due to:
1. Poetry/poetry-dynamic-versioning being deprecated in the package
2. Incompatibilities with the new dependency versions
3. The package expecting hatchling as the build backend

## Updated meta.yaml

Here's the updated `recipe/meta.yaml` for conda-forge:

```yaml
{% set name = "whos-there" %}
{% set version = "0.6.0" %}

package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  url: https://pypi.org/packages/source/{{ name[0] }}/{{ name }}/{{ name.replace('-', '_') }}-{{ version }}.tar.gz
  sha256: # UPDATE THIS with the sha256 from PyPI for version 0.6.0

build:
  number: 0
  noarch: python
  script: {{ PYTHON }} -m pip install . -vv --no-deps --no-build-isolation

requirements:
  host:
    - pip
    - python >=3.11
    - hatchling
    - uv-dynamic-versioning
  run:
    - python >=3.11
    - lightning >=2.6.1
    - python-telegram-bot >=22.6
    - requests >=2.32.5

test:
  imports:
    - whos_there
    - whos_there.senders
    - whos_there.callback
  commands:
    - pip check
  requires:
    - pip

about:
  home: https://twsl.github.io/whos-there/
  summary: The spiritual successor to knockknock for PyTorch Lightning, get notified when your training ends
  license: MIT
  license_file: LICENSE
  description: |
    The spiritual successor to knockknock for PyTorch Lightning, 
    get notified when your training is complete or when it crashes during the 
    process with a single callback.

    ## Features

    - Supports E-Mail, Discord, Slack, Teams, Telegram
  doc_url: https://twsl.github.io/whos-there/
  dev_url: https://github.com/twsl/whos-there

extra:
  recipe-maintainers:
    - twsl
    - sugatoray
```

## Key Changes

### 1. Version Update
```yaml
# OLD
{% set version = "0.4.1" %}

# NEW
{% set version = "0.6.0" %}
```

### 2. Build Requirements
```yaml
# OLD
requirements:
  host:
    - pip
    - python {{ python_min }}
    - poetry
    - poetry-dynamic-versioning

# NEW
requirements:
  host:
    - pip
    - python >=3.11
    - hatchling
    - uv-dynamic-versioning
```

### 3. Runtime Dependencies
Updated to match the current pyproject.toml:
```yaml
# OLD
  run:
    - python >={{ python_min }}
    - python-telegram-bot >=20.0
    - lightning >=2.2.0
    - requests >=2.26.0,<3.0.0

# NEW
  run:
    - python >=3.11
    - lightning >=2.6.1
    - python-telegram-bot >=22.6
    - requests >=2.32.5
```

### 4. Python Version
The package now requires Python 3.11+ (previously used a variable `python_min`).

### 5. Build Script
Added recommended flags for conda-forge:
```yaml
# OLD
script: {{ PYTHON }} -m pip install . -vv

# NEW
script: {{ PYTHON }} -m pip install . -vv --no-deps --no-build-isolation
```

## How to Get the SHA256

To get the sha256 for version 0.6.0:

```bash
curl -sL https://pypi.org/pypi/whos-there/0.6.0/json | jq -r '.urls[] | select(.packagetype=="sdist") | .digests.sha256'
```

Or visit: https://pypi.org/project/whos-there/0.6.0/#files and copy the SHA256 for the `.tar.gz` source distribution.

## Testing the Recipe Locally

If you want to test the recipe locally before submitting:

```bash
# Install conda-build
conda install conda-build

# Clone the feedstock
git clone https://github.com/conda-forge/whos-there-feedstock.git
cd whos-there-feedstock

# Update recipe/meta.yaml with the changes above

# Build the package
conda build recipe/

# Test the built package
conda install --use-local whos-there
python -c "import whos_there; print(whos_there.__version__)"
```

## Submitting the Update

1. Fork the [whos-there-feedstock](https://github.com/conda-forge/whos-there-feedstock) repository
2. Create a new branch: `git checkout -b update-v0.6.0`
3. Update `recipe/meta.yaml` with the changes above
4. Update the sha256 hash
5. Commit: `git commit -m "Update to version 0.6.0 and migrate to hatchling"`
6. Push and create a pull request
7. The Azure Pipelines CI will automatically test the build on all platforms

## Troubleshooting

### uv-dynamic-versioning availability

Good news! `uv-dynamic-versioning` is already available on conda-forge:
- Package: https://anaconda.org/conda-forge/uv-dynamic-versioning
- Latest version: 0.13.0
- It should work without any issues in the recipe

### Build still fails

If the build still fails:
1. Check the Azure Pipelines logs for specific error messages
2. Verify all dependencies are available on conda-forge
3. Consider using `pip` to install from PyPI as a temporary workaround:
   ```yaml
   source:
     url: https://pypi.io/packages/source/w/whos-there/whos_there-{{ version }}-py3-none-any.whl
   ```

## Additional Resources

- [conda-forge documentation](https://conda-forge.org/docs/)
- [PyPI package page](https://pypi.org/project/whos-there/)
- [GitHub repository](https://github.com/twsl/whos-there)
- [Current pyproject.toml](https://github.com/twsl/whos-there/blob/main/pyproject.toml)

## Contact

For questions or issues:
- Open an issue in the [whos-there repository](https://github.com/twsl/whos-there/issues)
- Mention @twsl or @sugatoray (conda-forge maintainers)
