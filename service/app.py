import hashlib
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import httpx
from fastapi import FastAPI, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from service.inspection import InspectionRequest, build_session_id, run_inspection


app = FastAPI(title="Home Renovation Assistant")

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


class MiniInspectRequest(BaseModel):
    user_id: str = Field(default="anonymous")
    session_id: str | None = None
    text: str = ""
    image_url: str | None = None


class InspectionResponse(BaseModel):
    answer: str
    session_id: str
    status: str
    engine: str


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


def extract_message(message: dict[str, str]) -> tuple[str, str, str | None]:
    msg_type = message.get("MsgType", "")
    user_text = message.get("Content", "").strip()
    pic_url = message.get("PicUrl") or None
    return msg_type, user_text, pic_url


def public_file_url(request: Request, file_name: str) -> str:
    public_base = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    if public_base:
        return f"{public_base}/uploads/{file_name}"
    return str(request.url_for("uploads", path=file_name))


async def save_upload(file: UploadFile) -> str:
    suffix = Path(file.filename or "upload.jpg").suffix.lower() or ".jpg"
    if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".heic"}:
        suffix = ".jpg"
    file_name = f"{int(time.time())}-{hashlib.sha1(os.urandom(16)).hexdigest()[:12]}{suffix}"
    target = UPLOAD_DIR / file_name
    content = await file.read()
    target.write_bytes(content)
    return file_name


async def inspect_request(req: InspectionRequest) -> InspectionResponse:
    result = await run_inspection(req)
    return InspectionResponse(
        answer=result.answer,
        session_id=result.session_id,
        status=result.status,
        engine=result.engine,
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/mini/inspect", response_model=InspectionResponse)
async def mini_inspect(payload: MiniInspectRequest) -> InspectionResponse:
    session_id = build_session_id(payload.user_id, payload.session_id)
    message_type = "image" if payload.image_url else "text"
    req = InspectionRequest(
        user_id=payload.user_id,
        session_id=session_id,
        message_type=message_type,
        text=payload.text,
        image_url=payload.image_url,
        source="miniapp",
    )
    return await inspect_request(req)


@app.post("/api/mini/inspect-upload", response_model=InspectionResponse)
async def mini_inspect_upload(
    request: Request,
    file: UploadFile = File(...),
    user_id: str = Form("anonymous"),
    session_id: str | None = Form(None),
    text: str = Form(""),
) -> InspectionResponse:
    file_name = await save_upload(file)
    image_url = public_file_url(request, file_name)
    resolved_session_id = build_session_id(user_id, session_id)
    req = InspectionRequest(
        user_id=user_id,
        session_id=resolved_session_id,
        message_type="image",
        text=text,
        image_url=image_url,
        source="miniapp_upload",
    )
    return await inspect_request(req)


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
    session_id = build_session_id(to_user, f"wechat-{to_user or 'anonymous'}")

    msg_type, user_text, image_url = extract_message(message)
    try:
        result = await run_inspection(
            InspectionRequest(
                user_id=to_user,
                session_id=session_id,
                message_type=msg_type,
                text=user_text,
                image_url=image_url,
                source="wechat",
            )
        )
        answer = result.answer
    except httpx.TimeoutException:
        answer = "已收到，图片检测需要更长时间。请稍后再发“继续”查看，或补充远景/带尺近景帮助判断。"
    except Exception as exc:
        answer = f"检测服务暂时不可用：{type(exc).__name__}。请稍后重试。"

    xml = text_reply(to_user, from_user, truncate_wechat_text(answer))
    return Response(content=xml, media_type="application/xml")
