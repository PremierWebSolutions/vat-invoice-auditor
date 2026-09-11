## The 10 that actually bite

Everything below this section is worth reading. These ten are the ones that have cost real money or real hours on PWS builds. If an agent only obeys ten rules, these:

| # | Rule | What happened when it was skipped |
|---|---|---|
| 1 | **The service-role key never leaves the server.** Anything named `VITE_*`, `EXPO_PUBLIC_*` or `NEXT_PUBLIC_*` is shipped to the browser in plain text | one leaked service key is a full database read/write for anyone who opens devtools |
| 2 | **RLS on every table, no exceptions** — and every service-role route re-checks ownership by hand | a pending record with a null owner was claimable by any authenticated account (a live IDOR in a PWS build) |
| 3 | **User files go to object storage, never local disk** | images written to the app's own filesystem vanished on redeploy while the DB rows kept pointing at them — a production blocker found in audit |
| 4 | **Every schema change is a migration file in git** | dashboard-clicked schema changes exist in one environment only and cannot be reviewed, replayed, or rolled back |
| 5 | **Every relation gets a real foreign key and an index** | an agent-built schema had *zero* FK constraints; integrity was app-code-only, and imperfect |
| 6 | **No silent fallbacks.** A failed send/write/charge returns an error or goes on a retry queue with an alert | email delivery silently degraded to log-only and still returned `201` — the recipient was never notified and nothing surfaced it |
| 7 | **Money is integers in minor units, and every webhook verifies its signature** | float arithmetic on prices and unverified webhooks are both silent-until-expensive |
| 8 | **Auth endpoints are rate-limited, behind a correctly-configured proxy trust setting** | sign-in was brute-forceable and the limiter itself was bypassable with a spoofed `X-Forwarded-For` |
| 9 | **Never delete or reset without a recoverable copy first** — branch the mess, don't discard it | the standard "reset hard and re-prompt" advice destroys uncommitted work, which is usually the thing you actually wanted |
| 10 | **Docs describe what exists, not what is planned** | a docstring implied a background worker that had never been written, and a status file claimed a stub for an API that was fully built |

---

# The rules

## 1. Mindset and role

- **You are a senior engineer on a small team with no QA department.** Nothing catches your mistakes downstream. Write accordingly.
- **Build what was asked. Nothing else.** No extra files, no extra features, no "while I was in there". Propose it, don't do it.
  - *Why: unrequested changes are the number-one source of bugs nobody knows to look for.*
- **If intent is ambiguous, ask one question and stop.** Do not guess, do not build both, do not "improve" something that was not mentioned.
- **When you hit a wall, say so and stop.** State what you tried, what you now believe is wrong, and two or three ways forward. Never switch approach silently.
  - *Why: a silent pivot means the next session inherits a codebase built on an assumption nobody agreed to.*
- **Never apologise. State the cause and the fix.** "That failed because X. Fixing by Y."
- **Report honestly.** If tests fail, show the output. If a step was skipped, say which. "Done" with hidden caveats is worse than "blocked".

## 2. Before any code

- **A plan exists before the first line.** What is being built, who for, the feature list (and explicitly what is *out* of scope), the stack, and the build order in sections.
  - *Why: the cheapest moment to cut scope is before any code exists.*
- **Prune the first draft of the plan hard.** Cut anything too complex for this phase, anything that is really a later phase, anything that is a nice-to-have. Ship the wedge.
- **A per-project `AGENTS.md` exists** and names the stack, directory layout, naming conventions, API patterns, and the deploy target. See the skeleton at the end.
- **Implement one section, verify it, commit it, then start the next.** Never build two sections at once.
  - *Why: without checkpoints, bugs from section 2 surface in section 6 and the trail is cold.*
- **New product or major module → write a PDR first**, in `Code Projects/<Product>/`. The existing PDRs are the model.

## 3. Git and version control

