# Setup — IamTharunsai/IamTharunsai

## 1. Create the special repo
1. GitHub → **New repository**
2. Repository name must be exactly: `IamTharunsai`
3. Public, check "Add a README" → Create.
   (If GitHub says "IamTharunsai/IamTharunsai already exists" — it already does, from your repo list. Just open it.)

## 2. Add the README + the two hand-made banner graphics
1. Replace the repo's README.md contents with `README.md` from this folder.
2. Also upload `hero-banner.svg` and `footer-banner.svg` from this folder into the **root** of the repo (same folder as README.md). These are the custom animated banners referenced at the top and bottom of the README — not a copy-paste template, built from scratch for this profile with an SVG editor's worth of gradients, a pulse-line sweep animation, and a "systems" node motif. If they're missing, those two banners just won't render.
3. Commit to `main`.

## 3. Turn on the two auto-updating graphics
These make the profile visibly reflect ongoing work — that was the whole point.

1. In the `IamTharunsai/IamTharunsai` repo, create the folder path `.github/workflows/`.
2. Add `snake.yml` (from this folder) at `.github/workflows/snake.yml`.
3. Add `profile-3d-contrib.yml` (from this folder) at `.github/workflows/profile-3d-contrib.yml`.
4. Add `fox-run.yml` (from this folder) at `.github/workflows/fox-run.yml`, plus `fox_run.py` in the repo root — this is the hand-built animated fox that runs your real contribution calendar (not a fork of the snake script).
5. Go to **Settings → Actions → General → Workflow permissions** → select **"Read and write permissions"** → Save.
   (All three workflows push commits back to your repo — without this they'll fail silently.)
6. Go to the **Actions** tab → run each workflow once manually ("Run workflow" button) instead of waiting for the schedule.
   - `generate snake animation` creates an `output` branch with the snake SVGs.
   - `3D profile contribution calendar` commits `profile-3d-contrib/*.svg` straight to `main`.
   - `fox run (custom contribution animation)` commits `fox-run.svg` straight to `main`.
7. Wait 1–2 minutes, refresh your profile page. All three images should now render instead of showing broken-image icons.

After this, the snake re-runs every 12 hours, the 3D graph every day, and the fox every day — pulling your real, current contribution data automatically. No further action needed.

## 4. Make sure the stats aren't empty
- If `github-readme-stats` shows 0s: GitHub's stats API undercounts by default for private repos. In the README, `count_private=true` is already set — but it only counts private repos you own, not org ones, and only if you're logged in when *you* view it (public viewers always see public-only counts — this is a GitHub API limitation, not fixable).
- If you want your private contributions (KytchenPulse, trading system, job-search AI repos) to count toward the green squares/streak at all: **Settings → Profile → "Include private contributions on my profile."**

## 5. Known things that are cosmetic, not bugs
- The 3D graph and snake images will show as broken links until step 3 finishes running once — that's expected on a brand-new repo.
- Trophy case and activity graph need at least a little public activity/stars to look full — they'll fill in as you push more.

## 6. If you want the real interactive 3D scroll site later
GitHub README can't run JavaScript or true scroll-driven 3D — that needs to live on a separate site (Three.js/GSAP, deployed free on GitHub Pages or Vercel) and get linked from the README's badge row. Say the word whenever you want that built — it's a separate project, not a README trick.
