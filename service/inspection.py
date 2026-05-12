import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx


ROOT_DIR = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT_DIR / ".codex" / "skills" / "renovation-inspection"


@dataclass
class InspectionRequest:
    user_id: str
    session_id: str
    message_type: str
    text: str = ""
    image_url: str | None = None
    source: str = "api"


@dataclass
class InspectionResult:
    answer: str
    session_id: str
    status: str = "ok"
    engine: str = "fallback"


def build_session_id(user_id: str | None, session_id: str | None = None) -> str:
    if session_id:
        return session_id
    if user_id:
        return f"user-{user_id}"
    return f"session-{uuid.uuid4().hex}"


async def run_inspection(req: InspectionRequest) -> InspectionResult:
    backend_url = os.getenv("INSPECTION_BACKEND_URL", "")
    if backend_url:
        answer = await call_external_backend(req, backend_url)
        return InspectionResult(answer=answer, session_id=req.session_id, engine="external_backend")

    if os.getenv("OPENAI_API_KEY"):
        try:
            answer = await call_openai_compatible(req)
            return InspectionResult(
                answer=answer,
                session_id=req.session_id,
                engine="openai_compatible",
            )
        except httpx.HTTPStatusError as exc:
            return InspectionResult(
                answer=model_error_reply(exc),
                session_id=req.session_id,
                status="provider_error",
                engine="openai_compatible",
            )

    return InspectionResult(
        answer=fallback_reply(req.message_type, req.text, req.image_url),
        session_id=req.session_id,
        engine="fallback",
    )


async def call_external_backend(req: InspectionRequest, backend_url: str) -> str:
    payload: dict[str, Any] = {
        "user_id": req.user_id,
        "session_id": req.session_id,
        "message_type": req.message_type,
        "text": req.text,
        "image_url": req.image_url,
        "source": req.source,
    }
    timeout = float(os.getenv("REPLY_TIMEOUT_SECONDS", "8"))
    headers = {"Content-Type": "application/json"}
    backend_token = os.getenv("INSPECTION_BACKEND_TOKEN", "")
    if backend_token:
        headers["Authorization"] = f"Bearer {backend_token}"

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(backend_url, headers=headers, json=payload)
        resp.raise_for_status()
    return extract_text(resp.text)


async def call_openai_compatible(req: InspectionRequest) -> str:
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    timeout = float(os.getenv("REPLY_TIMEOUT_SECONDS", "30"))
    endpoint = base_url.rstrip("/") + "/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": load_skill_prompt()},
            {
                "role": "user",
                "content": build_openai_user_content(
                    req,
                    supports_vision=model_supports_vision(base_url),
                ),
            },
        ],
        "temperature": 0.2,
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def model_supports_vision(base_url: str) -> bool:
    explicit = os.getenv("OPENAI_MODEL_SUPPORTS_VISION", "").strip().lower()
    if explicit in {"1", "true", "yes", "on"}:
        return True
    if explicit in {"0", "false", "no", "off"}:
        return False

    return "deepseek.com" not in base_url.lower()


def build_openai_user_content(
    req: InspectionRequest,
    supports_vision: bool,
) -> str | list[dict[str, Any]]:
    text = (
        req.text
        or "请作为家装施工问题检测助手，检查用户提供的装修证据，并按技能要求输出中文结果。"
    )
    if req.image_url and not supports_vision:
        text += (
            "\n\n注意：当前模型配置不支持直接读取图片。"
            f"用户提交了图片地址：{req.image_url}。"
            "请不要假装已经看到了图片，只能基于用户文字描述给出初步判断，"
            "并明确要求用户补充问题位置、尺寸、远景、带尺近景或改用视觉模型。"
        )

    if not supports_vision:
        return text

    user_content: list[dict[str, Any]] = [{"type": "text", "text": text}]
    if req.image_url and supports_vision:
        user_content.append({"type": "image_url", "image_url": {"url": req.image_url}})
    return user_content


def load_skill_prompt() -> str:
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    protocol = (SKILL_DIR / "references" / "evidence-capture-protocol.md").read_text(
        encoding="utf-8"
    )
    stage_matrix = (SKILL_DIR / "references" / "stage-inspection-matrix.yaml").read_text(
        encoding="utf-8"
    )
    shortcut_patterns = (SKILL_DIR / "references" / "shortcut-patterns.yaml").read_text(
        encoding="utf-8"
    )
    return "\n\n".join(
        [
            "Use the following renovation inspection skill and references.",
            skill,
            "# Evidence Capture Protocol",
            protocol,
            "# Stage Inspection Matrix",
            stage_matrix,
            "# Shortcut Patterns",
            shortcut_patterns,
        ]
    )


def extract_text(raw: str) -> str:
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


def model_error_reply(exc: httpx.HTTPStatusError) -> str:
    status_code = exc.response.status_code
    if status_code == 429:
        return (
            "检测模型当前触发限流或额度不足，图片已经到达本地服务，但暂时无法完成 AI 判断。\n\n"
            "你可以稍后重试，或切换/补充模型额度后再次提交。"
            "如果是现场验收场景，建议先补充远景、带尺近景和问题位置标注，后续重试时能提高判断准确度。"
        )

    if status_code in {401, 403}:
        return (
            "检测模型鉴权失败，请检查 `OPENAI_API_KEY`、模型权限或代理配置。"
            "本地 API 服务是可用的，但当前无法调用模型完成识别。"
        )

    if 500 <= status_code < 600:
        return (
            "检测模型服务暂时不可用。本地 API 服务已收到请求，请稍后重试，"
            "或临时切换 `INSPECTION_BACKEND_URL` / `OPENAI_MODEL`。"
        )

    return (
        f"检测模型返回异常状态 {status_code}。本地 API 服务已收到请求，"
        "但当前无法完成 AI 判断，请检查模型配置后重试。"
    )


def fallback_reply(message_type: str, text: str, image_url: str | None) -> str:
    if message_type == "image" or image_url:
        return (
            "已收到图片。当前 API 已联通，但检测模型后端还未配置。\n\n"
            "上线检测后，我会按以下结构返回：\n"
            "1. 结论\n2. 可以直接发给施工方\n3. 问题清单\n4. 需要补充的证据\n5. 依据和限制\n\n"
            "为了提高判断准确度，建议继续补充：远景、标记问题位置、带尺近景、侧面角度或 10-20 秒视频。"
        )

    if text:
        return (
            "已收到。当前 API 已联通，但检测模型后端还未配置。\n\n"
            "你可以发送装修现场图片；检测后端接入后，会自动识别施工阶段、问题风险和补拍建议。"
        )

    return "家装助手 API 已联通。请发送装修现场图片或问题描述。"
