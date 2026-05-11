# Renovation Inspection Fixtures

Use these fixtures to validate the skill manually or in automated prompt tests. Each fixture describes the expected behavior; media placeholders can be replaced with real test assets.

## Fixture 1: Image-Only Waterproofing

Input:
- `image_1`: Bathroom wall/floor waterproofing photo.

Expected:
- Stage is identified as `waterproofing`.
- Findings preserve `image_1`.
- Waterproofing concerns cite national or industry waterproofing sources when applicable.
- If height or continuity cannot be measured, output requests ruler/level/close-up evidence.
- Stage package checks include corners, pipe roots, threshold treatment, wall upturn, coating continuity, and water test records where relevant.

## Fixture 2: Video-Only Plumbing Rough-In

Input:
- `video_1`: Short walkthrough of bathroom/kitchen pipe routing.

Expected:
- Stage is identified as `plumbing_electrical_rough_in`.
- Findings use timestamp or frame references.
- Drainage slope, pipe fixing, and crossing concerns are qualified if not measurable.
- Hidden pressure-test conclusions are not made without records.
- Stage package checks request pressure test, drainage test, conduit continuity, full-route photos, and crossing close-ups.

## Fixture 3: Text-Only User Concern

Input:
- "厨房墙砖有几处空鼓，师傅说没问题，可以继续装橱柜吗？"

Expected:
- Stage is identified as `tiling_flooring` or stage confidence is marked low if insufficient.
- Output explains risk and next checks.
- Requests location, area, hollowing extent, tile size, and photos/video before definitive severity.
- Explicitly tells the user they can supplement photos or a short tapping video for follow-up assessment.
- Does not invent visual evidence.

## Fixture 4: Mixed Electrical Evidence

Input:
- `image_1`: Open wall chase with conduits and socket boxes.
- Text: "这是卧室水电阶段，准备封槽。"

Expected:
- Stage is identified as `plumbing_electrical_rough_in`.
- Findings preserve `image_1`.
- Electrical risks cite electrical installation sources when applicable.
- High-risk findings recommend responsible contractor or qualified electrician review before closure.
- Findings include common issue matches only for visible issues or user-provided evidence.

## Fixture 5: Insufficient Evidence

Input:
- Blurry close-up with no room or component context.

Expected:
- Output contains no definitive pass/fail claim.
- Stage is marked low confidence or candidate stages are listed.
- `evidence_gaps` lists exact missing views, measurements, and context.
- Output invites the user to supplement clearer photos, video, measurements, or records as applicable.

## Fixture 6: Window Gap / Edge Finishing

Input:
- `image_1`: Window frame bottom edge with visible oversized gap to tile or floor finish.

Expected:
- Stage is identified as `window_door_installation`.
- Finding includes `stage_id`, `stage_name`, and common issue match for oversized frame-to-floor/tile gap.
- Output distinguishes authoritative standards from manufacturer/design-node guidance and visual comparison.
- Output requests ruler-based gap photo, interior/exterior sealant views, and water-spray or rain observation evidence.
