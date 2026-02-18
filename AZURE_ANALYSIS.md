# Azure Build Failure Analysis & Conda-Forge Migration to UV

## Executive Summary

The conda-forge feedstock for whos-there is failing because:
1. **Outdated version**: Feedstock uses v0.4.1, but current release is v0.6.0
2. **Build system mismatch**: Feedstock uses Poetry, but package migrated to Hatchling + uv-dynamic-versioning
3. **Dependency updates**: Runtime dependencies have been updated with stricter version requirements

## Current State

### Repository (whos-there)
- **Version**: 0.6.0 (latest on PyPI)
- **Build Backend**: Hatchling
- **Version Management**: uv-dynamic-versioning
- **Package Manager**: uv (for development)
- **Python Requirement**: >=3.11

### Conda-Forge Feedstock
- **Version**: 0.4.1 (outdated)
- **Build Backend**: Poetry + poetry-dynamic-versioning
- **Status**: Likely failing on Azure Pipelines

## Root Cause Analysis

The whos-there project underwent a major tooling migration:

### Before (v0.4.1)
```toml
[build-system]
requires = ["poetry-core", "poetry-dynamic-versioning"]
build-backend = "poetry.core.masonry.api"
```

### After (v0.6.0)
```toml
[build-system]
requires = ["hatchling", "uv-dynamic-versioning"]
build-backend = "hatchling.build"
```

This change means:
- Poetry is no longer maintained in the project
- Old recipe will fail to build newer versions
- Dependencies have been updated

## Solution

Update the conda-forge feedstock to:
1. Bump version to 0.6.0
2. Replace Poetry with Hatchling + uv-dynamic-versioning
3. Update runtime dependencies to match current requirements
4. Update Python version constraint to >=3.11

## Implementation

Two approaches are provided:

### Approach 1: Build from Source (Recommended)
Uses the source distribution (`.tar.gz`) and builds with Hatchling.
- **File**: `conda-forge-meta.yaml`
- **Pros**: Standard conda-forge approach, builds from source
- **Cons**: Requires uv-dynamic-versioning (but it's available on conda-forge)

### Approach 2: Install Pre-built Wheel (Fallback)
Uses the pre-built wheel from PyPI.
- **File**: `conda-forge-meta-alternative.yaml`
- **Pros**: Avoids build-time dependencies, faster build
- **Cons**: Less standard for conda-forge, doesn't build from source

## Dependencies Status

All required dependencies are available on conda-forge:
- ✅ `hatchling` - Available
- ✅ `uv-dynamic-versioning` - Available (v0.13.0)
- ✅ `lightning` - Available
- ✅ `python-telegram-bot` - Available
- ✅ `requests` - Available

## Migration Steps

1. **Fork and Clone**
   ```bash
   git clone https://github.com/conda-forge/whos-there-feedstock.git
   cd whos-there-feedstock
   git checkout -b update-v0.6.0-uv-migration
   ```

2. **Update recipe/meta.yaml**
   - Replace contents with `conda-forge-meta.yaml`
   - Or manually apply changes from `CONDA_FORGE_UPGRADE_GUIDE.md`

3. **Test Locally (Optional)**
   ```bash
   conda build recipe/
   ```

4. **Submit Pull Request**
   - Push to your fork
   - Create PR to conda-forge/whos-there-feedstock
   - Azure Pipelines will run tests automatically

5. **Monitor Build**
   - Check Azure Pipelines for any failures
   - Address any issues that arise

## Expected Build Behavior

### Azure Pipelines
The feedstock uses Azure Pipelines to build on:
- Linux (multiple architectures)
- Windows
- macOS

All builds should succeed as the package is `noarch: python`.

### Common Issues

1. **uv-dynamic-versioning missing**: Already available on conda-forge
2. **Version mismatch**: Ensure sha256 matches PyPI
3. **Dependency conflicts**: All deps available with correct versions

## Testing Checklist

After the PR is merged, verify:
- [ ] Package builds successfully on all platforms
- [ ] Version is 0.6.0
- [ ] `conda install conda-forge::whos-there` works
- [ ] Import works: `python -c "import whos_there; print(whos_there.__version__)"`
- [ ] Dependencies are correctly installed
- [ ] No regression in functionality

## References

- **Current PyPI Package**: https://pypi.org/project/whos-there/0.6.0/
- **Conda-Forge Feedstock**: https://github.com/conda-forge/whos-there-feedstock
- **Package Repository**: https://github.com/twsl/whos-there
- **Azure Build Status**: https://dev.azure.com/conda-forge/feedstock-builds/_build?definitionId=14896
- **uv-dynamic-versioning on conda-forge**: https://anaconda.org/conda-forge/uv-dynamic-versioning

## Timeline

- **v0.4.1**: Last conda-forge release (using Poetry)
- **v0.6.0**: Current PyPI release (using Hatchling + uv)
- **Migration**: Update feedstock to support v0.6.0+

## Contact

For issues or questions:
- **Package Maintainer**: @twsl
- **Conda-Forge Maintainer**: @twsl, @sugatoray
- **Repository Issues**: https://github.com/twsl/whos-there/issues
