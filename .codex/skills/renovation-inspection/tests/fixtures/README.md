# Renovation Inspection Fixtures

Use these fixtures to validate the skill manually or in automated prompt tests. Each fixture describes the expected behavior; media placeholders can be replaced with real test assets.

## Fixture 1: Image-Only Waterproofing

Input:
- `image_1`: Bathroom wall/floor waterproofing photo.

Expected:
- Findings preserve `image_1`.
- Waterproofing concerns cite national or industry waterproofing sources when applicable.
- If height or continuity cannot be measured, output requests ruler/level/close-up evidence.

## Fixture 2: Video-Only Plumbing Rough-In

Input:
- `video_1`: Short walkthrough of bathroom/kitchen pipe routing.

Expected:
- Findings use timestamp or frame references.
- Drainage slope, pipe fixing, and crossing concerns are qualified if not measurable.
- Hidden pressure-test conclusions are not made without records.

## Fixture 3: Text-Only User Concern

Input:
- "厨房墙砖有几处空鼓，师傅说没问题，可以继续装橱柜吗？"

Expected:
- Output explains risk and next checks.
- Requests location, area, hollowing extent, tile size, and photos/video before definitive severity.
- Does not invent visual evidence.

## Fixture 4: Mixed Electrical Evidence

Input:
- `image_1`: Open wall chase with conduits and socket boxes.
- Text: "这是卧室水电阶段，准备封槽。"

Expected:
- Findings preserve `image_1`.
- Electrical risks cite electrical installation sources when applicable.
- High-risk findings recommend responsible contractor or qualified electrician review before closure.

## Fixture 5: Insufficient Evidence

Input:
- Blurry close-up with no room or component context.

Expected:
- Output contains no definitive pass/fail claim.
- `evidence_gaps` lists exact missing views, measurements, and context.
