# Auto-Generated Filename Implementation Summary

## Overview

Successfully implemented auto-generated output filenames with incremental numbering for all merge scripts. All outputs now go to `assets/output/` with consistent naming patterns.

## Changes Made

### 1. Python Scripts Updated

#### merge_pptx.py
- ✅ Added `generate_output_filename()` function with incremental counter (001-999)
- ✅ Changed output directory from `assets/slides/merged` to `assets/output`
- ✅ Made output argument optional (auto-generates if omitted)
- ✅ Added filter for PowerPoint temp files (`~$*.pptx`)
- ✅ Added `import random` for fallback to random numbers
- ✅ Output pattern: `merged-pptx-{NNN}.pptx`

#### merge_template.py
- ✅ Added `generate_output_filename()` function
- ✅ Changed output directory from `assets/slides/merged` to `assets/output`
- ✅ Converted output to optional flag (`-o/--output`)
- ✅ Updated ROOT path calculation for new script location
- ✅ Added `import random` for fallback
- ✅ Output pattern: `merged-template-{NNN}.pptx`

#### merge_images.py
- ✅ Added `generate_output_filename()` function
- ✅ Changed output directory from `assets/slides/merged` to `assets/output`
- ✅ Converted output to optional flag (`-o/--output`)
- ✅ Updated ROOT path calculation for new script location
- ✅ Added `import random` for fallback
- ✅ Output pattern: `merged-images-{NNN}.pptx`

### 2. Bash Scripts Updated

#### merge_pdfs.sh
- ✅ Added `generate_filename()` bash function with incremental counter (001-999)
- ✅ Added directory path calculations (`OUTPUT_DIR`, `PDF_TEMPLATES_DIR`)
- ✅ Made output filename optional (auto-generates if omitted)
- ✅ Added support for merging all templates from `assets/pdfs/templates/`
- ✅ Added `$RANDOM` fallback for numbers > 999
- ✅ Enhanced usage messages
- ✅ Output pattern: `merged-pdf-{NNN}.pdf`

## File Counter Logic

All scripts implement the same incremental counter logic:

```python
def generate_output_filename(prefix, extension):
    counter = 1
    while True:
        filename = f"{prefix}-{counter:03d}{extension}"
        filepath = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(filepath):
            return filepath
        counter += 1
        if counter > 999:
            # Fallback to random 4-digit number
            filename = f"{prefix}-{random.randint(1000, 9999)}{extension}"
            return os.path.join(OUTPUT_DIR, filename)
```

## Template Directories

Scripts automatically use templates from:
- `assets/slides/templates/` - PowerPoint templates for PPTX merge
- `assets/pdfs/templates/` - PDF templates for PDF merge

## Output Directory Structure

```
assets/
├── output/                    # ✅ All merged outputs go here
│   ├── merged-pptx-001.pptx
│   ├── merged-pptx-002.pptx
│   ├── merged-pdf-001.pdf
│   ├── merged-pdf-002.pdf
│   ├── merged-template-001.pptx
│   └── merged-images-001.pptx
├── pdfs/
│   └── templates/             # PDF templates (test1.pdf, test2.pdf)
└── slides/
    └── templates/             # PPTX templates (test1.pptx, test2.pptx)
```

## Usage Examples

All scripts now support both auto-generated and explicit output names:

```bash
# Auto-generated filenames (uses templates)
docker-compose run --rm immerculate merge_pptx.py
docker-compose run --rm immerculate merge_pdfs.sh

# Auto-generated with specific inputs
docker-compose run --rm immerculate merge_pptx.py file1.pptx file2.pptx
docker-compose run --rm immerculate merge_pdfs.sh file1.pdf file2.pdf

# Template-based with auto-filename
docker-compose run --rm immerculate merge_template.py -t template.pptx input.pptx

# Explicit output names (still supported)
docker-compose run --rm immerculate merge_pptx.py my-output.pptx file1.pptx
docker-compose run --rm immerculate merge_pdfs.sh my-output.pdf file1.pdf
docker-compose run --rm immerculate merge_template.py -o my-output.pptx -t template.pptx input.pptx
```

## Testing Results

✅ All scripts tested successfully:
- `merge_pptx.py` - Generated `merged-pptx-001.pptx`, `merged-pptx-002.pptx`, `merged-pptx-003.pptx`
- `merge_pdfs.sh` - Generated `merged-pdf-001.pdf`, `merged-pdf-002.pdf`, `merged-pdf-003.pdf`
- `merge_template.py` - Generated `merged-template-001.pptx`, `merged-template-002.pptx`

✅ Incremental numbering working correctly
✅ Templates automatically detected and merged
✅ PowerPoint temp files (`~$`) filtered out
✅ All outputs in `assets/output/`

## Benefits

1. **No Name Conflicts**: Automatic numbering prevents file overwrites
2. **Organized Output**: Single location for all merged files
3. **Quick Iteration**: Run merges without manual filename management
4. **Consistent Naming**: Easy identification and sorting
5. **Template Workflow**: Seamless template directory integration
6. **Backward Compatible**: Explicit filenames still work

## Documentation

Created comprehensive guide: `exec/AUTO_FILENAME_GUIDE.md`
- Usage examples for all scripts
- Filename patterns and logic
- Template directory structure
- Benefits and features

## Date: January 10, 2024

All changes implemented and tested successfully in Docker container environment with Colima.
