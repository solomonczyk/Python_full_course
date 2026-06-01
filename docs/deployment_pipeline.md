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
| Auto-deploy | Enabled — push/merge to `master` triggers production deploy |

## How Deployment is Triggered

### Normal workflow (GitHub → Vercel)

1. Developer creates a PR from `feature/*` or `fix/*` branch.
2. PR is reviewed and merged into `master` via GitHub.
3. GitHub push to `master` triggers Vercel webhook.
4. Vercel builds from the pushed commit and deploys to production.
5. Production URL: `https://python-full-course.vercel.app`

### Emergency fallback (Vercel CLI)

If GitHub integration is unavailable (outage, permission issue), deploy manually:

```bash
npx vercel --prod
```

**This is emergency-only.** The primary deployment path must be
GitHub → Vercel auto-deploy.

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

## Environment Variables

The following environment variables are set in Vercel Dashboard
(not committed to `vercel.json` for security):

| Variable | Purpose |
|----------|---------|
| `DB_PATH` | Path to SQLite database (`/tmp/progress.db` in production) |

No secrets (API keys, tokens) are used by this project.

## Verifying Deployed Commit

### Via Vercel Dashboard

1. Go to [Vercel → Deployments](https://vercel.com/andy-s-projects26/python-full-course/deployments)
2. The latest production deployment shows the Git commit hash and message.
3. Compare with `git log` on `master`.

### Via Vercel CLI

```bash
# List deployments
npx vercel list

# Inspect latest production deployment
npx vercel inspect $(npx vercel list | grep "Production" | head -1 | awk '{print $3}')

# Check for git metadata in the JSON output
npx vercel inspect <deployment-url> --format=json | jq '.meta'
```

The `meta` field should contain:
- `meta.githubCommitSha` — the deployed commit hash
- `meta.githubCommitMessage` — the commit message
- `meta.githubOrg` — `solomonczyk`
- `meta.githubRepo` — `Python_full_course`

## Verification Protocol

When confirming a GitHub-triggered deployment:

1. Push a commit to `master`.
2. Within 1–3 minutes, Vercel starts a new deployment.
3. Verify the deployment source is `github` (not CLI).
4. Verify the deployed commit matches the pushed commit.
5. Verify production URLs respond:
   - `https://python-full-course.vercel.app/` — home page
   - `https://python-full-course.vercel.app/lesson/1-1` — lesson page
   - `https://python-full-course.vercel.app/api/lessons/1-1` — API

## Why GitHub → Vercel Auto-Deploy?

1. **Traceability** — every production deployment links to a commit and PR.
2. **CI/CD** — enables future CI checks before production deploy.
3. **Reliability** — no dependency on a single developer's local environment.
4. **Audit trail** — deployment metadata includes commit hash and author.

The CLI deploy path (`npx vercel --prod`) exists only as an emergency
fallback and should not be used for routine deployments.
