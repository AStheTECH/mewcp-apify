import json
import logging

from fastmcp import FastMCP
from pydantic import Field

from .service import ApifyClient

logger = logging.getLogger("apify-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    """Register all Apify MCP tools."""

    @mcp.tool(
        name="apify_list_actors",
        description="List all Actors in your Apify account. Returns basic information about each Actor including ID, name, and creation date.",
    )
    async def apify_list_actors(
        api_token: str = Field(..., description="Apify API token for authentication"),
        my_only: bool = Field(
            default=True, description="Only return Actors owned by you"
        ),
        limit: int = Field(
            default=100, description="Maximum number of Actors to return", ge=1, le=1000
        ),
        offset: int = Field(
            default=0, description="Number of Actors to skip for pagination"
        ),
    ) -> str:
        """List Actors from Apify account."""
        try:
            client = ApifyClient(api_token)
            result = await client.list_actors(
                my_only=my_only, limit=limit, offset=offset
            )

            output = {
                "success": True,
                "total": result.get("total", 0),
                "count": result.get("count", 0),
                "actors": [
                    {
                        "id": a["id"],
                        "name": a.get("name"),
                        "username": a.get("username"),
                    }
                    for a in result.get("items", [])
                ],
            }
            logger.info(f"Retrieved {output['count']} Actors")
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to list Actors: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="apify_run_actor",
        description="Run an Actor on Apify platform. Provide Actor ID and input data. Returns run details including run ID and default dataset ID for results.",
    )
    async def apify_run_actor(
        api_token: str = Field(..., description="Apify API token for authentication"),
        actor_id: str = Field(
            ..., description="Actor ID to run (e.g., 'username~actor-name' or Actor ID)"
        ),
        input_data: str = Field(
            default="{}", description="JSON string of input data for the Actor"
        ),
        timeout_secs: int = Field(
            default=None, description="Run timeout in seconds", ge=0
        ),
        memory_mbytes: int = Field(
            default=None, description="Memory limit in MB", ge=128
        ),
        build: str = Field(
            default=None, description="Build tag or number (default: 'latest')"
        ),
    ) -> str:
        """Run an Actor on Apify."""
        try:
            client = ApifyClient(api_token)

            # Parse input data
            try:
                input_dict = json.loads(input_data)
            except json.JSONDecodeError as e:
                return json.dumps(
                    {"success": False, "error": f"Invalid JSON input: {str(e)}"}
                )

            options = {}
            if timeout_secs:
                options["timeout"] = timeout_secs
            if memory_mbytes:
                options["memory"] = memory_mbytes
            if build:
                options["build"] = build

            result = await client.run_actor(actor_id, input_dict, **options)

            output = {
                "success": True,
                "run_id": result.get("id"),
                "status": result.get("status"),
                "started_at": result.get("startedAt"),
                "default_dataset_id": result.get("defaultDatasetId"),
                "default_key_value_store_id": result.get("defaultKeyValueStoreId"),
            }
            logger.info(f"Started Actor run: {output['run_id']}")
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to run Actor {actor_id}: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="apify_get_run",
        description="Get details of an Actor run including status, start time, finish time, and storage IDs.",
    )
    async def apify_get_run(
        api_token: str = Field(..., description="Apify API token for authentication"),
        run_id: str = Field(..., description="Actor run ID"),
        wait_for_finish: int = Field(
            default=0,
            description="Seconds to wait for run completion (0-60)",
            ge=0,
            le=60,
        ),
    ) -> str:
        """Get Actor run details."""
        try:
            client = ApifyClient(api_token)
            result = await client.get_run(run_id, wait_for_finish=wait_for_finish)

            output = {
                "success": True,
                "run_id": result.get("id"),
                "actor_id": result.get("actId"),
                "status": result.get("status"),
                "started_at": result.get("startedAt"),
                "finished_at": result.get("finishedAt"),
                "default_dataset_id": result.get("defaultDatasetId"),
                "default_key_value_store_id": result.get("defaultKeyValueStoreId"),
                "usage_total_usd": result.get("usageTotalUsd"),
            }
            logger.info(
                f"Retrieved run details for {run_id}: status={output['status']}"
            )
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to get run {run_id}: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="apify_list_runs",
        description="List recent Actor runs from your account. Can filter by status.",
    )
    async def apify_list_runs(
        api_token: str = Field(..., description="Apify API token for authentication"),
        status: str = Field(
            default=None,
            description="Filter by status (e.g., 'SUCCEEDED', 'FAILED', 'RUNNING')",
        ),
        limit: int = Field(
            default=100, description="Maximum number of runs to return", ge=1, le=1000
        ),
        offset: int = Field(
            default=0, description="Number of runs to skip for pagination"
        ),
    ) -> str:
        """List Actor runs."""
        try:
            client = ApifyClient(api_token)
            result = await client.list_runs(
                status=status, limit=limit, offset=offset, desc=True
            )

            output = {
                "success": True,
                "total": result.get("total", 0),
                "count": result.get("count", 0),
                "runs": [
                    {
                        "id": r["id"],
                        "actor_id": r["actId"],
                        "status": r["status"],
                        "started_at": r["startedAt"],
                        "finished_at": r.get("finishedAt"),
                    }
                    for r in result.get("items", [])
                ],
            }
            logger.info(f"Retrieved {output['count']} runs")
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to list runs: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="apify_get_dataset_items",
        description="Retrieve items from an Actor's default dataset. Results are the output data produced by the Actor run.",
    )
    async def apify_get_dataset_items(
        api_token: str = Field(..., description="Apify API token for authentication"),
        dataset_id: str = Field(
            ..., description="Dataset ID (from Actor run response)"
        ),
        limit: int = Field(
            default=100, description="Maximum number of items to return", ge=1, le=10000
        ),
        offset: int = Field(
            default=0, description="Number of items to skip for pagination"
        ),
        clean: bool = Field(
            default=True, description="Remove hidden fields (starting with '#')"
        ),
    ) -> str:
        """Get dataset items from Actor run."""
        try:
            client = ApifyClient(api_token)
            items = await client.get_dataset_items(
                dataset_id, limit=limit, offset=offset, clean=clean
            )

            # Handle different response formats
            if isinstance(items, list):
                output = {
                    "success": True,
                    "count": len(items),
                    "items": items,
                }
            else:
                output = {
                    "success": True,
                    "data": items,
                }

            logger.info(f"Retrieved {output.get('count', len(items))} dataset items")
            return json.dumps(output, indent=2, default=str)
        except Exception as e:
            logger.error(
                f"Failed to get dataset items from {dataset_id}: {e}", exc_info=True
            )
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="apify_list_tasks",
        description="List Actor tasks in your account. Tasks are pre-configured Actor runs with saved input.",
    )
    async def apify_list_tasks(
        api_token: str = Field(..., description="Apify API token for authentication"),
        limit: int = Field(
            default=100, description="Maximum number of tasks to return", ge=1, le=1000
        ),
        offset: int = Field(
            default=0, description="Number of tasks to skip for pagination"
        ),
    ) -> str:
        """List Actor tasks."""
        try:
            client = ApifyClient(api_token)
            result = await client.list_tasks(limit=limit, offset=offset, desc=True)

            output = {
                "success": True,
                "total": result.get("total", 0),
                "count": result.get("count", 0),
                "tasks": [
                    {
                        "id": t["id"],
                        "name": t.get("name"),
                        "actor_id": t["actId"],
                        "username": t.get("username"),
                        "created_at": t.get("createdAt"),
                    }
                    for t in result.get("items", [])
                ],
            }
            logger.info(f"Retrieved {output['count']} tasks")
            return json.dumps(output, indent=2)
        except Exception as e:
            logger.error(f"Failed to list tasks: {e}", exc_info=True)
            return json.dumps({"success": False, "error": str(e)})

    @mcp.tool(
        name="apify_health_check",
        description="Check server readiness and basic connectivity.",
    )
    def apify_health_check() -> str:
        """Health check endpoint."""
        return json.dumps(
            {
                "status": "ok",
                "server": "CL Apify MCP Server",
                "type": "utility",
                "auth_required": True,
            }
        )
