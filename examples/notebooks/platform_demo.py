import json
import os
import pathlib
import time

import requests

# Set these in your notebook environment so the example stays reusable across
# clusters and products.
META_URL = os.environ.get("APP_META_URL", "https://chat.example.com/api/meta")
KSERVE_URL = os.environ.get(
    "KSERVE_URL",
    "http://amd-unified-memory-llama-predictor.private-ai-app.svc.cluster.local:8080/v1/chat/completions",
)
OUT_DIR = pathlib.Path("outputs")
OUT_DIR.mkdir(exist_ok=True)


def timed_get(url, timeout=20):
    started = time.time()
    resp = requests.get(url, timeout=timeout)
    return resp, time.time() - started


def timed_post(url, payload, timeout=45):
    started = time.time()
    resp = requests.post(url, json=payload, timeout=timeout)
    return resp, time.time() - started


meta_resp, meta_elapsed = timed_get(META_URL)
meta = meta_resp.json() if meta_resp.ok else {"status_code": meta_resp.status_code}

payload = {
    # Keep the model label generic; different runtimes will expect different
    # naming conventions or revision labels.
    "model": os.environ.get("KSERVE_MODEL", "qwen2.5:7b"),
    "messages": [
        {"role": "system", "content": "You are a concise technical demo assistant."},
        {"role": "user", "content": "Explain in two sentences why OpenShift AI helps enterprise model serving."},
    ],
    "max_tokens": 160,
    "temperature": 0.2,
}

kserve_resp, kserve_elapsed = timed_post(KSERVE_URL, payload)
reply = ""
if kserve_resp.ok:
    body = kserve_resp.json()
    reply = (((body.get("choices") or [{}])[0].get("message") or {}).get("content") or "").strip()

summary = {
    "captured_ts": int(time.time()),
    "meta_elapsed_s": round(meta_elapsed, 3),
    "kserve_elapsed_s": round(kserve_elapsed, 3),
    "app_version": meta.get("version"),
    "reply_preview": reply,
}

out = OUT_DIR / "platform_demo_summary.md"
out.write_text(
    "\n".join(
        [
            "# Platform Demo Summary",
            "",
            f"- App version: {summary['app_version']}",
            f"- App meta latency: {summary['meta_elapsed_s']}s",
            f"- KServe latency: {summary['kserve_elapsed_s']}s",
            "",
            "## KServe reply",
            "",
            reply or "_No reply returned_",
            "",
            "## Raw summary",
            "",
            "```json",
            json.dumps(summary, indent=2),
            "```",
        ]
    ),
    encoding="utf-8",
)
print(json.dumps(summary, indent=2))
print(f"Wrote {out}")