- **`main` is always deployable.** Work happens on `feature/…`, `fix/…` or `experiment/…` — lowercase, hyphens, short.
- **Start every piece of work from a clean tree.** `git status` first; commit or stash anything hanging around.
- **Commit every time something works.** Component renders → commit. Endpoint returns data → commit. Do not batch a day's work into one commit.
- **Commit message format:** `type: short description` — `feat: add coaching card`, `fix: verify stripe webhook signature`, `refactor: extract audio utils`.
- **Push after every commit**, to the feature branch. Never force-push `main`; force-push a feature branch only when you know who else has it (usually nobody).
- **Merge to `main` locally** (`git checkout main && git merge feature/x`) once it works end-to-end. Open a PR instead when you want an automated reviewer on it.
- **When three fix attempts have failed and the diff is getting worse, stop — but preserve, then reset:**
  ```bash
  git branch wip/failed-attempt && git reset --hard <last-good-commit>
  ```
  - *Why: layered failed rewrites interact with the original bug and make it harder, not easier. But a bare `reset --hard` throws away uncommitted work — including the one diagnostic edit that was actually right. Branch first; the branch costs nothing and can be deleted later.*
- **Re-approach with what you now know**, not with the same prompt. The failed attempts are evidence: say what you ruled out.

### Lovable specifically

Lovable's agent edits a cloud sandbox and syncs to the connected GitHub repo — the local-branch discipline above does not apply the same way, so the safety net is different:

- **Connect every Lovable project to GitHub on day one.** An unconnected project has no history you can diff, review, or restore outside Lovable.
- **Confirm which branch Lovable is writing to before any structural change**, in the project's GitHub settings. Assume the default branch unless you have checked.
- **Pin a Lovable version before anything structural** — schema change, auth change, payment change. That pin is your rollback.
- **Use plan mode for anything non-trivial** — agree the approach in chat before it writes code.
- **Review the diff before moving on**, every time. Not the preview: the diff.
- **When a build outgrows Lovable, move it to a local repo and Claude Code.** Signals: repeated regressions in files Lovable keeps rewriting, edge functions doing real logic, or more than one developer.

**Driving Lovable from Claude over MCP** — the default way PWS Lovable work now happens. There is no preview in front of a human, so the review gate has to be rebuilt deliberately:

- **Plan mode first for anything non-trivial**, then `send_message`, then **`get_diff` before the next message**. One change reviewed per message. Never chain two sends without reading the diff between them.
  - *Why: in the editor the preview is the review. Over MCP nothing is looked at unless the agent chooses to look, and an unreviewed change becomes the base for the next one.*
- **Check the diff against § 15, not against "does it look right"** — new tables have RLS, no new client-side secrets, schema changes captured as a migration, nothing built that wasn't asked for.
- **Lovable's reply must list the files it touched and any schema, RLS, auth or payment change.** Workspace knowledge instructs it to. If a reply arrives without that list, ask for it before sending anything else.
- **Route the risky work away from MCP entirely.** UI and copy over MCP; schema, auth and payments in a local repo where git gives real review. This removes the gap rather than patching it.
- Runbook: [[Ship a Lovable change]]. Register: [[Lovable Projects]].

## 4. Secrets, environment and configuration

- **Client-side env vars are public.** `VITE_*`, `EXPO_PUBLIC_*`, `NEXT_PUBLIC_*` and anything bundled by the build ships to every visitor in readable text. Only the anon/publishable key belongs there.
  - *Why: this is the single most common catastrophic vibe-code mistake. The agent needs a key, sees an env var pattern that works, and the service-role key ends up in the bundle.*
- **Service-role keys, API secrets and signing secrets live only in server-side environment config** — edge function secrets, server host env, CI secret store.
- **Never commit `.env`.** `.gitignore` it before the first commit, not after. If a secret has ever been committed, rotate it — deleting the file does not remove it from history.
- **Maintain `.env.example`** with every variable name, no values, and a one-line comment on where each is obtained.
- **No hardcoded values anywhere** — no URLs, no IDs, no version strings, no per-client content. Constants file, config, or environment.
  - *Why: a hardcoded dev domain and a hardcoded `"1.0.0"` both shipped in a PWS app. Both are invisible until they are wrong.*
- **Per-client and per-user content lives in the database, loaded at runtime.** Never in the codebase.
  - *Why: hardcoded tenant data breaks multi-tenancy, leaks between clients, and needs a deploy to change a sentence.*
- **Separate dev and production projects.** Never point a development branch at the production database. Seed dev with fake data.

## 5. Data, schema and multi-tenancy

