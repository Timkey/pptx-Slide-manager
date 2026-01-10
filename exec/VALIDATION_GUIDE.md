# Output Validation & Organization Guide

## Overview

All merge scripts now:
1. ✅ Organize outputs in script-specific subdirectories
2. ✅ Validate outputs immediately after creation
3. ✅ Support comprehensive validation via `validate_output.py`

## Output Directory Structure

```
assets/output/
├── merge_pptx/          # PowerPoint merge outputs
│   ├── merged-pptx-001.pptx
│   ├── merged-pptx-002.pptx
│   └── ...
├── merge_pdfs/          # PDF merge outputs
│   ├── merged-pdf-001.pdf
│   ├── merged-pdf-002.pdf
│   └── ...
├── merge_template/      # Template-based merge outputs
│   ├── merged-template-001.pptx
│   ├── merged-template-002.pptx
│   └── ...
└── merge_images/        # Image-based merge outputs
    ├── merged-images-001.pptx
    └── ...
```

## Automatic Validation

All merge scripts now validate outputs immediately after creation:

```bash
# When you run a merge:
docker-compose run --rm immerculate merge_pptx.py

# Output includes validation:
# Saved merged presentation to: /app/assets/output/merge_pptx/merged-pptx-001.pptx
# ✓ Validation: 2 slides, 40796 bytes
```

## Comprehensive Validation Tool

Use `validate_output.py` for detailed validation of any file or directory:

### Inside Container (Recommended)

```bash
# Validate all outputs
docker-compose run --rm immerculate validate_output.py

# Validate specific directory
docker-compose run --rm immerculate validate_output.py assets/output/merge_pptx

# Validate single file
docker-compose run --rm immerculate validate_output.py assets/output/merge_pptx/merged-pptx-001.pptx

# Using wrapper script
./exec/docker-validate-output.sh
```

### Validation Checks

#### For PPTX Files:
- ✅ File exists and has non-zero size
- ✅ Valid ZIP structure (PPTX is a ZIP archive)
- ✅ Contains required OOXML files
- ✅ No corrupted ZIP entries
- ✅ Can be loaded by python-pptx
- ✅ All slides are accessible
- ✅ Reports: slide count, layouts, masters, dimensions

#### For PDF Files:
- ✅ File exists and has non-zero size
- ✅ Valid PDF header (%PDF-)
- ✅ EOF marker present
- ✅ Reports: file size, PDF version

## Validation Output

### Successful Validation

```
======================================================================
VALIDATION REPORT: 3/3 files valid
======================================================================

✓ merged-pptx-001.pptx
    size_bytes: 40796
    size_kb: 39.84
    zip_entries: 41
    slides: 2
    slide_layouts: 12
    slide_masters: 1
    width: 12192000
    height: 6858000

✓ merged-pdf-001.pdf
    size_bytes: 71958
    size_kb: 70.27
    pdf_version: %PDF-

✅ All files are valid!
```

### Failed Validation

```
✗ corrupted.pptx
    size_bytes: 1024
    size_kb: 1.0
    ❌ ERROR: Not a valid ZIP file: Bad ZIP file
    
⚠️  1 file(s) have issues
```

## Common Issues & Fixes

### Issue: "Not a valid ZIP file"
**Cause**: File is corrupted or incomplete
**Fix**: Re-run the merge operation

### Issue: "No EOF marker found"
**Cause**: PDF was truncated during creation
**Fix**: Check available disk space, re-run merge

### Issue: "Slide X is corrupted"
**Cause**: Problem copying shapes from source slides
**Fix**: Check source files, report issue if persistent

## Preventing Corruption

1. **Ensure sufficient disk space**:
   ```bash
   df -h assets/output
   ```

2. **Validate sources before merging**:
   ```bash
   docker-compose run --rm immerculate validate_output.py assets/slides/templates
   ```

3. **Check merge operation completed**:
   - Look for "✓ Validation:" in output
   - Verify file size is reasonable

4. **Regular validation**:
   ```bash
   # Add to your workflow
   ./exec/docker-validate-output.sh
   ```

## Integration with Workflow

### Example Merge & Validate Workflow

```bash
# Start Colima (if not running)
./exec/start-colima.sh

# Merge templates
docker-compose run --rm immerculate merge_pptx.py

# Validate all outputs
./exec/docker-validate-output.sh

# Or validate specific script output
docker-compose run --rm immerculate validate_output.py assets/output/merge_pptx
```

### Automated Testing

```bash
# Run all merges and validate
echo "Running merges..."
docker-compose run --rm immerculate merge_pptx.py
docker-compose run --rm immerculate merge_pdfs.sh
docker-compose run --rm immerculate merge_template.py -t assets/slides/templates/test1.pptx

echo "Validating all outputs..."
./exec/docker-validate-output.sh
```

## Benefits of Organized Output

1. **Easy to Find**: Script-specific subdirectories make outputs easy to locate
2. **No Conflicts**: Different script types don't overwrite each other
3. **Clean Structure**: Organized hierarchy for better management
4. **Batch Operations**: Easy to validate/clean outputs by script type

## Cleaning Up Outputs

```bash
# Clean all outputs
rm -rf assets/output/merge_*

# Clean specific script outputs
rm -rf assets/output/merge_pptx
rm -rf assets/output/merge_pdfs

# Clean old numbered files (keep latest 5)
cd assets/output/merge_pptx
ls -t merged-pptx-*.pptx | tail -n +6 | xargs rm -f
```

## Exit Codes

- `0` - All files valid
- `1` - One or more files have issues

Use in scripts:
```bash
if ./exec/docker-validate-output.sh; then
    echo "All outputs valid!"
else
    echo "Validation failed!"
    exit 1
fi
```
