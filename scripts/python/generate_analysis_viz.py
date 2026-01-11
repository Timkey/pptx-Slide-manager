#!/usr/bin/env python3
"""
Generate interactive HTML visualization from analysis JSON files.
Creates a self-contained HTML file with embedded data and Chart.js visualizations.

Usage:
  python generate_analysis_viz.py <analysis_dir> [--output output.html]
"""
import argparse
import json
import sys
from pathlib import Path
from collections import Counter


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


def generate_html_visualization(analysis_dir, output_file, title="PPTX Analysis"):
    """Generate interactive HTML visualization."""
    full_data, outlier_data = load_analysis_data(analysis_dir)
    
    # Prepare data for search
    all_runs = []
    for result in full_data['results']:
        if result.get('success'):
            all_runs.extend(result.get('runs', []))
    
    # Get unique values for dropdowns
    unique_sizes = sorted(set(r.get('font_size') for r in all_runs if r.get('font_size')), reverse=True)
    unique_fonts = sorted(set(r.get('font_name') for r in all_runs if r.get('font_name')))
    unique_colors = sorted(set(r.get('color_resolved') or r.get('color_value') for r in all_runs 
                               if r.get('color_resolved') or r.get('color_value')))
    
    # Embed data as JSON
    embedded_data = {
        'full_data': full_data,
        'outlier_data': outlier_data,
        'unique_sizes': unique_sizes,
        'unique_fonts': unique_fonts,
        'unique_colors': unique_colors[:100]  # Limit colors to top 100
    }
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
            position: relative;
        }}
        
        .nav-bar {{
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            display: flex;
            gap: 10px;
            justify-content: space-between;
        }}
        
        .nav-link {{
            color: white;
            text-decoration: none;
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            transition: background 0.3s;
            font-size: 0.9em;
        }}
        
        .nav-link:hover {{
            background: rgba(255,255,255,0.3);
        }}
        
        .nav-group {{
            display: flex;
            gap: 10px;
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #dee2e6;
            padding: 0 30px;
        }}
        
        .tab {{
            padding: 15px 30px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 1em;
            color: #666;
            font-weight: 500;
            transition: all 0.3s;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
        }}
        
        .tab:hover {{
            color: #667eea;
            background: rgba(102, 126, 234, 0.1);
        }}
        
        .tab.active {{
            color: #667eea;
            border-bottom-color: #667eea;
            background: white;
        }}
        
        .tab-content {{
            display: none;
            padding: 30px;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .search-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        
        .search-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .form-group {{
            display: flex;
            flex-direction: column;
        }}
        
        label {{
            font-weight: 600;
            margin-bottom: 5px;
            color: #555;
            font-size: 0.9em;
        }}
        
        select, input {{
            padding: 10px;
            border: 2px solid #dee2e6;
            border-radius: 6px;
            font-size: 1em;
            transition: border-color 0.3s;
        }}
        
        select:focus, input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        button {{
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        button:active {{
            transform: translateY(0);
        }}
        
        .results {{
            margin-top: 20px;
        }}
        
        .result-card {{
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: box-shadow 0.3s;
        }}
        
        .result-card:hover {{
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .result-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f8f9fa;
        }}
        
        .result-file {{
            font-weight: 700;
            color: #667eea;
            font-size: 1.1em;
        }}
        
        .result-location {{
            color: #999;
            font-size: 0.9em;
        }}
        
        .result-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .detail-item {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 6px;
        }}
        
        .detail-label {{
            font-size: 0.8em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        
        .detail-value {{
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }}
        
        .result-text {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
            font-family: 'Courier New', monospace;
            color: #333;
            line-height: 1.6;
        }}
        
        .chart-container {{
            position: relative;
            margin-bottom: 40px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            font-size: 1.3em;
            font-weight: 700;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .outlier-section {{
            margin-bottom: 30px;
        }}
        
        .outlier-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px 8px 0 0;
            font-size: 1.2em;
            font-weight: 700;
        }}
        
        .outlier-count {{
            float: right;
            background: rgba(255,255,255,0.3);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .file-group {{
            border: 1px solid #dee2e6;
            border-top: none;
            padding: 20px;
            background: #fafafa;
        }}
        
        .file-name {{
            font-weight: 700;
            color: #667eea;
            font-size: 1.1em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #dee2e6;
        }}
        
        .outlier-item {{
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 1.1em;
        }}
        
        .loading {{
            text-align: center;
            padding: 20px;
            color: #667eea;
        }}
        
        .color-swatch {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid #333;
            vertical-align: middle;
            margin-right: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        .color-value {{
            display: inline-flex;
            align-items: center;
            font-family: 'Courier New', monospace;
        }}
        
        .detail-value .color-value {{
            font-weight: 600;
        }}
        
        @media (max-width: 768px) {{
            .stats {{
                grid-template-columns: 1fr;
            }}
            
            .tabs {{
                overflow-x: auto;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="nav-bar">
                <a href="../../../index.html" class="nav-link">← Home</a>
                <div class="nav-group">
                    <a href="../masses/visualization.html" class="nav-link">📖 Masses</a>
                    <a href="../music/visualization.html" class="nav-link">🎵 Music</a>
                </div>
            </div>
            <h1>{title}</h1>
            <p>Interactive Font Attribute Analysis & Visualization</p>
        </header>
        
        <div class="stats" id="statsContainer"></div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('overview')">Overview</button>
            <button class="tab" onclick="switchTab('charts')">Charts</button>
            <button class="tab" onclick="switchTab('outliers')">Outliers</button>
            <button class="tab" onclick="switchTab('search')">Search</button>
            <button class="tab" onclick="switchTab('files')">Files</button>
        </div>
        
        <div id="overview" class="tab-content active">
            <div class="chart-container">
                <h3 class="chart-title">Font Size Distribution</h3>
                <canvas id="sizeChart"></canvas>
            </div>
            <div class="chart-container">
                <h3 class="chart-title">Font Family Distribution</h3>
                <canvas id="fontChart"></canvas>
            </div>
        </div>
        
        <div id="charts" class="tab-content">
            <div class="chart-container">
                <h3 class="chart-title">Color Distribution</h3>
                <canvas id="colorChart"></canvas>
            </div>
            <div class="chart-container">
                <h3 class="chart-title">Outliers by Type</h3>
                <canvas id="outlierChart"></canvas>
            </div>
            <div class="chart-container">
                <h3 class="chart-title">Files by Complexity</h3>
                <canvas id="fileChart"></canvas>
            </div>
        </div>
        
        <div id="outliers" class="tab-content">
            <div id="outliersSummary"></div>
        </div>
        
        <div id="search" class="tab-content">
            <div class="search-section">
                <div class="search-row">
                    <div class="form-group">
                        <label>Font Size</label>
                        <select id="searchSize">
                            <option value="">All sizes</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Font Family</label>
                        <select id="searchFont">
                            <option value="">All fonts</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Color</label>
                        <select id="searchColor">
                            <option value="">All colors</option>
                        </select>
                    </div>
                </div>
                <div class="search-row">
                    <div class="form-group">
                        <label>File Name</label>
                        <input type="text" id="searchFile" placeholder="Enter file name...">
                    </div>
                    <div class="form-group">
                        <label>Text Content</label>
                        <input type="text" id="searchText" placeholder="Search in text...">
                    </div>
                    <div class="form-group" style="justify-content: flex-end;">
                        <label>&nbsp;</label>
                        <button onclick="performSearch()">Search</button>
                    </div>
                </div>
            </div>
            <div id="searchResults" class="results"></div>
        </div>
        
        <div id="files" class="tab-content">
            <div id="filesSummary"></div>
        </div>
    </div>
    
    <script>
        // Embedded data
        const analysisData = {json.dumps(embedded_data, indent=2)};
        
        // Global variables
        let currentTab = 'overview';
        let charts = {{}};
        
        // Helper function to render color with swatch
        function renderColorWithSwatch(colorValue) {{
            if (!colorValue || colorValue === 'N/A') return 'N/A';
            
            let bgColor = '#ddd';
            let displayValue = colorValue;
            
            // Check if it's a valid hex color (6 characters, no scheme)
            if (colorValue.match(/^[0-9A-F]{{6}}$/i)) {{
                bgColor = `#${{colorValue}}`;
            }} else if (colorValue.startsWith('#') && colorValue.length === 7) {{
                bgColor = colorValue;
            }}
            
            return `<span class="color-value"><span class="color-swatch" style="background-color: ${{bgColor}};"></span>${{displayValue}}</span>`;
        }}
        
        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {{
            initializeStats();
            initializeSearchDropdowns();
            initializeCharts();
            initializeOutliers();
            initializeFiles();
        }});
        
        function initializeStats() {{
            const stats = analysisData.outlier_data.statistics;
            const outliers = analysisData.outlier_data.outliers;
            
            const statsHTML = `
                <div class="stat-card">
                    <div class="stat-value">${{analysisData.full_data.files_analyzed}}</div>
                    <div class="stat-label">Files Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{stats.total_runs.toLocaleString()}}</div>
                    <div class="stat-label">Text Runs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{outliers.size.length.toLocaleString()}}</div>
                    <div class="stat-label">Size Outliers</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{outliers.name.length.toLocaleString()}}</div>
                    <div class="stat-label">Font Outliers</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${{outliers.color.length.toLocaleString()}}</div>
                    <div class="stat-label">Color Outliers</div>
                </div>
            `;
            
            document.getElementById('statsContainer').innerHTML = statsHTML;
        }}
        
        function initializeSearchDropdowns() {{
            const sizeSelect = document.getElementById('searchSize');
            analysisData.unique_sizes.forEach(size => {{
                const option = document.createElement('option');
                option.value = size;
                option.textContent = `${{size}}pt`;
                sizeSelect.appendChild(option);
            }});
            
            const fontSelect = document.getElementById('searchFont');
            analysisData.unique_fonts.forEach(font => {{
                const option = document.createElement('option');
                option.value = font;
                option.textContent = font;
                fontSelect.appendChild(option);
            }});
            
            const colorSelect = document.getElementById('searchColor');
            analysisData.unique_colors.forEach(color => {{
                const option = document.createElement('option');
                option.value = color;
                // Add color indicator prefix for valid hex colors
                if (color.match(/^[0-9A-F]{{6}}$/i)) {{
                    option.textContent = `■ ${{color}}`;
                    option.style.color = `#${{color}}`;
                    option.style.fontWeight = 'bold';
                }} else {{
                    option.textContent = color;
                }}
                colorSelect.appendChild(option);
            }});
        }}
        
        function initializeCharts() {{
            const stats = analysisData.outlier_data.statistics;
            
            // Font Size Chart
            const sizeData = Object.entries(stats.font_sizes)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);
            
            charts.size = new Chart(document.getElementById('sizeChart'), {{
                type: 'bar',
                data: {{
                    labels: sizeData.map(([size, _]) => `${{size}}pt`),
                    datasets: [{{
                        label: 'Occurrences',
                        data: sizeData.map(([_, count]) => count),
                        backgroundColor: 'rgba(102, 126, 234, 0.8)',
                        borderColor: 'rgba(102, 126, 234, 1)',
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    const pct = (context.parsed.y / stats.total_runs * 100).toFixed(1);
                                    return `${{context.parsed.y.toLocaleString()}} (${{pct}}%)`;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{ beginAtZero: true }}
                    }}
                }}
            }});
            
            // Font Family Chart
            const fontData = Object.entries(stats.font_names)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 7);
            
            charts.font = new Chart(document.getElementById('fontChart'), {{
                type: 'pie',
                data: {{
                    labels: fontData.map(([font, _]) => font),
                    datasets: [{{
                        data: fontData.map(([_, count]) => count),
                        backgroundColor: [
                            'rgba(102, 126, 234, 0.8)',
                            'rgba(118, 75, 162, 0.8)',
                            'rgba(237, 100, 166, 0.8)',
                            'rgba(255, 154, 158, 0.8)',
                            'rgba(250, 208, 196, 0.8)',
                            'rgba(155, 207, 230, 0.8)',
                            'rgba(189, 224, 254, 0.8)'
                        ],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ position: 'right' }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    const pct = (context.parsed / stats.total_runs * 100).toFixed(1);
                                    return `${{context.label}}: ${{context.parsed.toLocaleString()}} (${{pct}}%)`;
                                }}
                            }}
                        }}
                    }}
                }}
            }});
            
            // Color Chart
            const colorData = Object.entries(stats.colors)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);
            
            charts.color = new Chart(document.getElementById('colorChart'), {{
                type: 'bar',
                data: {{
                    labels: colorData.map(([color, _]) => color),
                    datasets: [{{
                        label: 'Occurrences',
                        data: colorData.map(([_, count]) => count),
                        backgroundColor: colorData.map(([color, _]) => {{
                            if (color.match(/^[0-9A-F]{{6}}$/i)) {{
                                return `#${{color}}`;
                            }}
                            return 'rgba(102, 126, 234, 0.8)';
                        }}),
                        borderWidth: 2,
                        borderColor: '#333'
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    const pct = (context.parsed.y / stats.total_runs * 100).toFixed(1);
                                    return `${{context.parsed.y.toLocaleString()}} (${{pct}}%)`;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{ beginAtZero: true }},
                        x: {{
                            ticks: {{
                                maxRotation: 45,
                                minRotation: 45
                            }}
                        }}
                    }}
                }}
            }});
            
            // Outlier Chart
            const outliers = analysisData.outlier_data.outliers;
            charts.outlier = new Chart(document.getElementById('outlierChart'), {{
                type: 'doughnut',
                data: {{
                    labels: ['Size Outliers', 'Font Outliers', 'Color Outliers'],
                    datasets: [{{
                        data: [outliers.size.length, outliers.name.length, outliers.color.length],
                        backgroundColor: [
                            'rgba(102, 126, 234, 0.8)',
                            'rgba(118, 75, 162, 0.8)',
                            'rgba(237, 100, 166, 0.8)'
                        ],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ position: 'bottom' }}
                    }}
                }}
            }});
            
            // File Complexity Chart
            const fileComplexity = analysisData.full_data.results
                .filter(r => r.success)
                .map(r => ({{
                    file: r.file.substring(0, 30),
                    runs: r.runs.length
                }}))
                .sort((a, b) => b.runs - a.runs)
                .slice(0, 10);
            
            charts.file = new Chart(document.getElementById('fileChart'), {{
                type: 'bar',
                data: {{
                    labels: fileComplexity.map(f => f.file),
                    datasets: [{{
                        label: 'Text Runs',
                        data: fileComplexity.map(f => f.runs),
                        backgroundColor: 'rgba(118, 75, 162, 0.8)',
                        borderColor: 'rgba(118, 75, 162, 1)',
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    indexAxis: 'y',
                    plugins: {{
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        x: {{ beginAtZero: true }}
                    }}
                }}
            }});
        }}
        
        function initializeOutliers() {{
            const outliers = analysisData.outlier_data.outliers;
            
            let html = '';
            
            // Size Outliers
            const sizeByFile = {{}};
            outliers.size.forEach(o => {{
                if (!sizeByFile[o.file]) sizeByFile[o.file] = [];
                sizeByFile[o.file].push(o);
            }});
            
            html += `
                <div class="outlier-section">
                    <div class="outlier-header">
                        Font Size Outliers
                        <span class="outlier-count">${{outliers.size.length}}</span>
                    </div>
                    <div class="file-group">
            `;
            
            Object.keys(sizeByFile).slice(0, 5).forEach(file => {{
                const items = sizeByFile[file].slice(0, 10);
                html += `<div class="file-name">${{file}} (${{sizeByFile[file].length}} outliers)</div>`;
                items.forEach(item => {{
                    const colorDisplay = renderColorWithSwatch(item.color_resolved || item.color_value);
                    html += `
                        <div class="outlier-item">
                            <strong>Slide ${{item.slide}}:</strong> ${{item.font_size}}pt, ${{colorDisplay}} - "${{item.text}}"
                        </div>
                    `;
                }});
            }});
            
            html += `</div></div>`;
            
            // Font Name Outliers
            const fontByFile = {{}};
            outliers.name.forEach(o => {{
                if (!fontByFile[o.file]) fontByFile[o.file] = [];
                fontByFile[o.file].push(o);
            }});
            
            html += `
                <div class="outlier-section">
                    <div class="outlier-header">
                        Font Name Outliers
                        <span class="outlier-count">${{outliers.name.length}}</span>
                    </div>
                    <div class="file-group">
            `;
            
            Object.keys(fontByFile).slice(0, 5).forEach(file => {{
                const items = fontByFile[file].slice(0, 10);
                html += `<div class="file-name">${{file}} (${{fontByFile[file].length}} outliers)</div>`;
                items.forEach(item => {{
                    const colorDisplay = renderColorWithSwatch(item.color_resolved || item.color_value);
                    html += `
                        <div class="outlier-item">
                            <strong>Slide ${{item.slide}}:</strong> ${{item.font_name}}, ${{colorDisplay}} - "${{item.text}}"
                        </div>
                    `;
                }});
            }});
            
            html += `</div></div>`;
            
            document.getElementById('outliersSummary').innerHTML = html;
        }}
        
        function initializeFiles() {{
            const results = analysisData.full_data.results.filter(r => r.success);
            
            let html = '<div class="results">';
            
            results.forEach(result => {{
                const runs = result.runs || [];
                const uniqueSizes = new Set(runs.map(r => r.font_size).filter(Boolean)).size;
                const uniqueFonts = new Set(runs.map(r => r.font_name).filter(Boolean)).size;
                const uniqueColors = new Set(runs.map(r => r.color_resolved || r.color_value).filter(Boolean)).size;
                
                html += `
                    <div class="result-card">
                        <div class="result-header">
                            <div class="result-file">${{result.file}}</div>
                        </div>
                        <div class="result-details">
                            <div class="detail-item">
                                <div class="detail-label">Slides</div>
                                <div class="detail-value">${{result.slides || 0}}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Text Runs</div>
                                <div class="detail-value">${{runs.length}}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Unique Sizes</div>
                                <div class="detail-value">${{uniqueSizes}}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Unique Fonts</div>
                                <div class="detail-value">${{uniqueFonts}}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Unique Colors</div>
                                <div class="detail-value">${{uniqueColors}}</div>
                            </div>
                        </div>
                    </div>
                `;
            }});
            
            html += '</div>';
            document.getElementById('filesSummary').innerHTML = html;
        }}
        
        function performSearch() {{
            const size = document.getElementById('searchSize').value;
            const font = document.getElementById('searchFont').value;
            const color = document.getElementById('searchColor').value;
            const fileName = document.getElementById('searchFile').value.toLowerCase();
            const textSearch = document.getElementById('searchText').value.toLowerCase();
            
            const resultsDiv = document.getElementById('searchResults');
            resultsDiv.innerHTML = '<div class="loading">Searching...</div>';
            
            setTimeout(() => {{
                let allRuns = [];
                analysisData.full_data.results.forEach(result => {{
                    if (result.success) {{
                        allRuns = allRuns.concat(result.runs || []);
                    }}
                }});
                
                let filtered = allRuns.filter(run => {{
                    if (size && run.font_size != size) return false;
                    if (font && run.font_name != font) return false;
                    if (color && (run.color_resolved || run.color_value) != color) return false;
                    if (fileName && !run.file.toLowerCase().includes(fileName)) return false;
                    if (textSearch && !run.text.toLowerCase().includes(textSearch)) return false;
                    return true;
                }});
                
                if (filtered.length === 0) {{
                    resultsDiv.innerHTML = '<div class="no-results">No results found. Try adjusting your search criteria.</div>';
                    return;
                }}
                
                let html = `<div class="no-results" style="padding: 10px; background: #e3f2fd; color: #1976d2; border-radius: 6px; margin-bottom: 20px;">
                    Found ${{filtered.length}} result${{filtered.length !== 1 ? 's' : ''}}
                </div>`;
                
                filtered.slice(0, 100).forEach(run => {{
                    const resolvedColor = run.color_resolved || run.color_value || 'N/A';
                    const colorDisplay = renderColorWithSwatch(resolvedColor);
                    html += `
                        <div class="result-card">
                            <div class="result-header">
                                <div class="result-file">${{run.file}}</div>
                                <div class="result-location">
                                    Slide ${{run.slide}} • Shape ${{run.shape}} • Para ${{run.paragraph}} • Run ${{run.run}}
                                </div>
                            </div>
                            <div class="result-details">
                                <div class="detail-item">
                                    <div class="detail-label">Font Size</div>
                                    <div class="detail-value">${{run.font_size || 'N/A'}}${{run.font_size ? 'pt' : ''}}</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">Font Family</div>
                                    <div class="detail-value">${{run.font_name || 'N/A'}}</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">Color</div>
                                    <div class="detail-value">${{colorDisplay}}</div>
                                </div>
                                <div class="detail-item">
                                    <div class="detail-label">Bold/Italic</div>
                                    <div class="detail-value">${{run.bold ? 'B' : ''}}${{run.italic ? 'I' : ''}}${{!run.bold && !run.italic ? 'N' : ''}}</div>
                                </div>
                            </div>
                            <div class="result-text">${{run.text}}</div>
                        </div>
                    `;
                }});
                
                if (filtered.length > 100) {{
                    html += `<div class="no-results">Showing first 100 of ${{filtered.length}} results</div>`;
                }}
                
                resultsDiv.innerHTML = html;
            }}, 100);
        }}
        
        function switchTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            currentTab = tabName;
        }}
    </script>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Interactive visualization saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate interactive HTML visualization')
    parser.add_argument('analysis_dir', help='Directory containing analysis JSON files')
    parser.add_argument('-o', '--output', help='Output HTML file')
    parser.add_argument('-t', '--title', default='PPTX Analysis', help='Title for the visualization')
    
    args = parser.parse_args()
    
    output_file = args.output
    if not output_file:
        output_file = Path(args.analysis_dir) / 'visualization.html'
    
    generate_html_visualization(args.analysis_dir, output_file, args.title)


if __name__ == '__main__':
    main()
