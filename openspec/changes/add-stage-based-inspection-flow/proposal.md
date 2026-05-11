## Why

The current renovation inspection skill analyzes visible issues directly, but it does not consistently anchor the inspection in the construction stage. Renovation quality judgment is more reliable when the skill first identifies the stage, then checks the relevant standards, expected work products, and common defects for that stage.

## What Changes

- Add a stage-based inspection flow before issue detection.
- Require the skill to classify the current construction stage from images, video, and text.
- Add a stage knowledge reference that maps each stage to applicable standards, required checks, common issues, and recommended evidence.
- Require findings to compare observed evidence against both stage-specific standards and common-stage defect patterns.
- Add behavior for ambiguous or mixed-stage inputs, including multiple candidate stages and targeted evidence requests.
- Extend validation fixtures to cover stage recognition and stage-specific issue comparison.

## Capabilities

### New Capabilities

- `stage-based-inspection-flow`: Covers construction-stage recognition, stage-specific standards retrieval, common issue comparison, and stage-aware recommendations for the renovation inspection skill.

### Modified Capabilities

None.

## Impact

- Updates `.codex/skills/renovation-inspection/SKILL.md` workflow.
- Adds a new stage reference file under `.codex/skills/renovation-inspection/references/`.
- Updates validation checklist and fixture descriptions.
- May require future expansion of the standards source list as more stages and trade-specific checks are added.
