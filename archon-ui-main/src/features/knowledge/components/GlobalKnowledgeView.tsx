/**
 * Global Knowledge View Component
 * Displays only global (shared) knowledge sources
 */

import { useMemo } from "react";
import { KnowledgeList } from "./KnowledgeList";
import { useKnowledgeSummaries } from "../hooks/useKnowledgeQueries";
import type { KnowledgeItemsFilter } from "../types";

interface GlobalKnowledgeViewProps {
  searchQuery?: string;
  typeFilter?: "all" | "technical" | "business";
  viewMode: "grid" | "table";
  onViewDocument: (sourceId: string) => void;
  onViewCodeExamples: (sourceId: string) => void;
  onDeleteSuccess: () => void;
  onRefreshStarted: (progressId: string) => void;
}

export const GlobalKnowledgeView: React.FC<GlobalKnowledgeViewProps> = ({
  searchQuery,
  typeFilter,
  viewMode,
  onViewDocument,
  onViewCodeExamples,
  onDeleteSuccess,
  onRefreshStarted,
}) => {
  // Build filter for global scope
  const filter = useMemo<KnowledgeItemsFilter>(() => {
    const f: KnowledgeItemsFilter = {
      page: 1,
      per_page: 100,
      scope: "global",
    };

    if (searchQuery) {
      f.search = searchQuery;
    }

    if (typeFilter && typeFilter !== "all") {
      f.knowledge_type = typeFilter;
    }

    return f;
  }, [searchQuery, typeFilter]);

  // Fetch global knowledge
  const { data, isLoading, error, refetch, activeOperations } = useKnowledgeSummaries(filter);

  const knowledgeItems = data?.items || [];

  return (
    <div className="space-y-4">
      {knowledgeItems.length === 0 && !isLoading && (
        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
          <p className="text-lg">No global knowledge sources found</p>
          <p className="text-sm mt-2">Add websites or documents that can be shared across all projects</p>
        </div>
      )}

      <KnowledgeList
        items={knowledgeItems}
        viewMode={viewMode}
        isLoading={isLoading}
        error={error}
        onRetry={refetch}
        onViewDocument={onViewDocument}
        onViewCodeExamples={onViewCodeExamples}
        onDeleteSuccess={onDeleteSuccess}
        activeOperations={activeOperations}
        onRefreshStarted={onRefreshStarted}
      />
    </div>
  );
};
