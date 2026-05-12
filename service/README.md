# Home Renovation Assistant Service

Deployable API service for the home renovation inspection skill. It supports WeChat official-account callbacks and WeChat Mini Program inspection calls.

## What It Does

- Handles WeChat official-account/test-account callback verification.
- Receives official-account text and image messages.
- Provides Mini Program JSON and `wx.uploadFile` inspection endpoints.
- Runs inspection through an external backend, OpenAI-compatible multimodal model, or deterministic fallback mode.

## Environment

Copy `.env.example` to your deployment environment variables. Do not commit real secrets.

Required:

- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`
- `WECHAT_TOKEN`: the callback token you configure in the WeChat test account page.

Optional:

- `INSPECTION_BACKEND_URL`: your home-renovation inspection API endpoint. If empty, the service returns a fallback "received" message.
- `INSPECTION_BACKEND_TOKEN`: optional bearer token for the inspection backend.
- `OPENAI_API_KEY`: enables the built-in OpenAI-compatible multimodal inspection mode when no external backend is configured.
- `OPENAI_BASE_URL`: default `https://api.openai.com/v1`.
- `OPENAI_MODEL`: default `gpt-4o-mini`.
- `UPLOAD_DIR`: default `uploads`.
- `REPLY_TIMEOUT_SECONDS`: default `4`.
- `PUBLIC_BASE_URL`: public HTTPS origin used to build uploaded image URLs, for example `https://your-domain.example.com`.

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
python3 -m venv .venv
. .venv/bin/activate
pip install -r service/requirements.txt
uvicorn service.app:app --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## Mini Program API

Add your deployed HTTPS domain to the Mini Program `request` and `uploadFile` legal domain allowlists before calling these endpoints from WeChat.

JSON request with an image URL:

```bash
curl -X POST http://127.0.0.1:8000/api/mini/inspect \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-openid",
    "text": "帮我看看这张装修图片",
    "image_url": "https://example.com/window-gap.jpg"
  }'
```

File upload request:

```bash
curl -X POST http://127.0.0.1:8000/api/mini/inspect-upload \
  -F "user_id=test-openid" \
  -F "text=帮我看看这张图" \
  -F "file=@../.codex/skills/renovation-inspection/tests/fixtures/images/window-bottom-gap.jpg"
```

Mini Program example:

```js
wx.request({
  url: 'https://your-domain.example.com/api/mini/inspect',
  method: 'POST',
  data: {
    user_id: openid,
    text: '帮我看看这张装修图片',
    image_url: imageUrl
  },
  success(res) {
    console.log(res.data.answer)
  }
})

wx.uploadFile({
  url: 'https://your-domain.example.com/api/mini/inspect-upload',
  filePath,
  name: 'file',
  formData: {
    user_id: openid,
    text: '帮我看看这张图'
  },
  success(res) {
    console.log(JSON.parse(res.data).answer)
  }
})
```

## Docker

Build from the repository root:

```bash
docker build -f service/Dockerfile -t home-renovation-assistant .
```

Run:

```bash
docker run --rm -p 8000:8000 \
  -e WECHAT_APP_ID="$WECHAT_APP_ID" \
  -e WECHAT_APP_SECRET="$WECHAT_APP_SECRET" \
  -e WECHAT_TOKEN="$WECHAT_TOKEN" \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  home-renovation-assistant
```

## WeChat Test Account

In the WeChat test account page, configure:

- URL: `https://your-domain.example.com/wechat/callback`
- Token: same as `WECHAT_TOKEN`

For local testing, expose the service through a tunnel such as Cloudflare Tunnel, ngrok, or another HTTPS reverse proxy.

## Current Limitations

- Image handling currently passes WeChat `PicUrl` to the inspection backend. For production, download images to object storage first because WeChat media URLs may expire or be inaccessible to third-party services.
- WeChat callback replies are synchronous. If the model takes longer than WeChat's callback window, the service returns a fallback message. Production should move detection to a background task and use customer-service messages or an H5 result page.
- Mini Program calls can wait longer than WeChat callbacks, but production should still use async tasks for large images or video.
- Secrets should be rotated if exposed in chat, logs, or command history.
