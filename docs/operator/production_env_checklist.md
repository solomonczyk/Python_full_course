# Production Environment Checklist

## Required Before Real Beta Participants

### Backend / API

- [ ] **OPERATOR_KEY set in production** — Run: `echo $OPERATOR_KEY` on the production server. Must return a non-empty, non-default value.
- [ ] **Default dev operator key not accepted in production** — Verify that `op-python-quest-dev-2026` returns 403 for operator endpoints.
  ```bash
  curl -X POST -H "X-Operator-Key: op-python-quest-dev-2026" \
    https://python-quest.vercel.app/api/beta/access/TEST-CODE/operator-unlock
  # Expected: 403 Invalid operator key
  ```
- [ ] **Beta access endpoints available** — Verify:
  ```bash
  curl https://python-quest.vercel.app/api/beta/access/TEST-CODE
  # Expected: 200 with valid response
  ```
- [ ] **Locked lesson returns 403** — Attempt to access a lesson from Part 2 without unlocking. Must return 403.
- [ ] **Operator unlock works** — Test the full unlock flow with a test code.
- [ ] **Feedback requirement works** — Verify that unlock without feedback is rejected: `"Feedback required before unlock"`.

### Frontend

- [ ] **Locked lessons visible** — Part 2 and Part 3 lessons show as locked in the UI.
- [ ] **Locked message clear** — The lock message explains staged access and what to do.
- [ ] **Feedback form visible** — Feedback form is accessible after Part 1 completion.
- [ ] **Part 1 access works** — Entering a valid beta code grants access to Part 1.
- [ ] **Part 2 locked by default** — Without unlock, Part 2 shows as locked.

### CI / Deploy

- [ ] **GitHub Actions green** — All workflows pass on the main branch.
- [ ] **Vercel Ready** — Latest deployment shows "Ready" in Vercel dashboard.
- [ ] **Backend tests pass** — Run:
  ```bash
  cd backend && python -m pytest tests/ -v
  ```
- [ ] **Frontend build passes** — Run:
  ```bash
  cd frontend && npm run build
  ```

### Privacy / Safety

- [ ] **No child personal data collected** — Verify no database table stores name, email, phone, age, address, or school of children.
- [ ] **No payment data** — No payment form, no Stripe/Paddle integration, no pricing page exposed.
- [ ] **No child profiles** — No registration, no login, no account creation flow.
- [ ] **No raw beta-code in analytics** — Check analytics events. Beta codes must not appear in event payloads.

## Production Blockers

| Condition | Action |
|---|---|
| **OPERATOR_KEY missing** | 🔴 BLOCKER — Set OPERATOR_KEY in Vercel environment variables immediately. Do not start beta. |
| **Default dev key works in production** | 🔴 BLOCKER — Fix key validation. The dev key `op-python-quest-dev-2026` must be rejected in production. |
| **Direct URL bypass works** | 🔴 BLOCKER — Stop beta immediately. Fix access control. |
| **GitHub Actions red** | 🔴 BLOCKER — Fix failing workflows before adding real participants. |
| **Vercel failed** | 🔴 BLOCKER — Deploy must be healthy before beta starts. |

## Pre-Launch Verification Command

Run this sequence to verify production readiness:

```bash
# 1. Check operator key is set
echo "OPERATOR_KEY is set: $([ -n "$OPERATOR_KEY" ] && echo YES || echo NO)"

# 2. Test beta access endpoint
curl -s https://python-quest.vercel.app/api/beta/access/TEST-CODE | python -m json.tool

# 3. Verify dev key is rejected
curl -s -o /dev/null -w "%{http_code}" \
  -X POST -H "X-Operator-Key: op-python-quest-dev-2026" \
  https://python-quest.vercel.app/api/beta/access/TEST-CODE/operator-unlock

# Expected: 403

# 4. Run backend tests
cd backend && python -m pytest tests/ -v --tb=short | tail -5

# 5. Run frontend build
cd frontend && npm run build 2>&1 | tail -5

# 6. Check git status
cd frontend && git status --short
```
