#!/usr/bin/env python3
"""
Script to update footer date to "June 20 2026" format across all HTML files.
"""

import os
from pathlib import Path

# Get the project directory
project_dir = Path("/Users/g/Desktop/vedantic-mappings")

# Find all HTML files
html_files = list(project_dir.rglob("*.html"))

print(f"Found {len(html_files)} HTML files to process.")

# Define the date replacement
replacements = [
    # Replace "20 June 2026" with "June 20 2026"
    (
        '20 June 2026',
        'June 20 2026'
    ),
]

processed_count = 0

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old_text, new_text in replacements:
            content = content.replace(old_text, new_text)
        
        # Only write if content changed
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {html_file.relative_to(project_dir)}")
            processed_count += 1
        else:
            print(f"- Skipped (no changes): {html_file.relative_to(project_dir)}")
            
    except Exception as e:
        print(f"✗ Error processing {html_file}: {e}")

print(f"\nDone! Processed {processed_count} files.")
print("Updated date format from '20 June 2026' to 'June 20 2026' in all footers.")