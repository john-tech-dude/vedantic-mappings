#!/usr/bin/env python3
"""
Script to remove target="_blank" from all HTML files.
This ensures all links open in the same tab instead of a new window.
"""

import os
import re
from pathlib import Path

# Get the project directory
project_dir = Path("/Users/g/Desktop/vedantic-mappings")

# Find all HTML files
html_files = list(project_dir.rglob("*.html"))

print(f"Found {len(html_files)} HTML files to process.")

processed_count = 0

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove target="_blank" from all anchor tags
        content = content.replace('target="_blank"', '')
        
        # Remove <base target="_blank"> tags entirely
        content = content.replace('<base target="_blank">', '')
        content = content.replace('<base target="_blank" />', '')
        
        # Also remove self-closing base tags
        content = content.replace('<base target="_blank"/>', '')
        
        # Remove target="_blank" from any other context
        content = re.sub(r'target\s*=\s*["\']_blank["\']', '', content)
        
        # Only write if content changed
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {html_file.relative_to(project_dir)}")
            processed_count += 1
        else:
            print(f"- Skipped (no target=\"_blank\" found): {html_file.relative_to(project_dir)}")
            
    except Exception as e:
        print(f"✗ Error processing {html_file}: {e}")

print(f"\nDone! Processed {processed_count} files.")
print("All links will now open in the same tab.")