- **RLS on every table with user data. No exceptions, including "internal" tables.** Policies scope reads *and* writes to the authenticated user's own rows.
  - *Why: without it, any authenticated user can potentially read or write any row. RLS is the last line, not the first.*
- **Every route using a service-role client re-verifies ownership by hand.** Service role bypasses RLS by design; an authenticated caller is not an authorised one.
  - *Why: change an ID in the request body and you are in someone else's data. This is the IDOR class, and it is the one that has actually appeared in a PWS build.*
- **Any record with a nullable owner is claimable.** Pending invites, unassigned companies, draft records: state explicitly who may claim them and enforce it in the `WHERE` clause, not in an `if`.
- **Every relation is a real foreign key with an index.** App-level integrity is not integrity.
- **Server generates primary keys.** A client-supplied ID that collides produces a raw 500, not a clean conflict.
- **Enums and CHECK constraints for status columns.** Free-text status fields drift into three spellings of "pending".
- **Every schema change is a migration file, committed.** No dashboard-only changes.
- **Claim/lifecycle transitions must be race-safe** — a compound `WHERE` that fails on the second attempt, not read-then-write.
- **Money is integers in the minor unit** (pence, cents). Never floats. Store the currency alongside every amount.
- **Backups exist and have been restored at least once.** An untested backup is a hope.
- **Account and data deletion is a real endpoint with real UI**, before any app store submission and before any real client data lands.

## 6. Security

- **Validate all input server-side.** Client validation is UX; the server is the gate. Use a schema validator, and validate the same shape the OpenAPI/type contract promises.
- **Rate-limit auth, upload and any unauthenticated endpoint.** Sign-in, sign-up, password reset, existence lookups, file upload.
  - *Why: an unthrottled sign-in is brute-forceable; an unthrottled "does this email exist" endpoint is a PII oracle; an unthrottled upload is a disk-DoS.*
- **Configure proxy trust before relying on client IP.** Behind a proxy without `trust proxy` (or equivalent), a rate limiter reading `X-Forwarded-For` gives every spoofed request a fresh bucket.
- **Hash session tokens at rest**, like passwords. Support revoke-all. Set a sane expiry.
- **Verify every webhook signature** — Stripe, and everything else — and make webhook handlers idempotent, because they will be delivered twice.
- **Sniff uploaded file types by magic bytes, not the client's `Content-Type`.** Cap size. Store outside the web root.
- **Lock CORS to known origins.** Never `cors()` with no options in production.
- **A global error handler exists**, returns a generic message to the client, and logs the detail server-side.
- **Never log secrets or PII** — no tokens, keys, passwords, full card data, or personal data in any log line. Redact at the logger.
- **HTTPS everywhere.** No plain HTTP calls, ever.
- **Dependencies:** `npm audit` in CI, Dependabot or Renovate on, and known vulnerabilities fixed rather than muted.

## 7. Code quality

- **Files past ~300 lines and functions past ~50 get split** — a review trigger, not a hard cap. Do not shred a coherent module to hit a number.
  - *Why: large files are hard for both humans and agents to reason about, and agents rewrite whole files.*
- **No `any` in TypeScript.** Type it or narrow it. `unknown` plus a guard beats `any`.
- **Descriptive names.** `getUserSalesMetrics()`, not `getData()`. `isCallActive`, not `flag`.
- **No commented-out code in a commit.** Git has it.
- **DRY at the third occurrence, not the second.** Two similar blocks are often coincidence; three is a pattern.
- **Small modules with one job and a clear interface.** Every external API integration gets its own module, so it can be swapped or mocked.
- **Idempotency keys on anything that creates or charges**, enforced by a unique index, returning the existing record rather than an error.
  - *Why: this was done right in a PWS build and it is the reason duplicate uploads never became duplicate charges.*

## 8. Debugging

- **Do not rewrite first.** State three or four possible causes, then investigate the most likely.
  - *Why: rewriting before you understand adds layers that hide the real bug.*
- **Add logging before changing logic.** Prove where the bug is; assumptions about location are wrong more often than not.
- **Use exact error text.** Never paraphrase an error message or a stack trace.
- **Isolate hard bugs** into a minimal reproduction — a standalone file or a scratch project. Remove the noise.
- **Three failures means the assumption is wrong, not the code.** Stop, name the assumption, test that instead. Preserve-then-reset per § 3.

