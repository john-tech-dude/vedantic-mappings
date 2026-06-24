#!/usr/bin/env python3
"""
Global SVG Diagram Contrast Fix for Light Theme
Scans all HTML files and adds CSS overrides for SVG colors that have poor contrast in light mode.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Color mappings from dark-optimized to light-optimized versions
COLOR_MAPPINGS = {
    # Dark indigo/blues → darker versions for light theme
    '#5a6a9a': '#4a5a7a',  # Dark indigo
    '#7a8aba': '#5a6a8a',  # Light indigo  
    '#8a9ab8': '#4a5070',  # Stone/gray
    '#9aabcc': '#6a7a9a',  # Light blue
    '#6a7a9a': '#4a5a7a',  # Medium indigo
    
    # Gold colors → darker versions for light theme
    '#c4a855': '#7a6020',  # Gold
    '#e0c878': '#8a7030',  # Light gold
    '#d4af37': '#8a7030',  # Similar gold (Messiah files)
    '#e6c86e': '#a08840',  # Light gold variant (Messiah files)
    '#b8960c': '#6a5010',  # Deep gold
    
    # Messiah-specific colors
    '#9aaebf': '#5a6080',  # Light gray/stone (Messiah)
    '#7c8ea0': '#4a5060',  # Medium gray (Messiah)
    
    # White → darker for light theme
    '#ffffff': '#e8ecf4',  # White to light gray
    '#fff': '#e8ecf4',     # White shortform
    
    # Dark background colors → lighter for light theme
    '#0c0f14': '#1a1e2e',  # Dark background (Messiah)
    
    # Other common diagram colors
    '#3a4a6a': '#2a3a5a',  # Dark blue
    '#4a5a7a': '#3a4050',  # Medium blue
}

# Pattern to find SVG elements with fill/stroke attributes
SVG_COLOR_PATTERN = re.compile(r'(fill|stroke)\s*=\s*"(#([0-9a-fA-F]{3,6}))"', re.IGNORECASE)

# Pattern to find text elements with fill attributes
TEXT_COLOR_PATTERN = re.compile(r'<text[^>]*\sfill\s*=\s*"(#([0-9a-fA-F]{3,6}))"', re.IGNORECASE)

# Pattern to find existing diagram card CSS
DIAGRAM_CARD_PATTERN = re.compile(r'\.(diagram-card|diagram-container)\s*{', re.IGNORECASE)

# Pattern to find if light theme CSS overrides already exist
LIGHT_THEME_OVERRIDES_PATTERN = re.compile(r'\[data-theme="light"\]\s*\.(diagram-card|diagram-container)', re.IGNORECASE)


def find_svg_colors(html_content: str) -> List[str]:
    """Find all unique SVG colors in the HTML content."""
    colors = set()
    for match in SVG_COLOR_PATTERN.finditer(html_content):
        colors.add(match.group(2).lower())
    return sorted(colors)


def find_text_colors(html_content: str) -> List[str]:
    """Find all unique text fill colors in the HTML content."""
    colors = set()
    for match in TEXT_COLOR_PATTERN.finditer(html_content):
        colors.add(match.group(2).lower())
    return sorted(colors)


def get_diagram_container_class(html_content: str) -> str:
    """Detect which diagram container class is used in the file."""
    if '.diagram-card' in html_content:
        return 'diagram-card'
    elif '.diagram-container' in html_content:
        return 'diagram-container'
    else:
        return 'diagram-card'  # default


def generate_css_overrides(found_colors: List[str], container_class: str = 'diagram-card') -> str:
    """Generate CSS rules for light theme color overrides."""
    css_rules = []
    
    for color in found_colors:
        if color in COLOR_MAPPINGS:
            override_color = COLOR_MAPPINGS[color]
            
            # Generate rules for fill attributes
            css_rules.append(f'[data-theme="light"] .{container_class} svg [fill="#{color}"],')
            css_rules.append(f'[data-theme="light"] .{container_class} svg [stroke="#{color}"] {{')
            css_rules.append(f'  fill: {override_color};')
            css_rules.append(f'  stroke: {override_color};')
            css_rules.append('}')
            
            # Generate rules for text elements specifically
            css_rules.append(f'[data-theme="light"] .{container_class} svg text[fill="#{color}"] {{')
            css_rules.append(f'  fill: {override_color};')
            css_rules.append('}')
    
    return '\n'.join(css_rules) if css_rules else ''


def process_html_file(file_path: Path) -> Tuple[bool, str]:
    """Process a single HTML file and add CSS overrides if needed."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has diagram card CSS
        if not DIAGRAM_CARD_PATTERN.search(content):
            return False, "No diagram card styles found"
        
        # Check if light theme overrides already exist
        if LIGHT_THEME_OVERRIDES_PATTERN.search(content):
            return False, "Light theme overrides already exist"
        
        # Find SVG colors in the file
        svg_colors = find_svg_colors(content)
        text_colors = find_text_colors(content)
        all_colors = sorted(set(svg_colors + text_colors))
        
        # Filter colors that need overrides
        colors_to_override = [color for color in all_colors if color in COLOR_MAPPINGS]
        
        if not colors_to_override:
            return False, "No colors need overriding"
        
        # Detect which container class is used
        container_class = get_diagram_container_class(content)
        
        # Generate CSS overrides
        css_overrides = generate_css_overrides(colors_to_override, container_class)
        
        if not css_overrides:
            return False, "No CSS overrides generated"
        
        # Find insertion point (after diagram CSS)
        diagram_match = DIAGRAM_CARD_PATTERN.search(content)
        if not diagram_match:
            return False, "Could not find diagram CSS"
        
        insertion_point = diagram_match.end()
        
        # Insert the CSS overrides
        css_block = f"""

/* SVG Diagram Color Fixes for Light Theme */
{css_overrides}
"""
        
        new_content = content[:insertion_point] + css_block + content[insertion_point:]
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"Added overrides for {len(colors_to_override)} colors ({container_class}): {', '.join(colors_to_override)}"
        
    except Exception as e:
        return False, f"Error processing file: {str(e)}"


