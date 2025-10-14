/**
 * Knowledge Folder Query Hooks
 * Handles folder-related queries and mutations
 */

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useToast } from "@/features/shared/hooks/useToast";
import { DISABLED_QUERY_KEY, STALE_TIMES } from "../../shared/config/queryPatterns";
import { knowledgeFolderService } from "../services/knowledgeFolderService";
import type { CreateFolderRequest, KnowledgeFolder, UpdateFolderRequest } from "../types";
import { knowledgeKeys } from "./useKnowledgeQueries";

// Query keys factory for folders
export const folderKeys = {
  all: ["knowledge-folders"] as const,
  byProject: (projectId: string) => [...folderKeys.all, "project", projectId] as const,
  detail: (folderId: string) => [...folderKeys.all, "detail", folderId] as const,
};

/**
 * Fetch folders for a project
 */
export function useProjectFolders(projectId: string | undefined) {
  return useQuery<KnowledgeFolder[]>({
    queryKey: projectId ? folderKeys.byProject(projectId) : DISABLED_QUERY_KEY,
    queryFn: () =>
      projectId ? knowledgeFolderService.listProjectFolders(projectId) : Promise.reject("No project ID provided"),
    enabled: !!projectId,
    staleTime: STALE_TIMES.normal,
  });
}

/**
 * Fetch a specific folder
 */
export function useFolder(folderId: string | undefined) {
  return useQuery<KnowledgeFolder>({
    queryKey: folderId ? folderKeys.detail(folderId) : DISABLED_QUERY_KEY,
    queryFn: () => (folderId ? knowledgeFolderService.getFolder(folderId) : Promise.reject("No folder ID provided")),
    enabled: !!folderId,
    staleTime: STALE_TIMES.normal,
  });
}

/**
 * Create folder mutation
 */
export function useCreateFolder() {
  const queryClient = useQueryClient();
  const { showToast } = useToast();

  return useMutation({
    mutationFn: (data: CreateFolderRequest) => knowledgeFolderService.createFolder(data),
    onSuccess: (folder) => {
      // Invalidate the project's folder list
      queryClient.invalidateQueries({ queryKey: folderKeys.byProject(folder.project_id) });
      showToast(`Folder "${folder.folder_name}" created successfully`, "success");
    },
    onError: (error) => {
      const errorMessage = error instanceof Error ? error.message : "Failed to create folder";
      showToast(errorMessage, "error");
    },
  });
}

/**
 * Update folder mutation
 */
export function useUpdateFolder() {
  const queryClient = useQueryClient();
  const { showToast } = useToast();

  return useMutation({
    mutationFn: ({ folderId, data }: { folderId: string; data: UpdateFolderRequest }) =>
      knowledgeFolderService.updateFolder(folderId, data),
    onSuccess: (folder) => {
      // Invalidate both the specific folder and the project's folder list
      queryClient.invalidateQueries({ queryKey: folderKeys.detail(folder.id) });
      queryClient.invalidateQueries({ queryKey: folderKeys.byProject(folder.project_id) });
      showToast("Folder updated successfully", "success");
    },
    onError: (error) => {
      const errorMessage = error instanceof Error ? error.message : "Failed to update folder";
      showToast(errorMessage, "error");
    },
  });
}

/**
 * Delete folder mutation
 */
export function useDeleteFolder() {
  const queryClient = useQueryClient();
  const { showToast } = useToast();

  return useMutation({
    mutationFn: (folderId: string) => knowledgeFolderService.deleteFolder(folderId),
    onSuccess: (_data, folderId) => {
      // Invalidate all folder queries and knowledge summaries
      queryClient.invalidateQueries({ queryKey: folderKeys.all });
      queryClient.invalidateQueries({ queryKey: knowledgeKeys.summariesPrefix() });
      showToast("Folder deleted successfully. Sources were preserved.", "success");
    },
    onError: (error) => {
      const errorMessage = error instanceof Error ? error.message : "Failed to delete folder";
      showToast(errorMessage, "error");
    },
  });
}
