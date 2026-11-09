# API Evaluation

## What I tested
- `POST /v1/heatmap` (submit), `GET /v1/status/{activity_id}` (poll)
- Authentication with the `api-key` header, key loaded from `.env`

## Attempts log
| # | Test | Result |
|---|------|--------|
| 1 | Heatmap over lower Manhattan, NY, 2024-07-15 | 400 `OUT_OF_COVERAGE` |
| 2 | Heatmap over San Marino, CA, same date | 200, got `activity_id` |
| 3 | Polled status until completed | Result saved to `outputs/02_result.json` (~100 KB, 90 map features) |
