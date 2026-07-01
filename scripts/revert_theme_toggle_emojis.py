#!/usr/bin/env python3
"""
Revert theme toggle icons from SVG back to emoji characters.
This keeps all other SVG replacements intact.
"""
import re
import sys
from pathlib import Path

# Check for dry-run flag
DRY_RUN = '--dry-run' in sys.argv or '-d' in sys.argv

# Patterns to replace SVG theme toggle icons back to emojis
replacements = [
    # Standard theme toggle icons (sun/moon)
    (re.compile(r'<span class="theme-toggle-icon theme-toggle-icon-sun"[^>]*>.*?</span>'), '<span class="theme-toggle-icon theme-toggle-icon-sun">☼</span>'),
    (re.compile(r'<span class="theme-toggle-icon theme-toggle-icon-moon"[^>]*>.*?</span>'), '<span class="theme-toggle-icon theme-toggle-icon-moon">☾</span>'),
    
    # TI theme toggle icons (used in some kabbalah/messiah files)
    (re.compile(r'<span class="theme-toggle-icon ti-sun"[^>]*>.*?</span>'), '<span class="theme-toggle-icon ti-sun">☼</span>'),
    (re.compile(r'<span class="theme-toggle-icon ti-moon"[^>]*>.*?</span>'), '<span class="theme-toggle-icon ti-moon">☾</span>'),
]

project_dir = Path("/Users/g/Desktop/vedantic-mappings")
html_files = sorted(list(project_dir.rglob("*.html")))

print("Reverting theme toggle icons from SVG back to emoji...")
if DRY_RUN:
    print("DRY RUN MODE - No files will be modified")
    print("=" * 60)

modified_files = 0
total_replacements = 0

for filepath in html_files:
    if '.git' in filepath.parts or '.gemini' in filepath.parts:
        continue
    
    try:
        content = filepath.read_text(encoding='utf-8')
        original_content = content
        
        file_replacements = 0
        
        for pattern, replacement in replacements:
            matches = pattern.findall(content)
            if matches:
                file_replacements += len(matches)
                content = pattern.sub(replacement, content)
        
        if content != original_content:
            if DRY_RUN:
                print(f"📋 Would revert {file_replacements} theme toggle icons in: {filepath.relative_to(project_dir)}")
                modified_files += 1
                total_replacements += file_replacements
            else:
                filepath.write_text(content, encoding='utf-8')
                print(f"✓ Reverted {file_replacements} theme toggle icons in: {filepath.relative_to(project_dir)}")
                modified_files += 1
                total_replacements += file_replacements
            
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")

print("=" * 60)
if DRY_RUN:
    print(f"DRY RUN COMPLETE")
    print(f"Would update {modified_files} files with {total_replacements} theme toggle icon reversions")
    print("Run without --dry-run flag to apply changes")
else:
    print(f"Reversion complete! Updated {modified_files} files, reverted {total_replacements} theme toggle icons to emojis.")
    print("All other SVG replacements remain intact.")