/**
 * ErrorBoundary unit tests (W8.1.1, updated W8.1.2 for lazy-Sentry).
 *
 * Coverage:
 *   1. Children render normally when no error is thrown.
 *   2. Fallback UI shows + captureExceptionLazy is called when a child
 *      throws during render. We mock sentryLazy because the lazy module
 *      schedules a real dynamic import we don't want in unit tests.
 *   3. The "Перезагрузить" button triggers window.location.reload.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErrorBoundary } from "./ErrorBoundary";

// Mock the lazy-Sentry shim — captureExceptionLazy is the only surface
// the boundary uses. The real module triggers a dynamic import of
// @sentry/react which we don't want exercised in unit tests.
vi.mock("../lib/sentryLazy", () => ({
  captureExceptionLazy: vi.fn(),
}));

import { captureExceptionLazy } from "../lib/sentryLazy";

/**
 * Minimal throw-on-render component. The conditional lets us flip
 * a single test prop to drive the boundary into either branch.
 */
function Bomb({ shouldThrow }: { shouldThrow: boolean }) {
  if (shouldThrow) {
    throw new Error("kaboom");
  }
  return <div>safe content</div>;
}

beforeEach(() => {
  vi.clearAllMocks();
  // React 19 still pipes caught render errors through console.error
  // even when an error boundary handles them. Silence to keep test
  // output readable; we restore in afterEach.
  vi.spyOn(console, "error").mockImplementation(() => {});
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe("<ErrorBoundary /> (W8.1.1)", () => {
  it("renders children when no error is thrown", () => {
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={false} />
      </ErrorBoundary>,
    );

    expect(screen.getByText("safe content")).toBeInTheDocument();
    // Sanity: no fallback markers leaked through.
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("renders the fallback UI when a child throws", () => {
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={true} />
      </ErrorBoundary>,
    );

    // role=alert + Russian copy are the user-visible contract.
    expect(screen.getByRole("alert")).toBeInTheDocument();
    expect(screen.getByText("Что-то пошло не так")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Перезагрузить" })).toBeInTheDocument();
  });

  it("forwards the error to captureExceptionLazy with React component stack", () => {
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={true} />
      </ErrorBoundary>,
    );

    expect(captureExceptionLazy).toHaveBeenCalledOnce();
    const [err, ctx] = vi.mocked(captureExceptionLazy).mock.calls[0]!;
    expect(err).toBeInstanceOf(Error);
    expect((err as Error).message).toBe("kaboom");
    // Component stack arrives via the React error info — verify it
    // landed in the contexts payload so the Sentry issue includes it.
    expect(ctx).toMatchObject({
      contexts: { react: { componentStack: expect.any(String) } },
    });
  });

  it("reloads the page when the user clicks Перезагрузить", async () => {
    // jsdom's location.reload is non-writable; redefine for the test.
    const reload = vi.fn();
    Object.defineProperty(window, "location", {
      configurable: true,
      value: { ...window.location, reload },
    });

    const user = userEvent.setup();
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={true} />
      </ErrorBoundary>,
    );

    await user.click(screen.getByRole("button", { name: "Перезагрузить" }));
    expect(reload).toHaveBeenCalledOnce();
  });
});
