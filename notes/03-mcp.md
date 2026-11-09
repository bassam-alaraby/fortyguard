# MCP Evaluation

## 1. MCP Configuration

The FortyGuard MCP server was configured in OpenCode using `opencode.json`.

Configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "fortyguard-mcp": {
        "type": "remote",
        "url": "https://tos-mcp.app.fortyguard.com/mcp",
        "oauth": false,
        "headers": {
          "Authorization": "Bearer {env:FORTYGUARD_API_KEY}"
        }
      }
    }
  }
}
```

The API key is stored in the project's `.env` file and loaded into the shell environment before launching OpenCode.

```bash
source .env
opencode
```

## 2. Environment

- **MCP Server:** FortyGuard Temperature MCP
- **MCP Server URL:** `https://tos-mcp.app.fortyguard.com/mcp`
- **Client:** OpenCode
- **Model:** GLM-5.3-Flash
- **Configuration:** `opencode.json`

## 3. Evaluation Prompt

The following prompt was sent to GLM-5.3-Flash in OpenCode to evaluate the MCP server.

```text
You have access to the FortyGuard Temperature MCP. I'm evaluating it as a new
developer. Please do the following and keep an honest, factual log as you go.

Tasks:
1. List every FortyGuard MCP tool available to you, with a one-line description
   of what each does and its required parameters.
2. Request a temperature heatmap for a ~1 km square area in San Marino, California
   (polygon, [lng, lat] order):
   [-118.1038, 34.1327], [-118.0938, 34.1327], [-118.0938, 34.1427],
   [-118.1038, 34.1427], [-118.1038, 34.1327]
   Use date 2026-11-09, time 12:00. Summarize the result (min, max, mean, std).
3. Compare that area with a second area in California of your choice (for example
   a park vs. a dense urban block) and tell me which is hotter and by how much.
4. Try at least one other tool from the list (environmental parameters,
   segmentation, or a heat report) on the same area.
5. Deliberately trigger one error case (for example an area outside the US, or
   a missing required parameter) and report exactly what the tool returned.

Logging rules:
- Write the log to notes/03-mcp-log.md in English, using these sections:
  Tools available, What I ran (tool, parameters, outcome, rough duration),
  Errors and friction (unclear tool names or descriptions, missing parameters,
  confusing output, slow calls), Output quality, and Observations about how
  well the tool descriptions let an AI use these tools without extra help.
- Record only what actually happened. Do not invent results or praise.
- Never print, log, or write the API key anywhere.
- Do not modify any file other than notes/03-mcp-log.md.
- Keep large raw outputs out of the log; summarize them.
```

## 4. Expected Output

The evaluation log should be written to:

[`03-mcp-log.md`](notes/03-mcp-log.md)