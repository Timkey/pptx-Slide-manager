#!/usr/bin/env python3
"""
Generate detailed, readable analysis report from analysis JSON files.
Shows all outliers grouped by type and file with full context.

Usage:
  python generate_detailed_report.py <analysis_dir>
"""
import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict


def load_analysis_data(analysis_dir):
    """Load full analysis and outlier data."""
    full_path = Path(analysis_dir) / 'full_analysis.json'
    outlier_path = Path(analysis_dir) / 'outlier_analysis.json'
    
    if not full_path.exists() or not outlier_path.exists():
        print(f"Error: Analysis files not found in {analysis_dir}")
        sys.exit(1)
    
    with open(full_path, 'r') as f:
        full_data = json.load(f)
    
    with open(outlier_path, 'r') as f:
        outlier_data = json.load(f)
    
    return full_data, outlier_data


def format_run_detail(run, indent="  "):
    """Format a single text run with full details."""
    lines = []
    lines.append(f"{indent}File: {run['file']}")
    lines.append(f"{indent}Location: Slide {run['slide']}, Shape {run['shape']}, Paragraph {run['paragraph']}, Run {run['run']}")
    lines.append(f"{indent}Text: \"{run['text']}\" ({run['text_length']} chars)")
    lines.append(f"{indent}Font: {run.get('font_name', 'N/A')}")
    
    # Font size with source
    if run.get('font_size'):
        source = run.get('font_size_source', 'unknown')
        lines.append(f"{indent}Size: {run['font_size']}pt (source: {source})")
    else:
        lines.append(f"{indent}Size: None")
    
    # Color with resolution
    if run.get('color_type'):
        lines.append(f"{indent}Color Type: {run['color_type']}")
        lines.append(f"{indent}Color Value: {run.get('color_value', 'N/A')}")
        if run.get('color_resolved') != run.get('color_value'):
            lines.append(f"{indent}Color Resolved: {run['color_resolved']}")
    
    # Formatting
    formatting = []
    if run.get('bold'):
        formatting.append('bold')
    if run.get('italic'):
        formatting.append('italic')
    if run.get('underline'):
        formatting.append('underline')
    if formatting:
        lines.append(f"{indent}Formatting: {', '.join(formatting)}")
    
    return "\n".join(lines)


def group_outliers_by_file(outliers):
    """Group outliers by file name."""
    grouped = defaultdict(list)
    for outlier in outliers:
        grouped[outlier['file']].append(outlier)
    return grouped


