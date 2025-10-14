/**
 * Knowledge Folder Service
 * Handles folder organization API operations
 */

import { callAPIWithETag } from "../../shared/api/apiClient";
import type { CreateFolderRequest, KnowledgeFolder, UpdateFolderRequest } from "../types";

const API_BASE = "/api/knowledge/folders";

export const knowledgeFolderService = {
  /**
   * List all folders for a project
   */
  async listProjectFolders(projectId: string): Promise<KnowledgeFolder[]> {
    return callAPIWithETag<KnowledgeFolder[]>(`${API_BASE}/projects/${projectId}/list`);
  },

  /**
   * Get a specific folder
   */
  async getFolder(folderId: string): Promise<KnowledgeFolder> {
    return callAPIWithETag<KnowledgeFolder>(`${API_BASE}/${folderId}`);
  },

  /**
   * Create a new folder
   */
  async createFolder(data: CreateFolderRequest): Promise<KnowledgeFolder> {
    return callAPIWithETag<KnowledgeFolder>(API_BASE, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  /**
   * Update a folder
   */
  async updateFolder(folderId: string, data: UpdateFolderRequest): Promise<KnowledgeFolder> {
    return callAPIWithETag<KnowledgeFolder>(`${API_BASE}/${folderId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a folder (unlinks sources but doesn't delete them)
   */
  async deleteFolder(folderId: string): Promise<{ success: boolean; message: string }> {
    return callAPIWithETag<{ success: boolean; message: string }>(`${API_BASE}/${folderId}`, {
      method: "DELETE",
    });
  },
};
