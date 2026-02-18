# Conda-Forge Documentation

This directory contains documentation for updating the conda-forge feedstock for the whos-there package.

## Files

### 1. AZURE_ANALYSIS.md
**Purpose**: Comprehensive analysis of Azure build failures and the migration strategy.
- Root cause analysis of build failures
- Current state vs desired state
- Migration timeline and dependencies
- Testing checklist

### 2. CONDA_FORGE_UPGRADE_GUIDE.md
**Purpose**: Step-by-step guide for maintainers to upgrade the feedstock.
- Detailed instructions for updating meta.yaml
- Key changes explained with before/after examples
- Troubleshooting common issues
- How to get SHA256 checksums

### 3. conda-forge-meta.yaml
**Purpose**: Ready-to-use meta.yaml for the conda-forge feedstock (Recommended approach).
- Complete recipe for version 0.6.0
- Uses Hatchling + uv-dynamic-versioning
- Builds from PyPI source distribution
- All checksums verified

### 4. conda-forge-meta-alternative.yaml
**Purpose**: Alternative meta.yaml using pre-built wheel (Fallback approach).
- Uses pre-built wheel from PyPI
- Avoids build-time dependencies
- Faster build times
- Use only if the primary approach has issues

## Quick Start

If you're a conda-forge maintainer for whos-there:

1. Read `AZURE_ANALYSIS.md` to understand what went wrong
2. Follow `CONDA_FORGE_UPGRADE_GUIDE.md` for step-by-step instructions
3. Use `conda-forge-meta.yaml` as your new recipe
4. If issues arise, try `conda-forge-meta-alternative.yaml`

## Key Changes

The main change is migrating from Poetry to Hatchling:

**Old (v0.4.1)**
```yaml
requirements:
  host:
    - poetry
    - poetry-dynamic-versioning
```

**New (v0.6.0)**
```yaml
requirements:
  host:
    - hatchling
    - uv-dynamic-versioning
```

## Testing

Before submitting a PR to conda-forge:

```bash
# Test build locally
conda install conda-build
conda build recipe/

# Test installation
conda install --use-local whos-there

# Verify import
python -c "import whos_there; print(whos_there.__version__)"
```

## Support

For questions or issues:
- Create an issue in this repository: https://github.com/twsl/whos-there/issues
- Mention @twsl or @sugatoray (conda-forge maintainers)
