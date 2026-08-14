/**
 * useDraftAutosave — wire a doc-create wizard into the draftResume layer
 * (W4.3, finding D4).
 *
 * A wizard calls this once with:
 *   - its `docType` + `route` (the resume key + where the hub resumes into),
 *   - a live `form` snapshot (the wizard's own serializable state — RHF
 *     `watch()`, a useReducer slice, whatever the wizard owns),
 *   - the `draftId` the create-flow has produced so far (null pre-create), and
 *   - `enabled` (false once the doc is signed / on a fresh manual entry that
 *     should NOT clobber an existing autosave — the wizard decides).
 *
 * It does three things, all browser-mode safe (sessionStorage fenced in the
 * store; ZERO Telegram-host SDK calls):
 *
 *   1. AUTOSAVE — persists `form` (debounced to the next idle tick) on every
 *      change, plus immediately whenever `draftId` flips from null → a real id
 *      (so the create-but-unsigned window is captured even if the user never
 *      types again before a timeout/close).
 *
 *   2. RESUME READ — exposes the snapshot loaded ONCE at mount (`resumed`) so
 *      the wizard can seed its form + hydrate the create-flow's `draftId`. The
 *      read is one-shot (a ref taken in a lazy initializer) so a re-render or a
 *      mid-session autosave can't swap the seed out from under the wizard.
 *
 *   3. CLEAR — `discard()` wipes the entry (call on a successful sign, or when
 *      the user explicitly abandons the draft).
 *
 * REOPEN-TO-SIGN (the D4 anti-double-draft half): the wizard hydrates the
 * create-flow's `draftId` from `resumed.draftId` on mount. With a non-null
 * `draftId`, useDocCreateFlow SKIPS the create leg and goes straight to submit
 * — so a resumed-after-create draft is reopened to sign, never recreated. This
 * hook persists the id; the wizard performs the hydration (it owns the flow).
 *
 * SERVER MIRROR (the «Черновики iHisobchi» half): sessionStorage dies on a hard
 * close of the WebView and is invisible to the bot, so the same snapshot is
 * ALSO pushed to `/drafts/local` — the durable copy both surfaces read. It is
 * debounced separately (much longer than the local write: the local one is
 * free, the network one is not) and is strictly best-effort. A failed mirror
 * degrades to exactly the old local-only behaviour and never surfaces an error
 * into a wizard the user is still typing in.
 *
 * React-Compiler discipline (mirrors useCounterpartyAutoResolve): the one-shot
 * resume snapshot is captured via a LAZY useState initializer (not a ref write
 * during render); the latest `form`/`draftId` are mirrored into refs inside an
 * effect (not during render); the autosave runs in an effect keyed on the
 * serialized snapshot. No synchronous setState during render or in an effect
 * body that would fight the wizard's own state.
 */
import { useCallback, useEffect, useRef, useState } from "react";

import { upsertLocalDraft } from "../api/localDrafts";
import { localDraftsMirrorEnabled } from "../lib/flags";
import {
  clearDraftResume,
  loadDraftResume,
  markDraftCreated,
  saveDraftResume,
  type DraftResumeEntry,
} from "../store/draftResume";

/** How long to sit on changes before pushing them to the server. Long enough
 *  that a burst of typing is one request, short enough that a user who closes
 *  the app mid-thought still has their work. */
const SERVER_MIRROR_DEBOUNCE_MS = 2_000;

export interface UseDraftAutosaveOptions<TForm> {
  /** Doc-type key (matches the route segment, e.g. "invoice"). */
  docType: string;
  /** Wizard route the hub resumes into (e.g. "/create/invoice"). */
  route: string;
  /** Live, serializable form snapshot. Persisted on change. */
  form: TForm;
  /** Server draft id once created (null pre-create). Persisted as the
   *  reopen-to-sign anchor the moment it flips non-null. */
  draftId: number | null;
  /** When false the hook neither reads nor writes (signed / disabled). */
  enabled?: boolean;
  /** Mirror the snapshot to `/drafts/local` so it survives a hard close and is
   *  visible to the bot. On by default (`VITE_LOCAL_DRAFTS_MIRROR=false` is the
   *  kill-switch); pass an explicit boolean to override per wizard. */
  mirrorToServer?: boolean;
  /** Human title for the server-side draft card ("Счёт-фактура №42"). The
   *  backend derives one when omitted. */
  title?: string;
}

export interface UseDraftAutosave<TForm> {
  /** The snapshot loaded ONCE at mount, or null when nothing to resume.
   *  Stable across the component's lifetime (one-shot). */
  resumed: DraftResumeEntry<TForm> | null;
  /** Delete this doc type's autosave entry (call on a successful sign). */
  discard: () => void;
}

