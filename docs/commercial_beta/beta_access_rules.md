# Commercial Beta Access Rules

## Access Model

| Rule | Detail |
|------|--------|
| **Beta-code based access** | Each participant receives a unique beta code (64-character hex string). Entering the code unlocks full beta access and restores progress if returning. |
| **No child account** | No email/password registration. No OAuth. No username creation. The beta code is the sole credential. |
| **No password** | Beta codes are not passwords — they are access tokens. If the code is lost, the parent/operator contacts the team for a code reissue. |
| **No personal child data** | The beta system does not ask for or store the child's name, email, age, or any other personal identifier. The participant ID is a hash of the beta code. |

---

## Who Can Join

| Criteria | Detail |
|----------|--------|
| **Beginner students** | No prior programming experience needed. Age recommendation: 10–16. Younger learners may participate with parent assistance. |
| **Parent/operator consent** | By activating the beta code, the parent/operator confirms they understand this is a beta product and consent to the child's participation under the access rules. |
| **Limited beta group** | The commercial beta is a controlled group. Not everyone who requests access is guaranteed entry. The team reserves the right to limit the group size to ensure support quality. |
| **Geographic restrictions** | None initially — the product is browser-based and works in any modern browser. Pricing is in USD; localised pricing is not available in beta. |

---

## What User Receives

| Item | Description |
|------|-------------|
| **Beta code** | A unique 64-character hex string delivered after payment confirmation (or invitation acceptance for free/ discounted participants). |
| **Access instructions** | A one-page guide explaining how to enter the beta code, start the quest, and restore progress on a different device. |
| **Progress restore instructions** | If the student switches devices or clears browser data, re-entering the beta code on the landing page restores all progress from the backend. |
| **Feedback form / instructions** | A link to the feedback form (or embedded feedback UI). Participants are encouraged to report bugs, confusing lessons, and suggestions. |

---

## What User Must Understand

| Statement | Detail |
|-----------|--------|
| **This is beta** | The product is feature-complete but not mass-market polished. Some rough edges, wording adjustments, and minor UI issues may exist. |
| **Bugs may exist** | Despite thorough testing (58 students, 0 critical blockers), edge cases may surface. Reporting them helps improve the product. |
| **Feedback is expected** | Beta participants are active contributors. Reporting confusing lessons, hard missions, or UI issues is part of the beta agreement. |
| **Product is not final** | Lessons, missions, dialogue, and progression may change during beta. Some features may be added or removed. |
| **No guaranteed post-beta access** | The 12-week access period is the guaranteed minimum. Post-beta terms (if any) will be communicated separately. |

---

## Forbidden Without Separate Layer

| Action | Status | Reason |
|--------|--------|--------|
| **Payment automation** | ❌ Forbidden in beta | Payment is handled manually (Stripe payment link or invoice). No in-product payment flow. |
| **Parent dashboard** | ❌ Forbidden in beta | Requires a separate account system, privacy policy, and parent authentication layer. |
| **Child personal profile** | ❌ Forbidden in beta | No child accounts, no avatars, no personal data collection. Beta codes are anonymous. |
| **Email marketing automation** | ❌ Forbidden in beta | No email collection, no mailing list, no automated marketing campaigns. |
| **School deployment** | ❌ Forbidden in beta | Classroom management, teacher dashboards, and cohort tracking are out of scope for commercial beta. |
| **Data collection beyond anonymous analytics** | ❌ Forbidden in beta | Only anonymous session events are tracked. No behavioural profiling, no ad targeting, no data sharing with third parties. |
