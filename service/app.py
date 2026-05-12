import hashlib
import os
import time
import xml.etree.ElementTree as ET
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Request, Response


app = FastAPI(title="Home Renovation Assistant")


def env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def verify_wechat_signature(signature: str, timestamp: str, nonce: str) -> bool:
    token = env("WECHAT_TOKEN")
    raw = "".join(sorted([token, timestamp, nonce]))
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()
    return digest == signature


def parse_wechat_xml(body: bytes) -> dict[str, str]:
    root = ET.fromstring(body)
    parsed: dict[str, str] = {}
    for child in root:
        parsed[child.tag] = child.text or ""
    return parsed


def text_reply(to_user: str, from_user: str, content: str) -> str:
    escaped = (
        content.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f"""<xml>
<ToUserName><![CDATA[{to_user}]]></ToUserName>
<FromUserName><![CDATA[{from_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{escaped}]]></Content>
</xml>"""


def truncate_wechat_text(text: str, limit: int = 1800) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n结果较长，已截断。请回复“继续”或补充图片继续分析。"


async def call_inspection_backend(
    user_id: str,
    message_type: str,
    text: str,
    image_url: str | None,
    session_id: str,
) -> str:
    backend_url = os.getenv("INSPECTION_BACKEND_URL", "")
    if not backend_url:
        return fallback_reply(message_type, text, image_url)

    payload: dict[str, Any] = {
        "user_id": user_id,
        "session_id": session_id,
        "message_type": message_type,
        "text": text,
        "image_url": image_url,
        "source": "wechat",
    }

    timeout = float(os.getenv("REPLY_TIMEOUT_SECONDS", "4"))
    headers = {"Content-Type": "application/json"}
    backend_token = os.getenv("INSPECTION_BACKEND_TOKEN", "")
    if backend_token:
        headers["Authorization"] = f"Bearer {backend_token}"

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(backend_url, headers=headers, json=payload)
        resp.raise_for_status()

    return extract_backend_text(resp.text)


def extract_backend_text(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return "已收到，但检测服务没有返回内容。"

    try:
        data = httpx.Response(200, text=raw).json()
    except Exception:
        data = None

    if isinstance(data, dict):
        for key in ("answer", "content", "text", "message", "msg"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return raw

    chunks: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("data:"):
            line = line[5:].strip()
        if line in ("[DONE]", "DONE"):
            continue
        chunks.append(line)
    return "\n".join(chunks) if chunks else raw


def fallback_reply(message_type: str, text: str, image_url: str | None) -> str:
    if message_type == "image" or image_url:
        return (
            "已收到图片。当前微信入口已联通，但家装检测后端还未配置。\n\n"
            "上线检测后，我会按以下结构返回：\n"
            "1. 结论\n2. 可以直接发给施工方\n3. 问题清单\n4. 需要补充的证据\n5. 依据和限制\n\n"
            "为了提高判断准确度，建议继续补充：远景、标记问题位置、带尺近景、侧面角度或 10-20 秒视频。"
        )

    if text:
        return (
            "已收到。当前微信入口已联通，但家装检测后端还未配置。\n\n"
            "你可以发送装修现场图片；检测后端接入后，会自动识别施工阶段、问题风险和补拍建议。"
        )

    return "家装助手微信入口已联通。请发送装修现场图片或问题描述。"


def extract_message(message: dict[str, str]) -> tuple[str, str, str | None]:
    msg_type = message.get("MsgType", "")
    user_text = message.get("Content", "").strip()
    pic_url = message.get("PicUrl") or None
    return msg_type, user_text, pic_url


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/wechat/callback")
async def verify_callback(
    signature: str,
    timestamp: str,
    nonce: str,
    echostr: str,
) -> Response:
    if not verify_wechat_signature(signature, timestamp, nonce):
        raise HTTPException(status_code=403, detail="invalid signature")
    return Response(content=echostr, media_type="text/plain")


@app.post("/wechat/callback")
async def wechat_callback(request: Request) -> Response:
    signature = request.query_params.get("signature", "")
    timestamp = request.query_params.get("timestamp", "")
    nonce = request.query_params.get("nonce", "")
    if not verify_wechat_signature(signature, timestamp, nonce):
        raise HTTPException(status_code=403, detail="invalid signature")

    body = await request.body()
    message = parse_wechat_xml(body)
    to_user = message.get("FromUserName", "")
    from_user = message.get("ToUserName", "")
    session_id = f"wechat-{to_user or 'anonymous'}"

    msg_type, user_text, image_url = extract_message(message)
    try:
        result = await call_inspection_backend(
            user_id=to_user,
            message_type=msg_type,
            text=user_text,
            image_url=image_url,
            session_id=session_id,
        )
    except httpx.TimeoutException:
        result = "已收到，图片检测需要更长时间。请稍后再发“继续”查看，或补充远景/带尺近景帮助判断。"
    except Exception as exc:
        result = f"检测服务暂时不可用：{type(exc).__name__}。请稍后重试。"

    xml = text_reply(to_user, from_user, truncate_wechat_text(result))
    return Response(content=xml, media_type="application/xml")
