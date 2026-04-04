from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class ActorRunOptions(TypedDict, total=False):
    """Options for running an Actor."""

    build: str
    timeoutSecs: int
    memoryMbytes: int
    maxItems: int
    restartOnError: bool


class RunActorRequest(TypedDict, total=False):
    """Request to run an Actor."""

    input: Dict[str, Any]
    options: ActorRunOptions


class ActorInfo(TypedDict):
    """Actor information."""

    id: str
    name: str
    username: str
    description: Optional[str]
    isPublic: bool
    createdAt: str


class RunInfo(TypedDict):
    """Actor run information."""

    id: str
    actId: str
    status: str
    startedAt: str
    finishedAt: Optional[str]
    defaultDatasetId: str
    defaultKeyValueStoreId: str


class BuildInfo(TypedDict):
    """Actor build information."""

    id: str
    actId: str
    status: str
    startedAt: str
    finishedAt: Optional[str]
    buildNumber: str


class TaskInfo(TypedDict):
    """Actor task information."""

    id: str
    name: str
    actId: str
    username: str
    createdAt: str


class DatasetItem(TypedDict):
    """Dataset item."""

    # Dynamic fields based on Actor output
    pass


class KeyValueRecord(TypedDict, total=False):
    """Key-value store record."""

    key: str
    value: Any
    contentType: str


class PaginationParams(TypedDict, total=False):
    """Pagination parameters."""

    limit: int
    offset: int
    desc: bool
