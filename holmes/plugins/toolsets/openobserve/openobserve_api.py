from typing import Any, Dict, List, Optional

import backoff
import requests  # type: ignore


def build_auth_headers(
    username: Optional[str],
    password: Optional[str],
    api_key: Optional[str],
    additional_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    headers: Dict[str, str] = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    elif username and password:
        import base64

        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers["Authorization"] = f"Basic {credentials}"

    if additional_headers:
        headers.update(additional_headers)

    return headers


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5,
    giveup=lambda e: isinstance(e, requests.exceptions.HTTPError)
    and e.response.status_code < 500,
)
def execute_openobserve_search(
    base_url: str,
    org_id: str,
    username: Optional[str],
    password: Optional[str],
    api_key: Optional[str],
    sql: str,
    start_time: int,
    end_time: int,
    size: int = 100,
    additional_headers: Optional[Dict[str, str]] = None,
    verify_ssl: bool = True,
    no_proxy: bool = False,
) -> List[Dict[str, Any]]:
    """Execute a search query against OpenObserve.

    Args:
        base_url: OpenObserve API base URL (e.g. http://localhost:5080)
        org_id: Organization ID
        sql: SQL query string
        start_time: Start time in microseconds since epoch
        end_time: End time in microseconds since epoch
        size: Maximum number of records to return

    Returns:
        List of log records (hits)
    """
    url = f"{base_url}/api/{org_id}/_search"
    payload = {
        "query": {
            "sql": sql,
            "start_time": start_time,
            "end_time": end_time,
            "from": 0,
            "size": size,
        },
    }

    try:
        response = requests.post(
            url,
            headers=build_auth_headers(username, password, api_key, additional_headers),
            json=payload,
            verify=verify_ssl,
            proxies={"http": None, "https": None} if no_proxy else None,
        )
        response.raise_for_status()

        result = response.json()
        return result.get("hits", [])

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Failed to query OpenObserve logs. URL: {url}, SQL: {sql}, "
            f"start_time: {start_time}, end_time: {end_time}, size: {size}. "
            f"Error: {str(e)}"
        )


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5,
    giveup=lambda e: isinstance(e, requests.exceptions.HTTPError)
    and e.response.status_code < 500,
)
def list_openobserve_streams(
    base_url: str,
    org_id: str,
    username: Optional[str],
    password: Optional[str],
    api_key: Optional[str],
    stream_type: str = "logs",
    additional_headers: Optional[Dict[str, str]] = None,
    verify_ssl: bool = True,
    no_proxy: bool = False,
) -> List[Dict[str, Any]]:
    """List available streams in OpenObserve.

    Returns:
        List of stream metadata dicts
    """
    url = f"{base_url}/api/{org_id}/streams"
    params = {"type": stream_type}

    try:
        response = requests.get(
            url,
            headers=build_auth_headers(username, password, api_key, additional_headers),
            params=params,
            verify=verify_ssl,
            proxies={"http": None, "https": None} if no_proxy else None,
        )
        response.raise_for_status()

        result = response.json()
        return result.get("list", [])

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Failed to list OpenObserve streams. URL: {url}. Error: {str(e)}"
        )
