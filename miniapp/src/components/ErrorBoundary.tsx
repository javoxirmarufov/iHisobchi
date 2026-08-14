/**
 * ErrorBoundary — top-level React error trap.
 *
 * Wraps the entire <RouterProvider /> in main.tsx so any uncaught
 * render-time exception (bad component, missing data, malformed
 * server payload, etc.) shows a friendly fallback in Russian
 * instead of a blank white screen.
 *
 * On error:
 *   1. Forward the error + componentStack to Sentry via
 *      `captureExceptionLazy` (sentryLazy.ts). If Sentry has loaded,
 *      the call goes straight through; if not yet (first ~500ms after
 *      boot), the error is buffered and replayed when Sentry arrives.
 *      See sentryLazy.ts for the buffer-and-replay pattern.
 *   2. Render a fallback panel (Tailwind tokens identical to the
 *      AuthGate states — bg-bg, text-ink, accent button) with a
 *      "Перезагрузить" button that calls `window.location.reload()`.
 *
 * Why a custom class instead of `Sentry.ErrorBoundary`:
 *   - We get exact control over the fallback markup (i18n via a
 *     plain Russian string is fine here — the user is already in
 *     a degraded state, no need to hit useT() which itself could
 *     throw if i18n hasn't initialized).
 *   - The Sentry HOC would force eager Sentry loading; lazy capture
 *     keeps Sentry off the critical path while preserving error
 *     reporting for the boundary.
 *
 * Note on React 19: error boundaries still must be class components
 * (no hook equivalent yet). `componentDidCatch` is the official
 * place to log; `getDerivedStateFromError` flips state for the
 * next render.
 */
import { Component } from "react";
import type { ErrorInfo, ReactNode } from "react";
import { WarningOctagon } from "@phosphor-icons/react";
import { captureExceptionLazy } from "../lib/sentryLazy";
import { Button } from "../ui/Button";

type ErrorBoundaryProps = {
  children: ReactNode;
};

type ErrorBoundaryState = {
  hasError: boolean;
};

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError(): ErrorBoundaryState {
    // React calls this before the next render; flipping `hasError`
    // here ensures the fallback shows on the very next paint without
    // waiting for componentDidCatch (which fires asynchronously).
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Capture in Sentry with the React component stack as extra
    // context. `componentStack` is the React-walked tree at the time
    // of the throw — way more useful than the JS stack alone for
    // pinpointing which route/component blew up.
    //
    // Routed through captureExceptionLazy so pre-Sentry-load throws
    // (race between mount + idle Sentry boot) are buffered and replayed.
    captureExceptionLazy(error, {
      contexts: {
        react: {
          componentStack: errorInfo.componentStack,
        },
      },
    });
  }

  handleReload = (): void => {
    // Full page reload is the right call here: state is poisoned,
    // QueryClient cache may be inconsistent, and Telegram WebApp
    // re-injects initData on reload so auth still works.
    window.location.reload();
  };

  render(): ReactNode {
    if (this.state.hasError) {
      return (
        <div
          role="alert"
          className="flex min-h-screen flex-col items-center justify-center bg-bg p-6 text-ink"
        >
          <div className="card-raised animate-fade-up flex w-full max-w-sm flex-col items-center gap-3 p-6 text-center">
            <span
              aria-hidden
              className="flex h-14 w-14 items-center justify-center rounded-pill"
              style={{ background: "var(--color-danger-soft)" }}
            >
              <WarningOctagon size={28} weight="duotone" className="text-danger" />
            </span>
            <h1 className="text-xl font-semibold">Что-то пошло не так</h1>
            <p className="text-md text-ink-secondary">
              Произошла непредвиденная ошибка. Мы уже получили уведомление и работаем над
              исправлением. Пожалуйста, перезагрузите приложение.
            </p>
            <Button variant="primary" size="md" onClick={this.handleReload} className="mt-2">
              Перезагрузить
            </Button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
