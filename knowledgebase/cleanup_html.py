#!/usr/bin/env python3
"""
Clean HTML wrapper tags from Perplexity-generated markdown files.
Removes HTML wrappers while preserving markdown and code blocks.
"""

import re
from pathlib import Path

def clean_html_artifacts(content: str) -> str:
    """Remove HTML wrapper tags while preserving markdown content."""

    # Remove <pre> wrapper tags with all attributes
    content = re.sub(r'<pre[^>]*>', '', content)
    content = re.sub(r'</pre>', '', content)

    # Remove <div> wrapper tags with all attributes
    content = re.sub(r'<div[^>]*>', '', content)
    content = re.sub(r'</div>', '', content)

    # Remove <button> tags (copy buttons, etc.)
    content = re.sub(r'<button[^>]*>.*?</button>', '', content, flags=re.DOTALL)

    # Remove other common HTML tags
    content = re.sub(r'<span[^>]*>', '', content)
    content = re.sub(r'</span>', '', content)

    # Clean up excessive blank lines (more than 2 consecutive)
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()

def process_file(file_path: Path) -> bool:
    """Process a single file to remove HTML artifacts."""
    try:
        print(f"Processing: {file_path.name}")

        # Read original content
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()

        # Clean HTML artifacts
        cleaned = clean_html_artifacts(original)

        # Write cleaned content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)

        # Calculate reduction
        original_size = len(original)
        cleaned_size = len(cleaned)
        reduction = original_size - cleaned_size

        print(f"  ✓ Cleaned {reduction} characters ({reduction/original_size*100:.1f}% reduction)")
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Process all files needing HTML cleanup."""

    base_path = Path(__file__).parent / "research_prompts.md" / "results"

    files_to_clean = [
        # Database files
        base_path / "database" / "01_DRIZZLE_QUERY_EXAMPLES.md",
        base_path / "database" / "02_SCHEMA_MIGRATIONS.md",
        base_path / "database" / "03_QUERY_OPTIMIZATION.md",
        # Frontend files
        base_path / "frontend" / "01_COMPONENT_PATTERNS.md",
        base_path / "frontend" / "02_HOOKS_PATTERNS.md",
        base_path / "frontend" / "03_FORMS_VALIDATION.md",
        base_path / "frontend" / "04_STATE_MANAGEMENT.md",
    ]

    print("=" * 60)
    print("HTML Artifact Cleanup")
    print("=" * 60)
    print()

    success_count = 0
    for file_path in files_to_clean:
        if file_path.exists():
            if process_file(file_path):
                success_count += 1
        else:
            print(f"Warning: File not found: {file_path}")

    print()
    print("=" * 60)
    print(f"Completed: {success_count}/{len(files_to_clean)} files cleaned")
    print("=" * 60)

if __name__ == "__main__":
    main()
