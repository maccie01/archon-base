/**
 * Unit tests for KnowledgeTabs component
 *
 * Tests tab navigation and content rendering.
 *
 * Created: 2025-10-14
 */

import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { KnowledgeTabs } from "../KnowledgeTabs";

vi.mock("../GlobalKnowledgeView", () => ({
  GlobalKnowledgeView: () => <div data-testid="global-view">Global Knowledge View</div>,
}));

vi.mock("../ProjectKnowledgeView", () => ({
  ProjectKnowledgeView: () => <div data-testid="project-view">Project Knowledge View</div>,
}));

vi.mock("../TagsIndexView", () => ({
  TagsIndexView: () => <div data-testid="tags-view">Tags Index View</div>,
}));

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });
}

function renderWithProviders(ui: React.ReactElement) {
  const queryClient = createTestQueryClient();
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  );
}

describe("KnowledgeTabs", () => {
  it("should render all three tabs", () => {
    renderWithProviders(<KnowledgeTabs />);

    expect(screen.getByRole("tab", { name: /global/i })).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: /projects/i })).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: /tags/i })).toBeInTheDocument();
  });

  it("should show global view by default", () => {
    renderWithProviders(<KnowledgeTabs />);

    expect(screen.getByTestId("global-view")).toBeInTheDocument();
    expect(screen.queryByTestId("project-view")).not.toBeInTheDocument();
    expect(screen.queryByTestId("tags-view")).not.toBeInTheDocument();
  });

  it("should switch to projects view when projects tab is clicked", async () => {
    const user = userEvent.setup();
    renderWithProviders(<KnowledgeTabs />);

    const projectsTab = screen.getByRole("tab", { name: /projects/i });
    await user.click(projectsTab);

    expect(screen.getByTestId("project-view")).toBeInTheDocument();
    expect(screen.queryByTestId("global-view")).not.toBeInTheDocument();
    expect(screen.queryByTestId("tags-view")).not.toBeInTheDocument();
  });

  it("should switch to tags view when tags tab is clicked", async () => {
    const user = userEvent.setup();
    renderWithProviders(<KnowledgeTabs />);

    const tagsTab = screen.getByRole("tab", { name: /tags/i });
    await user.click(tagsTab);

    expect(screen.getByTestId("tags-view")).toBeInTheDocument();
    expect(screen.queryByTestId("global-view")).not.toBeInTheDocument();
    expect(screen.queryByTestId("project-view")).not.toBeInTheDocument();
  });

  it("should highlight active tab", async () => {
    const user = userEvent.setup();
    renderWithProviders(<KnowledgeTabs />);

    const globalTab = screen.getByRole("tab", { name: /global/i });
    const projectsTab = screen.getByRole("tab", { name: /projects/i });

    expect(globalTab).toHaveAttribute("data-state", "active");
    expect(projectsTab).toHaveAttribute("data-state", "inactive");

    await user.click(projectsTab);

    expect(globalTab).toHaveAttribute("data-state", "inactive");
    expect(projectsTab).toHaveAttribute("data-state", "active");
  });

  it("should show tab icons", () => {
    renderWithProviders(<KnowledgeTabs />);

    const globalTab = screen.getByRole("tab", { name: /global/i });
    const projectsTab = screen.getByRole("tab", { name: /projects/i });
    const tagsTab = screen.getByRole("tab", { name: /tags/i });

    expect(globalTab.querySelector("svg")).toBeInTheDocument();
    expect(projectsTab.querySelector("svg")).toBeInTheDocument();
    expect(tagsTab.querySelector("svg")).toBeInTheDocument();
  });
});
