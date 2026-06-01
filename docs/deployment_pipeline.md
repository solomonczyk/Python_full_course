# Vercel → GitHub Deployment Pipeline

## Overview

This document describes the production deployment pipeline for **Python Full
Course** (Vercel project `andy-s-projects26/python-full-course`).

## Connected Repository

| Field | Value |
|-------|-------|
| GitHub repo | [`solomonczyk/Python_full_course`](https://github.com/solomonczyk/Python_full_course) |
| Vercel project | `andy-s-projects26/python-full-course` |
| Production branch | `master` |
| Auto-deploy | Enabled via GitHub Actions + Vercel Deploy Hook |
| Deploy hook URL | `https://api.vercel.com/v1/integrations/deploy/prj_OiUzohnPa84Tcd088T5K9XzFqfrV/4MTCFBO3i7` |

## How Deployment is Triggered

### Primary workflow (GitHub Actions → Vercel Deploy Hook)

1. Developer pushes to `master` or merges a PR.
2. GitHub Actions workflow `.github/workflows/deploy.yml` triggers.
3. Workflow calls the Vercel Deploy Hook (POST request).
4. Vercel builds from the repository and deploys to production.
5. Production URL: `https://python-full-course.vercel.app`

### Native Vercel GitHub Integration (Recommended, requires Dashboard setup)

The native Vercel GitHub app integration is **not yet fully authorized**. The repo is
connected (`vercel git connect` confirmed), but auto-deploy on push requires the
Vercel GitHub app to be installed in the repository.

**To complete the native integration:**

1. Go to [Vercel Dashboard → python-full-course → Settings → Git](https://vercel.com/andy-s-projects26/python-full-course/settings/git).
2. Click **"Connect Git Repository"** (if shown) or verify the connection.
3. If GitHub authorization is requested, authorize the Vercel GitHub app for
   `solomonczyk/Python_full_course`.
4. Set **Production Branch** to `master`.
5. Verify **Auto-deploy** is enabled for the production branch.

Once the native integration is active, push/merge to `master` will automatically
trigger a Vercel production deploy without relying on GitHub Actions.

### Emergency fallback (Vercel CLI)

If both automation paths are unavailable, deploy manually from your local machine:

```bash
npx vercel --prod
```

**This is emergency-only.** The primary deployment path must be
GitHub-triggered (Actions or native integration).

## Project Settings

| Setting | Value |
|---------|-------|
| Root directory | `.` (project root) |
| Framework preset | Other |
| Build command | `cd frontend && npm install && npm run build` |
| Output directory | `frontend/dist` |
| Install command | `npm install` (default) |
| Node.js version | 24.x |

### vercel.json

```json
{
  "version": 2,
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "functions": {
    "api/index.py": { "maxDuration": 10 }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" },
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "env": {
    "DB_PATH": "/tmp/progress.db"
  }
}
```

### Vercel Deploy Hook

- Name: `github-push`
- Branch: `master`
- ID: `4MTCFBO3i7`
- URL (sensitive): `https://api.vercel.com/v1/integrations/deploy/prj_OiUzohnPa84Tcd088T5K9XzFqfrV/4MTCFBO3i7`

This hook is called by the GitHub Actions workflow on push to `master`.

### GitHub Actions Workflow

Created at `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Vercel deploy hook
        run: |
          curl -s -X POST "${{ secrets.VERCEL_DEPLOY_HOOK_URL }}" > /dev/null
          echo "Vercel deploy triggered from GitHub Actions"
```

## Environment Variables

The following environment variables are set in Vercel Dashboard
(not committed to `vercel.json` for security):

| Variable | Purpose |
|----------|---------|
| `TURSO_AUTH_TOKEN` | Turso database authentication |
| `TURSO_DATABASE_URL` | Turso database connection URL |
| `DEEPSEEK_API_KEY` | DeepSeek API access |
| `DB_PATH` | Path to SQLite database (`/tmp/progress.db` in production) |

## Verifying Deployed Commit

### Via Vercel Dashboard

1. Go to [Vercel → Deployments](https://vercel.com/andy-s-projects26/python-full-course/deployments).
2. The latest production deployment shows the deploy timestamp and status.
3. Compare deployed lesson data with `git log` on `master`.

### Via Production API

Compare lesson content between local and production:

```bash
# Check lesson 1-2 Bagus lines from production
curl -s https://python-full-course.vercel.app/api/lessons/1-2 | \
  python3 -c "import sys,json;d=json.load(sys.stdin);b=[x for x in d['post_error_dialogue'] if x['character']=='bagus'];print(len(b))"

# Compare with local (after fix: 1, before fix: 2)
python3 -c "import json;d=json.load(open('backend/app/data/lessons.json',encoding='utf-8'));b=[x for x in d if x['id']=='1-2'][0];print(len([x for x in b['post_error_dialogue'] if x['character']=='bagus']))"
```

## Verification Protocol

When confirming a GitHub-triggered deployment:

1. Push a commit to `master`.
2. GitHub Actions workflow runs → calls Vercel Deploy Hook.
3. Vercel starts a new production deployment (typically 30–60s).
4. Verify production URLs respond:
   - `https://python-full-course.vercel.app/` — home page
   - `https://python-full-course.vercel.app/lesson/1-1` — lesson page (SPA)
   - `https://python-full-course.vercel.app/api/lessons/1-1` — API (JSON)
5. Verify the deployed commit matches expected content via the API endpoint.

## Why GitHub → Vercel Auto-Deploy?

1. **Traceability** — every production deployment links to a commit.
2. **CI/CD** — enables automated checks before production deploy.
3. **Reliability** — no dependency on a single developer's local environment.
4. **Audit trail** — deployment metadata documents who deployed what.

The CLI deploy path (`npx vercel --prod`) exists only as an emergency
fallback and should not be used for routine deployments.

## Setup History

- Git repo connected to Vercel project: ✅ `vercel git connect` (2026-06-01)
- Build settings configured in `vercel.json`: ✅ Pre-existing
- Vercel Deploy Hook created: ✅ `github-push` → `master` (2026-06-01)
- GitHub Actions workflow created: ✅ `.github/workflows/deploy.yml` (2026-06-01)
- Vercel GitHub app authorized in Dashboard: ❌ Requires manual step
