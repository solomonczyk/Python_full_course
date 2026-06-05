# Lesson Gap Policy

## Intentional Gaps

The following lesson IDs are intentionally absent from the current curriculum. They are reserved for future content.

### Missing IDs

| ID | Status | Reason |
|----|--------|--------|
| 5-5 | Reserved | Planned future lesson (topic TBD, likely file I/O) |
| 5-6 | Reserved | Planned future lesson (topic TBD, likely classes/OOP) |

### Coverage Gaps

The following Python topics are not covered in the current 92-lesson curriculum and are considered out of scope for the initial release:

| Topic | Status | Notes |
|-------|--------|-------|
| File I/O (`open`, `read`, `write`, `with` blocks) | Planned future module | Slots 5-5 and 5-6 reserved |
| Classes / OOP (`class`, `__init__`, methods, inheritance) | Planned future module | Slots 5-5 and 5-6 reserved |
| `try`/`except`/exception handling | Partially covered (error messages in missions) | Full lesson planned for future |
| `dict` type | Partially covered (analytics, JSON usage) | Dedicated lesson planned for future |

## Ordering Policy

- Lessons within a Part must appear in ascending `{chapter}.{lesson}` order.
- Cross-part ordering: Part N lessons all appear before Part N+1 lessons.
- Lesson `3-41` (Chapter 18, "Лестница отступов Багуса") is an intentional Part 3 capstone/reflection lesson placed after the Part 3 main content. Its chapter number (18) places it logically after the Part 3 main chapters (6-11) in the Part 3 ordering, and before Part 4 in the global sequence.

## Verification

- All lesson IDs in the JSON array must be unique.
- The display order must be: all Part 1 → all Part 2 → all Part 3 → all Part 4 → all Part 5.
- No Part X lesson may appear after a Part X+1 lesson in the array.
- Missing IDs must be documented here with a clear reason.
