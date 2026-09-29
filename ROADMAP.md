# Roadmap

Committed doc, not scratch. Kept current by hand as work ships.
**Shipped** = live in production. **Next** = intended, not promised.
**Declined** = decided against, with the reason, so it doesn't get re-proposed.
**Open questions** = unresolved calls, with what would settle them.

## Shipped

- **2026-09** **Pushes to `main` deploy; CI tests what production runs.** The Vercel project is
  now git-connected (production branch `main`); before this, only `vercel deploy --prod` deployed
  it, and a push produced no build. CI installs from `uv.lock` with `uv sync --locked`, as the
  Vercel build does: its old unpinned `pip install -e` pulled SQLAlchemy 2.1, whose default
  `postgresql://` driver is psycopg 3 (not installed), so every run since 2026-09-28 failed at
  import. `requires-python` is now `>=3.12`, which drops the lock's Python 3.9 fork that pinned
  vulnerable urllib3 1.26, python-dotenv 1.2.1 and pytest 8.4; all 7 Dependabot alerts are
  fixed (urllib3 2.8.0, python-dotenv 1.2.3, pytest 9.1.1).

- **2026-09** **Booking API is size-capped, rate-limited and CORS-restricted.** `server.py#create_app`
  sets `MAX_CONTENT_LENGTH` to 16 KB (413 past it) and allows CORS only from
  `https://vroom.crystalprism.io` (plus `http://localhost:3000` when `ENV_TYPE=Dev`), replacing `*`.
  The rate limit lives in the Vercel dashboard, not the repo: a Firewall rule, "Booking per-IP rate
  limit", caps `/api/vroom/*` at 30 requests/min per IP (fixed window, 429 past it). Proven live:
  35 requests returned 30 × 404 then 5 × 429.

- **2026-09** **Heroku decommissioned.** The `vroom-api` app and its add-ons were destroyed on
  2026-09-04 after three days of parallel running with zero real traffic. A final pre-destroy dump
  was taken and row-matched against Neon on every table before deletion. Its scheduler add-on held no active job.

- **2026-09** **Off Heroku onto Vercel.** The API is served from `vroom-api.crystalprism.io`;
  it keeps using the `crystalprism` database, now on Neon (project `old-sun-58330819`,
  PostgreSQL 18), shared with the main API and pause, so it is covered by that database's
  nightly dump.

  **The frontend's base URL is not in any committed file.** `vroom` reads it from the Netlify
  environment variable `VITE_SERVER_PATH`, set on all four deploy contexts to
  `https://vroom-api.crystalprism.io/`. **The trailing slash is load-bearing** — `src/api.ts`
  builds its one request as `` `${SERVER_PATH}api/vroom/booking` ``, concatenating directly. A
  Vite env var is baked in at build time, so changing it requires a redeploy, not just a save.

## Next

