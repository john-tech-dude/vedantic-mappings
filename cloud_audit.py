#!/usr/bin/env python3
import os
import subprocess
import sys

MODEL = "gpt-oss:120b-cloud"
FOLDER = "."
EXTENSION = ".md"   # change to ".html" if you want HTML files

def ask_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL, prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Timeout"
    except Exception as e:
        return f"Error: {e}"

def audit_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Could not read {filepath}: {e}")
        return

    max_chars = 8000
    if len(content) > max_chars:
        content = content[:max_chars] + "\n... (truncated)"

    prompt = f"""
You are a document consistency auditor. Review the following text and report:
- Consistent terminology (e.g., Ātman vs Atman)
- Markdown formatting errors
- Spelling or grammar mistakes
- Logical contradictions or unclear statements

If the document is consistent and well-formatted, just reply "OK".

FILE: {filepath}

CONTENT:
{content}
"""
    print(f"\nAuditing: {filepath}")
    print("Sending to cloud model...")
    response = ask_ollama(prompt)
    print("Response:")
    print(response)
    print("-" * 60)

def main():
    if not os.path.isdir(FOLDER):
        print(f"Folder '{FOLDER}' not found.")
        sys.exit(1)

    files = []
    for root, dirs, filenames in os.walk(FOLDER):
        for f in filenames:
            if f.endswith(EXTENSION):
                files.append(os.path.join(root, f))

    if not files:
        print(f"No {EXTENSION} files found in '{FOLDER}'")
        sys.exit(0)

    print(f"Found {len(files)} {EXTENSION} file(s). Auditing using cloud model '{MODEL}'...")
    for fpath in files:
        audit_file(fpath)

if __name__ == "__main__":
    main()
python3 cloud_audit.py
x

