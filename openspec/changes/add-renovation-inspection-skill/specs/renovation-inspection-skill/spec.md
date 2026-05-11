## ADDED Requirements

### Requirement: Multimodal renovation input handling
The skill SHALL accept renovation inspection requests containing images, videos, text, or any combination of those inputs.

#### Scenario: Inspect image and text together
- **WHEN** the user provides one or more construction photos with a text description of the renovation stage
- **THEN** the skill SHALL analyze both the visual evidence and the text context as one inspection request

#### Scenario: Inspect video evidence
- **WHEN** the user provides a renovation video
- **THEN** the skill SHALL extract time-referenced visual observations or representative frames for inspection

#### Scenario: Handle insufficient input
- **WHEN** the submitted media or text is too unclear to support reliable inspection
- **THEN** the skill SHALL explain what evidence is missing and request the specific additional views or context needed

### Requirement: Construction issue detection
The skill SHALL detect visible renovation construction issues related to quality, safety, workmanship, material installation, sequencing, protection, and standards compliance.

#### Scenario: Detect visible workmanship defects
- **WHEN** submitted evidence shows observable defects such as uneven tile gaps, poor wall flatness, exposed wiring, missing protection, or improper waterproofing details
- **THEN** the skill SHALL identify each visible defect as a separate finding

#### Scenario: Avoid unsupported hidden-work claims
- **WHEN** hidden plumbing, wiring, waterproofing, or structural details are not visible in the evidence
- **THEN** the skill SHALL avoid definitive conclusions about those hidden conditions and SHALL state the evidence limitation

### Requirement: Standards-backed assessment
The skill SHALL use applicable Chinese national standards as the primary assessment basis and SHALL use reputable enterprise renovation standards only as supplemental references.

#### Scenario: National standard applies
- **WHEN** an issue maps to an applicable national standard requirement
- **THEN** the skill SHALL cite the national standard as the primary basis for the finding

#### Scenario: Enterprise standard supplements judgment
- **WHEN** no precise national standard is available but a reputable enterprise decoration standard provides relevant workmanship guidance
- **THEN** the skill SHALL label that source as a supplemental benchmark and SHALL NOT present it as overriding national standards

#### Scenario: Source basis is unavailable
- **WHEN** the skill cannot identify a reliable standard or benchmark for an observed concern
- **THEN** the skill SHALL mark the basis as visual or practical judgment and SHALL lower or qualify confidence accordingly

### Requirement: Reference construction comparison
The skill SHALL retrieve or use high-quality construction reference images when visual comparison would improve inspection accuracy.

#### Scenario: Compare against good construction examples
- **WHEN** a finding depends on visual workmanship comparison
- **THEN** the skill SHALL compare observable attributes of the submitted evidence against high-quality reference examples

#### Scenario: Distinguish comparison from compliance
- **WHEN** reference images are used to support a finding
- **THEN** the skill SHALL distinguish reference-image comparison from standards-based compliance judgment

### Requirement: Severity-ranked findings
The skill SHALL rank identified issues by severity and SHALL provide severity labels that reflect safety risk, compliance risk, quality impact, rework cost, and urgency.

#### Scenario: Return findings in severity order
- **WHEN** multiple issues are detected
- **THEN** the skill SHALL list critical or high-risk issues before medium and low-risk issues

#### Scenario: Explain severity
- **WHEN** the skill assigns a severity to a finding
- **THEN** the skill SHALL explain the risk factors that caused that severity level

### Requirement: Actionable optimization recommendations
For each finding, the skill SHALL provide practical optimization or remediation advice that is appropriate to the renovation stage and observed evidence.

#### Scenario: Provide remediation steps
- **WHEN** the skill reports a construction problem
- **THEN** the skill SHALL include concrete next actions such as stop-work checks, rework suggestions, measurement checks, material verification, or professional inspection escalation

#### Scenario: Escalate high-risk issues
- **WHEN** a finding involves structural safety, electrical safety, gas, waterproofing failure, fire safety, or other high-risk areas
- **THEN** the skill SHALL recommend review by a qualified professional or responsible contractor before work continues

### Requirement: Structured inspection output
The skill SHALL return inspection results in a structured format suitable for both human reading and downstream rendering.

#### Scenario: Include required fields for each finding
- **WHEN** the skill returns a finding
- **THEN** the finding SHALL include severity, category, observed evidence, risk, reference basis, recommendation, confidence, and needed additional evidence when applicable

#### Scenario: Include overall summary
- **WHEN** the skill completes an inspection
- **THEN** the output SHALL include an overall assessment summary and the most urgent next steps

### Requirement: Privacy-aware media handling
The skill SHALL treat user-submitted renovation photos and videos as private user media.

#### Scenario: Avoid unnecessary retention
- **WHEN** media is processed for inspection
- **THEN** implementation SHALL avoid retaining media longer than necessary for the inspection workflow unless the user or product policy explicitly allows retention

#### Scenario: Avoid sensitive log exposure
- **WHEN** implementation logs inspection processing
- **THEN** logs SHALL avoid storing raw private media content or sensitive home-identifying details unless required by explicit debugging configuration
