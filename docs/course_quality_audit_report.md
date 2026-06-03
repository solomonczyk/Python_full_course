# Course Quality Audit Report

**Generated:** 2026-06-03T05:54:25.281218+00:00

## Summary

- **Total entities checked:** 1347
- **Total issues found:** 19

### Severity Breakdown

- ⏳ **can_defer**: 0
- 🚨 **must_fix_now**: 0
- 🔍 **needs_human_review**: 17
- 💅 **non_blocking_polish**: 2

### Items Checked

| Surface | Count |
|---------|-------|
| chapter_quests | 5 |
| code_examples | 103 |
| dialogue_blocks | 1000 |
| lessons | 92 |
| mission_blocks | 92 |
| quests | 6 |
| recaps | 9 |
| reviews | 40 |

### Inventory Summary

| Entity | Count |
|--------|-------|
| Lessons | 92 |
| Recaps | 9 |
| Quests | 6 |
| Chapter Quests | 5 |
| Reviews | 40 |

## Audit Checks Enabled

| Audit | Status |
|-------|--------|
| ✅ Structural audit | Enabled — checks required fields, data types, empty strings |
| ✅ Pedagogical prerequisite audit | Enabled — checks premature concepts in tasks/dialogues |
| ✅ Task-answer consistency audit | Enabled — checks task/answer match, code formatting |
| ✅ Dialogue quality audit | Enabled — checks character roles, Bagus, spoilers, length |
| ✅ Wording clarity audit | Enabled — checks risky pedagogical phrasing |
| ✅ Surface coverage audit | Enabled — checks missing educational blocks |
| ✅ Skill progression map | Enabled — references scripts/config/skill_progression.json |

## Safe Auto-Fix Policy

Only auto-fix issues that are structurally obvious and low-risk:

**Allowed:**
- Missing text copied from caption field
- Whitespace cleanup (trailing spaces, extra blank lines)
- Multiline code formatting if source clearly has line breaks
- Duplicated accidental spaces
- Typo in obvious field label

**Forbidden:**
- Changing teaching logic, expected answers, or checker behavior
- Rewriting dialogues, changing lesson order, or changing mission goal
- Mass content rewrites without human review
