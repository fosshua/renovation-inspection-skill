## ADDED Requirements

### Requirement: Deployable service runtime
The service SHALL be runnable as a deployable FastAPI application with documented environment variables and health checks.

#### Scenario: Health check
- **WHEN** a client calls `GET /health`
- **THEN** the service SHALL return a successful JSON health response

#### Scenario: Container runtime
- **WHEN** the service is built from the repository Dockerfile
- **THEN** it SHALL start the FastAPI app on the configured port

### Requirement: WeChat callback support
The service SHALL support WeChat official-account callback verification and text/image message handling.

#### Scenario: Callback verification
- **WHEN** WeChat sends a signed callback verification request
- **THEN** the service SHALL validate the signature and echo `echostr`

#### Scenario: Image message fallback
- **WHEN** WeChat sends an image message and no inspection backend is configured
- **THEN** the service SHALL return a text response confirming receipt and listing useful evidence to supplement

### Requirement: Mini Program inspection API
The service SHALL expose Mini Program compatible inspection endpoints.

#### Scenario: JSON inspection request
- **WHEN** a Mini Program sends text and optional image URL to `POST /api/mini/inspect`
- **THEN** the service SHALL return JSON with `answer`, `session_id`, and `status`

#### Scenario: Multipart image upload request
- **WHEN** a Mini Program uploads an image file to `POST /api/mini/inspect-upload`
- **THEN** the service SHALL store the file, run inspection with the uploaded image reference, and return JSON with `answer`, `session_id`, and `status`

### Requirement: Inspection backend abstraction
The service SHALL support multiple inspection execution modes without changing the public API.

#### Scenario: External backend configured
- **WHEN** `INSPECTION_BACKEND_URL` is set
- **THEN** the service SHALL forward normalized inspection payloads to that backend

#### Scenario: Model provider configured
- **WHEN** model provider credentials are set and no external backend is configured
- **THEN** the service SHALL call the model provider with the renovation inspection skill instructions

#### Scenario: No backend configured
- **WHEN** no backend or model provider is configured
- **THEN** the service SHALL return a deterministic fallback response instead of failing

### Requirement: Service tests
The service SHALL include tests for the deployable API surface.

#### Scenario: Local validation
- **WHEN** the service tests are run
- **THEN** they SHALL cover health, WeChat verification, Mini Program JSON inspection, Mini Program upload inspection, and fallback behavior
