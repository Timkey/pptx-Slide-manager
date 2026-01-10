# Merge PPTX Configuration

The merge script now supports JSON configuration files to specify the order and selection of slides to merge.

## Usage

### Command Line:
```bash
# Use config file
python scripts/python/merge_pptx.py --config merge-config.json

# Or with short flag
python scripts/python/merge_pptx.py -c assets/config/merge-config.json
```

### Docker:
```bash
docker-compose run --rm immerculate python3 scripts/python/merge_pptx.py --config merge-config.json
```

## Configuration Format

### Simple Format (all slides from each file):
```json
{
  "output": "merged-output.pptx",
  "parts": [
    "slides/templates/file1.pptx",
    "slides/templates/file2.pptx",
    "slides/templates/file3.pptx"
  ]
}
```

### Advanced Format (select specific slides):
```json
{
  "output": "custom-merge.pptx",
  "parts": [
    {
      "file": "slides/templates/file1.pptx",
      "slides": "all"
    },
    {
      "file": "slides/templates/file2.pptx",
      "slides": [0, 2, 5]
    },
    {
      "file": "slides/templates/file3.pptx",
      "slides": [1]
    }
  ]
}
```

## Path Resolution

Paths in the config are resolved relative to the `assets/` directory. So:
- `"slides/templates/file.pptx"` → `/path/to/assets/slides/templates/file.pptx`
- Absolute paths also work

## Examples

See:
- `assets/config/merge-config.json` - Default configuration
- `assets/config/merge-example-simple.json` - Simple format example  
- `assets/config/merge-example-advanced.json` - Advanced with slide selection

## Features

- ✅ Specify exact order of files
- ✅ Select specific slides by index (0-based)
- ✅ Mix and match files (can use same file multiple times)
- ✅ Theme/color/font preservation
- ✅ Background preservation
- ✅ Image data copying
