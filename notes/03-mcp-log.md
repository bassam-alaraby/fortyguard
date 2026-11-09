# MCP Evaluation Log — Session 03 (AI agent run)

Run date: 2026-11-10 (all data requested for 2026-11-09, 12:00 local). Plan detected by the server: `premium`.
All runs made through the FortyGuard MCP server in OpenCode. Nothing in this log quotes or includes the API key.

## Tools available (11)

| Tool | One-line description | Required parameters |
|---|---|---|
| `heatmap` | Submit a temperature/analytic heatmap for a polygon and local date window; returns `activity_id` and `status=processing`. | `polygon_aoi` (closed GeoJSON polygon, lng/lat), `date_time` (`start_date`, `filter_type`; `start_time` needed for filter_type 1/2; `end_date` for 4) |
| `heatmap_read` | Read persisted stats/progress of an existing heatmap activity (free). | `activity_id` (or `heatmap_id` alias) |
| `env_params` | Point-level environmental parameters (humidity, apparent/wet-bulb temp, AQI, irradiance, etc.) for one coordinate. | `latitude`, `longitude`, `temperature` (caller-supplied, °C), `date_time` incl. `filter_type` |
| `report` | Submit a multi-section heat-intelligence report for a point and date (temp in °F). | `latitude`, `longitude`, `temperature` (°F), `date`, `analysis` (1–5 types; ≤2 on premium) |
| `report_read` | Read an existing completed heat-intelligence report (no new generation). | `analytics_id` (or `activity_id` alias; `heatmap_id` for Dashboard reads) |
| `satellite` | Segmentation of satellite imagery for a point into land-cover classes. | `sat.latitude`, `sat.longitude`, `date_time` |
| `streetview` | Segmentation of street-view imagery (front/back) for a point into urban classes. | `latitude`, `longitude`, `vertical_angle`, `horizontal_angle`, `back_view` |
| `temperature_routing` | Submit temperature-aware routing between two points; async, returns `activity_id`. | `origin` (lat/lon), `destination` (lat/lon), `departure_time` (ISO-8601) |
| `temperature_routing_read` | Read an existing routing activity (no regeneration). | `activity_id` |
| `monitoring` | Manage recurring temperature monitors (create/read/update/delete/run, alerts, reports). | `operation` (others depend on the operation) |
| `credit_balance` | Read available API credits (free, read-only). | none |

## What I ran

| # | Tool | Parameters | Outcome | Rough duration | Credits |
|---|---|---|---|---|---|
| 1 | `credit_balance` | — | 973,100 credits available | instant | 0 |
| 2 | `heatmap` (San Marino, CA) | Polygon [[-118.1038,34.1327]…[-118.1038,34.1327]] (~1 km square), date 2026-11-09, start_time 12:00, filter_type 1, default granularity 100 | `status=processing` + `activity_id b8e184c3-f8b9-405b-8b56-fbfbdd52a3cc` | ~1.9 s submit | 4,220 reserved |
| 3 | `heatmap` (Griffith Park, LA) | Polygon around [34.1231, -118.3004] (~1 km square), same date/time | `status=processing` + `activity_id 42844d1c-bae3-4a0a-ab8a-2a41ae451fd8` | ~1.8 s submit | 4,220 reserved |
| 4 | `heatmap_read` (San Marino) | activity_id | `completed`; min 29.55, max 31.09, mean 30.45, std 0.42 °C | ~1.8 s | 0 |
| 5 | `heatmap_read` (Griffith Park) | activity_id | `completed`; min 28.98, max 30.94, mean 29.65, std 0.49 °C | ~1 s | 0 |
| 6 | `env_params` | lat 34.1377, lon -118.0988 (center of San Marino polygon), temp 30.45 °C (taken from my own completed heatmap, as the tool requires a caller-supplied temperature), date 2026-11-09 12:00, filter_type 1, analysis: RH, apparent temp, AQI | Completed; RH 18.7 %, apparent temp 27.0 °C, US AQI 53.9. Coinbase response also included wet-bulb 14.4 °C, heat index 28.5 °C, cloud cover 0 octas, elevation 212 m, city timezone `America/Los_Angeles` | ~12.3 s | 2,900 |
| 7 | `credit_balance` | — | 961,760 credits, matching 11,340 spent exactly; the failed error-case call did not consume credits | instant | 0 |

### Task 2 — San Marino heatmap result
Completed within a few seconds of polling (~10–40 s total between submission and read).
- min 29.55 °C, max 31.09 °C, mean 30.45 °C, std 0.42 °C (°C only; °F would need to be computed client-side).

### Task 3 — Comparison: San Marino (residential) vs Griffith Park (park)
- San Marino mean 30.45 °C vs Griffith Park mean 29.65 °C.
- San Marino (the residential/suburban area) was hotter on average by **0.80 °C**.
- On max: 31.09 vs 30.94 → San Marino hotter by **0.15 °C**.
- Direction of the result is plausible (park canopy shading vs. streets and roofs), but it is a single-hour snapshot of one Nov 9 midday; it is not proof of a systematic UHI difference.

## Errors and friction

