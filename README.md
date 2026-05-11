# Renovation Inspection Skill

Codex skill for inspecting residential renovation construction from images, videos, and text.

The skill helps identify visible construction quality, safety, workmanship, sequencing, and standards-related issues. It ranks findings by severity, cites applicable Chinese standards first, uses enterprise standards only as supplemental benchmarks, and includes remediation guidance plus uncertainty handling for insufficient evidence.

## Structure

- `.codex/skills/renovation-inspection/SKILL.md` - main skill instructions
- `.codex/skills/renovation-inspection/references/output-schema.json` - structured output contract
- `.codex/skills/renovation-inspection/references/standards-sources.yaml` - initial standards and benchmark source list
- `.codex/skills/renovation-inspection/references/reference-image-strategy.md` - reference image comparison rules
- `.codex/skills/renovation-inspection/references/severity-and-confidence.md` - severity and confidence rules
- `.codex/skills/renovation-inspection/tests/` - validation checklist and fixture descriptions

## Notes

Standards references must be verified against official or licensed sources before contractual, legal, or acceptance use. This skill is decision support and does not replace qualified engineering, inspection, or legal review.
