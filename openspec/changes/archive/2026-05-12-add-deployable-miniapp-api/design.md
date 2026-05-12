## Architecture

The service remains a lightweight FastAPI application. It exposes:

- `/wechat/callback` for WeChat official-account callback verification and message handling.
- `/api/mini/inspect` for Mini Program JSON requests with text and optional image URL.
- `/api/mini/inspect-upload` for Mini Program `wx.uploadFile` multipart requests.
- `/health` for deployment checks.

The service contains an inspection engine abstraction:

- If `INSPECTION_BACKEND_URL` is configured, forward requests to that backend.
- Else if `OPENAI_API_KEY` is configured, call an OpenAI-compatible multimodal endpoint using the bundled skill instructions.
- Else return a deterministic fallback response that confirms the gateway is reachable and explains the missing backend configuration.

## Mini Program Contract

`POST /api/mini/inspect`

```json
{
  "user_id": "openid-or-app-user-id",
  "session_id": "optional-session-id",
  "text": "帮我看看这张图",
  "image_url": "https://..."
}
```

`POST /api/mini/inspect-upload`

Multipart fields:

- `file`: image file from `wx.uploadFile`
- `user_id`: user identifier
- `session_id`: optional session identifier
- `text`: optional user text

## Security

- WeChat credentials, model keys, and backend tokens must be environment variables.
- Uploaded files are stored under a configurable local upload directory for MVP deployment.
- Production deployment should use object storage before public scale.

## Non-goals

- Full project management, database-backed issue tracking, and async report delivery.
- Permanent media hosting or long-term object storage integration.
- A polished Mini Program frontend.