- **Required, but easy to miss**: `filter_type` is mandatory for every `date_time` object. Leaving it out would fail; the error case for a missing parameter was not exercised here, because the coverage error (task 5) was triggered first. Nothing tried to catch that mistake automatically.
- **`env_params` requires a caller-supplied temperature** and its description commits the AI to ask the user if one is not available. Since I had just computed 30.45 °C for the same point/date/hour via `heatmap`, I used it; nothing verified that the two tools' temperatures are consistent, so the heat-index/apparent-temperature output depends entirely on my input.
- **Async-plus-poll pattern works**, but polling is free so the cost is only latency; two `heatmap_read` calls shown above were needed (the second was still in `processing` after the first). No push notification or wait mechanism is available from MCP.
- **Error returned was a thrown exception** (`Error`) carrying the whole JSON in the message, not a normal return: the agent has to string-search inside a message to analyze an error case.
- **Timing**: `env_params` took ~12 s (reported latency_ms 10.7 s) vs. sub-2 s for `heatmap` submissions and ~1–2 s for reads. Reasonable, but noticeably slower than the other calls.
- **Minor**: the heat map statistics come in `stats.temperature_stats` with proper suffixes (`minimum_celsius`, …), but `heatmap_read` also returns a redundant top-level `mean_temperature_celsius` duplicating the one inside the stats; the same mean value appears twice in the payload.

## Output quality

- **Task 2**: min/max/mean/std available directly from `heatmap_read`, in °C only; no °F option was visible in the heatmap payload. Numeric precision is to thousandths — finer than a 100 m grid may justify, but not a problem.
- **Task 3**: the direct mean comparison is easy and consistent. No caveat about accuracy is attached to the numbers in the response; confidence measurement is not exposed to the MCP user here.
- **Task 4 (`env_params`)**: correct and rich — RH 18.7 %, apparent temp 27.0 °C, AQI 53.9 (the analysis selection was honored exactly). Clear structure (`parameters` summary plus `raw` detail), well-labeled units. Note the apparent/apparent-temperature value (27.0 °C) is lower than the air temperature (30.45 °C) — reasonable for a very dry hour (RH 18.7 %), so the response is internally coherent; it also gives metadata like timezone, elevation 212 m, interval, and clear-sky irradiance with a thorough explanatory paragraph.
- **Error case**: clear, machine-readable message with `category`, `code` (`OUT_OF_COVERAGE`), `field`, and `retriable: false`, plus a re-worded version in the `message` top-level key. The response was consistent with the description's warning ("outside supported U.S. coverage is not allowed"). A service-level, structured error was easy to identify; the only friction was the fact that it surfaced as a thrown error in the MCP transport rather than a normal JSON return.

## Observations about tool-description quality (AI usability)

- Positive: descriptions consistently spell out the units (°C vs °F — notably `env_params` in °C but `report` in °F), the async pattern (submit → read with `activity_id`), filter_type semantics, and the availability limits (US-only, from 2021-01-01). These are exactly the things an AI gets wrong, so the descriptions do a lot of work without needing extra docs.
- The descriptions "self-censor" by printing plan costs (e.g., `3,500 credits on free/basic/startup, 4,220 on premium/hackathon`) before submission which is helpful for budget-awareness. The correct cost for my plan (premium: 4,220) was also echoed in the `trace` and `billing` blocks, confirming expectations.
- `heatmap_read`'s description says "read bounded persisted statistics from an existing temperature or analytic heatmap" — clear enough, but does not say what shape the stats payload would have; I had to run one to learn its shape. Similarly, `heatmap`'s description does not expose what the eventual completed payload looks like (it does not mention it returns only min/max/mean/std, not a grid of cell values or a rendered image).
- The `monitoring` tool's description is long but still vague for an agent (it lists operation verbs without step-by-step rules for each; the shape of `rules`/`boundary_geojson` for each op is not documented), and `credit_balance` has no concern beyond its two fields.
- The tools never offered a wait/retry mechanism from the server side; the agent has to invent its own polling strategy. A description hint about typical heatmap latency (a few seconds in my runs; reports "several minutes") would help AI callers.
- One friction for an AI evaluator: `env_params`'s strict stance (never invent a temperature — always ask the user) is correct for accuracy, but in an evaluation context where the previous tool call already produced the temperature, the description could acknowledge reusing a just-reported tool value so the agent does not always stall and ask the user.

## Summary of outcomes

| Task | Status |
|---|---|
| 1. Tools identified | 11 tools listed above |
| 2. San Marino heatmap | Completed; 29.55 / 31.09 / 30.45 °C (min/max/mean), std 0.42 |
| 3. Comparison | Griffith Park vs San Marino: San Marino hotter on mean by 0.80 °C (max by 0.15 °C) |
| 4. Other tool (`env_params`) | Completed; RH 18.7 %, apparent temp 27.0 °C, AQI 53.9, more detail in raw |
| 5. Error case (Toronto polygon) | Clean `OUT_OF_COVERAGE` error, field `polygon_aoi`, not retriable, no credits charged |

Total credits spent in this session: 11,340 (4,220 + 4,220 + 2,900); starting balance 973,100 → ending 961,760.
