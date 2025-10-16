#!/usr/bin/env python3
"""
Generate detailed list of duplicate knowledge items with IDs for deletion
"""

import json
from collections import defaultdict

# Load data
with open('/tmp/ki_page1.json') as f:
    page1 = json.load(f)

with open('/tmp/ki_page2.json') as f:
    page2 = json.load(f)

all_items = page1['items'] + page2['items']

# Group by title
title_groups = defaultdict(list)
for item in all_items:
    title_groups[item['title']].append(item)

duplicates = {title: items for title, items in title_groups.items() if len(items) > 1}

print("# Duplicate Knowledge Items - Detailed Deletion Guide")
print("")
print("Date: 2025-10-15")
print("Total duplicate groups: {}".format(len(duplicates)))
print("")

# Categorize duplicates
exact_dupes = []  # Same tags, likely identical content
cross_domain_dupes = []  # Different tags, may have different content
readme_dupes = []  # Special case - many READMEs
untagged_dupes = []  # Missing tags

for title, items in sorted(duplicates.items()):
    if title == "README.md":
        readme_dupes = items
        continue

    # Check if any are untagged
    has_untagged = any(not item['metadata'].get('tags') for item in items)
    if has_untagged:
        untagged_dupes.append((title, items))
        continue

    # Check if all have same tags
    tag_sets = [tuple(sorted(item['metadata'].get('tags', []))) for item in items]
    if len(set(tag_sets)) == 1:
        exact_dupes.append((title, items))
    else:
        cross_domain_dupes.append((title, items))

print("## Category 1: Exact Duplicates (Same Tags)")
print("")
print("These are likely ingestion errors. Keep the most recent, delete others.")
print("")

for title, items in sorted(exact_dupes):
    print("### {}".format(title))
    print("")
    tags = ', '.join(items[0]['metadata'].get('tags', []))
    print("**Tags**: {}".format(tags))
    print("")

    # Sort by creation date
    sorted_items = sorted(items, key=lambda x: x['created_at'], reverse=True)

    print("**KEEP**: {} (created: {})".format(
        sorted_items[0]['id'],
        sorted_items[0]['created_at'][:10]
    ))
    print("")

    for item in sorted_items[1:]:
        print("**DELETE**: {} (created: {})".format(
            item['id'],
            item['created_at'][:10]
        ))
        print("```bash")
        print("curl -X DELETE -H 'Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI' \\")
        print("  http://localhost:8181/api/knowledge-items/{}".format(item['id']))
        print("```")
        print("")

print("")
print("## Category 2: Cross-Domain Duplicates (Different Tags)")
print("")
print("These may have domain-specific content. Review before deletion.")
print("")

for title, items in sorted(cross_domain_dupes):
    print("### {}".format(title))
    print("")

    for item in items:
        tags = ', '.join(item['metadata'].get('tags', []))
        print("- **ID**: `{}`".format(item['id']))
        print("  **Tags**: {}".format(tags))
        print("  **Created**: {}".format(item['created_at'][:10]))
        print("  **Words**: {:,}".format(item['metadata'].get('word_count', 0)))
        print("")

    print("**Recommendation**: Review content to determine if truly duplicates.")
    print("")

print("")
print("## Category 3: README.md Duplicates")
print("")
print("Special case with 17 instances. Organized by tags:")
print("")

# Group READMEs by tag pattern
readme_by_category = defaultdict(list)
for item in readme_dupes:
    tags = item['metadata'].get('tags', [])
    if not tags:
        readme_by_category['untagged'].append(item)
    elif 'projects' in tags and 'netzwaechter refactored' in tags:
        # Extract the specific category
        category_tags = [t for t in tags if t not in ['projects', 'netzwaechter refactored']]
        if category_tags:
            readme_by_category['project-' + category_tags[0]].append(item)
        else:
            readme_by_category['project-general'].append(item)
    elif 'global' in tags:
        category_tags = [t for t in tags if t != 'global']
        if category_tags:
            readme_by_category['global-' + category_tags[0]].append(item)
        else:
            readme_by_category['global-only'].append(item)
    elif 'knowledge organization' in tags:
        readme_by_category['knowledge-org'].append(item)

for category, items in sorted(readme_by_category.items()):
    print("### {} ({} instances)".format(category, len(items)))
    print("")
    for item in items:
        tags = ', '.join(item['metadata'].get('tags', []))
        print("- `{}` - Tags: [{}]".format(item['id'], tags))
    print("")

print("**Recommendation for READMEs**:")
print("")
print("1. **DELETE untagged** (2 instances)")
print("2. **KEEP project-specific** versions (6 instances)")
print("3. **KEEP one global per topic** (review for actual differences)")
print("4. **KEEP knowledge-org** version")
print("")

print("")
print("## Category 4: Untagged Duplicates")
print("")

for title, items in sorted(untagged_dupes):
    print("### {}".format(title))
    print("")

    for item in items:
        tags = item['metadata'].get('tags', [])
        tag_str = ', '.join(tags) if tags else 'NONE'
        print("- **ID**: `{}`".format(item['id']))
        print("  **Tags**: {}".format(tag_str))
        print("  **Created**: {}".format(item['created_at'][:10]))
        print("")

    print("**Action**: Tag appropriately, then keep most recent.")
    print("")

print("")
print("## Summary")
print("")
print("- **Exact duplicates to delete**: {} items".format(
    sum(len(items) - 1 for _, items in exact_dupes)
))
print("- **Cross-domain duplicates to review**: {} items".format(
    sum(len(items) for _, items in cross_domain_dupes)
))
print("- **README.md instances**: {} (recommend deleting 5-8)".format(len(readme_dupes)))
print("- **Untagged duplicates**: {} items".format(
    sum(len(items) for _, items in untagged_dupes)
))
print("")
print("**Total potential deletions**: 20-30 items")
print("")
