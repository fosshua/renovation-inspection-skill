import hashlib
import os
import sys
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient


ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

os.environ["WECHAT_TOKEN"] = "testtoken"
os.environ["WECHAT_APP_ID"] = "testappid"
os.environ["WECHAT_APP_SECRET"] = "testsecret"
os.environ["UPLOAD_DIR"] = "/tmp/home-renovation-assistant-test-uploads"

from service.app import app  # noqa: E402
from service.inspection import (  # noqa: E402
    InspectionRequest,
    build_openai_user_content,
    model_supports_vision,
)


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_inspection_backends(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("INSPECTION_BACKEND_URL", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)


def wechat_signature(timestamp: str = "123", nonce: str = "abc") -> str:
    raw = "".join(sorted(["testtoken", timestamp, nonce]))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_wechat_verify_callback() -> None:
    response = client.get(
        "/wechat/callback",
        params={
            "signature": wechat_signature(),
            "timestamp": "123",
            "nonce": "abc",
            "echostr": "hello",
        },
    )
    assert response.status_code == 200
    assert response.text == "hello"


def test_mini_inspect_json_fallback() -> None:
    response = client.post(
        "/api/mini/inspect",
        json={
            "user_id": "mini-user",
            "text": "帮我看看这张装修图",
            "image_url": "https://example.com/window.jpg",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["engine"] == "fallback"
    assert data["session_id"] == "user-mini-user"
    assert "已收到图片" in data["answer"]


def test_mini_inspect_upload_fallback() -> None:
    fixture = (
        Path(__file__).resolve().parents[2]
        / ".codex"
        / "skills"
        / "renovation-inspection"
        / "tests"
        / "fixtures"
        / "images"
        / "window-bottom-gap.jpg"
    )
    with fixture.open("rb") as image:
        response = client.post(
            "/api/mini/inspect-upload",
            data={"user_id": "mini-user", "text": "帮我看窗户缝隙"},
            files={"file": ("window-bottom-gap.jpg", image, "image/jpeg")},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["engine"] == "fallback"
    assert "已收到图片" in data["answer"]


def test_wechat_image_message_fallback() -> None:
    xml = """<xml>
<ToUserName><![CDATA[gh_test]]></ToUserName>
<FromUserName><![CDATA[user_openid]]></FromUserName>
<CreateTime>123</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<PicUrl><![CDATA[https://example.com/test.jpg]]></PicUrl>
<MediaId><![CDATA[media123]]></MediaId>
</xml>"""
    response = client.post(
        "/wechat/callback",
        params={"signature": wechat_signature(), "timestamp": "123", "nonce": "abc"},
        content=xml,
        headers={"Content-Type": "application/xml"},
    )
    assert response.status_code == 200
    assert "<MsgType><![CDATA[text]]></MsgType>" in response.text
    assert "已收到图片" in response.text


def test_mini_inspect_model_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    async def raise_rate_limit(_req):  # type: ignore[no-untyped-def]
        request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
        response = httpx.Response(429, request=request, text="Too Many Requests")
        raise httpx.HTTPStatusError("rate limited", request=request, response=response)

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("service.inspection.call_openai_compatible", raise_rate_limit)

    response = client.post(
        "/api/mini/inspect",
        json={
            "user_id": "mini-user",
            "text": "帮我看看这张装修图",
            "image_url": "https://example.com/window.jpg",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "provider_error"
    assert data["engine"] == "openai_compatible"
    assert "限流" in data["answer"]


def test_deepseek_defaults_to_text_only_vision_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_MODEL_SUPPORTS_VISION", raising=False)
    assert model_supports_vision("https://api.deepseek.com") is False

    content = build_openai_user_content(
        InspectionRequest(
            user_id="mini-user",
            session_id="user-mini-user",
            message_type="image",
            text="瓷砖海棠角是不是太宽",
            image_url="https://example.com/tile.jpg",
        ),
        supports_vision=False,
    )

    assert isinstance(content, str)
    assert "当前模型配置不支持直接读取图片" in content
    assert "https://example.com/tile.jpg" in content
