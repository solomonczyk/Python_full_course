# MiroFish Next Real World Test Plan: Python Quest
**Status**: PREPARED — Ready for execution  
**Goal**: Validate market demand before building custom platform  
**Philosophy**: Test with minimal resources; fail fast if needed; double down on signals

---

## Phase 1: Immediate Validation (Week 1-2)

### Test 1: Stepik MVP Upload
**Goal**: Validate content-market fit with zero platform investment

**Actions**:
1. Prepare 3 demo lessons from current `lessons.json`:
   - Lesson 1: print() — "Твой голос в коде"
   - Lesson 2: variables — "Коробки для хранения данных"
   - Lesson 3: input() — "Слушай пользователя"
2. Create Stepik course page with:
   - Title: "Python Quest: Побег из Башни Багуса (Демо)"
   - Description using Offer A text
   - Clear "This is 3 lessons from full course" messaging
3. Upload lessons as text-based steps (approximate character dialog in descriptions)
4. Set price: Free
5. Enable: Reviews, comments, enrollment tracking

**Success Metrics**:
- 100+ organic enrollments in first 30 days
- > 3.5 star average rating
- 5+ "Where is the full course?" comments
- < 20% bounce rate on first lesson

**Decision Gates**:
- ✅ 100+ enrollments → Proceed to Phase 2
- ⚠️ 50-100 enrollments → Extend, improve discoverability
- ❌ < 50 enrollments → **PIVOT**: Content or positioning needs rework

**Effort**: 2-3 days  
**Cost**: €0

---

### Test 2: Landing Page + Email Capture
**Goal**: Test offer resonance and willingness-to-pay signals

**Actions**:
1. Create simple single-page landing (can be Carrd, Tilda, or simple HTML)
2. Include:
   - Offer A headline (primary)
   - 2-sentence description
   - Screenshot of final game
   - 3 bullet benefits (characters, final game, no dry theory)
   - Email capture form: "Получить 3 бесплатных урока"
   - Optional: "Сообщить о запуске полной версии"
3. Set up simple email confirmation
4. Create basic analytics (page views, email captures)

**Variants to Test**:
- Variant A (primary): Offer A — Gaming angle
- Variant B: Offer C — Adult beginner angle (if traffic allows)

**Success Metrics**:
- > 15% email capture rate
- > 100 emails in first 2 weeks
- > 5 "When can I pay?" or "How much?" inquiries

**Decision Gates**:
- ✅ > 15% capture + price inquiries → Strong signal
- ⚠️ 8-15% capture → Messaging needs refinement
- ❌ < 8% capture → **NO-GO**: Value proposition not resonating

**Effort**: 1-2 days  
**Cost**: €0-20 (domain optional)

---

### Test 3: Community Pulse Check
**Goal**: Gather qualitative feedback from target segments

**Actions**:
1. **Python communities** (Reddit r/learnpython, local Python groups):
   - Post: "Testing concept: story-driven Python course with final game project — would this have helped you as a beginner?"
   - Ask for honest feedback, not signups
   - Track: Upvotes, comments, sentiment

2. **Parent communities** (local parent groups, education forums):
   - Post: "Would your teen stay engaged with a Python course taught through characters, missions, and game creation?"
   - Track: Engagement, "where can I try" responses

3. **AI/ML communities**:
   - Post: "For AI beginners: would a story-based Python foundation course be useful, or do you prefer traditional format?"
   - Track: Responses, objections raised

**Success Metrics**:
- 10+ substantive comments per post
- > 50% positive/neutral sentiment
- 2+ "I'd try this" per community

**Decision Gates**:
- ✅ Strong positive engagement → Proceed
- ⚠️ Mixed but constructive → Iterate positioning
- ❌ Overwhelmingly negative → **PIVOT**: Format or concept issue

**Effort**: 1 day  
**Cost**: €0

---

## Phase 2: Engagement Validation (Week 3-4)

### Test 4: Telegram Mini-Marathon
**Goal**: Test engagement format and content quality with real users

**Actions**:
1. Create Telegram channel: "Python Quest — 5-дневный марафон"
2. Structure:
   - Day 1: Intro + Lesson 1 (print)
   - Day 2: Lesson 2 (variables) + mini-quiz
   - Day 3: Lesson 3 (input) + "what outputs?" challenge
   - Day 4: Lesson 4 preview (if/else) + find the bug
   - Day 5: Mission task + "What's next" (full course pitch)