## 9. Testing

- **"It runs" is not tested.** Tested means you can state the input, the expected output, and the assertion.
- **At least one end-to-end test per feature**, walking the real user path. Playwright for web.
- **Test the failure path too:** API error, empty form, expired session, offline, duplicate submit, wrong tenant.
- **Every auth rule gets a negative test.** A test that proves user A *cannot* read user B's row is worth ten happy-path tests.
- **Prototype risky integrations standalone first.** Prove the third-party API works in isolation before wiring it into the product.
- **Start from the vendor's reference implementation** where one exists. If theirs works and yours does not, the bug is yours.

## 10. Interface

- **No emojis in the UI.** Not in buttons, headings, labels, empty states, or notifications.
- **No glassmorphism, no gratuitous gradients, no purple-dominant palettes.** These read as machine-generated.
- **One spacing scale** (4/8/12/16/24/32/48) applied everywhere.
  - *Why: inconsistent spacing is the most common reason a UI feels wrong when every component looks fine alone.*
- **One font family, two at most.** Bundled or on a reliable host.
- **Contrast checked, in both themes** if there are two.
- **Loading states are required** on every async operation. A blank screen reads as broken.
- **Error states are required** and must be visible and actionable. `console.error` is not an error state.
- **Distinguish "waiting" from "failed".** Offline, queued and retrying are not errors — showing them as errors teaches users to distrust the app.
  - *Why: a PWS mobile app classified "no internet" as a failed upload after five attempts, so a user offline for an afternoon saw a screen full of errors for work that was fine.*
- **Every destructive action has a confirmation naming what will be destroyed.**
- **Never make an interactive element invisible or zero-size.** No `opacity: 0`, no 1×1 inputs, no controls positioned off-screen to catch input for something else to draw. If the user is asked to type into it, tap it, or read it, it must be visible and hit-testable where they are looking.
  - *Why: a PWS app's sign-in screen drew six fake digit boxes over a 1×1 zero-opacity text input — the standard segmented-OTP trick, because the framework offers no way to style one field as six boxes. When that hidden input failed to take focus the keyboard opened and every keystroke vanished, with nothing on screen able to report it. An invisible control cannot show its own state, so its failures are silent by construction. This is § 6's no-silent-fallbacks rule at the UI layer.*
  - **A visibly plain control that works beats an elegant one that can fail invisibly.** Take the simpler single field.

## 11. Copy

- **No placeholder text in a commit.** No lorem ipsum, no "TODO: copy here", no "Your amazing feature".
- **Every word earns its place.** If it can be cut without losing meaning, cut it.
- **Banned words:** leverage, streamline, empower, cutting-edge, revolutionary, seamless, robust solution, next level, unlock, elevate, effortless.
- **No fake social proof.** No invented testimonials, user counts, or case studies.
- **Specific CTAs.** "Start free trial", "Book a demo", "Download the report" — never "Get started".
- **At most one em-dash per page of shipped copy.** (Internal docs and code comments are exempt.)

## 12. Performance and cost

- **Check before installing.** If it is under ~50 lines of your own code, write it. Every dependency is bundle size, maintenance, and attack surface.
- **Lazy-load heavy routes and components.**
- **Debounce search inputs and expensive operations.** No API call per keystroke.
- **Optimise images:** compressed, modern format, correctly sized, lazy below the fold.
- **No unbounded loops over paid APIs.** Anything calling an LLM or a metered service gets a hard iteration cap, a token/spend cap, and a log line per call.
  - *Why: an agent-written retry loop against a paid API is a bill, not a bug report.*
- **Cap and cache AI calls.** Cache by input hash where the output is stable.

## 13. Operations

- **Error tracking is wired before launch**, not after the first incident. Sentry or equivalent, with source maps and release tagging.
- **Health check endpoint** on every deployed service.
- **Structured logs with a request ID**, so one user's journey can be followed.
- **Alert on the things that fail silently:** payment failures, webhook failures, email delivery failures, queue depth, background jobs that stopped running.
- **A deploy that cannot be rolled back is not finished.** Know the rollback command before you deploy.

