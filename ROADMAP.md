# Roadmap

Committed doc, not scratch. Kept current by hand as work ships.
**Shipped** = live in production. **Next** = intended, not promised.
**Declined** = decided against, with the reason, so it doesn't get re-proposed.
**Open questions** = unresolved calls, with what would settle them.

## Shipped

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