def scan_all_html_files(root_dir: Path) -> Dict[str, List[str]]:
    """Scan all HTML files and identify SVG colors used."""
    color_usage = {}
    
    for html_file in root_dir.rglob("*.html"):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if DIAGRAM_CARD_PATTERN.search(content):
                svg_colors = find_svg_colors(content)
                text_colors = find_text_colors(content)
                all_colors = sorted(set(svg_colors + text_colors))
                
                if all_colors:
                    color_usage[str(html_file)] = all_colors
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
    
    return color_usage


def main():
    """Main function to fix SVG contrast across all HTML files."""
    import sys
    
    root_dir = Path.cwd()
    
    # Check for command line flag to skip confirmation
    auto_mode = '--auto' in sys.argv or '-y' in sys.argv
    
    print("=" * 60)
    print("SVG Diagram Contrast Fix for Light Theme")
    print("=" * 60)
    print(f"Scanning directory: {root_dir}")
    print()
    
    # First, scan all files to show what will be fixed
    print("SCANNING FOR SVG DIAGRAMS...")
    color_usage = scan_all_html_files(root_dir)
    
    if not color_usage:
        print("No HTML files with diagram cards found.")
        return
    
    print(f"Found {len(color_usage)} file(s) with diagram cards:")
    print()
    
    for file_path, colors in color_usage.items():
        rel_path = Path(file_path).relative_to(root_dir)
        colors_needing_override = [c for c in colors if c in COLOR_MAPPINGS]
        print(f"  {rel_path}")
        print(f"    Colors found: {', '.join(colors)}")
        if colors_needing_override:
            print(f"    Will override: {', '.join(colors_needing_override)}")
        else:
            print(f"    No overrides needed")
        print()
    
    # Ask for confirmation unless in auto mode
    if not auto_mode:
        try:
            response = input("Proceed with fixes? (y/n): ").strip().lower()
            if response != 'y':
                print("Aborted.")
                return
        except EOFError:
            print("No input detected, running in auto mode...")
            auto_mode = True
    
    print()
    print("APPLYING FIXES...")
    print("-" * 60)
    
    # Process each file
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for file_path in color_usage.keys():
        path = Path(file_path)
        rel_path = path.relative_to(root_dir)
        
        success, message = process_html_file(path)
        
        if success:
            print(f"✓ {rel_path}: {message}")
            success_count += 1
        else:
            print(f"○ {rel_path}: {message}")
            skip_count += 1
    
    print("-" * 60)
    print(f"Complete! Success: {success_count}, Skipped: {skip_count}, Errors: {error_count}")


if __name__ == "__main__":
    main()