3. Recruit 20-30 participants from:
   - Email list from Test 2
   - Community posts from Test 3
   - Personal network (beginners)
4. Deliver content as:
   - Text explanations with character attribution
   - Code screenshots
   - Interactive polls for quizzes
   - Voice messages for character dialog (optional)

**Success Metrics**:
- > 60% complete all 5 days
- > 5 "When is the full course?" questions
- > 3 price inquiries
- > 50% daily engagement (polls, responses)

**Decision Gates**:
- ✅ > 60% completion + price inquiries → Strong engagement signal
- ⚠️ 40-60% completion → Content good, delivery needs work
- ❌ < 40% completion → **SOFT GO**: Content or format needs major rework

**Effort**: 5 days (spread over 2 weeks)  
**Cost**: €0

---

### Test 5: Pricing Sensitivity Survey
**Goal**: Determine viable price point before building payment infrastructure

**Actions**:
1. Send survey to email list from Test 2 (minimum 50 emails needed)
2. Questions:
   - "What best describes your interest in Python Quest?" (segment identification)
   - "Have you tried learning Python before?" (experience level)
   - "At what price would you consider this course: [€9, €19, €29, €39, €49, €79, >€100, Would not pay]"
   - "What would make you more likely to purchase?" (feature prioritization)
   - "What concerns do you have?" (objection discovery)
3. Offer incentive: "Survey participants get early access + 20% discount"

**Success Metrics**:
- > 30% survey response rate
- > 40% select €29-49 range
- < 20% select "Would not pay"
- Clear feature priority ranking

**Decision Gates**:
- ✅ > 40% at €29-49 + clear priorities → Proceed to paid test
- ⚠️ Split between €19 and €49 → Test both tiers
- ❌ > 30% "Would not pay" → **PIVOT**: Pricing or value proposition issue

**Effort**: 1 day  
**Cost**: €0

---

## Phase 3: Revenue Validation (Week 5-8)

### Test 6: Early Access Sale
**Goal**: Confirm willingness to pay with actual transactions

**Actions**:
1. Create simple payment page (Stripe, PayPal, or Buy Me a Coffee)
2. Offer: "Ранний доступ к Python Quest — часть 1 (уроки 1-10)"
3. Price: €19 (early bird)
4. Include:
   - 10 lessons from Part 1
   - Access to Telegram support group
   - Feedback surveys (required for iteration)
   - Full course upgrade option later
5. Sell to:
   - Email list (primary)
   - Telegram marathon completers (secondary)
   - Community posts (tertiary)

**Limitations**:
- No custom platform — deliver via PDF + GitHub + Telegram
- No progress tracking — manual checklist
- No fancy features — pure content value test

**Success Metrics**:
- 10+ sales in first 2 weeks
- > 70% content completion rate
- > 3 testimonials/reviews
- < 20% refund requests

**Decision Gates**:
- ✅ 10+ sales + good completion → **GO**: Build custom platform
- ⚠️ 5-10 sales → **SOFT GO**: Iterate content, expand marketing
- ❌ < 5 sales → **NO-GO**: Market not ready or positioning wrong

**Effort**: 3-4 days setup  
**Cost**: €0 (Stripe fees only on sales)

---

### Test 7: Positioning A/B Test
**Goal**: Determine best offer variant for each segment

**Actions**:
1. If traffic allows, create 2 landing variants:
   - Landing A: Offer A (Gaming angle)
   - Landing C: Offer C (Adult beginner — no "игра")
2. Drive equal traffic from:
   - Python communities (likely prefer C)
   - Gaming/teen communities (likely prefer A)
3. Measure: Email capture rate, qualitative feedback
4. Survey: "Which description resonated more with you?"

**Success Metrics**:
- Clear winner with > 20% difference in capture rate
- Qualitative feedback supports quantitative results

**Decision Gates**:
- ✅ Clear winner → Use for full launch
- ⚠️ Mixed results → Segment-specific positioning
- ❌ Both underperform → Messaging issue, not positioning

**Effort**: 1-2 days  
**Cost**: €0-50 (if using paid ads for traffic)

---

## Phase 4: Expansion Decision (Week 9-12)

### Decision Framework

Based on all tests, make GO / SOFT GO / PIVOT / NO-GO decision:

