/**
 * Main Knowledge Base View Component
 * Orchestrates the knowledge base UI using vertical slice architecture
 */

import { useEffect, useRef, useState } from "react";
import { useToast } from "@/features/shared/hooks/useToast";
import { CrawlingProgress } from "../../progress/components/CrawlingProgress";
import type { ActiveOperation } from "../../progress/types";
import { useActiveOperations } from "../../progress/hooks";
import { AddKnowledgeDialog } from "../components/AddKnowledgeDialog";
import { KnowledgeHeader } from "../components/KnowledgeHeader";
import { KnowledgeTabs } from "../components/KnowledgeTabs";
import { KnowledgeInspector } from "../inspector/components/KnowledgeInspector";
import { useKnowledgeItem } from "../hooks/useKnowledgeQueries";
import type { KnowledgeItem } from "../types";

export const KnowledgeView = () => {
  // View state
  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");
  const [searchQuery, setSearchQuery] = useState("");
  const [typeFilter, setTypeFilter] = useState<"all" | "technical" | "business">("all");

  // Dialog state
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
  const [inspectorItem, setInspectorItem] = useState<KnowledgeItem | null>(null);
  const [inspectorInitialTab, setInspectorInitialTab] = useState<"documents" | "code">("documents");
  const [selectedSourceId, setSelectedSourceId] = useState<string | null>(null);

  // Fetch active operations for crawl tracking
  const { data: activeOperationsData, refetch: refetchOperations } = useActiveOperations(true);
  const activeOperations = activeOperationsData?.operations || [];
  const hasActiveOperations = activeOperations.length > 0;

  // Fetch the selected knowledge item when needed
  const { data: fetchedItem } = useKnowledgeItem(selectedSourceId);

  // Toast notifications
  const { showToast } = useToast();
  const previousOperations = useRef<ActiveOperation[]>([]);

  // Track crawl completions and errors for toast notifications
  useEffect(() => {
    // Find operations that just completed or failed
    const finishedOps = previousOperations.current.filter((prevOp) => {
      const currentOp = activeOperations.find((op) => op.operation_id === prevOp.operation_id);
      // Operation disappeared from active list - check its final status
      return (
        !currentOp &&
        ["crawling", "processing", "storing", "document_storage", "completed", "error", "failed"].includes(
          prevOp.status,
        )
      );
    });

    // Show toast for each finished operation
    finishedOps.forEach((op) => {
      // Check if it was an error or success
      if (op.status === "error" || op.status === "failed") {
        // Show error message with details
        const errorMessage = op.message || "Operation failed";
        showToast(`❌ ${errorMessage}`, "error", 7000);
      } else if (op.status === "completed") {
        // Show success message
        const message = op.message || "Operation completed";
        showToast(`✅ ${message}`, "success", 5000);
      }

      // Refetch operations after completion
      refetchOperations();
    });

    // Update previous operations
    previousOperations.current = [...activeOperations];
  }, [activeOperations, showToast, refetchOperations]);

  // When fetchedItem loads, set it as the inspector item
  useEffect(() => {
    if (fetchedItem) {
      setInspectorItem(fetchedItem);
      setSelectedSourceId(null);
    }
  }, [fetchedItem]);

  const handleAddKnowledge = () => {
    setIsAddDialogOpen(true);
  };

  const handleViewDocument = (sourceId: string) => {
    setInspectorInitialTab("documents");
    setSelectedSourceId(sourceId);
  };

  const handleViewCodeExamples = (sourceId: string) => {
    setInspectorInitialTab("code");
    setSelectedSourceId(sourceId);
  };

  const handleDeleteSuccess = () => {
    // TanStack Query will automatically refetch
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <KnowledgeHeader
        totalItems={0}
        isLoading={false}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        typeFilter={typeFilter}
        onTypeFilterChange={setTypeFilter}
        viewMode={viewMode}
        onViewModeChange={setViewMode}
        onAddKnowledge={handleAddKnowledge}
      />

      {/* Main Content */}
      <div className="flex-1 overflow-auto px-6 pb-6">
        {/* Active Operations - Show at top when present */}
        {hasActiveOperations && (
          <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white/90">Active Operations ({activeOperations.length})</h3>
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <div className="w-2 h-2 bg-teal-400 dark:bg-teal-400 rounded-full animate-pulse" />
                Live Updates
              </div>
            </div>
            <CrawlingProgress onSwitchToBrowse={() => {}} />
          </div>
        )}

        {/* Knowledge Tabs */}
        <KnowledgeTabs
          searchQuery={searchQuery}
          typeFilter={typeFilter}
          viewMode={viewMode}
          onViewDocument={handleViewDocument}
          onViewCodeExamples={handleViewCodeExamples}
          onDeleteSuccess={handleDeleteSuccess}
          onRefreshStarted={() => {
            refetchOperations();
          }}
        />
      </div>

      {/* Dialogs */}
      <AddKnowledgeDialog
        open={isAddDialogOpen}
        onOpenChange={setIsAddDialogOpen}
        onSuccess={() => {
          setIsAddDialogOpen(false);
          refetchOperations();
        }}
      />

      {/* Knowledge Inspector Modal */}
      {inspectorItem && (
        <KnowledgeInspector
          item={inspectorItem}
          open={!!inspectorItem}
          onOpenChange={(open) => {
            if (!open) setInspectorItem(null);
          }}
          initialTab={inspectorInitialTab}
        />
      )}
    </div>
  );
};
