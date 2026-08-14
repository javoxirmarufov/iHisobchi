/**
 * useDraftAutosave tests (W4.3, fixes D4).
 *
 * Asserts the hook's three jobs against the real sessionStorage-backed store
 * (jsdom provides sessionStorage; the global test setup clears it after each
 * test, so each case is hermetic):
 *
 *   - one-shot RESUME read at mount (and `enabled:false` short-circuit),
 *   - AUTOSAVE on form change (persists the live snapshot),
 *   - markDraftCreated the moment `draftId` flips null → a real id (the
 *     reopen-to-sign anchor that closes the orphan / double-draft window),
 *   - discard() wipes the entry.
 */
import { describe, it, expect, beforeEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useDraftAutosave } from "./useDraftAutosave";
import {
  loadDraftResume,
  saveDraftResume,
  setDraftResumeBusiness,
  _clearAllDraftResumes,
} from "../store/draftResume";

type Form = { notes: string; count: number };

beforeEach(() => {
  _clearAllDraftResumes();
  setDraftResumeBusiness(5);
});

describe("useDraftAutosave — resume read", () => {
  it("returns the persisted snapshot once at mount", () => {
    saveDraftResume({
      docType: "invoice",
      route: "/create/invoice",
      draftId: 9101,
      form: { notes: "hi", count: 3 } satisfies Form,
    });

    const { result } = renderHook(() =>
      useDraftAutosave<Form>({
        docType: "invoice",
        route: "/create/invoice",
        form: { notes: "", count: 0 },
        draftId: null,
      }),
    );

    expect(result.current.resumed).not.toBeNull();
    expect(result.current.resumed!.form).toEqual({ notes: "hi", count: 3 });
    expect(result.current.resumed!.draftId).toBe(9101);
  });

  it("does NOT read when disabled", () => {
    saveDraftResume({
      docType: "invoice",
      route: "/create/invoice",
      draftId: null,
      form: { notes: "x", count: 1 },
    });
    const { result } = renderHook(() =>
      useDraftAutosave<Form>({
        docType: "invoice",
        route: "/create/invoice",
        form: { notes: "", count: 0 },
        draftId: null,
        enabled: false,
      }),
    );
    expect(result.current.resumed).toBeNull();
  });
});

describe("useDraftAutosave — autosave write", () => {
  it("persists the live form snapshot on mount and on change", () => {
    const { rerender } = renderHook(
      (props: { form: Form }) =>
        useDraftAutosave<Form>({
          docType: "invoice",
          route: "/create/invoice",
          form: props.form,
          draftId: null,
        }),
      { initialProps: { form: { notes: "first", count: 1 } } },
    );

    // Mount autosave.
    expect(loadDraftResume<Form>("invoice")!.form).toEqual({ notes: "first", count: 1 });

    // A form change re-persists.
    act(() => rerender({ form: { notes: "second", count: 2 } }));
    expect(loadDraftResume<Form>("invoice")!.form).toEqual({ notes: "second", count: 2 });
  });

  it("does NOT write when disabled", () => {
    renderHook(() =>
      useDraftAutosave<Form>({
        docType: "invoice",
        route: "/create/invoice",
        form: { notes: "nope", count: 0 },
        draftId: null,
        enabled: false,
      }),
    );
    expect(loadDraftResume("invoice")).toBeNull();
  });
});

describe("useDraftAutosave — markDraftCreated (reopen-to-sign anchor)", () => {
  it("records the server draftId the moment it flips null → a real id", () => {
    const { rerender } = renderHook(
      (props: { draftId: number | null }) =>
        useDraftAutosave<Form>({
          docType: "invoice",
          route: "/create/invoice",
          form: { notes: "body", count: 1 },
          draftId: props.draftId,
        }),
      { initialProps: { draftId: null as number | null } },
    );

    // Pre-create: snapshot exists with no id yet.
    expect(loadDraftResume<Form>("invoice")!.draftId).toBeNull();

    // The draft-POST returns id 9101 (created server-side, not yet signed).
    act(() => rerender({ draftId: 9101 }));

    const after = loadDraftResume<Form>("invoice")!;
    expect(after.draftId).toBe(9101);
    // The form bytes are preserved alongside the id.
    expect(after.form).toEqual({ notes: "body", count: 1 });
  });
});

describe("useDraftAutosave — discard", () => {
  it("wipes the entry", () => {
    const { result } = renderHook(() =>
      useDraftAutosave<Form>({
        docType: "invoice",
        route: "/create/invoice",
        form: { notes: "x", count: 1 },
        draftId: null,
      }),
    );
    expect(loadDraftResume("invoice")).not.toBeNull();
    act(() => result.current.discard());
    expect(loadDraftResume("invoice")).toBeNull();
  });
});
