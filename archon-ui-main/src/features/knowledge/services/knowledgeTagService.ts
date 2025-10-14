/**
 * Knowledge Tag Service
 * Handles tag management API operations
 */

import { callAPIWithETag } from "../../shared/api/apiClient";
import type { KnowledgeTag, SuggestTagsRequest } from "../types";

const API_BASE = "/api/knowledge/tags";

export const knowledgeTagService = {
  /**
   * Get all tags with optional category filter
   */
  async getAllTags(category?: string): Promise<KnowledgeTag[]> {
    const params = new URLSearchParams();
    if (category) {
      params.append("category", category);
    }
    const queryString = params.toString();
    const endpoint = `${API_BASE}${queryString ? `?${queryString}` : ""}`;
    return callAPIWithETag<KnowledgeTag[]>(endpoint);
  },

  /**
   * Get a specific tag by name
   */
  async getTagByName(tagName: string): Promise<KnowledgeTag> {
    return callAPIWithETag<KnowledgeTag>(`${API_BASE}/${tagName}`);
  },

  /**
   * Get tags grouped by category
   */
  async getTagsByCategory(): Promise<Record<string, string[]>> {
    return callAPIWithETag<Record<string, string[]>>(`${API_BASE}/categories/grouped`);
  },

  /**
   * Get suggested tags based on URL and content
   */
  async suggestTags(data: SuggestTagsRequest): Promise<string[]> {
    return callAPIWithETag<string[]>(`${API_BASE}/suggest`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
};
