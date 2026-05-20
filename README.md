**Run web scrapers, automate data extraction, and manage Actor pipelines through AI.**

A Model Context Protocol (MCP) server that exposes Apify's API for running Actors, managing runs, and retrieving scraped datasets.


## Overview

The Apify MCP Server provides end-to-end control over Apify's automation platform through AI:

- Discover and run Actors from your Apify account with custom inputs and resource limits
- Monitor run status and retrieve scraped output from datasets
- Browse and manage pre-configured Actor tasks

Perfect for:

- Triggering web scraping pipelines from conversational AI interfaces
- Polling run results and surfacing structured dataset output without leaving the chat
- Managing Actor task libraries and monitoring run history through natural language


## Tools

<details>
<summary><code>apify_health_check</code> — Check server readiness</summary>

Returns a status object confirming the server is running and reachable.

**Inputs:** _(none)_

**Output:**

```json
{
  "status": "ok",
  "server": "CL Apify MCP Server"
}
```

</details>


<details>
<summary><code>apify_list_actors</code> — List Actors in your account</summary>

Returns a paginated list of Actors in your Apify account, including ID, name, and username.

**Inputs:**
```
- `my_only` (boolean, optional) — Only return Actors owned by you (default: true)
- `limit`   (integer, optional) — Maximum number of Actors to return, 1–1000 (default: 100)
- `offset`  (integer, optional) — Number of Actors to skip for pagination (default: 0)
```

**Output:**

```json
{
  "success": true,
  "total": 12,
  "count": 12,
  "actors": [
    { "id": "abc123", "name": "web-scraper", "username": "myuser" }
  ]
}
```

</details>


<details>
<summary><code>apify_run_actor</code> — Run an Actor</summary>

Starts an Actor run with the provided input and optional resource constraints. Returns the run ID and default dataset ID for polling results.

**Inputs:**
```
- `actor_id`      (string, required)  — Actor ID to run (e.g. 'username~actor-name' or Actor ID)
- `input_data`    (string, optional)  — JSON string of input data for the Actor (default: '{}')
- `timeout_secs`  (integer, optional) — Run timeout in seconds
- `memory_mbytes` (integer, optional) — Memory limit in MB (min 128)
- `build`         (string, optional)  — Build tag or number (default: 'latest')
```

**Output:**

```json
{
  "success": true,
  "run_id": "run_XXXXXXXXXX",
  "status": "RUNNING",
  "started_at": "2024-01-01T00:00:00.000Z",
  "default_dataset_id": "dataset_XXXXXXXXXX",
  "default_key_value_store_id": "kvs_XXXXXXXXXX"
}
```

</details>


<details>
<summary><code>apify_get_run</code> — Get Actor run details</summary>

Retrieves the status and metadata of a specific Actor run. Optionally waits up to 60 seconds for the run to finish.

**Inputs:**
```
- `run_id`          (string, required)  — Actor run ID
- `wait_for_finish` (integer, optional) — Seconds to wait for run completion, 0–60 (default: 0)
```

**Output:**

```json
{
  "success": true,
  "run_id": "run_XXXXXXXXXX",
  "actor_id": "abc123",
  "status": "SUCCEEDED",
  "started_at": "2024-01-01T00:00:00.000Z",
  "finished_at": "2024-01-01T00:01:30.000Z",
  "default_dataset_id": "dataset_XXXXXXXXXX",
  "usage_total_usd": 0.012
}
```

</details>


<details>
<summary><code>apify_list_runs</code> — List recent Actor runs</summary>

Returns a paginated list of Actor runs from your account, sorted newest first. Optionally filter by run status.

**Inputs:**
```
- `status` (string, optional)  — Filter by status: 'SUCCEEDED', 'FAILED', 'RUNNING', 'ABORTED', etc.
- `limit`  (integer, optional) — Maximum number of runs to return, 1–1000 (default: 100)
- `offset` (integer, optional) — Number of runs to skip for pagination (default: 0)
```

**Output:**

