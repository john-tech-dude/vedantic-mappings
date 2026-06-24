#!/usr/bin/env python3
"""
Script to standardize table of content sidebars across all HTML files:
1. Remove emojis from nav-item-icon spans
2. Remove target="_blank" from links
3. Fix nav-menu max-height/overflow issues
4. Ensure consistent functionality
"""

import os
import glob
from pathlib import Path
import re

# Get the project directory
project_dir = Path("/Users/g/Desktop/vedantic-mappings")

# Find all HTML files
html_files = list(project_dir.rglob("*.html"))

print(f"Found {len(html_files)} HTML files to process.")

# Emoji replacements - replace emojis with consistent SVG icons or text
emoji_replacements = {
    '⌂': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    '🕉': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M6.34 17.66l-1.41 1.41"/><path d="M19.07 4.93l-1.41 1.41"/></svg>',
    '✡': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>',
    '✝': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    '☯': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1-4-10"/><path d="M2 12h20"/></svg>',
    '⚛': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="M12 2v4"/><path d="M12 18v4"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M6.34 17.66l-1.41 1.41"/><path d="M19.07 4.93l-1.41 1.41"/></svg>',
    '✦': '<svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><polygon points="12 2 15 9 20 9 17 14 22 14 17 19 20 19 15 22 12 19 9 17 9 20 15 14 9 9 14 7 4 9 7 9 4 12 2z"/></svg>',
    '📋': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>',
    '📅': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    '📖': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    '◈': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="7"/></svg>',
    '⊙': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>',
    '☀': '<svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>',
    '☾': '<svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
}

processed_count = 0

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Replace emojis in nav-item-icon spans with SVGs
        for emoji, svg_replacement in emoji_replacements.items():
            content = re.sub(
                rf'<span class="nav-item-icon">{re.escape(emoji)}</span>',
                f'<span class="nav-item-icon">{svg_replacement}</span>',
                content
            )
        
        # 2. Remove target="_blank" from all links in nav-menu
        # Only remove from nav-menu section to avoid affecting legitimate external links
        nav_menu_match = re.search(r'<div class="nav-menu[^"]*"(.*?)</div>', content, re.DOTALL)
        if nav_menu_match:
            nav_menu_content = nav_menu_match.group(0)
            nav_menu_content = re.sub(r'target="_blank"', '', nav_menu_content)
            content = content.replace(nav_menu_match.group(0), nav_menu_content)
        
        # 3. Remove target="_blank" from suspicious script tags (security issue)
        content = re.sub(r'<script[^>]*src=\'https://prod-chat-kimi[^>]*></script><base target="_blank">', '', content)
        
        # 4. Fix nav-menu CSS max-height issue - change from 80vh to 85vh and add proper padding
        content = re.sub(
            r'max-height: 80vh;',
            'max-height: 85vh; padding-bottom: 1rem;',
            content
        )
        
        # Also handle the case with different spacing
        content = re.sub(
            r'max-height:\s*80vh;',
            'max-height: 85vh; padding-bottom: 1rem;',
            content
        )
        
        # 5. Ensure overflow-y: auto is present in nav-menu
        if re.search(r'\.nav-menu\s*{', content):
            if 'overflow-y' not in content:
                # Add overflow-y after max-height
                content = re.sub(
                    r'(max-height:\s*85vh;[^}]*?)',
                    r'\1 overflow-y: auto;',
                    content
                )
        
        # 6. Remove emoji text content from nav-item-icon spans that might have been missed
        content = re.sub(
            r'<span class="nav-item-icon">[^<]*[🕉✡✝☯⚛✦📋📅📖◈⊙⌂☀☾]+[^<]*</span>',
            '<span class="nav-item-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="3"/></svg></span>',
            content
        )
        
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
print("\nChanges made:")
print("• Replaced all emojis in nav-item-icon spans with SVG icons")
print("• Removed target='_blank' from navigation links")
print("• Removed suspicious external scripts (security)")
print("• Fixed nav-menu max-height from 80vh to 85vh to prevent cutoff")
print("• Added padding-bottom to ensure last items are visible")
print("• Ensured overflow-y: auto for proper scrolling")