## Why

The renovation inspection skill can now identify construction stages, but it still needs stronger problem-discovery behavior inspired by professional inspection SOPs. Users need the tool to identify what is confirmed, what is only suspected, what has not been checked, whether the next construction step should proceed, and what evidence is needed to close the issue.

## What Changes

- Add stage-gate risk assessment to findings, especially whether the issue blocks the next construction step.
- Add evidence strength labels: `confirmed`, `suspected`, and `not_verifiable`.
- Add stage-specific missing-check lists so the skill reports what was checked and what remains unverified.
- Add next-shot guidance that tells users exactly which photos, videos, measurements, or records to provide next.
- Add rectification workflow fields for action, responsible party, reinspection evidence, and whether the issue blocks next-stage work.
- Add a common shortcut or poor-practice pattern library, such as using thick caulk to hide large window gaps or closing water/electrical chases before pressure tests.
- Add inspection completeness indicators for a stage, such as checked vs. unverified required checks.
- Keep the scope focused on problem discovery and issue closure, not full project management or contract enforcement.

## Capabilities

### New Capabilities

- `problem-discovery-sop-checks`: Covers stage-gate risk, evidence strength, missing-check reporting, next-shot guidance, rectification workflow, shortcut-pattern detection, and inspection completeness for the renovation inspection skill.

### Modified Capabilities

None.

## Impact

- Updates `.codex/skills/renovation-inspection/SKILL.md` output and reasoning workflow.
- Updates `references/output-schema.json` with problem-discovery fields.
- Adds or extends references for shortcut/poor-practice patterns and stage-gate checks.
- Updates validation checklist and fixtures to verify evidence strength, missing checks, next-shot guidance, and rectification closure.