```json
{
  "success": true,
  "total": 42,
  "count": 10,
  "runs": [
    {
      "id": "run_XXXXXXXXXX",
      "actor_id": "abc123",
      "status": "SUCCEEDED",
      "started_at": "2024-01-01T00:00:00.000Z",
      "finished_at": "2024-01-01T00:01:30.000Z"
    }
  ]
}
```

</details>


<details>
<summary><code>apify_get_dataset_items</code> — Retrieve dataset output</summary>

Fetches scraped items from an Actor run's default dataset. This is the primary way to read Actor output after a run completes.

**Inputs:**
```
- `dataset_id` (string, required)  — Dataset ID (returned in the Actor run response)
- `limit`      (integer, optional) — Maximum number of items to return, 1–10000 (default: 100)
- `offset`     (integer, optional) — Number of items to skip for pagination (default: 0)
- `clean`      (boolean, optional) — Remove hidden fields starting with '#' (default: true)
```

**Output:**

```json
{
  "success": true,
  "count": 25,
  "items": [
    { "url": "https://example.com", "title": "Example Page", "price": 29.99 }
  ]
}
```

</details>


<details>
<summary><code>apify_list_tasks</code> — List Actor tasks</summary>

Returns a paginated list of Actor tasks in your account. Tasks are pre-configured Actor runs with saved inputs.

**Inputs:**
```
- `limit`  (integer, optional) — Maximum number of tasks to return, 1–1000 (default: 100)
- `offset` (integer, optional) — Number of tasks to skip for pagination (default: 0)
```

**Output:**

```json
{
  "success": true,
  "total": 5,
  "count": 5,
  "tasks": [
    {
      "id": "task_XXXXXXXXXX",
      "name": "my-scraper-task",
      "actor_id": "abc123",
      "username": "myuser",
      "created_at": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Common Parameters</strong></summary>

- `limit` — Maximum number of records to return per request (max varies by endpoint)
- `offset` — Number of records to skip; use with `limit` for pagination
- `desc` — Sort order; list endpoints return results newest-first by default

</details>

<details>
<summary><strong>Resource ID Formats</strong></summary>

**Actors:**

```
{username}~{actor-name}  or  {actorId}
Example: apify~web-scraper  or  BwFbCCmwYxNqHr7TB
```

**Runs:**

```
{runId}
Example: HG7ML7M8z78YcAPEB
```

**Datasets:**

```
{datasetId}
Example: rHuMdwm6xCFt6WiEz
```

**Tasks:**

```
{taskId}
Example: KoJgnDhzbtGnuH5md
```

</details>

<details>
<summary><strong>Run Status Values</strong></summary>

- `READY` — Queued and waiting to start
- `RUNNING` — Currently executing
- `SUCCEEDED` — Completed successfully
- `FAILED` — Terminated with an error
- `ABORTING` — Abort in progress
- `ABORTED` — Stopped by user or timeout
- `TIMED-OUT` — Exceeded the timeout limit

</details>


## Getting Your Apify API Token

<details>
<summary><strong>Steps</strong></summary>

1. Go to the [Apify Console](https://console.apify.com/)
2. Click your profile avatar → **Settings** → **Integrations**
3. Under **API tokens**, click **+ Add new token**
4. Give the token a name and click **Create** — copy the token value immediately, it is only shown once

> Personal API tokens carry the same permissions as your account. For production integrations, create a scoped token with the minimum permissions required.

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API token not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API token is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Apify credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Add your Apify API token
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. When using `apify_run_actor`, pass `input_data` as a JSON **string**, not an object

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Apify API Error</strong></summary>

- **Cause:** Upstream Apify API returned an error
- **Solution:**
  1. Check Apify service status at [Apify Status Page](https://status.apify.com/)
  2. Verify your API token has the required permissions for the operation
  3. Review the error message for specific details (e.g. Actor not found, insufficient compute units)

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Apify API Documentation](https://docs.apify.com/api/v2)** — Official API reference
- **[Apify Console](https://console.apify.com/)** — Manage Actors, runs, and datasets
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
