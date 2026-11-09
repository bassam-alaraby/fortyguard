# FortyGuard Product Evaluation

A hands-on evaluation of the FortyGuard Temperature Dashboard, Temperature API and Temperature MCP.

## Repository structure

```
├── notes/
├── scripts/        Python scripts that call the API
├── outputs/        Real API responses
└── screenshots/    Dashboard screenshots
```

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install requests python-dotenv
   ```
2. Copy `.env.example` to `.env` and add your own key:
   ```
   FORTYGUARD_API_KEY=your_key_here
   FORTYGUARD_BASE_URL=https://api.fortyguard.com
   ```
3. Run the scripts from the repo root:
   ```bash
   python scripts/01_first_call.py
   python scripts/02_get_result.py <activity_id>
   ```

## Full Notes

| # | Notes | Files |
|---|-------|-------|
| 1 | Dashboard | [01-dashboard.md](notes/01-dashboard.md) |
| 2 | API | [02-api.md](notes/02-api.md) |
| 3 | MCP | [03-mcp.md](notes/03-mcp.md) |
