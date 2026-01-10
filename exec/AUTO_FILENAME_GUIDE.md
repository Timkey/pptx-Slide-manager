# Auto-Generated Filename Guide

All merge scripts now support auto-generated output filenames with incremental numbering. This makes it easy to run merges without having to specify unique output names each time.

## Features

- **Incremental Numbering**: Files are named with 3-digit counters (001-999)
- **Random Fallback**: After 999 files, switches to random 4-digit numbers
- **Unified Output**: All merged files go to `assets/output/`
- **Template Support**: Can merge templates from `assets/slides/templates/` or `assets/pdfs/templates/`

## Filename Patterns

Each script generates its own unique prefix:

| Script | Pattern | Example |
|--------|---------|---------|
| `merge_pptx.py` | `merged-pptx-{NNN}.pptx` | `merged-pptx-001.pptx` |
| `merge_pdfs.sh` | `merged-pdf-{NNN}.pdf` | `merged-pdf-001.pdf` |
| `merge_template.py` | `merged-template-{NNN}.pptx` | `merged-template-001.pptx` |
| `merge_images.py` | `merged-images-{NNN}.pptx` | `merged-images-001.pptx` |

## Usage Examples

### PowerPoint Merge (merge_pptx.py)

```bash
# Auto-generate filename, merge templates from assets/slides/templates/
docker-compose run --rm immerculate merge_pptx.py

# Auto-generate filename, merge specific files
docker-compose run --rm immerculate merge_pptx.py file1.pptx file2.pptx

# Specify output name
docker-compose run --rm immerculate merge_pptx.py my-output.pptx file1.pptx file2.pptx
```

### PDF Merge (merge_pdfs.sh)

```bash
# Auto-generate filename, merge templates from assets/pdfs/templates/
docker-compose run --rm immerculate merge_pdfs.sh

# Auto-generate filename, merge specific files
docker-compose run --rm immerculate merge_pdfs.sh file1.pdf file2.pdf

# Specify output name
docker-compose run --rm immerculate merge_pdfs.sh my-output.pdf file1.pdf file2.pdf
```

### Template-Based Merge (merge_template.py)

```bash
# Auto-generate filename
docker-compose run --rm immerculate merge_template.py -t template.pptx input1.pptx input2.pptx

# Specify output name
docker-compose run --rm immerculate merge_template.py -o my-output.pptx -t template.pptx input1.pptx
```

### Image-Based Merge (merge_images.py)

```bash
# Auto-generate filename
docker-compose run --rm immerculate merge_images.py input1.pptx input2.pptx

# Specify output name
docker-compose run --rm immerculate merge_images.py -o my-output.pptx input1.pptx input2.pptx
```

## Output Location

All outputs are saved to: `assets/output/`

This includes:
- ✅ Auto-generated merged files
- ✅ Explicitly named outputs
- ✅ Both PDF and PPTX formats

## Template Directories

Scripts automatically search for templates in:
- `assets/slides/templates/` - PowerPoint templates (.pptx)
- `assets/pdfs/templates/` - PDF templates (.pdf)

Note: PowerPoint temp files (starting with `~$`) are automatically filtered out.

## Incremental Counter Logic

1. Script checks `assets/output/` for existing files matching the pattern
2. Finds the next available number (001, 002, 003, ...)
3. If counter exceeds 999, switches to random 4-digit number
4. Returns the full path to the new file

## Benefits

- **No Name Conflicts**: Automatic numbering prevents overwriting
- **Organized Output**: All merged files in one location
- **Quick Iteration**: Run merges repeatedly without thinking about names
- **Consistent Naming**: Easy to identify merge outputs
- **Template Workflow**: Seamlessly work with template directories

## Checking Your Outputs

```bash
# List all auto-generated merged files
ls -lh assets/output/ | grep merged-

# Count merged files by type
ls assets/output/merged-pptx-*.pptx | wc -l
ls assets/output/merged-pdf-*.pdf | wc -l
```
