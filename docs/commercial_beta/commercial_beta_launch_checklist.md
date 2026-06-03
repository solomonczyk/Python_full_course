# Commercial Beta Launch Checklist

## Product

- [x] 92 lessons + 9 recaps available and tested
- [x] Mission checker verified (58 students, 0 critical blockers)
- [x] Progress persistence backend tested and verified
- [x] Progress restore across devices working
- [x] Beta code generation and validation flow working
- [x] Feedback channel / form available
- [ ] **Beta landing copy ready** — written, needs frontend integration
- [ ] **Beta code flow documented** — operator instructions for issuing codes
- [ ] **Progress restore instructions written** — one-page guide for parents

## Commercial

- [x] **Offer ready** — `docs/commercial_beta/commercial_beta_offer.md`
- [x] **Price hypothesis ready** — `docs/commercial_beta/pricing_hypothesis.md`
- [x] **FAQ ready** — `docs/commercial_beta/commercial_beta_faq.md`
- [x] **Access rules ready** — `docs/commercial_beta/beta_access_rules.md`
- [ ] **Beta limitations clear on all pages** — check every touchpoint (landing, payment link, post-purchase)
- [ ] **Payment link created** — Stripe payment link or similar for manual payment processing
- [ ] **Beta code delivery flow defined** — how does the parent receive the code after payment? (email, manual, in-app?)
- [ ] **Refund policy defined** — manual, but documented

## Safety / Privacy

- [x] **No child personal data collected** — verified in analytics payloads
- [x] **No raw beta-code in analytics** — participant_id is hashed
- [x] **No payment data stored in the product** — payment is external
- [x] **No external analytics provider connected** — analytics is custom, self-hosted
- [ ] **Privacy summary visible before beta code entry** — one-page notice
- [ ] **COPPA/GDPR-K compliance reviewed** — out of scope for this layer but should be documented

## Technical

- [ ] Backend tests pass
- [ ] Frontend type-check passes
- [ ] Frontend build passes
- [ ] Playwright smoke tests pass (if frontend changed)

## Decision

- [x] Ready for commercial beta (documentation layer)
- [ ] Not ready for mass paid launch (requires payment layer, parent dashboard, accounts, privacy policy)

---

## Launch Day Checklist

- [ ] Issue first beta code to test the full purchase → code → access flow
- [ ] Confirm progress persistence works for the first paid participant
- [ ] Confirm analytics export returns data for the first paid participant
- [ ] Monitor support channel for first 24 hours after first paid participant
- [ ] Confirm refund process works (manual test)
