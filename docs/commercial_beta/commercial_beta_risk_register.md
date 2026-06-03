# Commercial Beta Risk Register

| ID | Risk | Severity | Probability | Mitigation | Status |
|----|------|----------|-------------|------------|--------|
| CBR-001 | Parent expects final polished product despite beta labelling | 🟠 Major | Medium | Landing copy and FAQ repeatedly state "commercial beta — not a finished product." Beta access rules require explicit acknowledgment. Microcopy on payment page reiterates beta status. | Active |
| CBR-002 | Student loses motivation after first section | 🟠 Major | Medium | Course is designed with progressive difficulty and narrative momentum. If analytics show a drop-off point, the feedback channel allows targeted investigation. Consider adding a "what's next" preview after each quest. | Active |
| CBR-003 | Analytics incomplete for commercial decisions | 🟡 Minor | Low | Analytics export endpoint exists (GET /analytics/export). Data is in-memory (lost on server restart — known issue WBT-0002). Mitigation: migrate analytics to persistent storage before scaling commercial beta. | Active — tracked as WBT-0002 |
| CBR-004 | Backend progress persistence failure under commercial load | 🔴 Critical | Low | Backend has been tested with 58 concurrent participants at 100% persistence success. Load testing above 100 concurrent participants has not been performed. Mitigation: limit commercial beta group size to 50–100 participants initially. | Active |
| CBR-005 | Payment/legal layer not ready — parent expects automated purchase | 🟠 Major | Medium | The offer and FAQ explicitly state "payment is manual — no automated payment flow." The payment page is a separate link, not part of the product. Manual processing adds operational overhead but prevents scope creep. | Active — accepted constraint |
| CBR-006 | Privacy wording not final — parent concerns about child data | 🟠 Major | Medium | FAQ and access rules clearly state "no child personal data collected." No personal data fields exist in any payload. Mitigation: add a one-page privacy summary visible before beta code entry. Formal privacy policy (COPPA/GDPR-K) is out of scope for this layer but should be prepared before scale beyond 100 participants. | Active |
| CBR-007 | Support load underestimated — team cannot respond within 2 business days | 🟠 Major | Medium | Commercial beta group size is limited. Feedback is reviewed in batches. If support load exceeds capacity, options include: (a) pausing new beta entries, (b) extending response SLA to 5 business days, (c) adding a FAQ-driven self-help section. | Active |
| CBR-008 | Beta code shared publicly, leading to unauthorised access | 🟡 Minor | Low | Beta codes are 64-char hex strings — effectively unguessable. Risk is voluntary sharing by a participant. Mitigation: terms of use state "keep your beta code private." If abuse is detected, the code can be invalidated and a new one issued. | Active |
| CBR-009 | Parent expects full course (all future topics) within beta access period | 🟠 Major | Medium | FAQ and offer clearly state "the beta covers fundamentals — advanced topics are not available yet." The lesson list is visible on the quest map, so parents can see the available scope. Mitigation: add a "course scope" section to the landing page that lists what is and is not covered. | Active |
| CBR-010 | Post-beta transition confusion — parent does not understand what happens after 12 weeks | 🟠 Major | Medium | FAQ addresses post-beta process. Mitigation: send a reminder email 2 weeks before beta access expires (requires email collection — only parent email, no child data). If email collection is not yet implemented, display an in-product banner 2 weeks before expiry. | Active |

---

## Risk Summary

| Severity | Count | Action |
|----------|-------|--------|
| 🔴 Critical | 1 | CBR-004 — monitor group size, limit to 100 participants |
| 🟠 Major | 7 | CBR-001, CBR-002, CBR-005, CBR-006, CBR-007, CBR-009, CBR-010 — mitigate via clear communication and group size control |
| 🟡 Minor | 2 | CBR-003, CBR-008 — track but low priority |

## Risk Status Legend

| Status | Meaning |
|--------|---------|
| **Active** | Risk is present and being monitored |
| **Mitigated** | Risk has been addressed but not eliminated |
| **Closed** | Risk has passed or has been fully resolved |
| **Accepted** | Risk is acknowledged and accepted without further action |
