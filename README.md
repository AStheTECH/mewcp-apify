# Apify MCP Server

A Model Context Protocol (MCP) server that provides access to Apify's web scraping and automation platform API.

## Authentication

This server requires an Apify API token for authentication. You can obtain one from the [Apify Console Integrations page](https://console.apify.com/account#/integrations).

**Auth Model**: API token must be provided with every tool call (per-request authentication). The server is stateless and does not store authentication credentials between requests.

**MCP Type**: Utility (API token required per call, no multi-tenant session state)

## Available Tools

### Actor Management

#### `apify_list_actors`
List all Actors in your Apify account.

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `api_token` | string | ✅ Yes | Apify API token |
| `my_only` | boolean | ❌ No | Only return Actors owned by you (default: true) |
| `limit` | integer | ❌ No | Maximum Actors to return (1-1000, default: 100) |
| `offset` | integer | ❌ No | Skip N Actors for pagination (default: 0) |

#### `apify_run_actor`
Run an Actor on Apify platform.

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `api_token` | string | ✅ Yes | Apify API token |
| `actor_id` | string | ✅ Yes | Actor ID (e.g., `username~actor-name`) |
| `input_data` | string | ❌ No | JSON string of Actor input (default: "{}") |
| `timeout_secs` | integer | ❌ No | Run timeout in seconds |
| `memory_mbytes` | integer | ❌ No | Memory limit in MB (min 128) |
| `build` | string | ❌ No | Build tag or number (default: "latest") |

### Run Management

#### `apify_get_run`
Get details of an Actor run.

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `api_token` | string | ✅ Yes | Apify API token |
| `run_id` | string | ✅ Yes | Actor run ID |
| `wait_for_finish` | integer | ❌ No | Seconds to wait for completion (0-60) |

#### `apify_list_runs`
List recent Actor runs from your account.

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `api_token` | string | ✅ Yes | Apify API token |
| `status` | string | ❌ No | Filter by status (SUCCEEDED, FAILED, RUNNING, etc.) |
| `limit` | integer | ❌ No | Maximum runs to return (1-1000, default: 100) |
| `offset` | integer | ❌ No | Skip N runs for pagination (default: 0) |

### Data Retrieval

#### `apify_get_dataset_items`
Retrieve items from an Actor's default dataset.

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `api_token` | string | ✅ Yes | Apify API token |
| `dataset_id` | string | ✅ Yes | Dataset ID (from run response) |
| `limit` | integer | ❌ No | Maximum items to return (1-10000, default: 100) |
| `offset` | integer | ❌ No | Skip N items for pagination (default: 0) |
| `clean` | boolean | ❌ No | Remove hidden fields (default: true) |

### Task Management

#### `apify_list_tasks`
List Actor tasks in your account.

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `api_token` | string | ✅ Yes | Apify API token |
| `limit` | integer | ❌ No | Maximum tasks to return (1-1000, default: 100) |
| `offset` | integer | ❌ No | Skip N tasks for pagination (default: 0) |

### Utility

#### `apify_health_check`
Check server readiness and basic connectivity.

**Arguments**: None

## Setup

```bash
# Clone the repository
git clone <repository-url>
cd cl-mcp-apify

# Install dependencies
pip install -r requirements.txt