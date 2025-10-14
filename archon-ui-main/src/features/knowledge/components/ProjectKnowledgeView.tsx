/**
 * Project Knowledge View Component
 * Displays project-specific knowledge with folder organization
 */

import { useMemo, useState } from "react";
import { Folder, FolderOpen, ChevronRight, ChevronDown } from "lucide-react";
import { useProjects } from "../../projects/hooks/useProjectQueries";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../ui/primitives/select";
import { cn, glassCard } from "../../ui/primitives/styles";
import { useProjectFolders } from "../hooks/useKnowledgeFolders";
import { useKnowledgeSummaries } from "../hooks/useKnowledgeQueries";
import { KnowledgeList } from "./KnowledgeList";
import type { KnowledgeItemsFilter } from "../types";

interface ProjectKnowledgeViewProps {
  searchQuery?: string;
  typeFilter?: "all" | "technical" | "business";
  viewMode: "grid" | "table";
  onViewDocument: (sourceId: string) => void;
  onViewCodeExamples: (sourceId: string) => void;
  onDeleteSuccess: () => void;
  onRefreshStarted: (progressId: string) => void;
}

export const ProjectKnowledgeView: React.FC<ProjectKnowledgeViewProps> = ({
  searchQuery,
  typeFilter,
  viewMode,
  onViewDocument,
  onViewCodeExamples,
  onDeleteSuccess,
  onRefreshStarted,
}) => {
  const [selectedProjectId, setSelectedProjectId] = useState<string | undefined>(undefined);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());

  // Fetch projects
  const { data: projects } = useProjects();

  // Fetch folders for selected project
  const { data: folders } = useProjectFolders(selectedProjectId);

  // Build filter for project scope
  const filter = useMemo<KnowledgeItemsFilter>(() => {
    const f: KnowledgeItemsFilter = {
      page: 1,
      per_page: 100,
      scope: "project",
      project_id: selectedProjectId,
    };

    if (searchQuery) {
      f.search = searchQuery;
    }

    if (typeFilter && typeFilter !== "all") {
      f.knowledge_type = typeFilter;
    }

    return f;
  }, [searchQuery, typeFilter, selectedProjectId]);

  // Fetch project knowledge
  const { data, isLoading, error, refetch, activeOperations } = useKnowledgeSummaries(filter);

  const knowledgeItems = data?.items || [];

  // Group items by folder
  const itemsByFolder = useMemo(() => {
    const grouped: Record<string, typeof knowledgeItems> = {
      unfiled: [],
    };

    for (const item of knowledgeItems) {
      const folderId = item.folder_id || "unfiled";
      if (!grouped[folderId]) {
        grouped[folderId] = [];
      }
      grouped[folderId].push(item);
    }

    return grouped;
  }, [knowledgeItems]);

  const toggleFolder = (folderId: string) => {
    const newExpanded = new Set(expandedFolders);
    if (newExpanded.has(folderId)) {
      newExpanded.delete(folderId);
    } else {
      newExpanded.add(folderId);
    }
    setExpandedFolders(newExpanded);
  };

  return (
    <div className="space-y-4">
      {/* Project Selector */}
      <div className="flex items-center gap-4">
        <label htmlFor="project-select" className="text-sm font-medium text-gray-900 dark:text-white/90">
          Select Project:
        </label>
        <Select value={selectedProjectId} onValueChange={setSelectedProjectId}>
          <SelectTrigger id="project-select" className="w-64">
            <SelectValue placeholder="Choose a project..." />
          </SelectTrigger>
          <SelectContent>
            {projects?.map((project) => (
              <SelectItem key={project.id} value={project.id}>
                {project.title}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {!selectedProjectId && (
        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
          <p className="text-lg">Select a project to view its knowledge sources</p>
        </div>
      )}

      {selectedProjectId && knowledgeItems.length === 0 && !isLoading && (
        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
          <p className="text-lg">No knowledge sources for this project</p>
          <p className="text-sm mt-2">Add project-specific documentation and resources</p>
        </div>
      )}

      {selectedProjectId && (folders?.length || 0) > 0 && (
        <div className="space-y-4">
          {/* Render folders */}
          {folders?.map((folder) => {
            const folderItems = itemsByFolder[folder.id] || [];
            const isExpanded = expandedFolders.has(folder.id);

            return (
              <div
                key={folder.id}
                className={cn("rounded-lg border", glassCard.blur.sm, glassCard.transparency.light)}
                style={{ borderColor: folder.color_hex || "#6366f1" }}
              >
                {/* Folder Header */}
                <button
                  type="button"
                  className={[
                    "w-full flex items-center justify-between p-4",
                    "hover:bg-white/5 dark:hover:bg-black/5 transition-colors",
                  ].join(" ")}
                  onClick={() => toggleFolder(folder.id)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      toggleFolder(folder.id);
                    }
                  }}
                >
                  <div className="flex items-center gap-3">
                    {isExpanded ? (
                      <FolderOpen
                        className="w-5 h-5 text-[var(--folder-color)]"
                        style={{ "--folder-color": folder.color_hex } as React.CSSProperties}
                      />
                    ) : (
                      <Folder
                        className="w-5 h-5 text-[var(--folder-color)]"
                        style={{ "--folder-color": folder.color_hex } as React.CSSProperties}
                      />
                    )}
                    <div className="text-left">
                      <h3 className="font-semibold text-gray-900 dark:text-white/90">{folder.folder_name}</h3>
                      {folder.description && (
                        <p className="text-sm text-gray-600 dark:text-gray-400">{folder.description}</p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-500 dark:text-gray-400">{folderItems.length} items</span>
                    {isExpanded ? (
                      <ChevronDown className="w-4 h-4 text-gray-500" />
                    ) : (
                      <ChevronRight className="w-4 h-4 text-gray-500" />
                    )}
                  </div>
                </button>

                {/* Folder Content */}
                {isExpanded && folderItems.length > 0 && (
                  <div className="px-4 pb-4">
                    <KnowledgeList
                      items={folderItems}
                      viewMode={viewMode}
                      isLoading={false}
                      error={null}
                      onRetry={refetch}
                      onViewDocument={onViewDocument}
                      onViewCodeExamples={onViewCodeExamples}
                      onDeleteSuccess={onDeleteSuccess}
                      activeOperations={activeOperations}
                      onRefreshStarted={onRefreshStarted}
                    />
                  </div>
                )}
              </div>
            );
          })}

          {/* Unfiled items */}
          {itemsByFolder.unfiled && itemsByFolder.unfiled.length > 0 && (
            <div className={cn("rounded-lg border p-4", glassCard.blur.sm, glassCard.transparency.light)}>
              <h3 className="font-semibold text-gray-900 dark:text-white/90 mb-4">Unfiled Items</h3>
              <KnowledgeList
                items={itemsByFolder.unfiled}
                viewMode={viewMode}
                isLoading={false}
                error={null}
                onRetry={refetch}
                onViewDocument={onViewDocument}
                onViewCodeExamples={onViewCodeExamples}
                onDeleteSuccess={onDeleteSuccess}
                activeOperations={activeOperations}
                onRefreshStarted={onRefreshStarted}
              />
            </div>
          )}
        </div>
      )}

      {selectedProjectId && (folders?.length || 0) === 0 && knowledgeItems.length > 0 && (
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
      )}
    </div>
  );
};
