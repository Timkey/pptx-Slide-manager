# Python Scripts Organization

## 📁 Structure

```
scripts/python/
├── Production (5 scripts)
├── validation/ (10 scripts)
└── experimental/ (7 scripts)
```

## ⭐ Production Scripts

**Main merge utility:**
- `merge_pptx.py` - Complete PPTX merge with JSON config support
- `theme_resolver.py` - Theme color/font resolution (required by merge_pptx.py)

**Validation:**
- `validate_merge.py` - Test consistency between source and output

**Utilities:**
- `inspect_pptx.py` - Inspect PPTX structure and content
- `pdf_images_to_pptx.py` - Convert PDF to PPTX

## 🧪 Validation Scripts (`validation/`)

For testing consistency across templates:
- `validate_output.py` - Detailed validation with extensive checks
- `comprehensive_check.py` - Comprehensive comparison tools
- `deep_compare.py` - Deep comparison between presentations
- `formatting_utils.py` - Formatting validation utilities
- Plus other specialized validation tools

## 🔬 Experimental Scripts (`experimental/`)

Alternative implementations kept for reference:
- `merge*.py` - Early/alternative merge implementations
- `test_*.py` - Various test scripts

---

## Usage

### Merge presentations:
```bash
docker-compose run --rm immerculate python3 scripts/python/merge_pptx.py --config merge-config.json
```

### Validate output:
```bash
docker-compose run --rm immerculate python3 scripts/python/validate_merge.py \
  assets/output/merge_pptx/merged-pptx-001.pptx \
  --config merge-config.json
```

### Example validation output:
```
✅ Slide Count: 2/2 slides
✅ Shapes: All correct
✅ Text Content: All preserved
✅ Images: 1 image copied correctly
✅ Formatting: 22/22 explicit sizes, 0 SCHEME colors

✅ ALL VALIDATIONS PASSED
```

See [assets/config/README.md](../../assets/config/README.md) for config file documentation.
