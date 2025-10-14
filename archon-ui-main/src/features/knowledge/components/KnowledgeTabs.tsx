/**
 * Knowledge Tabs Component
 * Main tab navigation for Global / Projects / Tags views
 */

import { useState } from "react";
import { Globe, FolderTree, Tags } from "lucide-react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "../../ui/primitives/tabs";
import { GlobalKnowledgeView } from "./GlobalKnowledgeView";
import { ProjectKnowledgeView } from "./ProjectKnowledgeView";
import { TagsIndexView } from "./TagsIndexView";
import type { KnowledgeItem } from "../types";

interface KnowledgeTabsProps {
  searchQuery?: string;
  typeFilter?: "all" | "technical" | "business";
  viewMode: "grid" | "table";
  onViewDocument: (sourceId: string) => void;
  onViewCodeExamples: (sourceId: string) => void;
  onDeleteSuccess: () => void;
  onRefreshStarted: (progressId: string) => void;
}

export const KnowledgeTabs: React.FC<KnowledgeTabsProps> = ({
  searchQuery,
  typeFilter,
  viewMode,
  onViewDocument,
  onViewCodeExamples,
  onDeleteSuccess,
  onRefreshStarted,
}) => {
  const [activeTab, setActiveTab] = useState("global");

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
      <div className="flex justify-center mb-6">
        <TabsList className="grid w-auto grid-cols-3">
          <TabsTrigger value="global" color="cyan">
            <Globe className="w-4 h-4 mr-2" aria-hidden="true" />
            Global
          </TabsTrigger>
          <TabsTrigger value="projects" color="purple">
            <FolderTree className="w-4 h-4 mr-2" aria-hidden="true" />
            Projects
          </TabsTrigger>
          <TabsTrigger value="tags" color="blue">
            <Tags className="w-4 h-4 mr-2" aria-hidden="true" />
            Tags
          </TabsTrigger>
        </TabsList>
      </div>

      <TabsContent value="global" className="mt-0">
        <GlobalKnowledgeView
          searchQuery={searchQuery}
          typeFilter={typeFilter}
          viewMode={viewMode}
          onViewDocument={onViewDocument}
          onViewCodeExamples={onViewCodeExamples}
          onDeleteSuccess={onDeleteSuccess}
          onRefreshStarted={onRefreshStarted}
        />
      </TabsContent>

      <TabsContent value="projects" className="mt-0">
        <ProjectKnowledgeView
          searchQuery={searchQuery}
          typeFilter={typeFilter}
          viewMode={viewMode}
          onViewDocument={onViewDocument}
          onViewCodeExamples={onViewCodeExamples}
          onDeleteSuccess={onDeleteSuccess}
          onRefreshStarted={onRefreshStarted}
        />
      </TabsContent>

      <TabsContent value="tags" className="mt-0">
        <TagsIndexView />
      </TabsContent>
    </Tabs>
  );
};
