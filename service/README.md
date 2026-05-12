# Home Renovation Assistant API

Lightweight WeChat test-account service for the home renovation inspection skill.

## What It Does

- Handles WeChat test-account callback verification.
- Receives text and image messages.
- Forwards text/image messages to a configurable inspection backend.
- Returns a short WeChat text reply in the inspection report format.

## Environment

Copy `.env.example` to your deployment environment variables. Do not commit real secrets.

Required:

- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`
- `WECHAT_TOKEN`: the callback token you configure in the WeChat test account page.

Optional:

- `INSPECTION_BACKEND_URL`: your home-renovation inspection API endpoint. If empty, the service returns a fallback "received" message.
- `INSPECTION_BACKEND_TOKEN`: optional bearer token for the inspection backend.
- `REPLY_TIMEOUT_SECONDS`: default `4`.
- `PUBLIC_BASE_URL`: reserved for future public asset hosting.

The inspection backend should accept:

```json
{
  "user_id": "wechat-openid",
  "session_id": "wechat-openid",
  "message_type": "image",
  "text": "",
  "image_url": "https://...",
  "source": "wechat"
}
```

It should return JSON with one of `answer`, `content`, `text`, `message`, or `msg`, or plain text.

## Run Locally

```bash
cd service
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## WeChat Test Account

In the WeChat test account page, configure:

- URL: `https://your-domain.example.com/wechat/callback`
- Token: same as `WECHAT_TOKEN`

For local testing, expose the service through a tunnel such as Cloudflare Tunnel, ngrok, or another HTTPS reverse proxy.

## Current Limitations

- Image handling currently passes WeChat `PicUrl` to the inspection backend. For production, download images to object storage first because WeChat media URLs may expire or be inaccessible to third-party services.
- Replies are synchronous. If the model takes longer than WeChat's callback window, the service returns a fallback message. Production should move detection to a background task and use customer-service messages or an H5 result page.
- Secrets should be rotated if exposed in chat, logs, or command history.
