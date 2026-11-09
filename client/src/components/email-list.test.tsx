/**
 * Behavioural tests for `EmailList`.
 *
 * This is the first test in the client tree. Before it, `vite.config.ts` pointed Vitest at
 * `backend/**\/*.test.ts` and a setup file that do not exist, and `package.json` had no
 * `test` script — so nothing in `client/src` had ever been executed by a test runner.
 *
 * The fixtures are cast rather than constructed as `Email` because that type is inferred
 * from the Drizzle table and carries every column; the component reads seven of them and
 * the test should say which seven, not mirror the schema.
 */
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import type { EmailWithCategory } from "@shared/schema";

import { EmailList } from "./email-list";

function email(overrides: Partial<Record<string, unknown>> = {}): EmailWithCategory {
  return {
    id: 1,
    sender: "Ada Lovelace",
    subject: "Analytical engine notes",
    preview: "The engine weaves algebraic patterns",
    time: "09:41",
    isStarred: false,
    labels: [],
    confidence: null,
    categoryData: undefined,
    ...overrides,
  } as unknown as EmailWithCategory;
}

describe("EmailList", () => {
  it("shows skeletons, not rows, while loading", () => {
    const { container } = render(
      <EmailList emails={[email()]} loading={true} onEmailSelect={vi.fn()} />
    );

    // The loading branch returns before the empty-state check, so the row must be absent
    // even though an email was supplied, and exactly three placeholder rows must be present.
    expect(screen.queryByText("Ada Lovelace")).not.toBeInTheDocument();
    expect(container.querySelectorAll("div.p-4").length).toBe(3);
  });

  it("renders the empty state when there is nothing to show", () => {
    render(<EmailList emails={[]} loading={false} onEmailSelect={vi.fn()} />);

    expect(screen.getByText("No emails found")).toBeInTheDocument();
  });

  it("renders sender, subject, preview and time", () => {
    render(<EmailList emails={[email()]} loading={false} onEmailSelect={vi.fn()} />);

    expect(screen.getByText("Ada Lovelace")).toBeInTheDocument();
    expect(screen.getByText("Analytical engine notes")).toBeInTheDocument();
    expect(screen.getByText("The engine weaves algebraic patterns")).toBeInTheDocument();
    expect(screen.getByText("09:41")).toBeInTheDocument();
  });

  it("derives initials from the sender name", () => {
    render(
      <EmailList
        emails={[email({ sender: "Grace Hopper" })]}
        loading={false}
        onEmailSelect={vi.fn()}
      />
    );

    expect(screen.getByText("GH")).toBeInTheDocument();
  });

  it("calls onEmailSelect with the email that was clicked", async () => {
    const onEmailSelect = vi.fn();
    const selected = email({ id: 7, subject: "Second" });
    render(
      <EmailList
        emails={[email({ id: 1, subject: "First" }), selected]}
        loading={false}
        onEmailSelect={onEmailSelect}
      />
    );

    await userEvent.click(screen.getByText("Second"));

    expect(onEmailSelect).toHaveBeenCalledTimes(1);
    expect(onEmailSelect).toHaveBeenCalledWith(selected);
  });

  it("shows a star only on starred emails", () => {
    const { container } = render(
      <EmailList
        emails={[email({ id: 1, isStarred: true }), email({ id: 2, isStarred: false })]}
        loading={false}
        onEmailSelect={vi.fn()}
      />
    );

    // lucide renders `class="lucide lucide-star ..."`; counting is the only stable handle.
    expect(container.querySelectorAll("svg.lucide-star").length).toBe(1);
  });

  it("accepts labels as a comma-separated string", () => {
    render(
      <EmailList
        emails={[email({ labels: "inbox,important" })]}
        loading={false}
        onEmailSelect={vi.fn()}
      />
    );

    expect(screen.getByText("inbox")).toBeInTheDocument();
    expect(screen.getByText("important")).toBeInTheDocument();
  });

  it("accepts labels as an array", () => {
    render(
      <EmailList
        emails={[email({ labels: ["from-jules"] })]}
        loading={false}
        onEmailSelect={vi.fn()}
      />
    );

    expect(screen.getByText("from-jules")).toBeInTheDocument();
  });

  it("renders the category badge and the confidence figure", () => {
    render(
      <EmailList
        emails={[
          email({
            categoryData: { id: 3, name: "Work & Business" },
            confidence: 92,
          } as Partial<Record<string, unknown>>),
        ]}
        loading={false}
        onEmailSelect={vi.fn()}
      />
    );

    expect(screen.getByText("Work & Business")).toBeInTheDocument();
    expect(screen.getByText("92% confidence")).toBeInTheDocument();
  });
});
