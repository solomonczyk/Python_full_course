# Production Operator Key Verification

## What OPERATOR_KEY Protects

The `OPERATOR_KEY` environment variable controls access to **operator endpoints** in the staged beta access system:

| Endpoint | Method | Auth Required | Purpose |
|---|---|---|---|
| `/beta/access/{code}/operator-unlock` | POST | `X-Operator-Key` header | Unlocks next stage for a participant |
| `/beta/access/operator/pending-feedback` | GET | `X-Operator-Key` header | Lists participants needing review |

Without a valid key, these endpoints return HTTP 401/403 with `{"detail": "Invalid operator key"}`.

The `GET /beta/access/{code}` (read participant state) and `POST /beta/access/{code}/provide-feedback` (submit feedback) endpoints do NOT require operator auth — they are designed for participants and parents.

## Why Default Dev Key Is Forbidden in Production

The codebase contains a default dev key:

```python
OPERATOR_KEY = os.environ.get("OPERATOR_KEY", "op-python-quest-dev-2026")
```

This default (`op-python-quest-dev-2026`) is **only** for local development. In production:

- The key MUST be overridden via a Vercel environment variable
- The default key MUST be rejected in production (test verified: returns 401)
- The default key is committed to git in the source code, so anyone with repo access knows it
- A unique production key prevents unauthorized unlocks even if the source is leaked

## How Operator Unlock Is Tested

The verification script (`scripts/verify_operator_key.py`) performs these checks:

1. **Missing key** — Call `operator-unlock` without `X-Operator-Key` header → 401/403
2. **Wrong key** — Call with a fabricated wrong key → 401/403
3. **Default dev key** — Call with `op-python-quest-dev-2026` → 401/403 (in production)
4. **Real key (no feedback)** — Call with real key but no feedback → rejected by feedback gate
5. **Submit feedback** — Post feedback for dummy participant → confirmed
6. **Real key (after feedback)** — Call with real key after feedback → unlocks stage
7. **Pending feedback (no key)** — Access pending list without key → 401/403
8. **Pending feedback (with key)** — Access pending list with real key → returns data

Each test uses only dummy participant codes (prefixed `VRFY-` or `TEST-`). No real student data is ever used.

## How to Rotate OPERATOR_KEY Safely

**Prerequisites:** Vercel CLI authenticated as project owner.

### Rotate key (no downtime):
```bash
# 1. Generate new key (example — use your own secure generation)
NEW_KEY=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9!@#-' | head -c 32)

# 2. Update in Vercel (piped to stdin, never echoed to terminal)
echo "$NEW_KEY" | vercel env update OPERATOR_KEY production --yes

# 3. Redeploy to apply the new key
vercel --prod --yes
```

The key is **never displayed** during this process. It is stored encrypted in Vercel.

### Verify rotation:
```bash
# Save new key temporarily (without displaying)
echo "$NEW_KEY" > /tmp/pq_verify_temp.txt
# Run verification
python scripts/verify_operator_key.py
# Clean up
rm /tmp/pq_verify_temp.txt
```

## What NOT to Log or Commit

### Never commit:
- The actual `OPERATOR_KEY` value
- `.env` files containing `OPERATOR_KEY`
- Vercel env dumps
- CI logs containing the key

### Never log:
- The `OPERATOR_KEY` value (use `is_set: bool` in logs, not the value)
- The `X-Operator-Key` header value in request logs
- Environment variable dumps to log files

### Safe to commit:
- `OPERATOR_KEY = os.environ.get("OPERATOR_KEY", "op-python-quest-dev-2026")` — this is the env var read pattern, not the production value
- `$OPERATOR_KEY` in documentation — this is a shell variable reference, not a value
- Test keys (`"op-python-quest-dev-2026"`) in test files — these are well-known test values

## What to Do If Key Is Missing or Invalid

### In production:
| Symptom | Action |
|---|---|
| `OPERATOR_KEY` not set in Vercel | **BLOCKER.** Set immediately via `vercel env add OPERATOR_KEY production`, then redeploy |
| Still using default dev key | Same as missing — set a unique production key and redeploy |
| Key rotation failed | Check Vercel env, redeploy, test with verification script |
| `operator-unlock` returns 401 with real key | Check that env var was picked up by latest deploy; verify with `vercel env ls production` |
| Key exposed (leaked) | **Immediate rotation required.** Generate new key, update Vercel, redeploy. |

### Verification checklist:
```bash
# 1. Confirm key is set (not the value, just that it exists)
vercel env ls production | grep OPERATOR_KEY

# 2. Confirm operator endpoint rejects unauthorized requests
vercel curl -X POST "$URL/api/beta/access/TEST-CHECK/operator-unlock" \
  -H "Content-Type: application/json" -d '{}'

# 3. Confirm operator endpoint works with real key
vercel curl -X POST "$URL/api/beta/access/TEST-CHECK/operator-unlock" \
  -H "Content-Type: application/json" \
  -H "X-Operator-Key: $OPERATOR_KEY" -d '{}'
```

**Important:** Never pass the key value directly in a command that will be logged in CI or terminal history. Use environment variables or piped stdin.

## Security Design Principles

1. **Defense in depth** — Vercel Deployment Protection (SSO) protects the production URL at the infrastructure layer. The OPERATOR_KEY adds application-level protection for beta access control.
2. **Fail closed** — Missing or invalid key always returns 401/403, never allows access.
3. **No secret in code** — The production key exists only in Vercel encrypted storage.
4. **Auditable** — Every verification step is documented with proof artifacts.
5. **Feedback gate** — Even with a valid key, unlock requires prior feedback submission.