export function useDraftAutosave<TForm>(
  opts: UseDraftAutosaveOptions<TForm>,
): UseDraftAutosave<TForm> {
  const {
    docType,
    route,
    form,
    draftId,
    enabled = true,
    mirrorToServer = localDraftsMirrorEnabled(),
    title,
  } = opts;

  /* ─── One-shot resume read ──────────────────────────────────────────
   * Read the persisted snapshot exactly once at mount via a lazy useState
   * initializer. A lazy initializer runs in the render phase but only on the
   * FIRST render and only for the initial value, so it's the React-sanctioned
   * way to do a one-shot side-effect-free read (no ref write during render,
   * no setState-in-effect). `enabled === false` short-circuits to null. */
  const [resumed] = useState<DraftResumeEntry<TForm> | null>(() => {
    if (enabled === false) return null;
    return loadDraftResume<TForm>(docType);
  });

  /* ─── Latest-value refs (synced in an effect, never during render) ── */
  const formRef = useRef(form);
  const draftIdRef = useRef(draftId);
  const routeRef = useRef(route);
  useEffect(() => {
    formRef.current = form;
    draftIdRef.current = draftId;
    routeRef.current = route;
  });

  /* ─── Autosave on form change ───────────────────────────────────────
   * Keyed on the serialized snapshot so a deep change to `form` re-runs the
   * persist. JSON.stringify both detects the change AND is the exact payload we
   * store, so we compute it once. A non-serializable form yields null → the
   * autosave skips this tick (the store also guards, this is the cheap pre-check).
   * Skipped entirely when disabled. */
  let serialized: string | null = null;
  try {
    serialized = JSON.stringify(form);
  } catch {
    serialized = null;
  }
  useEffect(() => {
    if (enabled === false) return;
    if (serialized === null) return;
    saveDraftResume({
      docType,
      route: routeRef.current,
      draftId: draftIdRef.current,
      form: formRef.current,
    });
  }, [enabled, serialized, docType]);

  /* ─── Capture the create-but-unsigned window immediately ────────────
   * When `draftId` flips from null → a real id, persist it AT ONCE (don't wait
   * for the next form change). This is the reopen-to-sign anchor: a timeout /
   * swipe-close in the gap between create and sign now leaves a snapshot whose
   * `draftId` points at the real server draft, so the resume reopens it instead
   * of minting a second one. */
  useEffect(() => {
    if (enabled === false) return;
    if (draftId === null) return;
    // markDraftCreated only updates the id on an existing snapshot; if the
    // wizard hasn't autosaved yet (rare — the form change effect runs first on
    // any real input), fall back to a full save so the id is never lost.
    const existing = loadDraftResume(docType);
    if (existing === null) {
      if (serialized === null) return;
      saveDraftResume({ docType, route: routeRef.current, draftId, form: formRef.current });
    } else {
      markDraftCreated(docType, draftId);
    }
    // serialized intentionally omitted: this effect is about the id transition,
    // not the form bytes (the form-change effect owns those).
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled, draftId, docType]);

  /* ─── Server mirror ─────────────────────────────────────────────────
   * Debounced separately from the local write: sessionStorage is free, a POST
   * is not. Keyed on the same serialized snapshot, so a burst of typing
   * collapses into one request. Errors are swallowed — see the module doc: a
   * failed mirror is a missing safety net, never a broken wizard. */
  const titleRef = useRef(title);
  useEffect(() => {
    titleRef.current = title;
  });

  useEffect(() => {
    if (enabled === false || mirrorToServer === false) return;
    if (serialized === null) return;
    const timer = setTimeout(() => {
      // upsertLocalDraft never rejects (see its doc) — `void` is safe and keeps
      // an unreachable backend from surfacing an unhandled rejection into a
      // wizard the user is still typing in.
      void upsertLocalDraft({
        docType,
        route: routeRef.current,
        form: formRef.current,
        title: titleRef.current,
        // `draftId` is OUR server draft id (documents.id) — not the Didox id.
        // The backend resolves the Didox id from this row itself; sending it as
        // `didoxDocId` was wrong and left drafts pointing at a nonexistent
        // document.
        documentId: draftIdRef.current,
      });
    }, SERVER_MIRROR_DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [enabled, mirrorToServer, serialized, docType]);

  const discard = useCallback(() => {
    clearDraftResume(docType);
  }, [docType]);

  return { resumed, discard };
}
