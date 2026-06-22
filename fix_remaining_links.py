#!/usr/bin/env python3
"""
Fix remaining broken links after the initial pass.
"""

import os
import re
from pathlib import Path

project_dir = Path("/Users/g/Desktop/vedantic-mappings")
html_files = list(project_dir.rglob("*.html"))

print(f"Fixing remaining broken links...\n")

# Specific fixes needed
fixes = {
    # Advaita Vedanta files - add "advaita-" prefix
    'gaudapada.html': 'advaita-gaudapada.html',
    'adi-shankara.html': 'advaita-adi-shankara.html', 
    'ramana-maharshi.html': 'advaita-ramana-maharshi.html',
    'nisargadatta-maharaj.html': 'advaita-nisargadatta-maharaj.html',
    'adyashanti-comparison.html': 'advaita-adyashanti-comparison.html',
    # Gnosticism to Advaita
    '../advaita-vedanta/gaudapada.html': '../advaita-vedanta/advaita-gaudapada.html',
    # Gnosticism internal
    'gnosticism-spark.html': 'gnosticism-the_divine_spark.html',
}

fixed_count = 0

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        for broken, fixed in fixes.items():
            # Replace in href attributes
            content = content.replace(f'href="{broken}"', f'href="{fixed}"')
            content = content.replace(f"href='{broken}'", f"href='{fixed}'")
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {html_file.relative_to(project_dir)}")
            fixed_count += 1
            
    except Exception as e:
        print(f"✗ Error processing {html_file}: {e}")

print(f"\n✨ Done! Fixed {fixed_count} files.")
