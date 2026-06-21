#!/usr/bin/env python3
"""
Script to find and fix broken links in all HTML files.
Checks both internal (relative) and external links.
"""

import os
import re
from pathlib import Path
from urllib.parse import urlparse

project_dir = Path("/Users/g/Desktop/vedantic-mappings")
html_files = list(project_dir.rglob("*.html"))

print(f"Found {len(html_files)} HTML files to check.\n")

broken_links = []
fixed_count = 0

def check_link_exists(link_path, base_file):
    """Check if a relative link target exists."""
    # Handle anchors (same-page links)
    if link_path.startswith('#'):
        return True  # Anchor links are always valid within the page
    
    # Handle absolute URLs
    if link_path.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
        return True  # External links are not checked for file existence
    
    # Resolve relative path
    target_path = (base_file.parent / link_path).resolve()
    
    # If it's a directory, check if it exists
    if target_path.is_dir():
        return True
    
    # If it's a file, check if it exists
    if target_path.exists():
        return True
    
    return False

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all href attributes
        href_pattern = r'href=["\']([^"\']+)["\']'
        hrefs = re.findall(href_pattern, content)
        
        file_broken = []
        for href in hrefs:
            # Skip javascript: and # anchor-only links
            if href.startswith(('javascript:', '#')):
                continue
            
            # Check relative links
            if not href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                if not check_link_exists(href, html_file):
                    file_broken.append(href)
        
        if file_broken:
            broken_links.append({
                'file': html_file,
                'links': file_broken
            })
            
    except Exception as e:
        print(f"✗ Error processing {html_file}: {e}")

# Report broken links
if broken_links:
    print("🔍 Found broken links:\n")
    for item in broken_links:
        print(f"📄 {item['file'].relative_to(project_dir)}")
        for link in item['links']:
            print(f"   ✗ {link}")
        print()
else:
    print("✅ No broken links found!")

# Now try to fix common broken links
print("\n🔧 Attempting to fix common broken link patterns...\n")

for item in broken_links:
    try:
        html_file = item['file']
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        for broken_link in item['links']:
            # Try to find the correct file
            broken_filename = Path(broken_link).name
            
            # Search for the file in the project
            found_files = list(project_dir.rglob(broken_filename))
            
            if found_files:
                # Get the relative path from the current file
                correct_path = os.path.relpath(found_files[0], html_file.parent)
                
                # Fix the link (use forward slashes for web)
                correct_path = correct_path.replace('\\', '/')
                
                # Replace the broken link with the correct one
                content = content.replace(f'href="{broken_link}"', f'href="{correct_path}"')
                content = content.replace(f"href='{broken_link}'", f"href='{correct_path}'")
                
                print(f"✓ Fixed: {broken_link} → {correct_path}")
                print(f"  in {html_file.relative_to(project_dir)}")
                fixed_count += 1
        
        # Write back if changed
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
    except Exception as e:
        print(f"✗ Error fixing {item['file']}: {e}")

print(f"\n✨ Done! Fixed {fixed_count} broken links.")
print(f"📊 Total broken links remaining: {sum(len(item['links']) for item in broken_links) - fixed_count}")
