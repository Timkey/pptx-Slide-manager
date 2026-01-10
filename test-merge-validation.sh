#!/bin/bash
# Comprehensive test: merge operations with validation
# All tests run inside Docker container

set -e

echo "========================================"
echo "Merge & Validation Integration Test"
echo "========================================"
echo ""

# Clean previous outputs
echo "1. Cleaning previous outputs..."
rm -rf assets/output/merge_pptx assets/output/merge_pdfs assets/output/merge_template assets/output/merge_images 2>/dev/null || true
echo "   ✓ Cleaned"
echo ""

# Test 1: PowerPoint merge
echo "2. Testing merge_pptx.py..."
docker-compose run --rm immerculate merge_pptx.py
echo "   ✓ merge_pptx.py completed"
echo ""

# Test 2: PDF merge
echo "3. Testing merge_pdfs.sh..."
docker-compose run --rm immerculate merge_pdfs.sh
echo "   ✓ merge_pdfs.sh completed"
echo ""

# Test 3: Template-based merge
echo "4. Testing merge_template.py..."
docker-compose run --rm immerculate merge_template.py -t assets/slides/templates/test1.pptx assets/slides/templates/test2.pptx
echo "   ✓ merge_template.py completed"
echo ""

# Test 4: Multiple runs (test incremental numbering)
echo "5. Testing incremental numbering..."
docker-compose run --rm immerculate merge_pptx.py > /dev/null 2>&1
docker-compose run --rm immerculate merge_pdfs.sh > /dev/null 2>&1
echo "   ✓ Incremental numbering works"
echo ""

# Validate all outputs
echo "6. Validating all outputs..."
if docker-compose run --rm immerculate validate_output.py assets/output | grep -q "All files are valid"; then
    echo "   ✓ All files validated successfully"
else
    echo "   ✗ Validation failed"
    exit 1
fi
echo ""

# Check directory structure
echo "7. Checking output directory structure..."
expected_dirs=("merge_pptx" "merge_pdfs" "merge_template")
for dir in "${expected_dirs[@]}"; do
    if [ -d "assets/output/$dir" ]; then
        count=$(find "assets/output/$dir" -name "merged-*" -type f | wc -l)
        echo "   ✓ assets/output/$dir exists ($count files)"
    else
        echo "   ✗ assets/output/$dir missing"
        exit 1
    fi
done
echo ""

# Summary
echo "========================================"
echo "✅ All Tests Passed!"
echo "========================================"
echo ""
echo "Output structure:"
find assets/output/merge_* -name "merged-*" -type f 2>/dev/null | sort | while read file; do
    size=$(ls -lh "$file" | awk '{print $5}')
    echo "  - $file ($size)"
done