| Scenario | Stepik | Landing | Telegram | Pricing | Early Sales | Decision |
|----------|--------|---------|----------|---------|-------------|----------|
| Strong signals | 100+ | 15%+ | 60%+ | €29-49 | 10+ | **GO** |
| Good but patchy | 50-100 | 10-15% | 40-60% | €19-39 | 5-10 | **SOFT GO** |
| Weak engagement | < 50 | < 10% | < 40% | < €19 | < 5 | **PIVOT** |
| No interest | < 20 | < 5% | < 30% | mostly €0 | 0-1 | **NO-GO** |

### GO Path (Build Custom Platform)
**Conditions**: Strong signals across majority of tests

**Actions**:
1. Finalize content for all 5 parts
2. Build custom platform (3-6 months)
3. Implement: lessons, code execution, progress, basic auth
4. **Still delay**: payments (Stripe), comments (Discord integration), certificates
5. Launch with €39-49 price point
6. Add support tier (€79-99) after 100+ paid users

### SOFT GO Path (Iterate and Expand)
**Conditions**: Good signals but not strong enough for full platform investment

**Actions**:
1. Improve content based on feedback
2. Expand Stepik presence (all 5 parts)
3. Grow email list to 500+
4. Run another early access round
5. Build platform incrementally (revenue-funded)

### PIVOT Path (Change Direction)
**Conditions**: Weak engagement but some interest signals

**Consider**:
1. **Positioning pivot**: Adult-focused, remove characters
2. **Format pivot**: Video course instead of interactive
3. **Audience pivot**: Focus only on parents/teens
4. **Content pivot**: Different final project (chatbot vs game)

### NO-GO Path (Stop)
**Conditions**: No interest across tests

**Actions**:
1. Archive project
2. Document learnings
3. Consider: Open-source materials for community benefit

---

## Timeline Summary

| Week | Primary Test | Key Metric | Decision Point |
|------|--------------|------------|----------------|
| 1 | Stepik upload | 100+ enrollments | Proceed? |
| 1-2 | Landing page | 15%+ capture | Proceed? |
| 2 | Community pulse | Positive sentiment | Proceed? |
| 3-4 | Telegram marathon | 60%+ completion | Proceed? |
| 4 | Pricing survey | €29-49 acceptance | Proceed? |
| 5-6 | Early access sale | 10+ sales | GO/NO-GO |
| 7-8 | Positioning A/B | Clear winner | Final positioning |
| 9-12 | Build or iterate | — | Execute decision |

---

## Resource Requirements

| Phase | Time | Money | Skills Needed |
|-------|------|-------|---------------|
| 1 | 1 week | €0 | Content prep, copywriting |
| 2 | 2 weeks | €0 | Community engagement, survey design |
| 3 | 4 weeks | €0-50 | Basic payment setup, delivery logistics |
| 4 | 4 weeks | Variable | Development (if GO) |

**Total Validation Cost**: €0-50 + time  
**Risk**: Minimal — mostly time investment  
**Information Value**: Critical — prevents €15-30K wasted development

---

## Success Scenario (What Good Looks Like)

By end of Week 8:
- 200+ Stepik enrollments
- 150+ email captures (15% rate)
- 25 people completed Telegram marathon
- Survey: 50% willing to pay €39
- 15 early access sales at €19
- 3+ organic "When can I buy the full course?" per week

**Decision**: **GO** — Build custom platform with confidence

---

## Failure Scenario (When to Stop)

By end of Week 4:
- < 30 Stepik enrollments
- < 5% email capture
- Telegram marathon < 30% completion
- Survey: > 50% "Would not pay"
- Community posts: mostly negative or ignored

**Decision**: **NO-GO** or **PIVOT** — Market not responding, reassess fundamentals

---

## Next Immediate Actions (This Week)

1. **Today**: Prepare 3 lessons for Stepik format
2. **Tomorrow**: Create Carrd/Tilda landing page
3. **Day 3**: Upload to Stepik
4. **Day 4**: Post in 3 communities (Python, parents, AI)
5. **Day 5-7**: Monitor, respond to feedback, iterate messaging

**Checkpoint**: End of Week 1 — Do we have 50+ Stepik enrollments and 20+ emails? If yes, continue. If no, diagnose and adjust.

---

*This test plan prioritizes learning over building. The goal is to fail fast if the market isn't there, or double down if it is. Either outcome is valuable — uncertainty is not.*
