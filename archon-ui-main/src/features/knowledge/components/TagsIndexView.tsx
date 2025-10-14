/**
 * Tags Index View Component
 * Displays all knowledge tags organized by category
 */

import { useMemo, useState } from "react";
import { Tag, ChevronDown, ChevronRight } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { cn, glassCard } from "../../ui/primitives/styles";
import { useKnowledgeTags, useTagsByCategory } from "../hooks/useKnowledgeTags";

interface TagsIndexViewProps {
  onTagClick?: (tagName: string) => void;
}

export const TagsIndexView: React.FC<TagsIndexViewProps> = ({ onTagClick }) => {
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set(["framework", "language"]));
  const [searchQuery, setSearchQuery] = useState("");

  // Fetch all tags
  const { data: allTags, isLoading } = useKnowledgeTags();

  // Fetch tags grouped by category
  const { data: tagsByCategory } = useTagsByCategory();

  // Filter tags by search query
  const filteredTags = useMemo(() => {
    if (!allTags) return [];
    if (!searchQuery) return allTags;

    const query = searchQuery.toLowerCase();
    return allTags.filter(
      (tag) =>
        tag.tag_name.toLowerCase().includes(query) ||
        tag.description.toLowerCase().includes(query) ||
        tag.category.toLowerCase().includes(query),
    );
  }, [allTags, searchQuery]);

  // Group filtered tags by category
  const groupedTags = useMemo(() => {
    const grouped: Record<string, typeof filteredTags> = {};
    for (const tag of filteredTags) {
      if (!grouped[tag.category]) {
        grouped[tag.category] = [];
      }
      grouped[tag.category].push(tag);
    }
    return grouped;
  }, [filteredTags]);

  const toggleCategory = (category: string) => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(category)) {
      newExpanded.delete(category);
    } else {
      newExpanded.add(category);
    }
    setExpandedCategories(newExpanded);
  };

  const categoryDisplayNames: Record<string, string> = {
    framework: "Frameworks",
    language: "Languages",
    architecture: "Architecture",
    security: "Security",
    testing: "Testing",
    deployment: "Deployment",
    database: "Databases",
    api: "API",
    ui: "UI",
    documentation: "Documentation",
    general: "General",
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-gray-500 dark:text-gray-400">Loading tags...</div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Search */}
      <input
        type="text"
        placeholder="Search tags by name, description, or category..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className={cn(
          "w-full px-4 py-2 rounded-lg border",
          glassCard.blur.md,
          glassCard.transparency.medium,
          "border-gray-300/60 dark:border-gray-600/60",
          "focus:border-teal-400/70 focus:outline-none focus:ring-2 focus:ring-teal-400/20",
        )}
      />

      {filteredTags.length === 0 && (
        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
          <p className="text-lg">No tags found</p>
          {searchQuery && <p className="text-sm mt-2">Try adjusting your search query</p>}
        </div>
      )}

      {/* Tag Categories */}
      <div className="space-y-3">
        {Object.entries(groupedTags)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([category, tags]) => {
            const isExpanded = expandedCategories.has(category);
            const displayName = categoryDisplayNames[category] || category;

            return (
              <div
                key={category}
                className={cn("rounded-lg border", glassCard.blur.sm, glassCard.transparency.light)}
              >
                {/* Category Header */}
                <button
                  type="button"
                  className={[
                    "w-full flex items-center justify-between p-4",
                    "hover:bg-white/5 dark:hover:bg-black/5 transition-colors",
                  ].join(" ")}
                  onClick={() => toggleCategory(category)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      toggleCategory(category);
                    }
                  }}
                >
                  <div className="flex items-center gap-3">
                    <Tag className="w-5 h-5 text-teal-500" />
                    <h3 className="font-semibold text-gray-900 dark:text-white/90 uppercase text-sm tracking-wide">
                      {displayName}
                    </h3>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-500 dark:text-gray-400">{tags.length} tags</span>
                    {isExpanded ? (
                      <ChevronDown className="w-4 h-4 text-gray-500" />
                    ) : (
                      <ChevronRight className="w-4 h-4 text-gray-500" />
                    )}
                  </div>
                </button>

                {/* Category Tags */}
                {isExpanded && (
                  <div className="px-4 pb-4 space-y-3">
                    {tags
                      .sort((a, b) => a.tag_name.localeCompare(b.tag_name))
                      .map((tag) => (
                        <div
                          key={tag.id}
                          className={cn(
                            "p-3 rounded-md",
                            glassCard.blur.sm,
                            glassCard.transparency.medium,
                            "border border-gray-200/50 dark:border-gray-700/50",
                          )}
                        >
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <Badge
                                  variant="outline"
                                  className="font-mono text-xs"
                                  style={{
                                    borderColor: tag.color_hex || "#6366f1",
                                    color: tag.color_hex || "#6366f1",
                                  }}
                                >
                                  {tag.tag_name}
                                </Badge>
                                <span className="text-xs text-gray-500 dark:text-gray-400">
                                  {tag.usage_count} uses
                                </span>
                              </div>
                              <p className="text-sm text-gray-700 dark:text-gray-300 mb-1">{tag.description}</p>
                              {tag.usage_guidelines && (
                                <p className="text-xs text-gray-600 dark:text-gray-400 italic">
                                  Usage: {tag.usage_guidelines}
                                </p>
                              )}
                            </div>
                            {onTagClick && (
                              <button
                                type="button"
                                onClick={() => onTagClick(tag.tag_name)}
                                className={[
                                  "px-3 py-1 text-xs font-medium rounded-md",
                                  "bg-teal-500/10 text-teal-600 dark:text-teal-400",
                                  "hover:bg-teal-500/20 transition-colors",
                                ].join(" ")}
                              >
                                View Sources
                              </button>
                            )}
                          </div>
                        </div>
                      ))}
                  </div>
                )}
              </div>
            );
          })}
      </div>
    </div>
  );
};
