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
    const response = await callAPIWithETag<{ success: boolean; tags: KnowledgeTag[]; count: number }>(endpoint);
    return response.tags;
  },

  /**
   * Get a specific tag by name
   */
  async getTagByName(tagName: string): Promise<KnowledgeTag> {
    const response = await callAPIWithETag<{ success: boolean; tag: KnowledgeTag }>(`${API_BASE}/${tagName}`);
    return response.tag;
  },

  /**
   * Get tags grouped by category
   */
  async getTagsByCategory(): Promise<Record<string, string[]>> {
    const response = await callAPIWithETag<{
      success: boolean;
      categories: Record<string, string[]>;
      category_counts: Record<string, number>;
      total_tags: number;
    }>(`${API_BASE}/categories/grouped`);
    return response.categories;
  },

  /**
   * Get suggested tags based on URL and content
   */
  async suggestTags(data: SuggestTagsRequest): Promise<string[]> {
    const response = await callAPIWithETag<{
      success: boolean;
      suggested_tags: string[];
      count: number;
      source: { url: string; title: string };
    }>(`${API_BASE}/suggest`, {
      method: "POST",
      body: JSON.stringify(data),
    });
    return response.suggested_tags;
  },
};
