/**
 * Add Knowledge Dialog Component
 * Modal for crawling URLs or uploading documents
 */

import { Globe, Loader2, Upload } from "lucide-react";
import { useId, useState } from "react";
import { useToast } from "@/features/shared/hooks/useToast";
import { Button, Input, Label } from "../../ui/primitives";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "../../ui/primitives/dialog";
import { RadioGroup, RadioGroupItem } from "../../ui/primitives/radio-group";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../ui/primitives/select";
import { cn, glassCard } from "../../ui/primitives/styles";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../../ui/primitives/tabs";
import { useProjects } from "../../projects/hooks/useProjectQueries";
import { useCrawlUrl, useUploadDocument } from "../hooks";
import { useProjectFolders } from "../hooks/useKnowledgeFolders";
import type { CrawlRequest, KnowledgeScope, UploadMetadata } from "../types";
import { KnowledgeTypeSelector } from "./KnowledgeTypeSelector";
import { LevelSelector } from "./LevelSelector";
import { TagInput } from "./TagInput";

interface AddKnowledgeDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess: () => void;
  onCrawlStarted?: (progressId: string) => void;
}

export const AddKnowledgeDialog: React.FC<AddKnowledgeDialogProps> = ({
  open,
  onOpenChange,
  onSuccess,
  onCrawlStarted,
}) => {
  const [activeTab, setActiveTab] = useState<"crawl" | "upload">("crawl");
  const { showToast } = useToast();
  const crawlMutation = useCrawlUrl();
  const uploadMutation = useUploadDocument();

  // Generate unique IDs for form elements
  const urlId = useId();
  const fileId = useId();

  // Crawl form state
  const [crawlUrl, setCrawlUrl] = useState("");
  const [crawlType, setCrawlType] = useState<"technical" | "business">("technical");
  const [maxDepth, setMaxDepth] = useState("2");
  const [tags, setTags] = useState<string[]>([]);
  const [crawlScope, setCrawlScope] = useState<KnowledgeScope>("global");
  const [crawlProjectId, setCrawlProjectId] = useState<string>("");
  const [crawlFolderId, setCrawlFolderId] = useState<string>("");

  // Upload form state
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadType, setUploadType] = useState<"technical" | "business">("technical");
  const [uploadTags, setUploadTags] = useState<string[]>([]);
  const [uploadScope, setUploadScope] = useState<KnowledgeScope>("global");
  const [uploadProjectId, setUploadProjectId] = useState<string>("");
  const [uploadFolderId, setUploadFolderId] = useState<string>("");

  // Fetch projects for scope selection
  const { data: projects } = useProjects();

  // Fetch folders for selected projects
  const { data: crawlFolders } = useProjectFolders(crawlScope === "project" ? crawlProjectId : undefined);
  const { data: uploadFolders } = useProjectFolders(uploadScope === "project" ? uploadProjectId : undefined);

  const resetForm = () => {
    setCrawlUrl("");
    setCrawlType("technical");
    setMaxDepth("2");
    setTags([]);
    setCrawlScope("global");
    setCrawlProjectId("");
    setCrawlFolderId("");
    setSelectedFile(null);
    setUploadType("technical");
    setUploadTags([]);
    setUploadScope("global");
    setUploadProjectId("");
    setUploadFolderId("");
  };

  const handleCrawl = async () => {
    if (!crawlUrl) {
      showToast("Please enter a URL to crawl", "error");
      return;
    }

    try {
      const request: CrawlRequest = {
        url: crawlUrl,
        knowledge_type: crawlType,
        max_depth: parseInt(maxDepth, 10),
        tags: tags.length > 0 ? tags : undefined,
        scope: crawlScope,
        project_id: crawlScope === "project" ? crawlProjectId : undefined,
        folder_id: crawlFolderId || undefined,
      };

      const response = await crawlMutation.mutateAsync(request);

      // Notify parent about the new crawl operation
      if (response?.progressId && onCrawlStarted) {
        onCrawlStarted(response.progressId);
      }

      showToast("Crawl started successfully", "success");
      resetForm();
      onSuccess();
      onOpenChange(false);
    } catch (error) {
      // Display the actual error message from backend
      const message = error instanceof Error ? error.message : "Failed to start crawl";
      showToast(message, "error");
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      showToast("Please select a file to upload", "error");
      return;
    }

    try {
      const metadata: UploadMetadata = {
        knowledge_type: uploadType,
        tags: uploadTags.length > 0 ? uploadTags : undefined,
        scope: uploadScope,
        project_id: uploadScope === "project" ? uploadProjectId : undefined,
        folder_id: uploadFolderId || undefined,
      };

      const response = await uploadMutation.mutateAsync({ file: selectedFile, metadata });

      // Notify parent about the new upload operation if it has a progressId
      if (response?.progressId && onCrawlStarted) {
        onCrawlStarted(response.progressId);
      }

      // Upload happens in background - show appropriate message
      showToast(`Upload started for ${selectedFile.name}. Processing in background...`, "info");
      resetForm();
      // Don't call onSuccess here - the upload hasn't actually succeeded yet
      // onSuccess should be called when polling shows completion
      onOpenChange(false);
    } catch (error) {
      // Display the actual error message from backend
      const message = error instanceof Error ? error.message : "Failed to upload document";
      showToast(message, "error");
    }
  };

  const isProcessing = crawlMutation.isPending || uploadMutation.isPending;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Add Knowledge</DialogTitle>
          <DialogDescription>Crawl websites or upload documents to expand your knowledge base.</DialogDescription>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as "crawl" | "upload")}>
          <div className="flex justify-center">
            <TabsList>
              <TabsTrigger value="crawl" color="blue">
                <Globe className="w-4 h-4 mr-2" />
                Crawl Website
              </TabsTrigger>
              <TabsTrigger value="upload" color="purple">
                <Upload className="w-4 h-4 mr-2" />
                Upload Document
              </TabsTrigger>
            </TabsList>
          </div>

          {/* Crawl Tab */}
          <TabsContent value="crawl" className="space-y-6 mt-6">
            {/* Scope Selection */}
            <div className="space-y-3">
              <Label className="text-sm font-medium text-gray-900 dark:text-white/90">Scope</Label>
              <RadioGroup value={crawlScope} onValueChange={(v) => setCrawlScope(v as KnowledgeScope)}>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="global" id="crawl-global" />
                  <Label htmlFor="crawl-global" className="font-normal cursor-pointer">
                    Global (shared across all work)
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="project" id="crawl-project" />
                  <Label htmlFor="crawl-project" className="font-normal cursor-pointer">
                    Project-Specific
                  </Label>
                </div>
              </RadioGroup>
            </div>

            {/* Project and Folder Selection (only when project scope) */}
            {crawlScope === "project" && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="crawl-project-select">Project</Label>
                  <Select value={crawlProjectId} onValueChange={setCrawlProjectId}>
                    <SelectTrigger id="crawl-project-select">
                      <SelectValue placeholder="Select a project..." />
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

                {crawlProjectId && crawlFolders && crawlFolders.length > 0 && (
                  <div className="space-y-2">
                    <Label htmlFor="crawl-folder-select">Folder (optional)</Label>
                    <Select value={crawlFolderId} onValueChange={setCrawlFolderId}>
                      <SelectTrigger id="crawl-folder-select">
                        <SelectValue placeholder="No folder (unfiled)" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">No folder</SelectItem>
                        {crawlFolders.map((folder) => (
                          <SelectItem key={folder.id} value={folder.id}>
                            {folder.folder_name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}
              </div>
            )}

            {/* Enhanced URL Input Section */}
            <div className="space-y-3">
              <Label htmlFor={urlId} className="text-sm font-medium text-gray-900 dark:text-white/90">
                Website URL
              </Label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Globe className="h-5 w-5" style={{ color: "#0891b2" }} />
                </div>
                <Input
                  id={urlId}
                  type="url"
                  placeholder="https://docs.example.com or https://github.com/..."
                  value={crawlUrl}
                  onChange={(e) => setCrawlUrl(e.target.value)}
                  disabled={isProcessing}
                  className={cn(
                    "pl-10 h-12",
                    glassCard.blur.md,
                    glassCard.transparency.medium,
                    "border-gray-300/60 dark:border-gray-600/60 focus:border-cyan-400/70",
                  )}
                />
              </div>
            </div>

            <div className="space-y-6">
              <KnowledgeTypeSelector value={crawlType} onValueChange={setCrawlType} disabled={isProcessing} />

              <LevelSelector value={maxDepth} onValueChange={setMaxDepth} disabled={isProcessing} />
            </div>

            <TagInput
              tags={tags}
              onTagsChange={setTags}
              disabled={isProcessing}
              placeholder="Add tags like 'api', 'documentation', 'guide'..."
            />

            <Button
              onClick={handleCrawl}
              disabled={isProcessing || !crawlUrl}
              className={[
                "w-full bg-gradient-to-r from-cyan-500 to-cyan-600",
                "hover:from-cyan-600 hover:to-cyan-700",
                "backdrop-blur-md border border-cyan-400/50",
                "shadow-[0_0_20px_rgba(6,182,212,0.25)] hover:shadow-[0_0_30px_rgba(6,182,212,0.35)]",
                "transition-all duration-200",
              ].join(" ")}
            >
              {crawlMutation.isPending ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Starting Crawl...
                </>
              ) : (
                <>
                  <Globe className="w-4 h-4 mr-2" />
                  Start Crawling
                </>
              )}
            </Button>
          </TabsContent>

          {/* Upload Tab */}
          <TabsContent value="upload" className="space-y-6 mt-6">
            {/* Scope Selection */}
            <div className="space-y-3">
              <Label className="text-sm font-medium text-gray-900 dark:text-white/90">Scope</Label>
              <RadioGroup value={uploadScope} onValueChange={(v) => setUploadScope(v as KnowledgeScope)}>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="global" id="upload-global" />
                  <Label htmlFor="upload-global" className="font-normal cursor-pointer">
                    Global (shared across all work)
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="project" id="upload-project" />
                  <Label htmlFor="upload-project" className="font-normal cursor-pointer">
                    Project-Specific
                  </Label>
                </div>
              </RadioGroup>
            </div>

            {/* Project and Folder Selection (only when project scope) */}
            {uploadScope === "project" && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="upload-project-select">Project</Label>
                  <Select value={uploadProjectId} onValueChange={setUploadProjectId}>
                    <SelectTrigger id="upload-project-select">
                      <SelectValue placeholder="Select a project..." />
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

                {uploadProjectId && uploadFolders && uploadFolders.length > 0 && (
                  <div className="space-y-2">
                    <Label htmlFor="upload-folder-select">Folder (optional)</Label>
                    <Select value={uploadFolderId} onValueChange={setUploadFolderId}>
                      <SelectTrigger id="upload-folder-select">
                        <SelectValue placeholder="No folder (unfiled)" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">No folder</SelectItem>
                        {uploadFolders.map((folder) => (
                          <SelectItem key={folder.id} value={folder.id}>
                            {folder.folder_name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}
              </div>
            )}

            {/* Enhanced File Input Section */}
            <div className="space-y-3">
              <Label htmlFor={fileId} className="text-sm font-medium text-gray-900 dark:text-white/90">
                Document File
              </Label>

              {/* Custom File Upload Area */}
              <div className="relative">
                <input
                  id={fileId}
                  type="file"
                  accept=".txt,.md,.pdf,.doc,.docx,.html,.htm"
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                  disabled={isProcessing}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed z-10"
                />
                <div
                  className={cn(
                    "relative h-20 rounded-xl border-2 border-dashed transition-all duration-200",
                    "flex flex-col items-center justify-center gap-2 text-center p-4",
                    glassCard.blur.md,
                    selectedFile ? glassCard.tints.purple.light : glassCard.transparency.medium,
                    selectedFile ? "border-purple-400/70" : "border-gray-300/60 dark:border-gray-600/60",
                    !selectedFile && "hover:border-purple-400/50",
                    isProcessing && "opacity-50 cursor-not-allowed",
                  )}
                >
                  <Upload
                    className={cn("w-6 h-6", selectedFile ? "text-purple-500" : "text-gray-400 dark:text-gray-500")}
                  />
                  <div className="text-sm">
                    {selectedFile ? (
                      <div className="space-y-1">
                        <p className="font-medium text-purple-700 dark:text-purple-400">{selectedFile.name}</p>
                        <p className="text-xs text-purple-600 dark:text-purple-400">
                          {Math.round(selectedFile.size / 1024)} KB
                        </p>
                      </div>
                    ) : (
                      <div className="space-y-1">
                        <p className="font-medium text-gray-700 dark:text-gray-300">Click to browse or drag & drop</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          PDF, DOC, DOCX, TXT, MD files supported
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            <KnowledgeTypeSelector value={uploadType} onValueChange={setUploadType} disabled={isProcessing} />

            <TagInput
              tags={uploadTags}
              onTagsChange={setUploadTags}
              disabled={isProcessing}
              placeholder="Add tags like 'manual', 'reference', 'guide'..."
            />

            <Button
              onClick={handleUpload}
              disabled={isProcessing || !selectedFile}
              className={[
                "w-full bg-gradient-to-r from-purple-500 to-purple-600",
                "hover:from-purple-600 hover:to-purple-700",
                "backdrop-blur-md border border-purple-400/50",
                "shadow-[0_0_20px_rgba(147,51,234,0.25)] hover:shadow-[0_0_30px_rgba(147,51,234,0.35)]",
                "transition-all duration-200",
              ].join(" ")}
            >
              {uploadMutation.isPending ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4 mr-2" />
                  Upload Document
                </>
              )}
            </Button>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
};
