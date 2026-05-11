## 1. Skill Structure

- [x] 1.1 Create the renovation inspection skill directory and required skill metadata.
- [x] 1.2 Add the main skill instructions for scope, limitations, input handling, and output style.
- [x] 1.3 Define the structured inspection output schema with severity, category, evidence, risk, reference basis, recommendation, confidence, and missing evidence fields.

## 2. Input Processing

- [x] 2.1 Implement image input handling that preserves per-image evidence references.
- [x] 2.2 Implement video input handling with representative frame or timestamp extraction guidance.
- [x] 2.3 Implement text-context handling for renovation stage, room, trade, material, and user concern details.
- [x] 2.4 Add insufficient-evidence handling that asks for specific missing views or measurements.

## 3. Standards Retrieval

- [x] 3.1 Define the initial national-standard source list and metadata fields, including standard number, title, version or date, applicable scenario, and citation text.
- [x] 3.2 Define the supplemental enterprise-standard source list and mark each source as non-authoritative best-practice guidance.
- [x] 3.3 Implement retrieval ranking rules that prefer applicable national standards over enterprise standards.
- [x] 3.4 Add fallback behavior for findings based on visual or practical judgment when no reliable source applies.

## 4. Reference Image Comparison

- [x] 4.1 Define the reference-image source strategy, using a curated gallery, external retrieval, or both.
- [x] 4.2 Implement comparison guidance for observable attributes such as alignment, spacing, slope, protection, routing, flatness, waterproofing height, and installation completeness.
- [x] 4.3 Ensure output distinguishes reference-image comparison from standards-based compliance.

## 5. Inspection Reasoning

- [x] 5.1 Implement the staged analysis flow: normalize inputs, extract evidence, retrieve standards, retrieve references, detect issues, rank severity, and produce output.
- [x] 5.2 Define severity levels and ranking criteria based on safety risk, compliance risk, quality impact, rework cost, and urgency.
- [x] 5.3 Add high-risk escalation guidance for structural, electrical, gas, waterproofing, fire-safety, and similar issues.
- [x] 5.4 Add uncertainty and confidence rules to prevent unsupported hidden-work conclusions.

## 6. Privacy and Safety

- [x] 6.1 Document media privacy expectations and retention assumptions in the skill.
- [x] 6.2 Ensure logging guidance avoids raw private media and sensitive home-identifying details.
- [x] 6.3 Add limitation language that the skill is not a replacement for qualified professional inspection.

## 7. Validation

- [x] 7.1 Create representative test fixtures for image-only, video-only, text-only, and mixed-input inspections.
- [x] 7.2 Validate outputs include all required structured fields for every finding.
- [x] 7.3 Validate national standards are prioritized over enterprise standards in cited basis.
- [x] 7.4 Validate ambiguous or insufficient evidence produces missing-evidence guidance instead of definitive claims.
- [x] 7.5 Run OpenSpec validation for the change and fix any reported issues.
