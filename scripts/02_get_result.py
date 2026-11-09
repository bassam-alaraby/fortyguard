import sys
import time
import json
from pathlib import Path
import requests
from common import get_config

if len(sys.argv) != 2:
    raise SystemExit("Usage: python scripts/02_get_result.py <activity_id>")

activity_id = sys.argv[1]
base_url, api_key = get_config()

status_url = f"{base_url}/v1/status/{activity_id}"
headers = {"api-key": api_key}

output_dir = Path(__file__).resolve().parent.parent / "outputs"
output_dir.mkdir(exist_ok=True)

for _ in range(120):
    response = requests.get(status_url, headers=headers, timeout=30)
    body = response.json()

    if not response.ok or body.get("error"):
        print("API error:", body.get("code"), "-", body.get("message"))
        raise SystemExit(1)

    status_data = body["data"]
    status = status_data["status"].lower()

    if status in ("completed", "succeeded"):
        output_file = output_dir / f"02_result_{activity_id}.json"
        output_file.write_text(json.dumps(body, indent=2), encoding="utf-8")
        print(f"Task completed. Saved to {output_file} ({output_file.stat().st_size / 1024:.1f} KB)")
        break
    elif status in ("failed", "error"):
        output_file = output_dir / f"02_failed_{activity_id}.json"
        output_file.write_text(json.dumps(body, indent=2), encoding="utf-8")
        print(f"Task failed. Saved to {output_file}")
        raise SystemExit(1)
    else:
        print(f"Task is still processing... ({status})")
        time.sleep(5)
else:
    raise TimeoutError("Task did not complete in time.")
