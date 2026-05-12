## 1. OpenSpec

- [x] 1.1 Create proposal, design, spec, and tasks for deployable Mini Program API.
- [x] 1.2 Validate the OpenSpec change.

## 2. Service API

- [x] 2.1 Add Mini Program JSON inspection endpoint.
- [x] 2.2 Add Mini Program multipart image upload endpoint.
- [x] 2.3 Normalize text/image inputs into one inspection request shape.
- [x] 2.4 Preserve existing WeChat callback verification and message handling.

## 3. Inspection Engine

- [x] 3.1 Add external backend forwarding mode.
- [x] 3.2 Add OpenAI-compatible multimodal mode using bundled skill instructions.
- [x] 3.3 Add deterministic fallback mode for deployments without model credentials.
- [x] 3.4 Keep secrets in environment variables only.

## 4. Deployment

- [x] 4.1 Add Dockerfile for service deployment.
- [x] 4.2 Update service environment example.
- [x] 4.3 Update service README with Mini Program and deployment instructions.

## 5. Validation

- [x] 5.1 Add service tests for health and WeChat callback verification.
- [x] 5.2 Add service tests for Mini Program JSON and upload inspection.
- [x] 5.3 Run Python compile checks.
- [x] 5.4 Run service tests.
- [x] 5.5 Run OpenSpec validation.

## 6. Publishing

- [ ] 6.1 Commit implementation changes.
- [ ] 6.2 Push main branch update.
