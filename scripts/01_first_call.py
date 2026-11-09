import requests
from common import get_config

base_url, api_key = get_config()

submit_url = f"{base_url}/v1/heatmap"
headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-118.1038, 34.1327],
                        [-118.0938, 34.1327],
                        [-118.0938, 34.1427],
                        [-118.1038, 34.1427],
                        [-118.1038, 34.1327]
                    ]]
                }
            }
        ]
    },
    "date_time": {
        "start_date": "2026-11-09",
        "start_time": "12:00",
        "filter_type": 1
    },
    "granularity": 100
}

response = requests.post(submit_url, headers=headers, json=payload, timeout=30)
print(response.status_code)
body = response.json()

if not response.ok or body.get("error"):
    print("API error:", body.get("code"), "-", body.get("message"))
    raise SystemExit(1)

activity_id = body["data"]["activity_id"]
print(f"Task submitted. Activity ID: {activity_id}")
