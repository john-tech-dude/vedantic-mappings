#!/usr/bin/env python3
"""
Script to revert footer credit and copyright changes across all HTML files.
Changes back to: "Researched & Composed" and "© 2026 John M Q. All rights reserved."
"""

import os
import glob
from pathlib import Path

# Get the project directory
project_dir = Path("/Users/g/Desktop/vedantic-mappings")

# Find all HTML files
html_files = list(project_dir.rglob("*.html"))

print(f"Found {len(html_files)} HTML files to process.")

# Define the replacements
replacements = [
    # Replace the new credit line with the old one
    (
        '<div class="footer-credit">Curated from primary transcripts and oral teachings.</div>',
        '<div class="footer-credit">Researched &amp; Composed</div>'
    ),
    # Replace the two new copyright lines with the old single line
    (
        '''<div class="footer-copyright">Last updated: 20 June 2026 · Six cartographies</div>
        <div class="footer-copyright">A non-dual resource by J.M.Q. · © 2026</div>''',
        '<div class="footer-copyright">© 2026 John M Q. All rights reserved.</div>'
    ),
    # Also handle the version where it's on one line
    (
        '<div class="footer-version">Last updated: 20 June 2026 &middot; Six cartographies</div>',
        '<div class="footer-copyright">© 2026 John M Q. All rights reserved.</div>'
    ),
    # Handle the single copyright line version
    (
        '<div class="footer-copyright">A non-dual resource by J.M.Q. · © 2026</div>',
        '<div class="footer-copyright">© 2026 John M Q. All rights reserved.</div>'
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