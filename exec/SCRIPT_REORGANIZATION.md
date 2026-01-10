# Script Organization Complete

**Date:** January 10, 2026  
**Status:** ✅ Harmonized & Tested

## What Changed

### Problem
The project had an inconsistent structure with Python scripts in `src/` and bash scripts in `scripts/`, making it unclear that both were executable scripts rather than library code.

### Solution
Reorganized all scripts under a unified `scripts/` directory structure:

```
scripts/
├── bash/              # Shell scripts for PDF operations
│   ├── merge_pdfs.sh
│   ├── pdf_to_images.sh
│   ├── pdf_to_pptx.sh
│   └── pptx_to_pdf.sh
├── python/            # Python scripts for PPTX operations
│   ├── merge.py
│   ├── merge_pptx.py
│   ├── merge_cli.py
│   ├── merge_clone.py
│   ├── merge_images.py
│   ├── merge_template.py
│   ├── inspect_pptx.py
│   ├── pdf_images_to_pptx.py
│   ├── test_merge_templates.py
│   └── requirements.txt
└── setup_env.sh
```

### Benefits

1. **Clear organization**: All scripts in one place, organized by language
2. **Consistent treatment**: Python and bash scripts treated equally as executable scripts
3. **Better semantics**: `scripts/` clearly indicates executable code
4. **Simplified paths**: Easier to understand and navigate
5. **Docker-friendly**: Clean volume mounts without mixing concerns

## Changes Made

### 1. File Reorganization
- ✅ Moved all `*.py` from `src/` to `scripts/python/`
- ✅ Moved all `*.sh` from `scripts/` to `scripts/bash/`
- ✅ Moved `requirements.txt` to `scripts/python/`
- ✅ Made all scripts executable
- ✅ Removed empty `src/` folder (kept .venv for local dev if needed)

### 2. Docker Configuration
- ✅ Updated [Dockerfile](Dockerfile) to use new paths
- ✅ Updated [docker-compose.yml](docker-compose.yml) volume mounts
- ✅ Updated PATH to include both `scripts/bash` and `scripts/python`
- ✅ Fixed requirements.txt path in Docker build

### 3. Wrapper Scripts (exec/)
- ✅ Updated `docker-merge-pdfs.sh` → `/app/scripts/bash/merge_pdfs.sh`
- ✅ Updated `docker-pdf-to-images.sh` → `/app/scripts/bash/pdf_to_images.sh`
- ✅ Updated `docker-pdf-to-pptx.sh` → `/app/scripts/bash/pdf_to_pptx.sh`
- ✅ Updated `docker-run-python.sh` → `/app/scripts/python/$SCRIPT`
- ✅ Fixed pipefail issue in docker-run-python.sh

### 4. Test Suite
- ✅ Updated test script to check for `scripts/bash/` and `scripts/python/`
- ✅ Updated executable check for both script types
- ✅ Updated Python path tests
- ✅ All 20 tests passing

### 5. Documentation
- ✅ Updated [README.md](README.md) with new structure
- ✅ Added this summary document

### 6. Template Drift Test
- ✅ Created `test_merge_templates.py` script
- ✅ Merges templates from `assets/slides/templates/`
- ✅ Outputs to `assets/output/merged_test.pptx`
- ✅ Detects template drift automatically
- ✅ Working and tested

## Test Results

**Reorganization verified:**
```bash
✅ Docker image rebuilt successfully
✅ All 20 tests passing
✅ Scripts accessible in container at /app/scripts/bash/ and /app/scripts/python/
✅ Volume mounts working correctly
✅ Wrapper scripts functional
✅ Template merge test working
```

**Template Merge Test Output:**
```
✅ Merged file created: /app/assets/output/merged_test.pptx
✅ Total slides in merged: 2
⚠️  Some template drift detected (expected when merging different templates)
```

## Usage Examples

### Before
```bash
# Old mixed structure
./exec/docker-run-python.sh merge_pptx.py output.pptx input.pptx
# Used: /app/src/merge_pptx.py
```

### After
```bash
# New harmonized structure
./exec/docker-run-python.sh merge_pptx.py output.pptx input.pptx
# Uses: /app/scripts/python/merge_pptx.py

# Test template merging
./exec/docker-run-python.sh test_merge_templates.py
# Merges all templates and checks for drift
```

## File Paths in Container

| Host Path | Container Path |
|-----------|----------------|
| `scripts/bash/*.sh` | `/app/scripts/bash/*.sh` |
| `scripts/python/*.py` | `/app/scripts/python/*.py` |
| `scripts/python/requirements.txt` | `/app/requirements.txt` (copied during build) |
| `assets/` | `/app/assets/` |

## PATH Configuration

Scripts are automatically in PATH inside the container:
```bash
# Both locations in PATH
/app/scripts/bash:/app/scripts/python:...

# You can call directly:
merge_pdfs.sh output.pdf input1.pdf input2.pdf
merge_pptx.py output.pptx input1.pptx input2.pptx
```

## Migration Notes

### For Developers

If you had local workflows referencing `src/`:
1. Update paths from `src/` to `scripts/python/`
2. Rebuild Docker image: `make rebuild`
3. Run tests: `make test`

### For CI/CD

Update any scripts that reference:
- `src/requirements.txt` → `scripts/python/requirements.txt`
- `src/merge_pptx.py` → `scripts/python/merge_pptx.py`
- `scripts/merge_pdfs.sh` → `scripts/bash/merge_pdfs.sh`

## Verification Commands

```bash
# Check structure in container
docker-compose run --rm immerculate ls -la /app/scripts/

# List bash scripts
docker-compose run --rm immerculate ls -1 /app/scripts/bash/

# List Python scripts
docker-compose run --rm immerculate ls -1 /app/scripts/python/

# Run tests
./test.sh

# Test merge templates
./exec/docker-run-python.sh test_merge_templates.py
```

## Summary

The project structure is now harmonized with:
- ✅ All scripts under `scripts/` directory
- ✅ Clear separation: `bash/` and `python/` subdirectories
- ✅ Consistent treatment of all executable scripts
- ✅ Simplified Docker configuration
- ✅ Updated documentation
- ✅ All tests passing
- ✅ Template merge & drift detection working

**The reorganization is complete and production-ready!**

---

*Harmonization completed: January 10, 2026*  
*All tests passing • Documentation updated • Ready to use*
