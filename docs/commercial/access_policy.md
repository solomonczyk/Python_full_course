# Python Quest Access Policy

## Access Modes

| Mode | Access Level | Who |
|------|-------------|-----|
| **Demo access** | Free, no account required | Anyone visiting the landing page |
| **Beta access** | Free, no account required | First test students and observers |
| **Future paid access** | Paid, requires account system | Not implemented in this layer |

---

## Demo Access
- **What is available:**
  - Landing page with product description, hero section, How It Works, and FAQ.
  - "Start Quest" CTA that leads into the first lesson experience.
  - A limited interactive preview (first lesson or first quest).
  - Character dialogue sample (Ва introduces the steampunk world).
- **What is blocked:**
  - Full course access beyond the demo threshold.
  - Progress persistence (demo progress may not carry to a full account in the future).
  - Parent dashboard (not yet implemented).
- **CTA after demo:**
  - "Continue the Quest — Join Beta" — invites user to proceed into beta access with the understanding that feedback may be requested.

## Beta Access
- **Who can enter:**
  - First test students (5–10 initial participants, expanding after iteration).
  - Beginner-level learners aged 10–16 (or younger with parent support).
  - Parents/operators observing the experience.
  - Tutors or educators evaluating the product for potential classroom use.
- **What is included:**
  - Full access to all 92 lessons and 9 recaps.
  - All quests, missions, character dialogues, and skill progression.
  - Mission Checker feedback and hints.
  - Progress tracking (session-based, anonymous).
- **What feedback is expected:**
  - Which lessons were confusing or too hard.
  - Where motivation dropped.
  - UI/UX issues encountered.
  - Parent/operator observations.
  - Willingness to pay (if the product were paid).

## Future Paid Access
- **Not implemented in this layer.**
- **Requires separate payment/legal/privacy layer:**
  - Payment processor integration (Stripe, etc.).
  - Student account system with email/password or OAuth.
  - Privacy policy and terms of service.
  - Parental consent mechanism (for children under data protection regulations).
  - Purchase flow (one-time or subscription).
  - Account recovery and customer support.

## Data Policy For Beta
- **No sensitive child personal data:** The beta does not collect names, emails, phone numbers, precise ages, or any personal identifiers of children.
- **No payment data in this layer:** Beta is free. Payment credentials are never requested or stored.
- **Anonymous analytics only:** Events are tracked with anonymous session IDs (client-generated, no link to personal identity).
- **Parent/operator feedback may be collected manually:** Feedback forms or interviews are conducted with adults (parents/operators), not directly with children. Adult feedback collection follows standard data protection practices.

## Forbidden Until Separate Layer

The following are explicitly out of scope for the current beta and require a dedicated implementation layer with legal and privacy review:

| Feature | Reason |
|---------|--------|
| Payments | Requires payment processing, legal terms, refund policy |
| Parent dashboard with personal profiles | Requires account system, data storage, privacy policy |
| Child account system | Requires parental consent mechanism, COPPA/GDPR compliance |
| Email marketing automation | Requires consent collection, opt-out mechanism, privacy policy |
| Cross-session named progress | Requires accounts — anonymous session-only for beta |
| Third-party analytics SDK (Google Analytics, etc.) | May transmit personal data automatically — requires privacy review |
| Social sharing / referral features | May expose child's activity to social networks |
