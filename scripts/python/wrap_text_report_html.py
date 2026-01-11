#!/usr/bin/env python3
"""
Generate HTML wrapper for text reports with navigation back to index.

Usage:
  python wrap_text_report_html.py <text_file> <output_html> <title>
"""
import argparse
import sys
from pathlib import Path


def wrap_text_report(text_file, output_file, title):
    """Wrap text report in HTML with navigation."""
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 1.5em;
        }}
        
        .back-link {{
            color: white;
            text-decoration: none;
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            transition: background 0.3s;
        }}
        
        .back-link:hover {{
            background: rgba(255,255,255,0.3);
        }}
        
        .content {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow-x: auto;
        }}
        
        pre {{
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 0.9em;
            line-height: 1.4;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <a href="../../../index.html" class="back-link">← Back to Home</a>
    </div>
    
    <div class="content">
        <pre>{content}</pre>
    </div>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Wrap text report in HTML with navigation')
    parser.add_argument('text_file', help='Input text file')
    parser.add_argument('output_file', help='Output HTML file')
    parser.add_argument('-t', '--title', default='Analysis Report', help='Report title')
    
    args = parser.parse_args()
    wrap_text_report(args.text_file, args.output_file, args.title)


if __name__ == '__main__':
    main()
