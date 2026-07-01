#!/usr/bin/env python3
"""
Standardize chapter separator icons to match TOC icons across all sections.
This ensures consistency between navigation sidebar and footer chapter navigation.
"""
import re
import sys
from pathlib import Path

# Check for dry-run flag
DRY_RUN = '--dry-run' in sys.argv or '-d' in sys.argv

# Define the correct SVG for each section based on their TOC icons
section_svgs = {
    'advaita-vedanta': '<span class="chapter-sep"><svg class="icon-om" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 22s-8-4.5-8-11.5C4 6.5 8 2 12 2s8 4.5 8 8.5c0 7-8 11.5-8 11.5Z"/><path d="M12 22s-4-3-4-8.5C8 10 10 6 12 6s4 4 4 7.5c0 5.5-4 8.5-4 8.5Z"/><path d="M12 22c1.5 0 3-1 4-2.5M12 22c-1.5 0-3-1-4-2.5"/></svg></span>',
    'taoism': '<span class="chapter-sep"><svg class="icon-yinyang" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="M12 2a5 5 0 0 0 0 10 5 5 0 0 1 0 10"/><circle cx="12" cy="7" r="1.5" fill="currentColor"/><circle cx="12" cy="17" r="1.5" fill="none" stroke="currentColor" stroke-width="1"/></svg></span>',
    'messiah': '<span class="chapter-sep"><svg class="icon-cross" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 2v20M8 8h8"/></svg></span>',
    'quantum_mechanics': '<span class="chapter-sep"><svg class="icon-atom" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><ellipse cx="12" cy="12" rx="3" ry="10" transform="rotate(45 12 12)"/><ellipse cx="12" cy="12" rx="3" ry="10" transform="rotate(-45 12 12)"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg></span>',
    'kabbalah': '<span class="chapter-sep"><svg class="icon-star-david" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 2.5l5.5 9.5H6.5z"/><path d="M12 21.5L6.5 12h11z"/></svg></span>',
    'gnosticism': '<span class="chapter-sep"><svg class="icon-diamond" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M2.7 10.3a2.4 2.4 0 0 0 0 3.4l7.6 7.6a2.4 2.4 0 0 0 3.4 0l7.6-7.6a2.4 2.4 0 0 0 0-3.4L13.7 2.7a2.4 2.4 0 0 0-3.4 0z"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg></span>'
}

# Pattern to match any chapter separator content
chapter_sep_pattern = re.compile(r'<span class="chapter-sep">.*?</span>', re.DOTALL)

project_dir = Path("/Users/g/Desktop/vedantic-mappings")
html_files = sorted(list(project_dir.rglob("*.html")))

print("Standardizing chapter separator icons to match TOC icons...")
if DRY_RUN:
    print("DRY RUN MODE - No files will be modified")
    print("=" * 60)

modified_files = 0
total_replacements = 0

for filepath in html_files:
    if '.git' in filepath.parts or '.gemini' in filepath.parts:
        continue
    
    # Determine which section this file belongs to
    section = None
    for sec in section_svgs.keys():
        if sec in str(filepath):
            section = sec
            break
    
    if not section:
        continue
    
    try:
        content = filepath.read_text(encoding='utf-8')
        original_content = content
        
        # Count current chapter separators
        current_seps = chapter_sep_pattern.findall(content)
        if not current_seps:
            continue
            
        # Replace all chapter separators with the correct SVG for this section
        new_content = chapter_sep_pattern.sub(section_svgs[section], content)
        
        if new_content != original_content:
            file_replacements = len(current_seps)
            if DRY_RUN:
                print(f"📋 Would standardize {file_replacements} chapter separators in: {filepath.relative_to(project_dir)}")
                modified_files += 1
                total_replacements += file_replacements
            else:
                filepath.write_text(new_content, encoding='utf-8')
                print(f"✓ Standardized {file_replacements} chapter separators in: {filepath.relative_to(project_dir)}")
                modified_files += 1
                total_replacements += file_replacements
            
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")

print("=" * 60)
if DRY_RUN:
    print(f"DRY RUN COMPLETE")
    print(f"Would update {modified_files} files with {total_replacements} chapter separator standardizations")
    print("Run without --dry-run flag to apply changes")
else:
    print(f"Complete! Updated {modified_files} files, standardized {total_replacements} chapter separators.")
    print("All chapter separators now match their respective TOC icons.")