## 14. Documentation

- **`README.md` in every repo:** what it is, how to set it up, how to run it, how to deploy it, what the environment variables are.
- **Update docs in the same commit as the change.** Not later.
  - *Why: an outdated doc is worse than none — it actively misleads the next agent, which will trust it. A PWS repo carried a status file claiming its API was a stub long after the API was complete.*
- **Never document something that does not exist.** No docstrings describing a planned worker, no README sections for unbuilt features. If it is planned, it goes in the plan, marked as planned.
- **Store third-party API docs locally** in `docs/api/` and reference them from `AGENTS.md`, so the agent reads them instead of inventing endpoints.
- **Write down non-obvious decisions and their reason**, one line each, in the repo. "Chose X over Y because Z."
  - *Why: without the reason, the next agent reverses a deliberate decision as an improvement.*

## 15. Definition of done

A feature is done when **all** of these are true. Anything less is "in progress", whatever it looks like in the preview.

- [ ] Works end-to-end on the real path, not just the happy click-through
- [ ] Loading and error states exist and are visible
- [ ] The failure path is tested, including the cross-tenant negative test
- [ ] RLS/authorisation checked for every new table and route
- [ ] No new secrets client-side, no new hardcoded values
- [ ] Migration committed if the schema changed
- [ ] Docs and `AGENTS.md` updated in the same commit
- [ ] Committed and pushed, with a message that says what changed

**Refactor when it works, never when it is broken.** Once green, ask: duplicated logic, oversized files, anything simpler? Then commit the refactor separately.

**End every session with everything committed and pushed**, and a final commit message or note saying what comes next.

---

## Per-project AGENTS.md

Paste the global rules above, then this, filled in:

```markdown
## This project

**What it is:** one sentence.
**Stack:** framework, database, auth, payments, hosting, and where each lives.
**Deploy:** how it ships, and how to roll back.
**Environments:** dev and prod project IDs/URLs, and which is which.

## Layout
- `path/` — what lives here

## Conventions
- naming, file placement, API shape, error shape

## Rules that override the global set
- <rule> — because <reason>

## Do not touch
- <files or systems requiring a human>

## Gotchas
- <the things nobody could reconstruct later>
```

**The gotchas section is the one that matters.** Everything else can be re-derived from the code; a gotcha cannot.

---

## This project

**What it is:** a drop-in folder that turns a Claude project into a UK VAT invoice compliance auditor, checking sales invoices against VAT Notice 700/21 and regulation 14 of the VAT Regulations 1995 — built as Andy's entry for the Clief Notes weekly comp "THE AUDITOR".
**Stack:** Markdown files plus four offline checkers in Python 3 standard library, and one deliberately-online shell script kept out of CI. No dependencies, no network calls (except that one script), no API keys, no database, no server.
**Deploy:** push to the public GitHub repo `PremierWebSolutions/vat-invoice-auditor`. Judges pin to the last commit before the deadline (Friday 2026-09-11, 11:59 PM EST), so `main` must be submission-ready at every commit.
**Environments:** none — the repo is the product.

## Layout
- `identity.md` — who the auditor is and what standard it enforces
- `rules.md` — audit order, citation format, severity classification
- `examples.md` — worked example audits with citations
- `reference/` — the actual standard text, version-dated, under the Open Government Licence; `MANIFEST.md` records each file's SHA-256
- `fixtures/` — synthetic test invoices (compliant and deliberately broken), inputs only, no answers
- `judge-answer-key/` — the fixture answer sheet, deliberately outside `fixtures/`; never routed to or read by the auditor's own files, never uploaded in a real drop-in. `CLAUDE.md` names it exactly once, as a prohibition (see the gotcha below for why that is allowed)
- `invoices/` — the user's own working folder for real invoices (PDF or text). Only `README.md` and the shipped `SAMPLE-invoice.pdf` are tracked; everything else is git-ignored so real client documents never reach the public repo. Nothing in `tools/` scans it
- `tools/` — four offline checkers (citations/quotes, arithmetic, no-network proof, reference integrity), one online freshness script kept out of CI, the `audit.sh` runner (calls the Claude CLI), and the checkers' own test fixtures under `tools/testdata/`
- `docs/` — decisions log, severity review notes (`review-notes.md`), and five receipts: `cold-walk.md`, `refusal-under-pressure.md`, `verdict-under-pressure.md`, `reword-robustness.md`, `batch-run.md`

