import logging
import os
from typing import Any, ClassVar, Dict, Optional, Tuple, Type

from pydantic import Field

from holmes.core.tools import (
    CallablePrerequisite,
    StructuredToolResult,
    StructuredToolResultStatus,
    Tool,
    ToolInvokeContext,
    ToolParameter,
    Toolset,
    ToolsetTag,
)
from holmes.plugins.toolsets.consts import (
    STANDARD_END_DATETIME_TOOL_PARAM_DESCRIPTION,
    TOOLSET_CONFIG_MISSING_ERROR,
)
from holmes.plugins.toolsets.logging_utils.logging_api import (
    DEFAULT_LOG_LIMIT,
    DEFAULT_TIME_SPAN_SECONDS,
)
from holmes.plugins.toolsets.openobserve.openobserve_api import (
    execute_openobserve_search,
    list_openobserve_streams,
)
from holmes.plugins.toolsets.utils import (
    process_timestamps_to_rfc3339,
    standard_start_datetime_tool_param_description,
    to_unix,
    toolset_name_for_one_liner,
)
from holmes.utils.pydantic_utils import ToolsetConfig


class OpenObserveConfig(ToolsetConfig):
    _deprecated_mappings: ClassVar[Dict[str, Optional[str]]] = {
        "url": "api_url",
    }

    api_url: str = Field(
        title="URL",
        description="OpenObserve API URL",
        examples=["http://localhost:5080", "https://openobserve.example.com"],
    )
    org_id: str = Field(
        default="default",
        title="Organization ID",
        description="OpenObserve organization ID",
    )
    username: Optional[str] = Field(
        default=None,
        title="Username",
        description="OpenObserve username (email) for Basic auth",
        examples=["root@example.com"],
    )
    password: Optional[str] = Field(
        default=None,
        title="Password",
        description="OpenObserve password for Basic auth",
    )
    api_key: Optional[str] = Field(
        default=None,
        title="API Key",
        description="OpenObserve Bearer token for authentication (alternative to username/password)",
    )
    additional_headers: Optional[Dict[str, str]] = Field(
        default=None,
        title="Additional Headers",
        description="Additional HTTP headers to include in requests",
    )
    verify_ssl: bool = Field(
        default=True,
        title="Verify SSL",
        description="Whether to verify SSL certificates",
    )
    no_proxy: bool = Field(
        default=False,
        title="No Proxy",
        description="Bypass system proxy settings for all requests (useful when OpenObserve is on localhost)",
    )


class OpenObserveToolset(Toolset):
    config_classes: ClassVar[list[Type[OpenObserveConfig]]] = [OpenObserveConfig]

    def __init__(self):
        super().__init__(
            name="openobserve/logs",
            description="Queries logs from OpenObserve using SQL.",
            icon_url="https://openobserve.ai/favicon.ico",
            docs_url="",
            prerequisites=[CallablePrerequisite(callable=self.prerequisites_callable)],
            tools=[],
            tags=[ToolsetTag.CORE],
            enabled=False,
        )
        self.tools = [
            OpenObserveSearch(toolset=self),
            OpenObserveListStreams(toolset=self),
        ]
        instructions_filepath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "instructions.jinja2")
        )
        self._load_llm_instructions(jinja_template=f"file://{instructions_filepath}")

    def prerequisites_callable(self, config: dict[str, Any]) -> Tuple[bool, str]:
        if not config:
            logging.debug("OpenObserve config not provided")
            return False, TOOLSET_CONFIG_MISSING_ERROR

        try:
            self._config = OpenObserveConfig(**config)
            return self.health_check()
        except Exception as e:
            logging.exception("Failed to set up OpenObserve toolset")
            return False, str(e)

    def health_check(self) -> Tuple[bool, str]:
        """Test connectivity by listing streams."""
        c = self._config
        try:
            _ = list_openobserve_streams(
                base_url=c.api_url,
                org_id=c.org_id,
                username=c.username,
                password=c.password,
                api_key=c.api_key,
                additional_headers=c.additional_headers,
                verify_ssl=c.verify_ssl,
                no_proxy=c.no_proxy,
            )
        except Exception as e:
            return False, f"Unable to connect to OpenObserve.\n{str(e)}"
        return True, ""


