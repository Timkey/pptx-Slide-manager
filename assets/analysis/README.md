# PPTX Analysis Visualization

Interactive HTML visualizations of font attribute analysis for PPTX files from Dropbox folders.

## Files

### Masses Analysis
- **Source**: `/Users/nomad/Dropbox/1._Masses/` (28 files since Dec 1, 2025)
- **Visualization**: [visualization.html](masses/visualization.html) (26MB)
- **Detailed Report**: [detailed_report.txt](masses/detailed_report.txt) (6,478 lines)
- **JSON Data**: 
  - [full_analysis.json](masses/full_analysis.json) - Complete analysis of 26,879 text runs
  - [outlier_analysis.json](masses/outlier_analysis.json) - Outlier detection results
  - [summary.txt](masses/summary.txt) - Quick summary

### Music Analysis
- **Source**: `/Users/nomad/Dropbox/4. Music/` (12 files since Dec 1, 2025)
- **Visualization**: [visualization.html](music/visualization.html) (944KB)
- **Detailed Report**: [detailed_report.txt](music/detailed_report.txt) (547 lines)
- **JSON Data**:
  - [full_analysis.json](music/full_analysis.json) - Complete analysis of 945 text runs
  - [outlier_analysis.json](music/outlier_analysis.json) - Outlier detection results
  - [summary.txt](music/summary.txt) - Quick summary

## Using the Interactive Visualizations

### Opening the Visualization
Simply double-click the `visualization.html` file or open it with your browser:
```bash
open assets/analysis/masses/visualization.html
open assets/analysis/music/visualization.html
```

### Features

#### 1. **Overview Tab**
- Font size distribution chart (bar chart)
- Font family distribution chart (pie chart)
- Quick statistics cards at the top

#### 2. **Charts Tab**
- Color distribution chart (bar chart with actual colors)
- Outliers by type (doughnut chart)
- Files by complexity (horizontal bar chart)

#### 3. **Outliers Tab**
- Font size outliers grouped by file
- Font name outliers grouped by file
- Color outliers grouped by file
- Shows first 5 files with samples

#### 4. **Search Tab**
Interactive search with filters:
- **Font Size**: Dropdown of all sizes found
- **Font Family**: Dropdown of all fonts found
- **Color**: Dropdown of all colors (RGB and SCHEME)
- **File Name**: Text search for file names
- **Text Content**: Search within text runs

Results show:
- File name and location (slide, shape, paragraph, run)
- Font attributes (size, family, color)
- Text formatting (bold, italic)
- Full text content

#### 5. **Files Tab**
Summary of all analyzed files:
- Number of slides
- Number of text runs
- Unique font sizes, families, and colors

### Technical Details

**No Server Required**: The HTML file contains all data embedded as JavaScript. It works completely offline with no network requests.

**No CORS Issues**: All data is embedded directly in the HTML file, avoiding any cross-origin resource loading issues.

**Chart.js**: Uses Chart.js from CDN for visualizations (requires internet connection for initial load of Chart.js library).

**Performance**: 
- Masses visualization: 26MB (includes 26,879 text runs)
- Music visualization: 944KB (includes 945 text runs)
- Search limited to first 100 results for performance

### Analysis Details

**Theme Resolution**:
- ✅ SCHEME colors resolved to RGB (74.2% success rate)
- ✅ Master font sizes extracted when not explicit
- ✅ Theme fonts tracked (surface values)

**Unresolved SCHEME Colors**:
- TEXT_1 (13): 177 occurrences in Masses, 5 in Music
- TEXT_2 (15): 133 occurrences in Masses, 3 in Music
- BACKGROUND_1 (14): 6 occurrences in Masses, 0 in Music

**Outlier Detection**:
- Outliers are attributes used by less than 10% of text runs
- Common values (>10%) are not flagged as outliers
- Helps identify inconsistencies across presentations

## Regenerating Visualizations

If you re-run the analysis and want to update visualizations:

```bash
# Regenerate analysis
python3 scripts/python/analyze_pptx_fonts.py "/Users/nomad/Dropbox/1._Masses" \
    --since 2025-12-01 --output assets/analysis/masses

# Regenerate visualization
python3 scripts/python/generate_analysis_viz.py assets/analysis/masses \
    -t "Masses Analysis - December 2025+"

# Regenerate detailed report
python3 scripts/python/generate_detailed_report.py assets/analysis/masses
```

## Scripts Used

1. **analyze_pptx_fonts.py**: Analyzes PPTX files for font attributes with theme resolution
2. **generate_detailed_report.py**: Generates readable text report from JSON
3. **generate_analysis_viz.py**: Creates interactive HTML visualization

All scripts are in `scripts/python/` directory.
