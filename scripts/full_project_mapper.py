import os
import re
import requests

def extract_links_raw(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        matches = re.findall(r'href=["\']([^"\']+)["\']', content)
        clean_links = []
        for m in matches:
            clean = m.split('#')[0].strip()
            if clean and not clean.startswith(('http', 'mailto:', 'tel:', '#')):
                clean_links.append(clean)
        return list(set(clean_links))
    except Exception:
        return []

def scan_all_html_files(project_root):
    all_links = {}
    for root, dirs, files in os.walk(project_root):
        # Skip hidden git folders
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, project_root)
                
                # Extract all targets from this file
                raw_hrefs = extract_links_raw(abs_path)
                resolved_targets = []
                
                file_dir = os.path.dirname(abs_path)
                for href in raw_hrefs:
                    target_abs = os.path.normpath(os.path.join(file_dir, href))
                    if os.path.isdir(target_abs):
                        target_file = os.path.join(target_abs, "index.html")
                    else:
                        target_file = target_abs
                        
                    if os.path.exists(target_file):
                        resolved_targets.append(os.path.relpath(target_file, project_root))
                
                all_links[rel_path] = resolved_targets
    return all_links

# Define paths relative to your current standing location
current_dir = os.getcwd()
# Look up one level if we are standing inside a subfolder, otherwise stay here
project_root = current_dir if os.path.exists(os.path.join(current_dir, 'vedantic-mappings.code-workspace')) else os.path.dirname(current_dir)

print(f"🔍 Mapping complete network graph for root: {os.path.basename(project_root)}...")
link_map = scan_all_html_files(project_root)

# Convert to structural string representation
map_text_lines = []
for source_file, targets in sorted(link_map.items()):
    map_text_lines.append(f"📄 File: {source_file}")
    if not targets:
        map_text_lines.append("    └── (No outbound internal links)")
    for t in sorted(set(targets)):
        map_text_lines.append(f"    └── Links To ➔ {t}")

network_graph = "\n".join(map_text_lines)

print("\n--- DETECTED PROJECT LINK NETWORK GRAPH ---")
print(network_graph[:2000] + "\n...[Truncated for console display]..." if len(network_graph) > 2000 else network_graph)
print("-------------------------------------------\n")

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("Error: OPENROUTER_API_KEY environment variable is missing.")
    exit(1)

print("🤖 Requesting OpenRouter to analyze your network connectivity flow...")

prompt = f"""
Analyze this map of file inter-linking within my philosophical digital garden. Trace how fluidly a user can traverse across the different traditions (Advaita, Kabbalah, Gnosticism, Taoism, Quantum Mechanics) via the detected links, identify any completely orphaned files, and evaluate if the navigation from the index down to the edge content is cohesive:

{network_graph}
"""

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": prompt}]
    }
)

if response.status_code == 200:
    print("\n--- AI RE-LINKING INTEGRITY ANALYSIS ---")
    print(response.json()['choices'][0]['message']['content'])
else:
    print(f"\nError connecting to API ({response.status_code}): {response.text}")

