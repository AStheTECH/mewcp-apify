import logging

# Apify API Configuration
APIFY_API_BASE = "https://api.apify.com"
APIFY_API_VERSION = "v2"

# API Endpoints
APIFY_ACTORS_ENDPOINT = f"{APIFY_API_BASE}/{APIFY_API_VERSION}/acts"
APIFY_ACTOR_RUNS_ENDPOINT = f"{APIFY_API_BASE}/{APIFY_API_VERSION}/actor-runs"
APIFY_ACTOR_BUILDS_ENDPOINT = f"{APIFY_API_BASE}/{APIFY_API_VERSION}/actor-builds"
APIFY_TASKS_ENDPOINT = f"{APIFY_API_BASE}/{APIFY_API_VERSION}/actor-tasks"
APIFY_DATASETS_ENDPOINT = f"{APIFY_API_BASE}/{APIFY_API_VERSION}/datasets"
APIFY_KEY_VALUE_STORES_ENDPOINT = (
    f"{APIFY_API_BASE}/{APIFY_API_VERSION}/key-value-stores"
)
APIFY_REQUEST_QUEUES_ENDPOINT = f"{APIFY_API_BASE}/{APIFY_API_VERSION}/request-queues"

# Default pagination limits
DEFAULT_LIMIT = 100
MAX_LIMIT = 1000


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