## Conventions
- Every finding cites a specific provision using the citation format defined in `rules.md`; citation IDs must resolve against `reference/` (the checker enforces this).
- Severity levels are exactly the three defined in `rules.md` — do not invent new ones.
- Fixture invoices are plain markdown, one invoice per file, named `<compliant|broken>-<short-slug>.md`.

## Rules that override the global set
- The global sections on RLS, auth, payments, webhooks, env vars, error tracking and health checks do not apply — because this repo has no server, database, users, or secrets of any kind. They are not overridden, they are out of scope; nothing here may quietly grow the kind of code that would bring them back into scope.

## Do not touch
- `reference/` file bodies below their attribution header — they are verbatim excerpts of Crown copyright material under OGL v3.0. Never paraphrase, reword, or "tidy" them. The only valid edit is a fresh re-fetch from the source with an updated access date.

## Gotchas
- **All invoice data in this repo is synthetic.** No real client, supplier, VAT number, or address may ever appear — Andy is a practising accountant and this repo is public.
- The competition auto-fails a `reference/` folder that does not contain the standard itself — a summary or a link is a fail. Keep the verbatim text in.
- The README must NOT tell users to load every file into context — an earlier comp cycle failed entries for exactly that. Catalog first, load one card at a time.
- Judges actively try to break entries (past cycles planted a bad citation, a fabricated quote, a planted SHA, and a wrong line number) — `tools/check_citations.py` must fail loudly on any citation that doesn't resolve against `reference/` AND on any double-quoted span in the QUOTE_FILES list that appears in no fixture and no reference card; `tools/check_arithmetic.py` must fail loudly on any fixture whose stated net/VAT/total figures don't reconcile against each other, with an unrecognised invoice shape treated as a hard failure, never a silent skip. All checker gates must run offline with zero dependencies — `tools/check_no_network.py` proves it by scanning their source for real imports/calls, not by trusting the claim, and it must be extended to cover any new checker script added later. Never put a quoted span in a QUOTE_FILES entry unless it is a verbatim quote of a fixture or the standard, and never hand-adjust a fixture's arithmetic without re-running the checker.
- `tools/check_freshness.sh` is the one *checker* allowed to touch the network — do not add network calls to any other checker, and do not add `tools/check_freshness.sh` (or anything like it) to CI; it stays a manual/periodic tool by design. `tools/audit.sh` also reaches the network, because it invokes the Claude CLI and the Claude CLI is the auditor; it is a runner, not a checker, and never belongs in CI either.
- `audits/` is git-ignored on purpose: `tools/audit.sh` users are told to redirect reports there, and a saved report of a real supplier invoice must never be committable. Do not remove that ignore line.
- `reference/MANIFEST.md` is generated by `python3 tools/check_reference_integrity.py --write` — never hand-edit its hashes. Regenerate it only immediately after a deliberate, disclosed re-fetch of a `reference/` file, never to silence an unexplained mismatch.
- VAT numbers in fixtures use obviously-fake but format-valid GB patterns; the checker does not validate VAT number checksums (out of scope, documented).
- **Never move the answer key back into `fixtures/`, and never route to it from `identity.md`/`rules.md`/`examples.md`.** Past judging cycles have shown that an instruction telling the auditor not to read a file is not trusted on its own — the fix is the file's folder position, not the wording of the warning. `judge-answer-key/` being a sibling of `fixtures/`, not a child, is the whole point. **Deliberate exception:** `CLAUDE.md` names the folder once, as a flat prohibition ("never open"). That is allowed, and it is the only place it is allowed, because a prohibition on top of the folder move is strictly stronger than the move alone — provided nobody ever mistakes the sentence for the mechanism. The mechanism is the folder position; the sentence is belt and braces. Two receipts (`docs/cold-walk.md`, `docs/refusal-under-pressure.md`) record sessions reading that sentence and honouring it, which is the other reason it stays. Written down here because the global ruleset says a divergence that isn't written down with its reason is how a ruleset dies.
