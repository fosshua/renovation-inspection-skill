## Why

Renovation quality review currently depends on manual expert inspection, which is slow, inconsistent, and difficult to scale from casual photo, video, or text submissions. A dedicated AI skill can turn homeowner or project-manager inputs into structured construction issue detection, severity ranking, and standards-based improvement advice.

## What Changes

- Add a renovation inspection skill that accepts images, videos, and text describing an active renovation or completed construction detail.
- Analyze submitted evidence for construction quality, safety, compliance, workmanship, and sequencing issues.
- Reference national standards as the primary normative basis, and use major-company decoration standards as secondary benchmarks when national standards are absent or less specific.
- Retrieve and compare high-quality construction examples to improve judgment precision and explain what “good” looks like.
- Return findings sorted by severity, with evidence, likely risk, applicable reference basis, and actionable optimization suggestions.
- Include uncertainty handling when visual evidence is incomplete, ambiguous, or insufficient for a confident conclusion.

## Capabilities

### New Capabilities

- `renovation-inspection-skill`: Covers multimodal renovation input handling, AI construction issue detection, standards-backed severity assessment, reference-image comparison, and recommendation output.

### Modified Capabilities

None.

## Impact

- Adds a new skill workflow and related prompt, input, retrieval, analysis, and output contracts.
- Requires access to multimodal model capabilities for image and video inspection.
- Requires a standards knowledge source covering relevant Chinese national standards and curated major-company renovation standards.
- Requires an image/reference retrieval mechanism for high-quality construction examples.
- May introduce storage, privacy, and retention considerations for user-submitted home renovation media.
