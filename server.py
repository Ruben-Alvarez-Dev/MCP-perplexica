"""MCP Server for Vane/Perplexica.

This server provides MCP tools for interacting with Vane (Perplexica) search API.
"""

import logging
import sys
from typing import Any, Dict, List, Optional

import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from config import get_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

config = get_config()
server = Server("mcp-vane")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="web_search",
            description="Perform a web search using Vane/Perplexica",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                    "recency_days": {
                        "type": "number",
                        "description": "Limit results to within specified days",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="deep_search",
            description="Perform a deep search with source retrieval",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The deep search query",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="academic_search",
            description="Search for academic papers and research",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The academic search query",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="image_search",
            description="Search for images",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The image search query",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="video_search",
            description="Search for videos",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The video search query",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="news_search",
            description="Search for news articles",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The news search query",
                    },
                    "recency_days": {
                        "type": "number",
                        "description": "Limit to news within specified days",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="local_search",
            description="Search using local knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The local search query",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="youtube_transcript",
            description="Extract transcript from a YouTube video",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_id": {
                        "type": "string",
                        "description": "The YouTube video ID",
                    },
                },
                "required": ["video_id"],
            },
        ),
        Tool(
            name="health_check",
            description="Check if Vane API is healthy",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


def make_vane_request(
    endpoint: str, payload: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make request to Vane API."""
    url = config.get_vane_url(endpoint)
    try:
        response = requests.post(
            url,
            json=payload or {},
            timeout=30,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.error(f"Timeout requesting {url}")
        raise Exception("Request to Vane API timed out")
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error requesting {url}")
        raise Exception("Could not connect to Vane API")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        raise Exception(f"Vane API request failed: {str(e)}")


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    if name != "health_check" and name != "youtube_transcript":
        query = arguments.get("query", "").strip()
        if not query:
            return [TextContent(type="text", text="Error: query cannot be empty")]
        if len(query) > 500:
            return [
                TextContent(
                    type="text", text="Error: query too long (max 500 characters)"
                )
            ]
        arguments["query"] = query

    try:
        if name == "web_search":
            result = make_vane_request(
                "api/search",
                {
                    "query": arguments["query"],
                    "recency_days": arguments.get("recency_days"),
                },
            )
            return [TextContent(type="text", text=str(result))]

        elif name == "deep_search":
            result = make_vane_request(
                "api/search/deep",
                {"query": arguments["query"]},
            )
            return [TextContent(type="text", text=str(result))]

        elif name == "academic_search":
            result = make_vane_request(
                "api/search/academic",
                {"query": arguments["query"]},
            )
            return [TextContent(type="text", text=str(result))]

        elif name == "image_search":
            result = make_vane_request(
                "api/search/images",
                {"query": arguments["query"]},
            )
            return [TextContent(type="text", text=str(result))]

        elif name == "video_search":
            result = make_vane_request(
                "api/search/videos",
                {"query": arguments["query"]},
            )
            return [TextContent(type="text", text=str(result))]

        elif name == "news_search":
            result = make_vane_request(
                "api/search/news",
                {
                    "query": arguments["query"],
                    "recency_days": arguments.get("recency_days"),
                },
            )
            return [TextContent(type="text", text=str(result))]

        elif name == "youtube_transcript":
            result = make_vane_request(
                "api/youtube/transcript",
                {"video_id": arguments["video_id"]},
            )
            return [TextContent(type="text", text=str(result))]

        elif name == "health_check":
            result = make_vane_request("health")
            return [TextContent(type="text", text=str(result))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Tool error: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main() -> None:
    """Main entry point."""
    logger.info("Starting MCP Vane server...")
    logger.info(f"Vane base URL: {config.vane_base_url}")

    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