class OpenObserveSearch(Tool):
    toolset: OpenObserveToolset
    name: str = "openobserve_search"
    description: str = (
        "Search logs in OpenObserve using SQL queries. "
        "Example: SELECT * FROM default WHERE level = 'ERROR' ORDER BY _timestamp DESC"
    )
    parameters: Dict[str, ToolParameter] = {
        "sql": ToolParameter(
            description="SQL query string. Use str_match(field, 'value') for substring search, "
            "or standard SQL WHERE clauses for filtering. "
            "Example: SELECT * FROM default WHERE level = 'ERROR' ORDER BY _timestamp DESC",
            type="string",
            required=True,
        ),
        "start": ToolParameter(
            description=standard_start_datetime_tool_param_description(
                DEFAULT_TIME_SPAN_SECONDS
            ),
            type="string",
            required=False,
        ),
        "end": ToolParameter(
            description=STANDARD_END_DATETIME_TOOL_PARAM_DESCRIPTION,
            type="string",
            required=False,
        ),
        "limit": ToolParameter(
            description=f"Maximum number of entries to return (default: {DEFAULT_LOG_LIMIT})",
            type="integer",
            required=False,
        ),
    }

    def get_parameterized_one_liner(self, params: dict) -> str:
        return f"{toolset_name_for_one_liner(self.toolset.name)}: search {params}"

    def _invoke(self, params: dict, context: ToolInvokeContext) -> StructuredToolResult:
        (start, end) = process_timestamps_to_rfc3339(
            start_timestamp=params.get("start"),
            end_timestamp=params.get("end"),
            default_time_span_seconds=DEFAULT_TIME_SPAN_SECONDS,
        )

        config = self.toolset._config
        sql = params.get("sql", "SELECT * FROM default LIMIT 10")
        limit = params.get("limit") or DEFAULT_LOG_LIMIT

        # Convert RFC3339 to microseconds for OpenObserve
        start_us = to_unix(start) * 1_000_000
        end_us = to_unix(end) * 1_000_000

        try:
            data = execute_openobserve_search(
                base_url=config.api_url,
                org_id=config.org_id,
                username=config.username,
                password=config.password,
                api_key=config.api_key,
                sql=sql,
                start_time=start_us,
                end_time=end_us,
                size=limit,
                additional_headers=config.additional_headers,
                verify_ssl=config.verify_ssl,
                no_proxy=config.no_proxy,
            )

            if data:
                return StructuredToolResult(
                    status=StructuredToolResultStatus.SUCCESS,
                    data=data,
                    params=params,
                )
            else:
                return StructuredToolResult(
                    status=StructuredToolResultStatus.NO_DATA,
                    params=params,
                )
        except Exception as e:
            return StructuredToolResult(
                status=StructuredToolResultStatus.ERROR,
                params=params,
                error=str(e),
            )


class OpenObserveListStreams(Tool):
    toolset: OpenObserveToolset
    name: str = "openobserve_list_streams"
    description: str = "List available log streams in OpenObserve. Use this to discover stream names before querying."
    parameters: Dict[str, ToolParameter] = {}

    def get_parameterized_one_liner(self, params: dict) -> str:
        return f"{toolset_name_for_one_liner(self.toolset.name)}: list streams"

    def _invoke(self, params: dict, context: ToolInvokeContext) -> StructuredToolResult:
        config = self.toolset._config
        try:
            streams = list_openobserve_streams(
                base_url=config.api_url,
                org_id=config.org_id,
                username=config.username,
                password=config.password,
                api_key=config.api_key,
                additional_headers=config.additional_headers,
                verify_ssl=config.verify_ssl,
                no_proxy=config.no_proxy,
            )

            if streams:
                # Return just the stream names and basic info
                stream_info = [
                    {
                        "name": s.get("name"),
                        "stream_type": s.get("stream_type"),
                        "storage_type": s.get("storage_type"),
                    }
                    for s in streams
                ]
                return StructuredToolResult(
                    status=StructuredToolResultStatus.SUCCESS,
                    data=stream_info,
                    params=params,
                )
            else:
                return StructuredToolResult(
                    status=StructuredToolResultStatus.NO_DATA,
                    params=params,
                )
        except Exception as e:
            return StructuredToolResult(
                status=StructuredToolResultStatus.ERROR,
                params=params,
                error=str(e),
            )
