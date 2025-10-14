/**
 * Unit tests for useKnowledgeFolders hooks
 *
 * Tests query hooks for folder operations.
 *
 * Created: 2025-10-14
 */

import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useProjectFolders, useCreateFolder, useUpdateFolder, useDeleteFolder } from "../useKnowledgeFolders";
import { knowledgeFolderService } from "../../services/knowledgeFolderService";

vi.mock("../../services/knowledgeFolderService", () => ({
  knowledgeFolderService: {
    listProjectFolders: vi.fn(),
    getFolder: vi.fn(),
    createFolder: vi.fn(),
    updateFolder: vi.fn(),
    deleteFolder: vi.fn(),
  },
}));

vi.mock("@/features/shared/config/queryPatterns", () => ({
  DISABLED_QUERY_KEY: ["disabled"],
  STALE_TIMES: {
    instant: 0,
    realtime: 3_000,
    frequent: 5_000,
    normal: 30_000,
    rare: 300_000,
    static: Infinity,
  },
}));

vi.mock("@/features/shared/hooks/useToast", () => ({
  useToast: () => ({
    showToast: vi.fn(),
  }),
}));

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });
}

function createWrapper(queryClient: QueryClient) {
  return ({ children }: { children: React.ReactNode }) =>
    React.createElement(QueryClientProvider, { client: queryClient }, children);
}

describe("useProjectFolders", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should fetch folders for a project", async () => {
    const mockFolders = [
      {
        id: "folder-1",
        project_id: "project-1",
        folder_name: "Authentication",
        description: "Auth docs",
        color_hex: "#6366f1",
        icon_name: "lock",
        sort_order: 0,
        created_at: "2025-10-14T00:00:00Z",
        updated_at: "2025-10-14T00:00:00Z",
      },
    ];

    vi.mocked(knowledgeFolderService.listProjectFolders).mockResolvedValue(mockFolders);

    const queryClient = createTestQueryClient();
    const { result } = renderHook(() => useProjectFolders("project-1"), {
      wrapper: createWrapper(queryClient),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual(mockFolders);
    expect(knowledgeFolderService.listProjectFolders).toHaveBeenCalledWith("project-1");
  });

  it("should not fetch when project_id is undefined", () => {
    const queryClient = createTestQueryClient();
    const { result } = renderHook(() => useProjectFolders(undefined), {
      wrapper: createWrapper(queryClient),
    });

    expect(result.current.data).toBeUndefined();
    expect(result.current.fetchStatus).toBe("idle");
    expect(knowledgeFolderService.listProjectFolders).not.toHaveBeenCalled();
  });

  it("should handle errors", async () => {
    vi.mocked(knowledgeFolderService.listProjectFolders).mockRejectedValue(
      new Error("Failed to fetch folders")
    );

    const queryClient = createTestQueryClient();
    const { result } = renderHook(() => useProjectFolders("project-1"), {
      wrapper: createWrapper(queryClient),
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error).toBeDefined();
  });
});

describe("useCreateFolder", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should create a folder", async () => {
    const newFolder = {
      id: "folder-1",
      project_id: "project-1",
      folder_name: "Authentication",
      description: "Auth docs",
      color_hex: "#6366f1",
      icon_name: "lock",
      sort_order: 0,
      created_at: "2025-10-14T00:00:00Z",
      updated_at: "2025-10-14T00:00:00Z",
    };

    vi.mocked(knowledgeFolderService.createFolder).mockResolvedValue(newFolder);

    const queryClient = createTestQueryClient();
    const { result } = renderHook(() => useCreateFolder(), {
      wrapper: createWrapper(queryClient),
    });

    result.current.mutate({
      project_id: "project-1",
      folder_name: "Authentication",
      description: "Auth docs",
      color_hex: "#6366f1",
      icon_name: "lock",
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual(newFolder);
    expect(knowledgeFolderService.createFolder).toHaveBeenCalledWith({
      project_id: "project-1",
      folder_name: "Authentication",
      description: "Auth docs",
      color_hex: "#6366f1",
      icon_name: "lock",
    });
  });

  it("should handle creation errors", async () => {
    vi.mocked(knowledgeFolderService.createFolder).mockRejectedValue(
      new Error("Failed to create folder")
    );

    const queryClient = createTestQueryClient();
    const { result } = renderHook(() => useCreateFolder(), {
      wrapper: createWrapper(queryClient),
    });

    result.current.mutate({
      project_id: "project-1",
      folder_name: "Authentication",
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error).toBeDefined();
  });
});

describe("useUpdateFolder", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should update a folder", async () => {
    const updatedFolder = {
      id: "folder-1",
      project_id: "project-1",
      folder_name: "Updated Name",
      description: "Updated description",
      color_hex: "#10b981",
      icon_name: "lock",
      sort_order: 0,
      created_at: "2025-10-14T00:00:00Z",
      updated_at: "2025-10-14T01:00:00Z",
    };

    vi.mocked(knowledgeFolderService.updateFolder).mockResolvedValue(updatedFolder);

    const queryClient = createTestQueryClient();
    const { result } = renderHook(() => useUpdateFolder(), {
      wrapper: createWrapper(queryClient),
    });

    result.current.mutate({
      folderId: "folder-1",
      data: {
        folder_name: "Updated Name",
        description: "Updated description",
        color_hex: "#10b981",
      },
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual(updatedFolder);
    expect(knowledgeFolderService.updateFolder).toHaveBeenCalledWith(
      "folder-1",
      {
        folder_name: "Updated Name",
        description: "Updated description",
        color_hex: "#10b981",
      }
    );
  });

  it("should handle update errors", async () => {
    vi.mocked(knowledgeFolderService.updateFolder).mockRejectedValue(
      new Error("Failed to update folder")
    );

    const queryClient = createTestQueryClient();
    const { result } = renderHook(() => useUpdateFolder(), {
      wrapper: createWrapper(queryClient),
    });

    result.current.mutate({
      folderId: "folder-1",
      data: {
        folder_name: "Updated Name",
      },
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error).toBeDefined();
  });
});

describe("useDeleteFolder", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should delete a folder", async () => {
    vi.mocked(knowledgeFolderService.deleteFolder).mockResolvedValue({ success: true, message: "Deleted" });

    const queryClient = createTestQueryClient();
    const { result } = renderHook(() => useDeleteFolder(), {
      wrapper: createWrapper(queryClient),
    });

    result.current.mutate("folder-1");

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(knowledgeFolderService.deleteFolder).toHaveBeenCalledWith("folder-1");
  });

  it("should handle deletion errors", async () => {
    vi.mocked(knowledgeFolderService.deleteFolder).mockRejectedValue(
      new Error("Failed to delete folder")
    );

    const queryClient = createTestQueryClient();
    const { result } = renderHook(() => useDeleteFolder(), {
      wrapper: createWrapper(queryClient),
    });

    result.current.mutate("folder-1");

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error).toBeDefined();
  });
});
