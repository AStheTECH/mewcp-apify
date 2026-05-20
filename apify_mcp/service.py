import json
import logging
from typing import Any, Dict, List, Optional

import httpx
from fastmcp_credentials import get_credentials

from .config import (
    APIFY_ACTORS_ENDPOINT,
    APIFY_ACTOR_BUILDS_ENDPOINT,
    APIFY_ACTOR_RUNS_ENDPOINT,
    APIFY_DATASETS_ENDPOINT,
    APIFY_KEY_VALUE_STORES_ENDPOINT,
    APIFY_TASKS_ENDPOINT,
)

logger = logging.getLogger("apify-mcp-server")


class ApifyClient:
    """Client for Apify API v2."""

    def __init__(self):
        cred = get_credentials()
        api_token = cred.fields.get("api_token")
        if not api_token:
            raise ValueError("No 'api_token' found in credentials")
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to Apify API."""
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
                timeout=60.0,
            )
            response.raise_for_status()
            # Most endpoints return {"data": ...}
            result = response.json()
            if "data" in result:
                return result["data"]
            return result

    # Actor Management

    async def list_actors(
        self, my_only: bool = False, limit: int = 100, offset: int = 0
    ) -> Dict[str, Any]:
        """List Actors."""
        params = {"limit": limit, "offset": offset}
        if my_only:
            params["my"] = 1
        return await self._request("GET", APIFY_ACTORS_ENDPOINT, params=params)

    async def get_actor(self, actor_id: str) -> Dict[str, Any]:
        """Get Actor by ID."""
        url = f"{APIFY_ACTORS_ENDPOINT}/{actor_id}"
        return await self._request("GET", url)

    async def run_actor(
        self, actor_id: str, input_data: Dict[str, Any], **options
    ) -> Dict[str, Any]:
        """Run an Actor."""
        url = f"{APIFY_ACTORS_ENDPOINT}/{actor_id}/runs"
        params = {k: v for k, v in options.items() if v is not None}
        return await self._request("POST", url, params=params, json_data=input_data)

    # Actor Runs

    async def list_runs(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        desc: bool = False,
    ) -> Dict[str, Any]:
        """List Actor runs."""
        params = {"limit": limit, "offset": offset, "desc": 1 if desc else 0}
        if status:
            params["status"] = status
        return await self._request("GET", APIFY_ACTOR_RUNS_ENDPOINT, params=params)

    async def get_run(self, run_id: str, wait_for_finish: int = 0) -> Dict[str, Any]:
        """Get Actor run details."""
        url = f"{APIFY_ACTOR_RUNS_ENDPOINT}/{run_id}"
        params = {"waitForFinish": wait_for_finish} if wait_for_finish else None
        return await self._request("GET", url, params=params)

    async def abort_run(self, run_id: str, gracefully: bool = False) -> Dict[str, Any]:
        """Abort an Actor run."""
        url = f"{APIFY_ACTOR_RUNS_ENDPOINT}/{run_id}/abort"
        params = {"gracefully": 1 if gracefully else 0}
        return await self._request("POST", url, params=params)

    # Actor Builds

    async def list_builds(
        self, limit: int = 100, offset: int = 0, desc: bool = False
    ) -> Dict[str, Any]:
        """List Actor builds."""
        params = {"limit": limit, "offset": offset, "desc": 1 if desc else 0}
        return await self._request("GET", APIFY_ACTOR_BUILDS_ENDPOINT, params=params)

    async def get_build(
        self, build_id: str, wait_for_finish: int = 0
    ) -> Dict[str, Any]:
        """Get Actor build details."""
        url = f"{APIFY_ACTOR_BUILDS_ENDPOINT}/{build_id}"
        params = {"waitForFinish": wait_for_finish} if wait_for_finish else None
        return await self._request("GET", url, params=params)

    # Actor Tasks

    async def list_tasks(
        self, limit: int = 100, offset: int = 0, desc: bool = False
    ) -> Dict[str, Any]:
        """List Actor tasks."""
        params = {"limit": limit, "offset": offset, "desc": 1 if desc else 0}
        return await self._request("GET", APIFY_TASKS_ENDPOINT, params=params)

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get Actor task details."""
        url = f"{APIFY_TASKS_ENDPOINT}/{task_id}"
        return await self._request("GET", url)

    async def run_task(
        self, task_id: str, input_data: Optional[Dict[str, Any]] = None, **options
    ) -> Dict[str, Any]:
        """Run an Actor task."""
        url = f"{APIFY_TASKS_ENDPOINT}/{task_id}/runs"
        params = {k: v for k, v in options.items() if v is not None}
        return await self._request(
            "POST", url, params=params, json_data=input_data or {}
        )

    # Datasets

    async def get_dataset_items(
        self,
        dataset_id: str,
        limit: Optional[int] = None,
        offset: int = 0,
        desc: bool = False,
        clean: bool = False,
        format: str = "json",
    ) -> Any:
        """Get dataset items."""
        url = f"{APIFY_DATASETS_ENDPOINT}/{dataset_id}/items"
        params = {"offset": offset, "format": format, "desc": 1 if desc else 0}
        if limit:
            params["limit"] = limit
        if clean:
            params["clean"] = 1

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url, headers=self.headers, params=params, timeout=60.0
            )
            response.raise_for_status()
            if format == "json":
                return response.json()
            return response.text

    # Key-Value Stores

    async def get_record(
        self, store_id: str, record_key: str
    ) -> Optional[Dict[str, Any]]:
        """Get record from key-value store."""
        url = f"{APIFY_KEY_VALUE_STORES_ENDPOINT}/{store_id}/records/{record_key}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, timeout=30.0)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
