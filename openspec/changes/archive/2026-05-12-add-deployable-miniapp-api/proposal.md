## Why

The repository now has a WeChat callback gateway, but it is not yet a complete deployable service for WeChat Mini Program access. It lacks a Mini Program HTTP API, direct image upload support, deployment packaging, and a built-in inspection backend adapter that can run without wiring an external service first.

## What Changes

- Add a deployable FastAPI service shape for both WeChat official-account callbacks and Mini Program HTTP calls.
- Add Mini Program endpoints for text/image URL inspection and multipart image upload inspection.
- Add an internal inspection engine abstraction with a fallback implementation and an OpenAI-compatible multimodal implementation.
- Package runtime configuration, Docker deployment, and health checks.
- Add lightweight tests for health, WeChat signature verification, Mini Program inspection request handling, upload handling, and fallback behavior.

## Capabilities

### New Capabilities

- `deployable-miniapp-api`: Provides deployable API service behavior for WeChat callback and Mini Program clients.

### Modified Capabilities

None.

## Impact

- Updates `service/` application code and documentation.
- Adds deployment artifacts such as `Dockerfile`.
- Adds tests and test dependencies for the service.
- Does not commit real WeChat secrets or model provider credentials.
