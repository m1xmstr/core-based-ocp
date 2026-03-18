"""Minimal notebook-style demo for a private AI serving endpoint."""

import json
import urllib.request

ENDPOINT = "https://private-ai-app.example.com/api/meta"

with urllib.request.urlopen(ENDPOINT, timeout=10) as response:
    payload = json.loads(response.read().decode("utf-8"))

print("Platform metadata:")
print(json.dumps(payload, indent=2, sort_keys=True))
