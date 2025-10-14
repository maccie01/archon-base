/**
 * Knowledge Tag Query Hooks
 * Handles tag-related queries
 */

import { useQuery } from "@tanstack/react-query";
import { DISABLED_QUERY_KEY, STALE_TIMES } from "../../shared/config/queryPatterns";
import { knowledgeTagService } from "../services/knowledgeTagService";
import type { KnowledgeTag, SuggestTagsRequest } from "../types";

// Query keys factory for tags
export const tagKeys = {
  all: ["knowledge-tags"] as const,
  byCategory: () => [...tagKeys.all, "by-category"] as const,
  detail: (tagName: string) => [...tagKeys.all, "detail", tagName] as const,
  suggest: (params: SuggestTagsRequest) => [...tagKeys.all, "suggest", params] as const,
};

/**
 * Fetch all tags with optional category filter
 */
export function useKnowledgeTags(category?: string) {
  return useQuery<KnowledgeTag[]>({
    queryKey: category ? ([...tagKeys.all, category] as const) : tagKeys.all,
    queryFn: () => knowledgeTagService.getAllTags(category),
    staleTime: STALE_TIMES.rare, // Tags change infrequently
  });
}

/**
 * Fetch a specific tag by name
 */
export function useKnowledgeTag(tagName: string | undefined) {
  return useQuery<KnowledgeTag>({
    queryKey: tagName ? tagKeys.detail(tagName) : DISABLED_QUERY_KEY,
    queryFn: () => (tagName ? knowledgeTagService.getTagByName(tagName) : Promise.reject("No tag name provided")),
    enabled: !!tagName,
    staleTime: STALE_TIMES.rare,
  });
}

/**
 * Fetch tags grouped by category
 */
export function useTagsByCategory() {
  return useQuery<Record<string, string[]>>({
    queryKey: tagKeys.byCategory(),
    queryFn: () => knowledgeTagService.getTagsByCategory(),
    staleTime: STALE_TIMES.rare,
  });
}

/**
 * Get suggested tags based on URL and content
 */
export function useSuggestTags(params: SuggestTagsRequest | undefined, enabled = false) {
  return useQuery<string[]>({
    queryKey: params ? tagKeys.suggest(params) : DISABLED_QUERY_KEY,
    queryFn: () => (params ? knowledgeTagService.suggestTags(params) : Promise.reject("No params provided")),
    enabled: enabled && !!params,
    staleTime: STALE_TIMES.static, // Suggestions for the same URL shouldn't change
  });
}