def generate_detailed_report(analysis_dir, output_file=None):
    """Generate comprehensive analysis report."""
    full_data, outlier_data = load_analysis_data(analysis_dir)
    stats = outlier_data['statistics']
    outliers = outlier_data['outliers']
    
    lines = []
    lines.append("=" * 100)
    lines.append("COMPREHENSIVE PPTX FONT ATTRIBUTE ANALYSIS REPORT")
    lines.append("=" * 100)
    lines.append("")
    
    # Overall statistics
    lines.append(f"Total files analyzed: {full_data['files_analyzed']}")
    successful = [r for r in full_data['results'] if r.get('success', False)]
    failed = [r for r in full_data['results'] if not r.get('success', True)]
    lines.append(f"Successful: {len(successful)}")
    lines.append(f"Failed: {len(failed)}")
    lines.append(f"Total text runs: {stats['total_runs']}")
    lines.append("")
    
    # Failed files if any
    if failed:
        lines.append("=" * 100)
        lines.append("FAILED FILES")
        lines.append("=" * 100)
        for f in failed:
            lines.append(f"  {f['file']}: {f.get('error', 'Unknown error')}")
        lines.append("")
    
    # OUTLIERS SECTION - This comes first per user request
    lines.append("=" * 100)
    lines.append("OUTLIERS ANALYSIS")
    lines.append("=" * 100)
    lines.append("")
    lines.append(f"Total outliers detected:")
    lines.append(f"  Font size outliers: {len(outliers['size'])}")
    lines.append(f"  Font name outliers: {len(outliers['name'])}")
    lines.append(f"  Color outliers: {len(outliers['color'])}")
    lines.append("")
    
    # Font Size Outliers
    if outliers['size']:
        lines.append("-" * 100)
        lines.append(f"FONT SIZE OUTLIERS ({len(outliers['size'])} total)")
        lines.append("-" * 100)
        lines.append("")
        
        # Group by file
        grouped = group_outliers_by_file(outliers['size'])
        for file_name in sorted(grouped.keys()):
            file_outliers = grouped[file_name]
            lines.append(f"File: {file_name} ({len(file_outliers)} outliers)")
            lines.append("-" * 80)
            
            # Group by size value
            by_size = defaultdict(list)
            for o in file_outliers:
                by_size[o.get('font_size')].append(o)
            
            for size in sorted(by_size.keys(), key=lambda x: (x is None, x), reverse=True):
                size_runs = by_size[size]
                lines.append(f"\n  Size: {size}pt ({len(size_runs)} occurrences)")
                for run in size_runs[:10]:  # Show first 10 per size
                    lines.append(f"    Slide {run['slide']}: \"{run['text'][:60]}\"")
                if len(size_runs) > 10:
                    lines.append(f"    ... and {len(size_runs) - 10} more")
            lines.append("")
    
    # Font Name Outliers
    if outliers['name']:
        lines.append("-" * 100)
        lines.append(f"FONT NAME OUTLIERS ({len(outliers['name'])} total)")
        lines.append("-" * 100)
        lines.append("")
        
        grouped = group_outliers_by_file(outliers['name'])
        for file_name in sorted(grouped.keys()):
            file_outliers = grouped[file_name]
            lines.append(f"File: {file_name} ({len(file_outliers)} outliers)")
            lines.append("-" * 80)
            
            # Group by font name
            by_font = defaultdict(list)
            for o in file_outliers:
                by_font[o.get('font_name')].append(o)
            
            for font in sorted(by_font.keys()):
                font_runs = by_font[font]
                lines.append(f"\n  Font: {font} ({len(font_runs)} occurrences)")
                for run in font_runs[:10]:
                    lines.append(f"    Slide {run['slide']}: \"{run['text'][:60]}\"")
                if len(font_runs) > 10:
                    lines.append(f"    ... and {len(font_runs) - 10} more")
            lines.append("")
    
    # Color Outliers
    if outliers['color']:
        lines.append("-" * 100)
        lines.append(f"COLOR OUTLIERS ({len(outliers['color'])} total)")
        lines.append("-" * 100)
        lines.append("")
        
        grouped = group_outliers_by_file(outliers['color'])
        for file_name in sorted(grouped.keys()):
            file_outliers = grouped[file_name]
            lines.append(f"File: {file_name} ({len(file_outliers)} outliers)")
            lines.append("-" * 80)
            
            # Group by resolved color
            by_color = defaultdict(list)
            for o in file_outliers:
                color_key = o.get('color_resolved') or o.get('color_value') or 'None'
                by_color[color_key].append(o)
            
            for color in sorted(by_color.keys()):
                color_runs = by_color[color]
                lines.append(f"\n  Color: {color} ({len(color_runs)} occurrences)")
                for run in color_runs[:10]:
                    lines.append(f"    Slide {run['slide']}: \"{run['text'][:60]}\"")
                if len(color_runs) > 10:
                    lines.append(f"    ... and {len(color_runs) - 10} more")
            lines.append("")
    
    # DISTRIBUTIONS SECTION
    lines.append("=" * 100)
    lines.append("ATTRIBUTE DISTRIBUTIONS")
    lines.append("=" * 100)
    lines.append("")
    
    # Font Size Distribution
    lines.append("-" * 100)
    lines.append("FONT SIZE DISTRIBUTION")
    lines.append("-" * 100)
    lines.append("")
    lines.append(f"Common sizes (>10% threshold):")
    for size in stats['common_sizes']:
        count = stats['font_sizes'].get(str(size), 0)
        pct = (count / stats['total_runs']) * 100
        lines.append(f"  {size}pt: {count} ({pct:.1f}%)")
    lines.append("")
    lines.append("All sizes:")
    for size, count in sorted(stats['font_sizes'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / stats['total_runs']) * 100
        lines.append(f"  {size}pt: {count} ({pct:.1f}%)")
    lines.append("")
    
    # Font Family Distribution
    lines.append("-" * 100)
    lines.append("FONT FAMILY DISTRIBUTION")
    lines.append("-" * 100)
    lines.append("")
    lines.append(f"Common fonts (>10% threshold):")
    for name in stats['common_names']:
        count = stats['font_names'].get(name, 0)
        pct = (count / stats['total_runs']) * 100
        lines.append(f"  {name}: {count} ({pct:.1f}%)")
    lines.append("")
    lines.append("All fonts:")
    for name, count in sorted(stats['font_names'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / stats['total_runs']) * 100
        lines.append(f"  {name}: {count} ({pct:.1f}%)")
    lines.append("")
    
    # Color Distribution
    lines.append("-" * 100)
    lines.append("COLOR DISTRIBUTION")
    lines.append("-" * 100)
    lines.append("")
    lines.append(f"Common colors (>10% threshold):")
    for color in stats['common_colors']:
        count = stats['colors'].get(color, 0)
        pct = (count / stats['total_runs']) * 100
        lines.append(f"  {color}: {count} ({pct:.1f}%)")
    lines.append("")
    lines.append("All colors:")
    for color, count in sorted(stats['colors'].items(), key=lambda x: x[1], reverse=True)[:50]:
        pct = (count / stats['total_runs']) * 100
        lines.append(f"  {color}: {count} ({pct:.1f}%)")
    lines.append("")
    
    # File-by-file summary
    lines.append("=" * 100)
    lines.append("FILE-BY-FILE SUMMARY")
    lines.append("=" * 100)
    lines.append("")
    
    for result in sorted(full_data['results'], key=lambda x: x.get('file', '')):
        if not result.get('success'):
            continue
        
        runs = result.get('runs', [])
        lines.append(f"File: {result['file']}")
        lines.append(f"  Slides: {result.get('slides', 0)}")
        lines.append(f"  Text runs: {len(runs)}")
        
        if runs:
            # Count unique attributes
            sizes = set(r.get('font_size') for r in runs if r.get('font_size'))
            fonts = set(r.get('font_name') for r in runs if r.get('font_name'))
            colors = set(r.get('color_resolved') or r.get('color_value') for r in runs if r.get('color_resolved') or r.get('color_value'))
            
            lines.append(f"  Unique font sizes: {len(sizes)}")
            lines.append(f"  Unique font families: {len(fonts)}")
            lines.append(f"  Unique colors: {len(colors)}")
        lines.append("")
    
    # Output
    report_text = "\n".join(lines)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report_text)
        print(f"Detailed report saved to: {output_file}")
    else:
        print(report_text)


def main():
    parser = argparse.ArgumentParser(description='Generate detailed analysis report from JSON files')
    parser.add_argument('analysis_dir', help='Directory containing analysis JSON files')
    parser.add_argument('-o', '--output', help='Output file (default: detailed_report.txt in analysis_dir)')
    
    args = parser.parse_args()
    
    output_file = args.output
    if not output_file:
        output_file = Path(args.analysis_dir) / 'detailed_report.txt'
    
    generate_detailed_report(args.analysis_dir, output_file)


if __name__ == '__main__':
    main()
