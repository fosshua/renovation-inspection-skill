## Context

The repository currently contains OpenSpec artifacts only, so this change defines the intended behavior and implementation approach for a new Codex-style skill rather than modifying an existing application module. The skill will help users inspect renovation construction from photos, videos, and text, with outputs grounded in Chinese national standards first, supplemented by standards from reputable decoration companies and visual comparison against high-quality施工 examples.

Primary stakeholders are homeowners, renovation project managers, inspectors, and implementers who need the skill to produce traceable, severity-ranked findings instead of vague visual impressions. Because submitted media may contain private home interiors, the design must treat media handling, retention, and source citation as first-class concerns.

## Goals / Non-Goals

**Goals:**

- Provide a reusable skill workflow for multimodal renovation inspection.
- Accept image, video, and text evidence, including combinations of these inputs.
- Produce structured findings sorted by severity, with evidence, risk, standards basis, and improvement recommendations.
- Prefer national standards as authoritative references and use enterprise standards only as supplemental benchmarks.
- Retrieve and compare high-quality construction reference images when they improve visual judgment.
- Express uncertainty when the available evidence cannot support a confident conclusion.

**Non-Goals:**

- Replace licensed工程监理, structural engineers, electricians, plumbers, or legal compliance review.
- Guarantee hidden-work quality for concealed plumbing, wiring, waterproofing, or structural work not visible in the submitted evidence.
- Build a full standards database, crawl all enterprise standards, or implement live image search inside this proposal.
- Make final legal or warranty determinations.

## Decisions

1. **Use a staged inspection pipeline.**

   The skill will process each request through input normalization, media evidence extraction, standards retrieval, reference-example retrieval, issue analysis, severity ranking, and final response generation. This keeps multimodal perception, retrieval, and judgment separable and testable.

   Alternative considered: a single large prompt that directly analyzes all inputs. That is simpler, but it makes citation, uncertainty handling, and future source upgrades harder to control.

2. **Make national standards the primary authority.**

   Retrieval will rank applicable national standards above enterprise standards. Enterprise standards can clarify workmanship expectations, but the output must label them as secondary references and must not imply they override national standards.

   Alternative considered: merge all standards into one undifferentiated knowledge base. That would be easier to query but could misrepresent the authority of different sources.

3. **Use reference images as comparative evidence, not normative law.**

   High-quality construction images will be used to compare observable features such as waterproofing height, tile gap consistency, pipe routing, socket box alignment, putty flatness, drain slope, and protection measures. The final finding must distinguish visual best-practice comparison from standard-based compliance.

   Alternative considered: use reference images as pass/fail labels. That would be brittle because construction details vary by region, phase, material, and site constraints.

4. **Return structured, severity-ranked findings.**

   Each issue will include severity, category, observed evidence, risk, reference basis, recommendation, confidence, and whether more evidence is needed. This supports consistent downstream rendering and review.

   Alternative considered: free-form narrative output. That is easier for quick answers, but it makes severity ordering and auditability weaker.

5. **Support video through representative evidence extraction.**

   Video inputs will be sampled into key frames or time-coded observations before inspection. Findings from video must include timestamps or frame references when possible.

   Alternative considered: treat video as an opaque file summary. That loses traceability and makes it hard for users to verify where an issue was observed.

## Risks / Trade-offs

- **Incomplete or low-quality media may cause false positives or missed issues** -> The skill must report confidence, list missing evidence, and avoid definitive claims when evidence is insufficient.
- **Standards can change and may differ by project type or locality** -> Standards sources must include version/date metadata where available, and the output must identify the basis used rather than claiming universal coverage.
- **Enterprise standards may be proprietary or inconsistent** -> Use them only when source provenance is clear, and label them as supplementary best-practice benchmarks.
- **Reference images can bias judgment toward one construction style** -> Retrieve multiple examples where possible and compare observable attributes instead of aesthetic similarity.
- **Home renovation media may contain private information** -> Implementation must avoid unnecessary retention, redact or avoid exposing sensitive content in logs, and document storage behavior.
- **The skill may be mistaken for a professional inspection report** -> Responses must include a concise limitation note when issues involve safety, structure, electrical, waterproofing, or legal compliance.

## Migration Plan

This is a new capability with no migration from existing behavior. Implementation can be introduced as a new skill directory, then validated with representative image, video, and text fixtures before enabling it for regular use.

Rollback is to remove or disable the new skill entry and its retrieval configuration; no existing capability should depend on it.

## Open Questions

- Which exact national standards will be included in the initial standards corpus, and how will updates be tracked?
- Which enterprise standards are legally usable as references, and what citation format should be used?
- Will reference-image retrieval use an internal curated gallery, external search, or both?
- What media retention policy should apply to user-uploaded renovation photos and videos?
